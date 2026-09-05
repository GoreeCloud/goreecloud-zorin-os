#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TOKEN_KEYS = (
    "canvas", "surface", "elevated", "deep", "text", "muted", "border",
    "accent", "accent_hover", "accent_soft", "selection", "atmosphere_amber",
    "on_accent",
)

TOKEN_MAP = {
    "accent2": "accent_hover",
    "soft": "accent_soft",
    "amber": "atmosphere_amber",
    "on": "on_accent",
}

def parse_args():
    p=argparse.ArgumentParser(description="Render the GoreeCloud Zorin wallpaper catalog from repository source.")
    p.add_argument("--output", required=True, type=Path)
    return p.parse_args()

def mode_label(mode: str) -> str:
    return {"light":"Light","dark":"Dark","deep-dark":"Deep Dark"}[mode]

def main() -> int:
    args=parse_args()
    manifest=json.loads((ROOT/"config/wallpapers.json").read_text(encoding="utf-8"))
    palettes=json.loads((ROOT/"config/palettes.json").read_text(encoding="utf-8"))
    palette_by_id={v["id"]:v for v in palettes["variants"]}
    args.output.mkdir(parents=True, exist_ok=True)

    generated=0
    copied=0
    for item in manifest["catalog"]:
        out=args.output/f"{item['id']}.svg"
        if not item.get("generated"):
            src=ROOT/item["source"]
            if not src.is_file():
                raise SystemExit(f"Missing wallpaper source: {item['source']}")
            shutil.copyfile(src,out)
            copied += 1
            continue

        src=ROOT/item["source"]
        if not src.is_file():
            raise SystemExit(f"Missing wallpaper template: {item['source']}")
        palette=palette_by_id[item["theme_id"]]
        text=src.read_text(encoding="utf-8")
        values={key:palette[key] for key in TOKEN_KEYS}
        for template_key,palette_key in TOKEN_MAP.items():
            values[template_key]=palette[palette_key]
        values["mode_label"]=mode_label(item["mode"])
        for key,value in values.items():
            text=text.replace("{{"+key+"}}",value)
        if "{{" in text or "}}" in text:
            raise SystemExit(f"Unresolved wallpaper template token in {item['source']} for {item['id']}")
        out.write_text(text,encoding="utf-8")
        generated += 1

    print(f"Rendered wallpaper catalog: {copied} direct + {generated} generated = {copied+generated}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
