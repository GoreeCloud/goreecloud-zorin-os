#!/usr/bin/env python3
from __future__ import annotations

import json
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "desktop-assets.json"
IMAGE_TYPE = 0xFFFD0002


def fail(message: str) -> None:
    raise SystemExit(message)


def validate_svg(path: Path) -> None:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        fail(f"{path}: invalid SVG XML: {exc}")
    if not root.tag.endswith("svg"):
        fail(f"{path}: root element is not SVG")
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1].lower() == "script":
            fail(f"{path}: scripts are prohibited")
        for attr, value in node.attrib.items():
            if attr.rsplit("}", 1)[-1].lower() == "href" and value.startswith(("http:", "https:", "file:", "data:")):
                fail(f"{path}: external resources are prohibited")


def validate_xcursor(path: Path, expected_sizes: set[int]) -> None:
    data = path.read_bytes()
    if len(data) < 16:
        fail(f"{path}: cursor file is too small")
    magic, header_size, version, ntoc = struct.unpack_from("<4sIII", data, 0)
    if magic != b"Xcur" or header_size != 16 or version != 0x00010000:
        fail(f"{path}: invalid Xcursor header")
    if ntoc != len(expected_sizes):
        fail(f"{path}: expected {len(expected_sizes)} cursor frames, found {ntoc}")
    observed: set[int] = set()
    for index in range(ntoc):
        offset = 16 + index * 12
        type_id, subtype, position = struct.unpack_from("<III", data, offset)
        if type_id != IMAGE_TYPE:
            fail(f"{path}: unsupported cursor TOC type {type_id:#x}")
        if position + 36 > len(data):
            fail(f"{path}: cursor frame position escapes file")
        chunk = struct.unpack_from("<IIIIIIIII", data, position)
        chunk_header, chunk_type, chunk_subtype, chunk_version, width, height, xhot, yhot, _delay = chunk
        if chunk_header != 36 or chunk_type != IMAGE_TYPE or chunk_version != 1:
            fail(f"{path}: invalid Xcursor image chunk")
        if chunk_subtype != subtype or width != subtype or height != subtype:
            fail(f"{path}: Xcursor frame dimensions/subtype mismatch")
        if xhot >= width or yhot >= height:
            fail(f"{path}: Xcursor hotspot lies outside image")
        end = position + 36 + width * height * 4
        if end > len(data):
            fail(f"{path}: cursor pixel payload escapes file")
        observed.add(subtype)
    if observed != expected_sizes:
        fail(f"{path}: cursor frame sizes differ: {sorted(observed)}")


def main() -> int:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    if config.get("schema_version") != 1:
        fail("desktop asset schema_version must be 1")
    if config.get("design_direction") != "light-first":
        fail("desktop assets must preserve the light-first product direction")

    icons = config["icon_theme"]
    cursors = config["cursor_theme"]
    if icons["id"] != "GoreeCloud-Zorin":
        fail("icon theme ID changed unexpectedly")
    if cursors["id"] != "GoreeCloud-Zorin-Cursors":
        fail("cursor theme ID changed unexpectedly")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        icon_out = tmp_path / "icons"
        cursor_out = tmp_path / "cursors"
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build_icons.py"), "--output", str(icon_out)], check=True)
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build_cursors.py"), "--output", str(cursor_out)], check=True)

        icon_root = icon_out / icons["id"]
        cursor_root = cursor_out / cursors["id"]
        if not (icon_root / "index.theme").is_file():
            fail("generated icon theme is missing index.theme")
        if not (cursor_root / "index.theme").is_file():
            fail("generated cursor theme is missing index.theme")

        icon_index = (icon_root / "index.theme").read_text(encoding="utf-8")
        for inherit in icons["inherits"]:
            if inherit not in icon_index:
                fail(f"generated icon theme does not inherit {inherit}")

        svgs = sorted(icon_root.rglob("*.svg"))
        if len(svgs) < int(icons["minimum_generated_icons"]):
            fail(f"generated icon theme contains only {len(svgs)} SVG icons")
        for path in svgs:
            validate_svg(path)

        for required_symbolic in ("folder-symbolic.svg", "folder-open-symbolic.svg"):
            if not (icon_root / "scalable" / "places" / required_symbolic).is_file():
                fail(f"generated icon theme is missing {required_symbolic}")

        identity = ROOT / icons["identity_source"]
        if (icon_root / "scalable" / "apps" / "start-here.svg").read_bytes() != identity.read_bytes():
            fail("start-here icon does not preserve the canonical GoreeCloud mark")

        expected_sizes = {int(value) for value in cursors["sizes"]}
        cursor_dir = cursor_root / "cursors"
        for name in cursors["required_cursor_names"]:
            path = cursor_dir / name
            if not path.is_file():
                fail(f"generated cursor theme is missing required cursor: {name}")
            validate_xcursor(path, expected_sizes)

    print("GoreeCloud icon and cursor theme validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
