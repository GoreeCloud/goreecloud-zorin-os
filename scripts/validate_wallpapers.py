#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "wallpapers.json"
PALETTES = ROOT / "config" / "palettes.json"
IDENTITIES = ROOT / "config" / "wallpaper-identities.json"
EXPECTED_CATEGORIES = {"GoreeCloud", "Glaze UI", "Wardveil Security", "Privacy Shield"}
EXPECTED_MODES = {"light", "dark", "deep-dark"}
EXPECTED_IDENTITY = {
    "GoreeCloud": "goreecloud",
    "Glaze UI": "glaze-ui",
    "Wardveil Security": "wardveil-security",
    "Privacy Shield": "privacy-shield",
}

# Wallpaper is environmental artwork, not an extension of interaction/status color.
# Keep semantic UI roles out of wallpaper source so changing an accent, selection,
# warning, or destructive contract cannot silently recolor identity artwork.
FORBIDDEN_WALLPAPER_TOKENS = {
    "{{accent}}",
    "{{accent2}}",
    "{{accent_hover}}",
    "{{accent_soft}}",
    "{{soft}}",
    "{{on}}",
    "{{on_accent}}",
    "{{selection}}",
    "{{amber}}",
    "{{atmosphere_amber}}",
    "{{destructive}}",
    "{{destructive_hover}}",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def validate_safe_svg(path: Path, label: str) -> ET.Element:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        fail(f"{label}: invalid SVG XML: {exc}")
    if not root.tag.endswith("svg"):
        fail(f"{label}: root element is not SVG")
    for element in root.iter():
        local_name = element.tag.rsplit("}", 1)[-1].lower()
        if local_name == "script":
            fail(f"{label}: script content is prohibited")
        for attr, value in element.attrib.items():
            attr_name = attr.rsplit("}", 1)[-1].lower()
            if attr_name == "href" and value.startswith(("http://", "https://", "data:", "file:")):
                fail(f"{label}: external/embedded href is prohibited")
    return root


def geometry_signature(root: ET.Element) -> list[tuple[str, tuple[tuple[str, str], ...]]]:
    keep = {"d", "cx", "cy", "r", "x", "y", "x1", "y1", "x2", "y2", "points"}
    result = []
    for element in root.iter():
        local = element.tag.rsplit("}", 1)[-1]
        if local not in {"path", "circle", "polygon", "polyline", "rect", "line", "ellipse"}:
            continue
        attrs = tuple(
            sorted(
                (k.rsplit("}", 1)[-1], v)
                for k, v in element.attrib.items()
                if k.rsplit("}", 1)[-1] in keep
            )
        )
        if attrs:
            result.append((local, attrs))
    return result


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    palettes = json.loads(PALETTES.read_text(encoding="utf-8"))
    identities = json.loads(IDENTITIES.read_text(encoding="utf-8"))
    palette_by_id = {v["id"]: v for v in palettes["variants"]}

    if data.get("schema_version") != 3:
        fail("Wallpaper manifest schema_version must be 3")
    if identities.get("schema_version") != 1:
        fail("Wallpaper identity manifest schema_version must be 1")
    if identities.get("authority", {}).get("repository") != "GoreeCloud/goreecloud-branding-assets":
        fail("Wallpaper identity authority must be the unified GoreeCloud branding repository")
    if data.get("design_system", {}).get("version") != palettes["design_system"]["version"]:
        fail("Wallpaper manifest and theme palettes must target the same Glaze UI version")

    primary = data.get("wallpapers", [])
    catalog = data.get("catalog", [])
    if len(primary) != 3:
        fail("Primary wallpaper compatibility set must contain exactly three entries")
    if len(catalog) < 20:
        fail("Wallpaper catalog must contain at least 20 entries")
    if len(catalog) != data.get("collection", {}).get("total"):
        fail("Wallpaper catalog count does not match collection.total")
    if data.get("collection", {}).get("minimum_total", 0) < 20:
        fail("Wallpaper collection minimum_total must be at least 20")

    ids = [w["id"] for w in catalog]
    if len(ids) != len(set(ids)):
        fail("Duplicate wallpaper IDs found")
    categories = {w["category"] for w in catalog}
    if categories != EXPECTED_CATEGORIES:
        fail(f"Wallpaper categories mismatch: {sorted(categories)}")
    counts = Counter(w["category"] for w in catalog)
    if any(counts[category] < 5 for category in EXPECTED_CATEGORIES):
        fail(f"Every wallpaper category must contain at least five options: {dict(counts)}")

    primary_ids = {w["id"] for w in primary}
    catalog_ids = set(ids)
    if not primary_ids <= catalog_ids:
        fail("Primary wallpaper entries must also exist in the full catalog")
    if {w["mode"] for w in primary} != EXPECTED_MODES:
        fail("Primary wallpaper set must cover Light, Dark, and Deep Dark")

    identity_geometry: dict[str, list[tuple[str, tuple[tuple[str, str], ...]]]] = {}
    for asset_id, asset in identities.get("assets", {}).items():
        path = ROOT / asset["local_path"]
        if not path.is_file():
            fail(f"{asset_id}: synchronized canonical identity asset missing")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != asset["sha256"]:
            fail(f"{asset_id}: synchronized canonical identity SHA-256 mismatch")
        root = validate_safe_svg(path, asset_id)
        if root.attrib.get("viewBox") != asset["viewBox"]:
            fail(f"{asset_id}: identity viewBox differs from pinned authority metadata")
        signature = geometry_signature(root)
        if not signature:
            fail(f"{asset_id}: canonical identity geometry signature is empty")
        identity_geometry[asset_id] = signature

    required = {
        "id", "category", "family", "mode", "theme_id", "file",
        "canvas", "accent", "accent_soft", "atmosphere_amber", "role",
        "identity", "source", "generated",
    }
    for item in catalog:
        missing = required - set(item)
        if missing:
            fail(f"{item.get('id','<unknown>')}: missing keys: {sorted(missing)}")
        if item["mode"] not in EXPECTED_MODES:
            fail(f"{item['id']}: invalid mode {item['mode']}")
        if item["role"] != "canonical-identity-derived-wallpaper":
            fail(f"{item['id']}: wallpaper must be explicitly identity-derived")
        if item["identity"] != EXPECTED_IDENTITY[item["category"]]:
            fail(f"{item['id']}: identity/category mapping mismatch")
        palette = palette_by_id.get(item["theme_id"])
        if palette is None:
            fail(f"{item['id']}: unknown theme_id {item['theme_id']}")
        if item["mode"] != palette["mode"]:
            fail(f"{item['id']}: mode does not match theme palette")
        # These manifest fields remain compatibility metadata for the V1.1
        # installed collection. They are deliberately not presentation inputs.
        for key in ("canvas", "accent", "accent_soft", "atmosphere_amber"):
            if item[key] != palette[key]:
                fail(f"{item['id']}: {key} does not match {item['theme_id']}")

        source = ROOT / item["source"]
        if not source.is_file():
            fail(f"{item['id']}: missing repository source {item['source']}")
        if not item.get("generated") or source.suffix != ".in":
            fail(f"{item['id']}: identity-derived wallpaper must use a generated .svg.in template")
        template = source.read_text(encoding="utf-8")
        if "{{identity_inner}}" not in template or "{{identity_viewbox}}" not in template:
            fail(f"{item['id']}: source template does not embed the canonical identity")
        forbidden = sorted(token for token in FORBIDDEN_WALLPAPER_TOKENS if token in template)
        if forbidden:
            fail(
                f"{item['id']}: wallpaper source consumes semantic UI token(s): "
                f"{', '.join(forbidden)}"
            )

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        rendered = tmp_path / "rendered"
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_wallpapers.py"), "--output", str(rendered)],
            check=True,
        )

        for item in catalog:
            path = rendered / f"{item['id']}.svg"
            if not path.is_file():
                fail(f"{item['id']}: rendered wallpaper is missing")
            svg = validate_safe_svg(path, item["id"])
            if svg.attrib.get("width") != "3840" or svg.attrib.get("height") != "2160":
                fail(f"{item['id']}: native size must be 3840x2160")
            if svg.attrib.get("viewBox") != "0 0 3840 2160":
                fail(f"{item['id']}: viewBox must be 0 0 3840 2160")

            asset_id = identities["category_asset"][item["category"]][item["mode"]]
            rendered_signature = geometry_signature(svg)
            rendered_set = set(rendered_signature)
            missing_geometry = [entry for entry in identity_geometry[asset_id] if entry not in rendered_set]
            if missing_geometry:
                fail(f"{item['id']}: rendered wallpaper does not preserve all canonical identity geometry")

        catalog_path = tmp_path / "goreecloud-zorin.xml"
        subprocess.run(
            [
                sys.executable, str(ROOT / "scripts" / "build_background_catalog.py"),
                "--manifest", str(MANIFEST),
                "--filename-root", str(rendered),
                "--output", str(catalog_path),
            ],
            check=True,
        )
        xml_root = ET.parse(catalog_path).getroot()
        if xml_root.tag != "wallpapers":
            fail("Generated GNOME background catalog root must be <wallpapers>")
        wallpaper_nodes = xml_root.findall("wallpaper")
        if len(wallpaper_nodes) != len(catalog):
            fail("Generated GNOME background catalog count does not match manifest")
        for node in wallpaper_nodes:
            filename = node.findtext("filename")
            if not filename or not filename.endswith(".svg"):
                fail("Generated GNOME background catalog contains an invalid filename")

    print(
        f"Wallpaper collection validation passed: {len(catalog)} identity-derived assets, "
        f"{dict(counts)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
