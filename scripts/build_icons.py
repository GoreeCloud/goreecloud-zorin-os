#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "desktop-assets.json"
DEFAULT_OUTPUT = ROOT / "build" / "icons"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the GoreeCloud Zorin icon theme.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def svg(body: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">\n'
        '  <defs>\n'
        '    <linearGradient id="frost" x1="0" y1="0" x2="0" y2="1">\n'
        '      <stop stop-color="#FBFDFE"/>\n'
        '      <stop offset="1" stop-color="#DCECF6"/>\n'
        '    </linearGradient>\n'
        '  </defs>\n'
        f'{body}\n'
        '</svg>\n'
    )


def folder_icon(glyph: str = "") -> str:
    return svg(
        '  <path d="M6 18c0-3 2-5 5-5h15l5 6h22c3 0 5 2 5 5v26c0 4-3 7-7 7H13c-4 0-7-3-7-7Z" fill="#8FC4E8" opacity=".5"/>\n'
        '  <path d="M6 23h52v27c0 4-3 7-7 7H13c-4 0-7-3-7-7Z" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/>\n'
        '  <path d="M10 27h44" stroke="#FFFFFF" stroke-width="2" opacity=".9"/>\n'
        + glyph
    )


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))["icon_theme"]
    theme = args.output.expanduser().resolve() / cfg["id"]
    if theme.exists():
        shutil.rmtree(theme)

    dirs = {
        "places": theme / "scalable" / "places",
        "devices": theme / "scalable" / "devices",
        "apps": theme / "scalable" / "apps",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)

    inherits = ",".join(cfg["inherits"])
    write(
        theme / "index.theme",
        "[Icon Theme]\n"
        f"Name={cfg['name']}\n"
        f"Comment={cfg['comment']}\n"
        f"Inherits={inherits}\n"
        "Example=folder\n"
        "Directories=scalable/places,scalable/devices,scalable/apps\n\n"
        "[scalable/places]\nSize=64\nType=Scalable\nMinSize=16\nMaxSize=512\nContext=Places\n\n"
        "[scalable/devices]\nSize=64\nType=Scalable\nMinSize=16\nMaxSize=512\nContext=Devices\n\n"
        "[scalable/apps]\nSize=64\nType=Scalable\nMinSize=16\nMaxSize=512\nContext=Applications\n",
    )

    place_icons = {
        "folder": folder_icon(),
        "folder-documents": folder_icon('  <path d="M25 32h15v16H25z" fill="#FFFFFF" stroke="#174EA6" stroke-width="1.5"/><path d="M28 36h9M28 40h9M28 44h7" stroke="#3B82F6" stroke-width="1.5" stroke-linecap="round"/>'),
        "folder-download": folder_icon('  <path d="M32 31v13m-6-5 6 6 6-6" fill="none" stroke="#174EA6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'),
        "folder-music": folder_icon('  <path d="M38 31v13c0 4-7 5-7 1 0-3 4-4 7-3V34l9-2v10c0 4-7 5-7 1 0-3 4-4 7-3V29Z" fill="#174EA6"/>'),
        "folder-pictures": folder_icon('  <rect x="23" y="31" width="22" height="16" rx="2" fill="#FFFFFF" stroke="#174EA6" stroke-width="1.5"/><circle cx="39" cy="35" r="2" fill="#3B82F6"/><path d="m25 44 6-6 4 4 3-3 5 5" fill="none" stroke="#3B82F6" stroke-width="2"/>'),
        "folder-videos": folder_icon('  <rect x="24" y="32" width="20" height="15" rx="3" fill="#FFFFFF" stroke="#174EA6" stroke-width="1.5"/><path d="m32 36 7 4-7 4Z" fill="#3B82F6"/>'),
        "user-home": svg('  <path d="M10 31 32 12l22 19v21a5 5 0 0 1-5 5H15a5 5 0 0 1-5-5Z" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><path d="M25 57V39h14v18" fill="#DCECF6" stroke="#174EA6" stroke-width="2"/>'),
        "user-desktop": svg('  <rect x="7" y="10" width="50" height="35" rx="5" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><path d="M23 54h18M28 45v9m8-9v9" stroke="#174EA6" stroke-width="2.5" stroke-linecap="round"/>'),
        "user-trash": svg('  <path d="M18 20h28l-2 36H20Z" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><path d="M15 17h34M26 12h12" stroke="#174EA6" stroke-width="3" stroke-linecap="round"/>'),
        "user-trash-full": svg('  <path d="M18 20h28l-2 36H20Z" fill="#DCECF6" stroke="#3B82F6" stroke-width="2"/><path d="M15 17h34M26 12h12" stroke="#174EA6" stroke-width="3" stroke-linecap="round"/><path d="m25 29 14 17M39 29 25 46" stroke="#3B82F6" stroke-width="2.5"/>'),
    }
    for name, content in place_icons.items():
        write(dirs["places"] / f"{name}.svg", content)

    device_icons = {
        "drive-harddisk": svg('  <rect x="8" y="13" width="48" height="38" rx="8" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><path d="M14 39h36" stroke="#8FC4E8" stroke-width="2"/><circle cx="47" cy="45" r="3" fill="#3B82F6"/>'),
        "drive-removable-media": svg('  <rect x="13" y="9" width="38" height="46" rx="8" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><rect x="21" y="16" width="22" height="17" rx="3" fill="#DCECF6" stroke="#174EA6" stroke-width="1.5"/><circle cx="32" cy="45" r="4" fill="#3B82F6"/>'),
        "network-server": svg('  <rect x="9" y="9" width="46" height="18" rx="5" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><rect x="9" y="37" width="46" height="18" rx="5" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><circle cx="46" cy="18" r="3" fill="#3B82F6"/><circle cx="46" cy="46" r="3" fill="#3B82F6"/>'),
        "computer": svg('  <rect x="7" y="9" width="50" height="34" rx="5" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><path d="M22 55h20M28 43v12m8-12v12" stroke="#174EA6" stroke-width="2.5" stroke-linecap="round"/>'),
        "phone": svg('  <rect x="19" y="5" width="26" height="54" rx="7" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><circle cx="32" cy="52" r="2" fill="#174EA6"/>'),
        "media-flash": svg('  <path d="M23 6h18v12h6v37a4 4 0 0 1-4 4H21a4 4 0 0 1-4-4V18h6Z" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><path d="M27 6v12m10-12v12" stroke="#174EA6" stroke-width="2"/>'),
    }
    for name, content in device_icons.items():
        write(dirs["devices"] / f"{name}.svg", content)

    identity = ROOT / cfg["identity_source"]
    if not identity.is_file():
        raise SystemExit(f"Missing canonical GoreeCloud mark: {identity}")
    shutil.copyfile(identity, dirs["apps"] / "start-here.svg")
    shutil.copyfile(identity, dirs["apps"] / "goreecloud.svg")

    print(f"Built GoreeCloud icon theme: {theme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
