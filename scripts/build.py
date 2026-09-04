#!/usr/bin/env python3
"""Generate GoreeCloud Zorin OS theme variants from shared templates."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "build" / "themes"
PALETTES = ROOT / "config" / "palettes.json"
TEMPLATES = {
    "index.theme": ROOT / "src" / "index.theme.in",
    "gtk-2.0/gtkrc": ROOT / "src" / "gtk-2.0" / "gtkrc.in",
    "gtk-3.0/gtk.css": ROOT / "src" / "gtk-3.0" / "gtk.css.in",
    "gtk-4.0/gtk.css": ROOT / "src" / "gtk-4.0" / "gtk.css.in",
    "gnome-shell/gnome-shell.css": ROOT / "src" / "gnome-shell" / "gnome-shell.css.in",
}
PLACEHOLDER = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="directory that will contain generated theme folders",
    )
    return parser.parse_args()


def load_config() -> dict:
    with PALETTES.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if data.get("schema_version") != 1:
        raise SystemExit("Unsupported palette schema version")
    variants = data.get("variants")
    if not isinstance(variants, list) or not variants:
        raise SystemExit("No theme variants are defined")
    return data


def token_map(variant: dict) -> dict[str, str]:
    tokens = {
        key.upper(): str(value)
        for key, value in variant.items()
        if isinstance(value, (str, int, float))
    }
    tokens["THEME_ID"] = str(variant["id"])
    return tokens


def render(template: str, tokens: dict[str, str], source: Path) -> str:
    missing = sorted(set(PLACEHOLDER.findall(template)) - set(tokens))
    if missing:
        raise SystemExit(f"{source}: missing tokens: {', '.join(missing)}")

    result = PLACEHOLDER.sub(lambda match: tokens[match.group(1)], template)
    unresolved = PLACEHOLDER.findall(result)
    if unresolved:
        raise SystemExit(f"{source}: unresolved placeholders remain")
    return result


def main() -> int:
    args = parse_args()
    output = args.output.expanduser().resolve()
    config = load_config()

    templates = {
        relative: path.read_text(encoding="utf-8")
        for relative, path in TEMPLATES.items()
    }

    generated = []
    for variant in config["variants"]:
        theme_id = variant.get("id")
        if not isinstance(theme_id, str) or not re.fullmatch(r"[A-Za-z0-9-]+", theme_id):
            raise SystemExit(f"Invalid theme id: {theme_id!r}")

        tokens = token_map(variant)
        theme_root = output / theme_id

        for relative, template in templates.items():
            destination = theme_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                render(template, tokens, TEMPLATES[relative]),
                encoding="utf-8",
            )

        # Zorin OS 17+ requires this explicit marker before patched libadwaita
        # will load a third-party theme into native libadwaita applications.
        marker = theme_root / "gtk-4.0" / ".libadwaita"
        marker.write_text("", encoding="utf-8")

        generated.append(theme_root)

    print(f"Generated {len(generated)} theme variants in {output}")
    for path in generated:
        print(f"  {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
