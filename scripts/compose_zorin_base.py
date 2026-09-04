#!/usr/bin/env python3
"""Compose generated GoreeCloud overrides with the verified Zorin OS 17.3 base."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

TARGET_PACKAGE = "zorin-desktop-themes"
TARGET_PACKAGE_VERSION = "4.2.2"
DEFAULT_BASE_ROOT = Path("/usr/share/themes")
DEFAULT_COPYRIGHT = Path("/usr/share/doc/zorin-desktop-themes/copyright")
GTK3_ADWAITA_IMPORT_PREFIX = '@import url("resource:///org/gtk/libgtk/theme/Adwaita/'

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
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def compose_variant(
    theme_root: Path,
    base_root: Path,
    theme_id: str,
    base_name: str,
    evidence: dict,
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

    gtk3_banner = (
        "\n\n/* GoreeCloud Glaze UI V1.1 semantic overrides.\n"
        " * GTK 3 base copied locally from the verified installed Zorin OS 17.3 theme. */\n"
    )
    gtk4_banner = (
        "\n\n/* GoreeCloud Glaze UI V1.1 semantic overrides.\n"
        " * GTK 4 base copied locally from the verified installed Zorin OS 17.3 theme. */\n"
    )
    shell_banner = (
        "\n\n/* GoreeCloud Glaze UI V1.1 semantic overrides.\n"
        " * Base copied locally from the verified installed Zorin OS 17.3 Shell theme. */\n"
    )
    composed_gtk3 = base_gtk3.rstrip() + gtk3_banner + gtk3_override
    composed_gtk4 = base_gtk4.rstrip() + gtk4_banner + gtk4_override.lstrip()
    composed_shell = base_shell.rstrip() + shell_banner + shell_override.lstrip()

    (gtk3_dir / "gtk.css").write_text(composed_gtk3, encoding="utf-8")
    # Keep the explicitly selected GoreeCloud variant even when a GTK 3
    # application requests a dark variant independently.
    if (gtk3_dir / "gtk-dark.css").exists():
        (gtk3_dir / "gtk-dark.css").write_text(composed_gtk3, encoding="utf-8")
    (gtk3_dir / "goreecloud-overrides.css").write_text(gtk3_override, encoding="utf-8")

    (gtk4_dir / "gtk.css").write_text(composed_gtk4, encoding="utf-8")
    # Keep an explicit-variant appearance even if a patched libadwaita path asks
    # for gtk-dark.css because the desktop color preference differs from the
    # Applications theme selected in Zorin Appearance.
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
        "verified_files": evidence,
        "note": (
            "The GoreeCloud repository does not redistribute these Zorin base bytes. "
            "The installer copied them locally from this device after exact hash verification, "
            "then appended GoreeCloud Glaze UI semantic overrides."
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

    package_version = installed_package_version()
    if package_version != TARGET_PACKAGE_VERSION:
        raise SystemExit(
            f"Unsupported {TARGET_PACKAGE} version {package_version!r}; "
            f"verified target version is {TARGET_PACKAGE_VERSION!r}. "
            "Run ./scripts/diagnose.sh before adapting this Development candidate."
        )

    verified = {
        base_name: verify_base(base_root, base_name)
        for base_name in sorted(set(VARIANT_BASE.values()))
    }

    for theme_id, base_name in VARIANT_BASE.items():
        if not (theme_root / theme_id).is_dir():
            raise SystemExit(f"Generated theme folder is missing: {theme_root / theme_id}")
        compose_variant(theme_root, base_root, theme_id, base_name, verified[base_name])
        print(f"Composed {theme_id} with verified {base_name} target base")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
