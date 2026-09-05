#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PALETTES = ROOT / "config" / "palettes-v1.2.json"
EXPECTED_MODES = {"light", "dark", "deep-dark"}
EXPECTED_SIGNATURE = {
    "light": {"canvas": "#F4F8FA", "surface": "#FBFDFE", "text": "#151C22"},
    "dark": {"canvas": "#151C22", "deep": "#0E1419", "text": "#F4F8FA"},
    "deep-dark": {"canvas": "#070C11", "deep": "#04080C", "text": "#F4F8FA"},
}
REQUIRED = {
    "id", "display_name", "mode", "gtk_base_import", "canvas", "surface",
    "elevated", "deep", "text", "muted", "border", "accent", "accent_hover",
    "accent_soft", "on_accent", "selection", "destructive",
    "destructive_hover", "atmosphere_amber", "frost", "edge_light",
    "atmosphere", "shell_panel", "shell_surface", "shell_elevated",
    "shell_border", "shell_hover", "shell_active", "shell_shadow",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def srgb_channel(value: int) -> float:
    c = value / 255.0
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def luminance(value: str) -> float:
    if len(value) != 7 or not value.startswith("#"):
        fail(f"Contrast validation requires #RRGGBB, got {value!r}")
    rgb = [int(value[i:i + 2], 16) for i in (1, 3, 5)]
    r, g, b = (srgb_channel(channel) for channel in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def main() -> int:
    data = json.loads(PALETTES.read_text(encoding="utf-8"))
    design = data.get("design_system", {})
    if data.get("schema_version") != 1:
        fail("V1.2 preview palette schema_version must be 1")
    if design.get("version") != "1.2.0":
        fail("V1.2 preview must explicitly target Glaze UI 1.2.0")
    if design.get("lifecycle") != "development":
        fail("V1.2 preview must remain lifecycle=development until acceptance is complete")
    if design.get("stable_predecessor") != "1.1.0":
        fail("V1.2 preview must identify V1.1.0 as its stable predecessor")

    variants = data.get("variants", [])
    if {variant.get("mode") for variant in variants} != EXPECTED_MODES:
        fail("V1.2 preview must define Light, Dark, and Deep Dark")
    if len(variants) != 3:
        fail("V1.2 preview must define exactly three Zorin appearance variants")

    for variant in variants:
        mode = variant["mode"]
        missing = REQUIRED - set(variant)
        if missing:
            fail(f"{variant.get('id', mode)}: missing V1.2 tokens: {sorted(missing)}")
        for key, expected in EXPECTED_SIGNATURE[mode].items():
            if variant[key].upper() != expected:
                fail(f"{variant['id']}: {key} must be {expected}, got {variant[key]}")

        text_ratio = contrast(variant["text"], variant["canvas"])
        muted_ratio = contrast(variant["muted"], variant["canvas"])
        accent_ratio = contrast(variant["on_accent"], variant["accent"])
        if text_ratio < 7.0:
            fail(f"{variant['id']}: primary text/canvas contrast {text_ratio:.2f} < 7.0")
        if muted_ratio < 4.5:
            fail(f"{variant['id']}: muted text/canvas contrast {muted_ratio:.2f} < 4.5")
        if accent_ratio < 4.5:
            fail(f"{variant['id']}: on-accent/accent contrast {accent_ratio:.2f} < 4.5")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        theme_output = tmp_path / "themes"
        wallpaper_output = tmp_path / "wallpapers"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build.py"),
                "--palette-config",
                str(PALETTES),
                "--output",
                str(theme_output),
            ],
            check=True,
        )
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build_wallpapers.py"),
                "--palette-config",
                str(PALETTES),
                "--output",
                str(wallpaper_output),
            ],
            check=True,
        )
        if len(list(theme_output.glob("*/index.theme"))) != 3:
            fail("V1.2 preview did not render all three theme variants")
        if len(list(wallpaper_output.glob("*.svg"))) < 20:
            fail("V1.2 preview did not render the complete wallpaper catalog")

    print("Glaze UI V1.2 preview contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
