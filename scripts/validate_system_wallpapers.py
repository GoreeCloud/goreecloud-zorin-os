#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "zorin-stock-wallpapers-17.3.json"
SCRIPT = ROOT / "scripts" / "system_wallpapers.py"
WRAPPER = ROOT / "scripts" / "system_wallpapers.sh"

EXPECTED_PACKAGES = {
    "zorin-os-wallpapers": "17.1",
    "zorin-os-wallpapers-17": "17.1",
    "zorin-os-pro-wallpapers": "17",
    "zorin-os-pro-wallpapers-17": "17",
}
EXPECTED_CATALOGS = {
    "/usr/share/gnome-background-properties/zorin-default-wallpapers.xml": "zorin-os-wallpapers",
    "/usr/share/gnome-background-properties/zorin-os-17-wallpapers.xml": "zorin-os-wallpapers-17",
    "/usr/share/gnome-background-properties/zorin-os-17-pro-wallpapers.xml": "zorin-os-pro-wallpapers-17",
}
EXPECTED_WALLPAPER_COUNT = 28
EXPECTED_REPLACEMENT_COUNT = 24


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        fail("Stock wallpaper manifest schema_version must be 1")
    if data.get("status") != "Development":
        fail("Stock wallpaper migration must remain Development until target acceptance")
    if data.get("target") != {"id": "zorin", "version": "17.3"}:
        fail("Stock wallpaper manifest must remain pinned to the verified Zorin OS 17.3 target")
    if data.get("recovery_root") != "/var/lib/goreecloud-zorin/wallpaper-recovery":
        fail("Unexpected stock wallpaper recovery root")

    packages = {item["name"]: item["version"] for item in data.get("packages", [])}
    if packages != EXPECTED_PACKAGES:
        fail(f"Audited package/version set changed: {packages}")

    catalogs = {item["path"]: item["owner"] for item in data.get("catalogs", [])}
    if catalogs != EXPECTED_CATALOGS:
        fail(f"Audited stock catalog set changed: {catalogs}")

    wallpapers = data.get("wallpaper_files", [])
    if len(wallpapers) != EXPECTED_WALLPAPER_COUNT:
        fail(f"Expected {EXPECTED_WALLPAPER_COUNT} audited stock wallpaper files")
    wallpaper_paths = [item["path"] for item in wallpapers]
    if len(wallpaper_paths) != len(set(wallpaper_paths)):
        fail("Duplicate stock wallpaper paths in audit manifest")
    for item in wallpapers:
        path = item["path"]
        owner = item["owner"]
        if not path.startswith("/usr/share/backgrounds/") or not path.lower().endswith(".jpg"):
            fail(f"Unexpected stock wallpaper path: {path}")
        if owner not in EXPECTED_PACKAGES:
            fail(f"Unexpected package owner {owner} for {path}")

    all_paths = list(catalogs) + wallpaper_paths
    if len(all_paths) != len(set(all_paths)):
        fail("Duplicate audited path across stock catalogs/wallpapers")

    replacement = data.get("replacement", {})
    if replacement.get("expected_wallpaper_count") != EXPECTED_REPLACEMENT_COUNT:
        fail("Replacement catalog must require exactly 24 GoreeCloud wallpapers")
    if replacement.get("user_background_dir") != "~/.local/share/backgrounds/GoreeCloud-Zorin":
        fail("Unexpected user replacement background directory")
    if replacement.get("user_catalog") != "~/.local/share/gnome-background-properties/goreecloud-zorin.xml":
        fail("Unexpected user replacement catalog path")

    text = SCRIPT.read_text(encoding="utf-8")
    for token in (
        "def plan(",
        "def apply(",
        "def restore(",
        "def finalize(",
        "def simulate_purge(",
        "def verify_replacement_ready(",
        '"--simulate", "purge"',
        '"purge", "--yes"',
        '"download", *self.package_specs()',
        '"stock-files.tar"',
        "apt-purge-simulation.txt",
        "stock-files.sha256.tsv",
    ):
        if token not in text:
            fail(f"System wallpaper workflow is missing required safety mechanism: {token}")
    if "shutil.rmtree" in text or "rm -rf" in text:
        fail("System wallpaper workflow must not use broad recursive deletion")
    if "os.walk(resolved, topdown=False)" not in text:
        fail("Finalize must use bounded transaction-tree deletion")
    if not SCRIPT.stat().st_mode & 0o111:
        fail("scripts/system_wallpapers.py must be executable")
    if not WRAPPER.stat().st_mode & 0o111:
        fail("scripts/system_wallpapers.sh must be executable")
    wrapper_text = WRAPPER.read_text(encoding="utf-8")
    if "exec python3" not in wrapper_text or "system_wallpapers.py" not in wrapper_text:
        fail("system wallpaper shell wrapper must delegate directly to the Python workflow")

    print(
        "System wallpaper replacement source validation passed: "
        f"{len(packages)} packages, {len(catalogs)} catalogs, "
        f"{len(wallpapers)} stock images, {EXPECTED_REPLACEMENT_COUNT} replacement wallpapers"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
