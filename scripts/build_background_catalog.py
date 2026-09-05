#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path

MODE_ORDER = {"light": 0, "dark": 1, "deep-dark": 2}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build a GNOME Background Properties catalog for GoreeCloud wallpapers.")
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--filename-root", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument(
        "--mode",
        choices=("light", "dark", "deep-dark"),
        default=None,
        help=(
            "optionally expose only one wallpaper mode in GNOME Settings; "
            "without this option all Light, Dark, and Deep Dark wallpapers are visible"
        ),
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    source_catalog = data.get("catalog", [])
    if len(source_catalog) < 20:
        raise SystemExit("Wallpaper source catalog must contain at least 20 entries")

    if args.mode is not None and not any(item.get("mode") == args.mode for item in source_catalog):
        raise SystemExit(f"Wallpaper catalog contains no {args.mode} entries")

    category_order = {
        category: index
        for index, category in enumerate(data.get("collection", {}).get("categories", []))
    }
    catalog = sorted(
        source_catalog,
        key=lambda item: (
            MODE_ORDER.get(item.get("mode"), 99),
            category_order.get(item.get("category"), 99),
            item.get("family", ""),
            item.get("id", ""),
        ),
    )

    root = ET.Element("wallpapers")
    visible = 0
    for item in catalog:
        is_visible = args.mode is None or item.get("mode") == args.mode
        if is_visible:
            visible += 1
        wallpaper = ET.SubElement(
            root,
            "wallpaper",
            {"deleted": "false" if is_visible else "true"},
        )
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
    print(f"Generated GNOME wallpaper catalog: {visible} visible / {len(catalog)} source entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
