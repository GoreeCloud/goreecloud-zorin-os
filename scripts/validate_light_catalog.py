#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "wallpapers.json"
PALETTES = ROOT / "config" / "palettes-v1.2.json"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    source_catalog = data.get("catalog", [])
    light_ids = {item["id"] for item in source_catalog if item.get("mode") == "light"}
    if len(source_catalog) != 24:
        fail(f"Expected 24 source wallpaper entries, found {len(source_catalog)}")
    if len(light_ids) != 8:
        fail(f"Expected exactly 8 Light wallpaper entries, found {len(light_ids)}")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        rendered = tmp_path / "wallpapers"
        catalog_path = tmp_path / "goreecloud-zorin.xml"

        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build_wallpapers.py"),
                "--palette-config",
                str(PALETTES),
                "--output",
                str(rendered),
            ],
            check=True,
        )
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build_background_catalog.py"),
                "--manifest",
                str(MANIFEST),
                "--filename-root",
                str(rendered),
                "--mode",
                "light",
                "--output",
                str(catalog_path),
            ],
            check=True,
        )

        root = ET.parse(catalog_path).getroot()
        nodes = root.findall("wallpaper")
        if len(nodes) != 24:
            fail(f"Light-first catalog must retain 24 compatibility entries, found {len(nodes)}")

        visible = [node for node in nodes if node.attrib.get("deleted") == "false"]
        hidden = [node for node in nodes if node.attrib.get("deleted") == "true"]
        if len(visible) != 8:
            fail(f"Light-first catalog must expose exactly 8 wallpapers, found {len(visible)}")
        if len(hidden) != 16:
            fail(f"Light-first catalog must hide exactly 16 compatibility wallpapers, found {len(hidden)}")

        visible_ids: set[str] = set()
        for node in visible:
            filename = node.findtext("filename")
            if not filename:
                fail("Visible wallpaper entry has no filename")
            path = Path(filename)
            if not path.is_file():
                fail(f"Visible wallpaper file is missing: {path}")
            visible_ids.add(path.stem)

        if visible_ids != light_ids:
            fail(
                "Visible wallpaper IDs differ from the Light source set: "
                f"expected {sorted(light_ids)}, got {sorted(visible_ids)}"
            )

        for node in hidden:
            filename = node.findtext("filename")
            if not filename or not Path(filename).is_file():
                fail(f"Hidden compatibility wallpaper is missing: {filename}")

    print("Light-first wallpaper catalog validation passed: 8 visible / 16 hidden compatibility entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
