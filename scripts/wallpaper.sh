#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT/assets/wallpapers"
DEST_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/backgrounds/GoreeCloud-Zorin"
STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/goreecloud-zorin/wallpaper"
SCHEMA="org.gnome.desktop.background"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/wallpaper.sh install
  ./scripts/wallpaper.sh apply current|light|dark|deep-dark
  ./scripts/wallpaper.sh restore
  ./scripts/wallpaper.sh status

The helper installs GoreeCloud wallpaper assets user-locally. Applying a wallpaper
changes only the current user's GNOME desktop background settings and records a
restorable settings snapshot first. It never deletes or overwrites Zorin's
system wallpaper files.
EOF
}

wallpaper_file_for_mode() {
  case "$1" in
    light) printf '%s\n' "goreecloud-horizon-light.svg" ;;
    dark) printf '%s\n' "goreecloud-horizon-dark.svg" ;;
    deep-dark) printf '%s\n' "goreecloud-horizon-deep-dark.svg" ;;
    *) return 1 ;;
  esac
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
      echo "Choose light, dark, or deep-dark explicitly." >&2
      return 2
      ;;
  esac
}

schema_has_key() {
  gsettings list-keys "$SCHEMA" 2>/dev/null | grep -Fxq -- "$1"
}

install_wallpapers() {
  mkdir -p -- "$DEST_DIR"
  for file in \
    goreecloud-horizon-light.svg \
    goreecloud-horizon-dark.svg \
    goreecloud-horizon-deep-dark.svg; do
    test -f "$SOURCE_DIR/$file"
    cp -f -- "$SOURCE_DIR/$file" "$DEST_DIR/$file"
  done
  printf 'Installed GoreeCloud wallpapers to:\n  %s\n' "$DEST_DIR"
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
  local mode="$1"
  if [[ "$mode" == "current" ]]; then
    mode="$(detect_mode)"
  fi

  local file
  file="$(wallpaper_file_for_mode "$mode")" || {
    echo "Unknown wallpaper mode: $mode" >&2
    usage >&2
    exit 64
  }

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

  printf 'Applied GoreeCloud %s wallpaper:\n  %s\n' "$mode" "$target"
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

show_status() {
  printf 'GoreeCloud wallpaper asset directory:\n  %s\n' "$DEST_DIR"
  if [[ -d "$DEST_DIR" ]]; then
    find "$DEST_DIR" -maxdepth 1 -type f -name 'goreecloud-horizon-*.svg' -print | sort
  fi
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
