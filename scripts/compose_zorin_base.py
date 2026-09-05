#!/usr/bin/env python3
"""Compose generated GoreeCloud overrides with the verified Zorin OS 17.3 base."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

TARGET_PACKAGE = "zorin-desktop-themes"
TARGET_PACKAGE_VERSION = "4.2.2"
DEFAULT_BASE_ROOT = Path("/usr/share/themes")
DEFAULT_COPYRIGHT = Path("/usr/share/doc/zorin-desktop-themes/copyright")
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PALETTES = REPO_ROOT / "config" / "palettes.json"
GTK3_ADWAITA_IMPORT_PREFIX = '@import url("resource:///org/gtk/libgtk/theme/Adwaita/'

# The verified Zorin OS 17.3 GTK 4 files correspond to the pre-5.x theme
# generation. Their state contract uses generic row.activatable selectors and
# switch:backdrop:checked / switch:checked slider ordering rather than the
# newer navigation-sidebar and child-combinator forms. The complete local base
# is still verified by byte size and SHA-256 before any rewrite occurs.
GTK4_STATE_SELECTORS = (
    "row.activatable:selected",
    "row.activatable:selected label",
    "row.activatable:selected:active",
    "row.activatable:selected:backdrop, row.activatable:selected:backdrop:hover",
    "switch:checked",
    "switch:backdrop:checked",
    "switch:checked slider",
    "switch:backdrop:checked slider",
)

BASES = {
    "ZorinBlue-Light": {
        "gtk3_css": {
            "path": "gtk-3.0/gtk.css",
            "bytes": 215389,
            "sha256": "bc06ff2fac92e56951b8f4141b8324acc1e38db783ec3a0b3cf438e8c87d9fe6",
        },
        "gtk_css": {
            "path": "gtk-4.0/gtk.css",
            "bytes": 196060,
            "sha256": "b29cfbaa713955b14517798e2c15a67184136d9913944c1d0cf22fce0d1b3e0c",
        },
        "shell_css": {
            "path": "gnome-shell/gnome-shell.css",
            "bytes": 110634,
            "sha256": "3d94563d7c680be4ac0632b95bb0c205954377488c774a653d8655dbc2ca0823",
        },
    },
    "ZorinBlue-Dark": {
        "gtk3_css": {
            "path": "gtk-3.0/gtk.css",
            "bytes": 214797,
            "sha256": "71e9d93ad1e58f75e52bb7b724fa38409961368b5d9edda4c3b921fac6e44604",
        },
        "gtk_css": {
            "path": "gtk-4.0/gtk.css",
            "bytes": 195469,
            "sha256": "90ffa76c872443d1549f09c814be8c22d68169a0dfb19e0508339e3613add77d",
        },
        "shell_css": {
            "path": "gnome-shell/gnome-shell.css",
            "bytes": 111171,
            "sha256": "e36202095055bda8de6f225227a91911623775aa0896c24b8568c0d52982f8d7",
        },
    },
}

VARIANT_BASE = {
    "GoreeCloud-Zorin-Light": "ZorinBlue-Light",
    "GoreeCloud-Zorin-Dark": "ZorinBlue-Dark",
    "GoreeCloud-Zorin-DeepDark": "ZorinBlue-Dark",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "theme_root",
        type=Path,
        help="directory containing generated GoreeCloud-Zorin-* theme folders",
    )
    parser.add_argument(
        "--base-root",
        type=Path,
        default=DEFAULT_BASE_ROOT,
        help="system theme root; defaults to /usr/share/themes",
    )
    parser.add_argument(
        "--palette-config",
        type=Path,
        default=DEFAULT_PALETTES,
        help=(
            "palette contract used for target GTK 4 state rewrites and composition metadata; "
            "defaults to config/palettes.json"
        ),
    )
    return parser.parse_args()


def resolve_input(path: Path) -> Path:
    path = path.expanduser()
    if path.is_absolute():
        return path.resolve()
    return (REPO_ROOT / path).resolve()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_palette_contract(path: Path) -> tuple[dict[str, object], dict[str, dict[str, str]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise SystemExit(f"Unsupported palette schema in {path}")
    design = data.get("design_system")
    if not isinstance(design, dict) or not design.get("version"):
        raise SystemExit(f"Palette contract is missing design_system.version: {path}")
    variants = data.get("variants")
    if not isinstance(variants, list):
        raise SystemExit(f"Palette contract has no variants list: {path}")
    palettes = {variant["id"]: variant for variant in variants}
    missing = sorted(set(VARIANT_BASE) - set(palettes))
    if missing:
        raise SystemExit(f"Missing GoreeCloud palette definitions for: {', '.join(missing)}")
    return design, palettes


def installed_package_version() -> str:
    try:
        result = subprocess.run(
            ["dpkg-query", "-W", "-f=${Version}", TARGET_PACKAGE],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise SystemExit(
            f"Required target package {TARGET_PACKAGE!r} is unavailable; "
            "this Development composer only supports the verified Zorin OS 17.3 target."
        ) from exc
    return result.stdout.strip()


def verify_base(base_root: Path, base_name: str) -> dict[str, dict[str, object]]:
    expected = BASES[base_name]
    evidence: dict[str, dict[str, object]] = {}
    for label, spec in expected.items():
        path = base_root / base_name / str(spec["path"])
        if not path.is_file():
            raise SystemExit(f"Required verified Zorin base file is missing: {path}")
        actual_size = path.stat().st_size
        actual_hash = sha256_file(path)
        if actual_size != spec["bytes"] or actual_hash != spec["sha256"]:
            raise SystemExit(
                "Zorin base stylesheet differs from the verified Zorin OS 17.3 target; "
                f"refusing speculative composition for {path}.\n"
                f"Expected bytes={spec['bytes']} sha256={spec['sha256']}\n"
                f"Actual   bytes={actual_size} sha256={actual_hash}\n"
                "Run ./scripts/diagnose.sh and update the Development compatibility evidence before installing."
            )
        evidence[label] = {
            "path": str(path),
            "bytes": actual_size,
            "sha256": actual_hash,
        }
    return evidence


def strip_standalone_gtk3_import(css: str) -> str:
    """Remove the standalone Adwaita import before appending overrides to Zorin GTK 3."""
    lines = css.splitlines()
    kept: list[str] = []
    removed = 0
    for line in lines:
        if line.strip().startswith(GTK3_ADWAITA_IMPORT_PREFIX):
            removed += 1
            continue
        kept.append(line)
    if removed != 1:
        raise SystemExit(
            "Generated GTK 3 override must contain exactly one standalone Adwaita import "
            f"before Zorin base composition; found {removed}."
        )
    return "\n".join(kept).lstrip() + "\n"


def replace_selector_rule_once(css: str, selector: str, new_rule: str, label: str) -> str:
    """Replace one selector block in an already hash-verified Zorin GTK 4 base.

    The complete Zorin source file is verified by exact size and SHA-256 before
    this function runs. Matching the verified Zorin OS 17.3 selector contract
    therefore keeps the rewrite narrow while avoiding dependence on declaration
    values that legitimately differ between Light and Dark.
    """
    selector_pattern = r"\s+".join(re.escape(part) for part in selector.split())
    pattern = re.compile(rf"(?m)^[ \t]*{selector_pattern}\s*\{{[^{{}}]*\}}")
    matches = list(pattern.finditer(css))
    if len(matches) != 1:
        literal_count = css.count(selector)
        raise SystemExit(
            "Verified Zorin GTK 4 selector changed unexpectedly; "
            f"refusing speculative state rewriting for {label}. "
            f"Found {len(matches)} rule matches and {literal_count} literal occurrences."
        )
    match = matches[0]
    return css[: match.start()] + new_rule + css[match.end() :]


def rewrite_target_gtk4_states(
    css: str,
    base_name: str,
    palette: dict[str, str],
) -> tuple[str, int]:
    """Rewrite verified Zorin OS 17.3 selected/checked state blocks."""
    if base_name not in {"ZorinBlue-Light", "ZorinBlue-Dark"}:
        raise SystemExit(f"No verified GTK 4 state rewrite profile exists for {base_name}")

    text = palette["text"]
    selection = palette["selection"]
    accent = palette["accent"]
    on_accent = palette["on_accent"]

    replacements = [
        (
            GTK4_STATE_SELECTORS[0],
            f"row.activatable:selected {{ color: {text}; background-color: {selection}; background: image({selection}); box-shadow: none; }}",
            "row activatable selected",
        ),
        (
            GTK4_STATE_SELECTORS[1],
            f"row.activatable:selected label {{ color: {text}; }}",
            "row activatable selected label",
        ),
        (
            GTK4_STATE_SELECTORS[2],
            f"row.activatable:selected:active {{ color: {text}; background-color: {selection}; background: image({selection}); box-shadow: none; }}",
            "row activatable active-selected",
        ),
        (
            GTK4_STATE_SELECTORS[3],
            f"row.activatable:selected:backdrop, row.activatable:selected:backdrop:hover {{ color: {text}; background-color: {selection}; background-image: none; box-shadow: none; }}",
            "row activatable selected backdrop",
        ),
        (
            GTK4_STATE_SELECTORS[4],
            f"switch:checked {{ color: {on_accent}; background-color: {accent}; background: image({accent}); }}",
            "switch checked",
        ),
        (
            GTK4_STATE_SELECTORS[5],
            f"switch:backdrop:checked {{ color: {on_accent}; background-color: {accent}; background-image: none; }}",
            "switch checked backdrop",
        ),
        (
            GTK4_STATE_SELECTORS[6],
            f"switch:checked slider {{ background-color: {on_accent}; box-shadow: none; }}",
            "switch checked slider",
        ),
        (
            GTK4_STATE_SELECTORS[7],
            f"switch:backdrop:checked slider {{ background-color: {on_accent}; }}",
            "switch checked backdrop slider",
        ),
    ]

    for selector, new_rule, label in replacements:
        css = replace_selector_rule_once(css, selector, new_rule, label)
    return css, len(replacements)


def compose_variant(
    theme_root: Path,
    base_root: Path,
    theme_id: str,
    base_name: str,
    evidence: dict,
    palette: dict[str, str],
    design: dict[str, object],
    palette_path: Path,
) -> None:
    theme = theme_root / theme_id
    gtk3_dir = theme / "gtk-3.0"
    gtk4_dir = theme / "gtk-4.0"
    shell_dir = theme / "gnome-shell"
    gtk3_override_path = gtk3_dir / "gtk.css"
    gtk4_override_path = gtk4_dir / "gtk.css"
    shell_override_path = shell_dir / "gnome-shell.css"

    for path in (gtk3_override_path, gtk4_override_path, shell_override_path):
        if not path.is_file():
            raise SystemExit(f"Generated override file is missing for {theme_id}: {path}")

    gtk3_override = strip_standalone_gtk3_import(
        gtk3_override_path.read_text(encoding="utf-8")
    )
    gtk4_override = gtk4_override_path.read_text(encoding="utf-8")
    shell_override = shell_override_path.read_text(encoding="utf-8")

    base_theme = base_root / base_name
    shutil.copytree(base_theme / "gtk-3.0", gtk3_dir, dirs_exist_ok=True)
    shutil.copytree(base_theme / "gtk-4.0", gtk4_dir, dirs_exist_ok=True)
    shutil.copytree(base_theme / "gnome-shell", shell_dir, dirs_exist_ok=True)

    base_gtk3 = (base_theme / "gtk-3.0" / "gtk.css").read_text(encoding="utf-8")
    base_gtk4 = (base_theme / "gtk-4.0" / "gtk.css").read_text(encoding="utf-8")
    base_shell = (base_theme / "gnome-shell" / "gnome-shell.css").read_text(encoding="utf-8")
    base_gtk4, gtk4_state_rewrites = rewrite_target_gtk4_states(
        base_gtk4,
        base_name,
        palette,
    )

    design_name = str(design.get("name", "Glaze UI"))
    design_version = str(design["version"])
    lifecycle = design.get("lifecycle")
    design_label = f"{design_name} {design_version}"
    if lifecycle:
        design_label += f" ({lifecycle})"

    gtk3_banner = (
        f"\n\n/* GoreeCloud {design_label} semantic overrides.\n"
        " * GTK 3 base copied locally from the verified installed Zorin OS 17.3 theme. */\n"
    )
    gtk4_banner = (
        f"\n\n/* GoreeCloud {design_label} semantic overrides.\n"
        " * GTK 4 base copied locally from the verified installed Zorin OS 17.3 theme.\n"
        " * Hash-pinned Zorin 17.3 selected/checked state blocks were rewritten above before overrides. */\n"
    )
    shell_banner = (
        f"\n\n/* GoreeCloud {design_label} semantic overrides.\n"
        " * Base copied locally from the verified installed Zorin OS 17.3 Shell theme. */\n"
    )
    composed_gtk3 = base_gtk3.rstrip() + gtk3_banner + gtk3_override
    composed_gtk4 = base_gtk4.rstrip() + gtk4_banner + gtk4_override.lstrip()
    composed_shell = base_shell.rstrip() + shell_banner + shell_override.lstrip()

    (gtk3_dir / "gtk.css").write_text(composed_gtk3, encoding="utf-8")
    if (gtk3_dir / "gtk-dark.css").exists():
        (gtk3_dir / "gtk-dark.css").write_text(composed_gtk3, encoding="utf-8")
    (gtk3_dir / "goreecloud-overrides.css").write_text(gtk3_override, encoding="utf-8")

    (gtk4_dir / "gtk.css").write_text(composed_gtk4, encoding="utf-8")
    (gtk4_dir / "gtk-dark.css").write_text(composed_gtk4, encoding="utf-8")
    (gtk4_dir / "goreecloud-overrides.css").write_text(gtk4_override, encoding="utf-8")
    (gtk4_dir / ".libadwaita").write_bytes(b"")

    (shell_dir / "gnome-shell.css").write_text(composed_shell, encoding="utf-8")
    (shell_dir / "goreecloud-overrides.css").write_text(shell_override, encoding="utf-8")

    provenance = {
        "status": "Development target composition",
        "target": "Zorin OS 17.3",
        "package": TARGET_PACKAGE,
        "package_version": TARGET_PACKAGE_VERSION,
        "base_theme": base_name,
        "palette_contract": str(palette_path),
        "design_system": {
            "name": design_name,
            "version": design_version,
            "lifecycle": lifecycle,
        },
        "verified_files": evidence,
        "target_rewrites": {
            "gtk4_selected_and_checked_state_rules": gtk4_state_rewrites,
        },
        "note": (
            "The GoreeCloud repository does not redistribute these Zorin base bytes. "
            "The installer copied them locally from this device after exact hash verification, "
            "rewrote only the verified Zorin OS 17.3 GTK 4 generic selected-row and checked-switch "
            "state blocks in that hash-pinned base using the selected Glaze palette contract, "
            "then appended GoreeCloud semantic overrides."
        ),
    }
    (theme / "goreecloud-base.json").write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if DEFAULT_COPYRIGHT.is_file():
        shutil.copy2(DEFAULT_COPYRIGHT, theme / "ZORIN_BASE_COPYRIGHT")


def main() -> int:
    args = parse_args()
    theme_root = args.theme_root.expanduser().resolve()
    base_root = args.base_root.expanduser().resolve()
    palette_path = resolve_input(args.palette_config)

    package_version = installed_package_version()
    if package_version != TARGET_PACKAGE_VERSION:
        raise SystemExit(
            f"Unsupported {TARGET_PACKAGE} version {package_version!r}; "
            f"verified target version is {TARGET_PACKAGE_VERSION!r}. "
            "Run ./scripts/diagnose.sh before adapting this Development candidate."
        )

    design, palettes = load_palette_contract(palette_path)
    verified = {
        base_name: verify_base(base_root, base_name)
        for base_name in sorted(set(VARIANT_BASE.values()))
    }

    for theme_id, base_name in VARIANT_BASE.items():
        if not (theme_root / theme_id).is_dir():
            raise SystemExit(f"Generated theme folder is missing: {theme_root / theme_id}")
        compose_variant(
            theme_root,
            base_root,
            theme_id,
            base_name,
            verified[base_name],
            palettes[theme_id],
            design,
            palette_path,
        )
        print(
            f"Composed {theme_id} with verified {base_name} target base, "
            f"{design.get('name', 'Glaze UI')} {design['version']} palette state rewrites, "
            "and verified Zorin 17.3 GTK 4 selected/checked state rewrites"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
