#!/usr/bin/env python3
from __future__ import annotations

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
EXPECTED_CATEGORIES = {"GoreeCloud", "Glaze UI", "Wardveil Security", "Privacy Shield"}
EXPECTED_MODES = {"light", "dark", "deep-dark"}


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    palettes = json.loads(PALETTES.read_text(encoding="utf-8"))
    palette_by_id = {v["id"]: v for v in palettes["variants"]}

    if data.get("schema_version") != 2:
        fail("Wallpaper manifest schema_version must be 2")
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

    required = {
        "id", "category", "family", "mode", "theme_id", "file",
        "canvas", "accent", "accent_soft", "atmosphere_amber", "role", "source", "generated",
    }
    for item in catalog:
        missing = required - set(item)
        if missing:
            fail(f"{item.get('id','<unknown>')}: missing keys: {sorted(missing)}")
        if item["mode"] not in EXPECTED_MODES:
            fail(f"{item['id']}: invalid mode {item['mode']}")
        palette = palette_by_id.get(item["theme_id"])
        if palette is None:
            fail(f"{item['id']}: unknown theme_id {item['theme_id']}")
        if item["mode"] != palette["mode"]:
            fail(f"{item['id']}: mode does not match theme palette")
        for key in ("canvas", "accent", "accent_soft", "atmosphere_amber"):
            if item[key] != palette[key]:
                fail(f"{item['id']}: {key} does not match {item['theme_id']}")

        source = ROOT / item["source"]
        if not source.is_file():
            fail(f"{item['id']}: missing repository source {item['source']}")
        if item.get("generated"):
            if source.suffix != ".in":
                fail(f"{item['id']}: generated wallpaper source must be a .svg.in template")
        else:
            if source.suffix.lower() != ".svg":
                fail(f"{item['id']}: direct wallpaper source must be SVG")

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
            try:
                svg = ET.parse(path).getroot()
            except ET.ParseError as exc:
                fail(f"{item['id']}: invalid rendered SVG XML: {exc}")
            if not svg.tag.endswith("svg"):
                fail(f"{item['id']}: rendered root element is not SVG")
            if svg.attrib.get("width") != "3840" or svg.attrib.get("height") != "2160":
                fail(f"{item['id']}: native size must be 3840x2160")
            if svg.attrib.get("viewBox") != "0 0 3840 2160":
                fail(f"{item['id']}: viewBox must be 0 0 3840 2160")
            for element in svg.iter():
                local_name = element.tag.rsplit("}", 1)[-1].lower()
                if local_name == "script":
                    fail(f"{item['id']}: script content is prohibited")
                for attr, value in element.attrib.items():
                    attr_name = attr.rsplit("}", 1)[-1].lower()
                    if attr_name == "href" and value.startswith(("http://", "https://", "data:", "file:")):
                        fail(f"{item['id']}: external/embedded href is prohibited")

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

    print(f"Wallpaper collection validation passed: {len(catalog)} assets, {dict(counts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
