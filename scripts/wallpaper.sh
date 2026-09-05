#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT/assets/wallpapers"
MANIFEST="$ROOT/config/wallpapers.json"
DEST_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/backgrounds/GoreeCloud-Zorin"
CATALOG_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/gnome-background-properties"
CATALOG_FILE="$CATALOG_DIR/goreecloud-zorin.xml"
STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/goreecloud-zorin/wallpaper"
SCHEMA="org.gnome.desktop.background"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/wallpaper.sh install
  ./scripts/wallpaper.sh list
  ./scripts/wallpaper.sh apply current|light|dark|deep-dark|WALLPAPER_ID
  ./scripts/wallpaper.sh restore
  ./scripts/wallpaper.sh status

The helper installs the full GoreeCloud wallpaper collection user-locally and
writes a GNOME Background Properties catalog under the current user's data
directory. Applying a wallpaper changes only the current user's GNOME desktop
background settings and records a restorable settings snapshot first.

This helper does not remove stock Zorin system wallpaper files. Use the
read-only scripts/diagnose_backgrounds.sh before any privileged replacement.
EOF
}

detect_mode() {
  local theme
  theme="$(gsettings get org.gnome.desktop.interface gtk-theme 2>/dev/null | tr -d "'" || true)"
  case "$theme" in
    GoreeCloud-Zorin-Light) printf '%s\n' "light" ;;
    GoreeCloud-Zorin-Dark) printf '%s\n' "dark" ;;
    GoreeCloud-Zorin-DeepDark) printf '%s\n' "deep-dark" ;;
    *)
      echo "Cannot infer a GoreeCloud wallpaper from GTK theme: ${theme:-unknown}" >&2
      echo "Choose a wallpaper ID or light, dark, or deep-dark explicitly." >&2
      return 2
      ;;
  esac
}

primary_id_for_mode() {
  python3 - "$MANIFEST" "$1" <<'PY'
import json, sys
data=json.load(open(sys.argv[1], encoding="utf-8"))
mode=sys.argv[2]
matches=[w["id"] for w in data["wallpapers"] if w["mode"] == mode]
if len(matches) != 1:
    raise SystemExit(f"Expected one primary wallpaper for {mode}; found {len(matches)}")
print(matches[0])
PY
}

file_for_id() {
  python3 - "$MANIFEST" "$1" <<'PY'
import json, sys
data=json.load(open(sys.argv[1], encoding="utf-8"))
wallpaper_id=sys.argv[2]
matches=[w["id"] for w in data["catalog"] if w["id"] == wallpaper_id]
if len(matches) != 1:
    raise SystemExit(f"Unknown or duplicate wallpaper ID: {wallpaper_id}")
print(matches[0] + ".svg")
PY
}

schema_has_key() {
  gsettings list-keys "$SCHEMA" 2>/dev/null | grep -Fxq -- "$1"
}

install_wallpapers() {
  python3 "$ROOT/scripts/validate_wallpapers.py" >/dev/null
  mkdir -p -- "$DEST_DIR" "$CATALOG_DIR"
  local temp_dir
  temp_dir="$(mktemp -d)"
  trap 'rm -rf -- "$temp_dir"' RETURN
  python3 "$ROOT/scripts/build_wallpapers.py" --output "$temp_dir" >/dev/null
  while IFS= read -r wallpaper_id; do
    [[ -n "$wallpaper_id" ]] || continue
    cp -f -- "$temp_dir/$wallpaper_id.svg" "$DEST_DIR/$wallpaper_id.svg"
  done < <(python3 - "$MANIFEST" <<'PY'
import json, sys
data=json.load(open(sys.argv[1], encoding="utf-8"))
for item in data["catalog"]:
    print(item["id"])
PY
)
  python3 "$ROOT/scripts/build_background_catalog.py" \
    --manifest "$MANIFEST" \
    --filename-root "$DEST_DIR" \
    --output "$CATALOG_FILE"
  rm -rf -- "$temp_dir"
  trap - RETURN
  printf 'Installed GoreeCloud wallpaper collection to:\n  %s\n' "$DEST_DIR"
  printf 'Installed user background catalog to:\n  %s\n' "$CATALOG_FILE"
}

