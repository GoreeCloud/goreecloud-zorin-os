#!/usr/bin/env python3
"""Read-only GTK 4/libadwaita runtime-precedence diagnostic for Zorin OS 17.3.

This helper does not modify settings, themes, configuration files, processes, or
system packages. It is intended to distinguish installed-theme CSS correctness
from user-config or libadwaita runtime provider precedence.
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
MATCH_RE = re.compile(
    r"(?i)(#bde6fb|#174f52|#1c8a8d|row\.activatable:selected|"
    r"navigation-sidebar|switch:checked|switch:backdrop:checked|\.libadwaita)"
)
SAFE_ENV_KEYS = (
    "GTK_THEME",
    "GTK_DEBUG",
    "GDK_DEBUG",
    "ADW_DEBUG_COLOR_SCHEME",
    "XDG_CONFIG_HOME",
    "XDG_DATA_HOME",
    "XDG_DATA_DIRS",
)


def section(title: str) -> None:
    print(f"\n== {title} ==")


def run(*args: str) -> str | None:
    try:
        result = subprocess.run(
            args,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def print_file_evidence(path: Path, *, max_matches: int = 120) -> None:
    print(path)
    if not path.exists():
        print("  status: missing")
        return
    if path.is_symlink():
        try:
            print(f"  symlink -> {path.resolve(strict=True)}")
        except FileNotFoundError:
            print(f"  symlink -> broken ({os.readlink(path)})")
            return
    if not path.is_file():
        print("  status: not a regular file")
        return
    print(f"  bytes: {path.stat().st_size}")
    print(f"  sha256: {sha256(path)}")
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"  read error: {exc}")
        return
    matches = 0
    for lineno, line in enumerate(text.splitlines(), start=1):
        if MATCH_RE.search(line):
            print(f"  {lineno}: {line}")
            matches += 1
            if matches >= max_matches:
                print(f"  ... truncated after {max_matches} matching lines")
                break
    if matches == 0:
        print("  targeted state/color matches: none")


def print_directory(path: Path) -> None:
    print(path)
    if not path.exists():
        print("  status: missing")
        return
    if not path.is_dir():
        print("  status: not a directory")
        return
    entries = sorted(path.iterdir(), key=lambda item: item.name)
    if not entries:
        print("  status: empty")
        return
    for entry in entries[:100]:
        kind = "dir" if entry.is_dir() else "file"
        if entry.is_symlink():
            kind = "symlink"
        suffix = ""
        if entry.is_symlink():
            try:
                suffix = f" -> {entry.resolve(strict=True)}"
            except FileNotFoundError:
                suffix = f" -> broken ({os.readlink(entry)})"
        print(f"  {kind:7s} {entry.name}{suffix}")
    if len(entries) > 100:
        print(f"  ... {len(entries) - 100} more entries omitted")


def gsetting(schema: str, key: str) -> str:
    value = run("gsettings", "get", schema, key)
    return value if value is not None else "unavailable"


def process_env(pid: str) -> dict[str, str]:
    env_path = Path("/proc") / pid / "environ"
    try:
        raw = env_path.read_bytes()
    except OSError:
        return {}
    env: dict[str, str] = {}
    for item in raw.split(b"\0"):
        if b"=" not in item:
            continue
        key_b, value_b = item.split(b"=", 1)
        key = key_b.decode("utf-8", errors="replace")
        if key in SAFE_ENV_KEYS:
            env[key] = value_b.decode("utf-8", errors="replace")
    return env


def libadwaita_path() -> Path | None:
    output = run("ldconfig", "-p")
    if not output:
        return None
    for line in output.splitlines():
        if "libadwaita-1.so.0" not in line or "=>" not in line:
            continue
        candidate = Path(line.split("=>", 1)[1].strip())
        if candidate.is_file():
            return candidate
    return None


def print_library_strings(path: Path) -> None:
    print(path)
    strings = run("strings", str(path))
    if strings is None:
        print("  strings output unavailable")
        return
    needles = (".libadwaita", "gtk-4.0", "gtk-theme-name", "/themes/", "settings.ini")
    matched = [line for line in strings.splitlines() if any(needle in line for needle in needles)]
    if not matched:
        print("  targeted path/provider strings: none")
        return
    for line in matched[:80]:
        print(f"  {line}")
    if len(matched) > 80:
        print(f"  ... {len(matched) - 80} more matching strings omitted")


def main() -> int:
    print("GoreeCloud GTK 4/libadwaita runtime diagnostic (read-only)")
    print("This helper changes no settings, files, processes, or packages.")

    section("Repository")
    print(f"commit: {run('git', '-C', str(REPO_ROOT), 'rev-parse', 'HEAD') or 'unavailable'}")
    print(f"branch: {run('git', '-C', str(REPO_ROOT), 'branch', '--show-current') or 'unavailable'}")

    section("Current theme settings")
    print(f"GTK theme: {gsetting('org.gnome.desktop.interface', 'gtk-theme')}")
    print(f"color scheme: {gsetting('org.gnome.desktop.interface', 'color-scheme')}")
    print(f"Shell user theme: {gsetting('org.gnome.shell.extensions.user-theme', 'name')}")
    print(f"process GTK_THEME: {os.environ.get('GTK_THEME', '<unset>')}")
    print(f"XDG_CONFIG_HOME: {os.environ.get('XDG_CONFIG_HOME', '<unset; defaults to ~/.config>')}")
    print(f"XDG_DATA_HOME: {os.environ.get('XDG_DATA_HOME', '<unset; defaults to ~/.local/share>')}")

    section("User GTK 4 configuration directory")
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config"))
    gtk4_config = config_home / "gtk-4.0"
    print_directory(gtk4_config)
    for name in ("gtk.css", "gtk-dark.css", "settings.ini"):
        print_file_evidence(gtk4_config / name)

    section("Installed GoreeCloud Dark GTK 4 files")
    data_home = Path(os.environ.get("XDG_DATA_HOME", HOME / ".local" / "share"))
    installed_gtk4 = data_home / "themes" / "GoreeCloud-Zorin-Dark" / "gtk-4.0"
    print_directory(installed_gtk4)
    for name in ("gtk.css", "gtk-dark.css", ".libadwaita"):
        print_file_evidence(installed_gtk4 / name)

    section("Settings process environment")
    pids_text = run("pidof", "gnome-control-center")
    if not pids_text:
        print("gnome-control-center: not running")
    else:
        pids = pids_text.split()
        print(f"gnome-control-center pid(s): {' '.join(pids)}")
        for pid in pids:
            print(f"  pid {pid} selected environment:")
            env = process_env(pid)
            if not env:
                print("    no targeted override variables set or /proc access unavailable")
            else:
                for key in SAFE_ENV_KEYS:
                    if key in env:
                        print(f"    {key}={env[key]}")

    section("libadwaita patch/provider strings")
    lib_path = libadwaita_path()
    if lib_path is None:
        print("libadwaita-1.so.0 path: unavailable")
    else:
        print_library_strings(lib_path)

    section("Interpretation boundary")
    print("If the installed GoreeCloud GTK 4 files contain #174F52/#1C8A8D while Settings still renders #BDE6FB,")
    print("the generated theme bytes are not the missing source. User GTK 4 configuration or libadwaita provider precedence")
    print("must be resolved before making further styling changes. Do not copy, replace, or delete ~/.config/gtk-4.0 files")
    print("based only on this diagnostic; preserve existing user configuration until its ownership/purpose is identified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
