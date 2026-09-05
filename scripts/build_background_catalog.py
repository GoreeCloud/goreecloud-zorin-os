#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build a GNOME Background Properties catalog for GoreeCloud wallpapers.")
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--filename-root", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument(
        "--mode",
        choices=("light", "dark", "deep-dark"),
        default=None,
        help="optionally expose only one wallpaper mode in the generated GNOME catalog",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    catalog = data.get("catalog", [])
    if len(catalog) < 20:
        raise SystemExit("Wallpaper source catalog must contain at least 20 entries")

    if args.mode is not None:
        catalog = [item for item in catalog if item.get("mode") == args.mode]
        if not catalog:
            raise SystemExit(f"Wallpaper catalog contains no {args.mode} entries")

    root = ET.Element("wallpapers")
    for item in catalog:
        wallpaper = ET.SubElement(root, "wallpaper", {"deleted": "false"})
        title = f"{item['category']} — {item['family']}"
        if args.mode is None:
            title += f" — {item['mode'].replace('-', ' ').title()}"
        ET.SubElement(wallpaper, "name").text = title
        ET.SubElement(wallpaper, "filename").text = str((args.filename_root / f"{item['id']}.svg").resolve())
        ET.SubElement(wallpaper, "options").text = "zoom"
        ET.SubElement(wallpaper, "pcolor").text = item["canvas"]
        ET.SubElement(wallpaper, "scolor").text = item["canvas"]
        ET.SubElement(wallpaper, "shade_type").text = "solid"

    ET.indent(root, space="  ")
    tree = ET.ElementTree(root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(args.output, encoding="utf-8", xml_declaration=True)
    print(f"Generated GNOME wallpaper catalog: {len(catalog)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
