#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_GTK=0

if [[ "${1:-}" == "--gtk" ]]; then
  RUN_GTK=1
elif [[ $# -gt 0 ]]; then
  echo "Usage: $0 [--gtk]" >&2
  exit 64
fi

python3 -m py_compile "$ROOT/scripts/build.py"
bash -n "$ROOT/scripts/install.sh"
bash -n "$ROOT/scripts/uninstall.sh"
bash -n "$ROOT/scripts/validate.sh"

TEMP_ROOT="$(mktemp -d)"
TEMP_HOME="$(mktemp -d)"
cleanup() {
  rm -rf -- "$TEMP_ROOT" "$TEMP_HOME"
}
trap cleanup EXIT

python3 "$ROOT/scripts/build.py" --output "$TEMP_ROOT"

python3 - "$ROOT" "$TEMP_ROOT" <<'PY'
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
generated = Path(sys.argv[2])

config = json.loads((root / "config" / "palettes.json").read_text(encoding="utf-8"))
required = {
    "id", "display_name", "mode", "gtk_base_import",
    "canvas", "surface", "elevated", "deep", "text", "muted", "border",
    "accent", "accent_hover", "accent_soft", "on_accent", "selection",
    "destructive", "destructive_hover", "atmosphere_amber",
    "shell_panel", "shell_surface", "shell_elevated", "shell_border",
    "shell_hover", "shell_active", "shell_shadow",
}

ids = []
for variant in config["variants"]:
    missing = required - set(variant)
    if missing:
        raise SystemExit(f"{variant.get('id', '<unknown>')}: missing palette keys: {sorted(missing)}")
    ids.append(variant["id"])

if len(ids) != len(set(ids)):
    raise SystemExit("Duplicate theme IDs found")

for theme_id in ids:
    theme_root = generated / theme_id
    required_files = [
        theme_root / "index.theme",
        theme_root / "gtk-3.0" / "gtk.css",
        theme_root / "gnome-shell" / "gnome-shell.css",
    ]
    for path in required_files:
        if not path.is_file():
            raise SystemExit(f"Missing generated file: {path}")

    for path in required_files:
        text = path.read_text(encoding="utf-8")
        if "{{" in text or "}}" in text:
            raise SystemExit(f"Unresolved template marker in {path}")

    gtk = (theme_root / "gtk-3.0" / "gtk.css").read_text(encoding="utf-8")
    shell = (theme_root / "gnome-shell" / "gnome-shell.css").read_text(encoding="utf-8")

    for label, css in (("gtk", gtk), ("shell", shell)):
        if css.count("{") != css.count("}"):
            raise SystemExit(f"{theme_id}: unbalanced braces in {label} stylesheet")

    if "resource:///org/gtk/libgtk/theme/Adwaita/" not in gtk:
        raise SystemExit(f"{theme_id}: GTK compatibility base import is missing")
    if "gtk-4.0" in str(theme_root) or (theme_root / "gtk-4.0").exists():
        raise SystemExit(f"{theme_id}: unvalidated GTK 4 output must not be generated")
    if list(theme_root.rglob(".libadwaita")):
        raise SystemExit(f"{theme_id}: libadwaita opt-in marker must not be generated")

    index = (theme_root / "index.theme").read_text(encoding="utf-8")
    if f"GtkTheme={theme_id}" not in index:
        raise SystemExit(f"{theme_id}: index.theme does not identify its GTK theme")

# Prevent accidental reusable secret material in the small text repository.
secret_patterns = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"][^'\"]+['\"]"),
]
for path in root.rglob("*"):
    if not path.is_file() or ".git" in path.parts or "build" in path.parts:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for pattern in secret_patterns:
        if pattern.search(text):
            raise SystemExit(f"Potential reusable secret material detected in {path}")

print("Static theme validation passed")
PY

if [[ "$RUN_GTK" -eq 1 ]]; then
  command -v xvfb-run >/dev/null || {
    echo "xvfb-run is required for --gtk validation" >&2
    exit 69
  }

  mkdir -p "$TEMP_HOME/.local/share/themes"
  cp -a "$TEMP_ROOT"/GoreeCloud-Zorin-* "$TEMP_HOME/.local/share/themes/"

  for theme in GoreeCloud-Zorin-Light GoreeCloud-Zorin-Dark GoreeCloud-Zorin-DeepDark; do
    echo "GTK smoke-load: $theme"
    HOME="$TEMP_HOME" \
    GTK_THEME="$theme" \
    THEME_CSS="$TEMP_ROOT/$theme/gtk-3.0/gtk.css" \
    NO_AT_BRIDGE=1 \
    xvfb-run -a python3 - <<'PY'
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk

# Parse the generated stylesheet explicitly. This treats GTK CSS parser
# errors as validation failures without converting unrelated runtime warnings
# (for example, a missing AT-SPI bus in headless CI) into fatal signals.
errors = []
provider = Gtk.CssProvider()
provider.connect(
    "parsing-error",
    lambda _provider, _section, error: errors.append(str(error)),
)
provider.load_from_path(os.environ["THEME_CSS"])
if errors:
    raise SystemExit("GTK CSS parsing failed: " + " | ".join(errors))

screen = Gdk.Screen.get_default()
if screen is None:
    raise SystemExit("GTK smoke-load could not acquire an Xvfb screen")
Gtk.StyleContext.add_provider_for_screen(
    screen,
    provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER,
)

window = Gtk.Window()
box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
box.set_border_width(12)
box.pack_start(Gtk.Entry(), False, False, 0)
box.pack_start(Gtk.Button(label="GoreeCloud"), False, False, 0)
box.pack_start(Gtk.Switch(), False, False, 0)
window.add(box)
window.show_all()
while Gtk.events_pending():
    Gtk.main_iteration()
window.destroy()
PY
  done
fi

echo "Validation completed successfully"