backup_settings() {
  mkdir -p -- "$STATE_DIR"
  local stamp snapshot
  stamp="$(date +%Y%m%d-%H%M%S)"
  snapshot="$STATE_DIR/settings-$stamp.txt"
  : > "$snapshot"
  for key in picture-uri picture-uri-dark picture-options primary-color secondary-color color-shading-type; do
    if schema_has_key "$key"; then
      printf '%s\t%s\n' "$key" "$(gsettings get "$SCHEMA" "$key")" >> "$snapshot"
    fi
  done
  printf '%s\n' "$snapshot"
}

apply_wallpaper() {
  local selection="$1" mode wallpaper_id file
  if [[ "$selection" == "current" ]]; then
    mode="$(detect_mode)"
    wallpaper_id="$(primary_id_for_mode "$mode")"
  elif [[ "$selection" == "light" || "$selection" == "dark" || "$selection" == "deep-dark" ]]; then
    wallpaper_id="$(primary_id_for_mode "$selection")"
  else
    wallpaper_id="$selection"
  fi

  file="$(file_for_id "$wallpaper_id")"
  command -v gsettings >/dev/null 2>&1 || {
    echo "gsettings is required to apply a wallpaper." >&2
    exit 69
  }

  install_wallpapers >/dev/null
  local snapshot uri target
  snapshot="$(backup_settings)"
  target="$DEST_DIR/$file"
  uri="$(python3 - "$target" <<'PY'
from pathlib import Path
import sys
print(Path(sys.argv[1]).resolve().as_uri())
PY
)"

  gsettings set "$SCHEMA" picture-uri "'$uri'"
  if schema_has_key picture-uri-dark; then
    gsettings set "$SCHEMA" picture-uri-dark "'$uri'"
  fi
  if schema_has_key picture-options; then
    gsettings set "$SCHEMA" picture-options "'zoom'"
  fi

  printf 'Applied GoreeCloud wallpaper %s:\n  %s\n' "$wallpaper_id" "$target"
  printf 'Previous GNOME background settings were preserved at:\n  %s\n' "$snapshot"
}

restore_wallpaper() {
  command -v gsettings >/dev/null 2>&1 || {
    echo "gsettings is required to restore wallpaper settings." >&2
    exit 69
  }

  local snapshot
  snapshot="$(find "$STATE_DIR" -maxdepth 1 -type f -name 'settings-*.txt' -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -n1 | cut -d' ' -f2- || true)"
  if [[ -z "$snapshot" || ! -f "$snapshot" ]]; then
    echo "No GoreeCloud wallpaper settings snapshot is available to restore." >&2
    exit 1
  fi

  while IFS=$'\t' read -r key value; do
    [[ -n "$key" ]] || continue
    if schema_has_key "$key"; then
      gsettings set "$SCHEMA" "$key" "$value"
    fi
  done < "$snapshot"

  printf 'Restored GNOME background settings from:\n  %s\n' "$snapshot"
}

list_wallpapers() {
  python3 - "$MANIFEST" <<'PY'
import json, sys
data=json.load(open(sys.argv[1], encoding="utf-8"))
for category in data["collection"]["categories"]:
    print(f"\n{category}")
    for item in data["catalog"]:
        if item["category"] == category:
            print(f"  {item['id']:<38} {item['family']} / {item['mode']}")
PY
}

show_status() {
  printf 'GoreeCloud wallpaper asset directory:\n  %s\n' "$DEST_DIR"
  if [[ -d "$DEST_DIR" ]]; then
    find "$DEST_DIR" -maxdepth 1 -type f -name '*.svg' -print | sort
  fi
  printf '\nUser background catalog:\n  %s\n' "$CATALOG_FILE"
  if command -v gsettings >/dev/null 2>&1; then
    printf '\nCurrent GNOME background settings:\n'
    for key in picture-uri picture-uri-dark picture-options; do
      if schema_has_key "$key"; then
        printf '%-18s %s\n' "$key" "$(gsettings get "$SCHEMA" "$key")"
      fi
    done
  fi
}

case "${1:-}" in
  install)
    [[ $# -eq 1 ]] || { usage >&2; exit 64; }
    install_wallpapers
    ;;
  list)
    [[ $# -eq 1 ]] || { usage >&2; exit 64; }
    list_wallpapers
    ;;
  apply)
    [[ $# -eq 2 ]] || { usage >&2; exit 64; }
    apply_wallpaper "$2"
    ;;
  restore)
    [[ $# -eq 1 ]] || { usage >&2; exit 64; }
    restore_wallpaper
    ;;
  status)
    [[ $# -eq 1 ]] || { usage >&2; exit 64; }
    show_status
    ;;
  *)
    usage >&2
    exit 64
    ;;
esac
