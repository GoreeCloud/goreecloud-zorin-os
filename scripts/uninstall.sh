#!/usr/bin/env bash
set -euo pipefail

DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
THEME_DEST="$DATA_HOME/themes"
ICON_DEST="$DATA_HOME/icons"
STAMP="$(date +%Y%m%d-%H%M%S)"
THEME_RECOVERY_ROOT="$THEME_DEST/.goreecloud-zorin-recovery/uninstalled-$STAMP"
ASSET_RECOVERY_ROOT="$ICON_DEST/.goreecloud-zorin-recovery/uninstalled-$STAMP"
THEMES=(
  "GoreeCloud-Zorin-Light"
  "GoreeCloud-Zorin-Dark"
  "GoreeCloud-Zorin-DeepDark"
)
ICON_THEME="GoreeCloud-Zorin"
CURSOR_THEME="GoreeCloud-Zorin-Cursors"

reset_if_selected() {
  if ! command -v gsettings >/dev/null 2>&1; then
    return 0
  fi

  local current
  current="$(gsettings get org.gnome.desktop.interface gtk-theme 2>/dev/null | tr -d "'" || true)"
  case "$current" in
    GoreeCloud-Zorin-Light|GoreeCloud-Zorin-Dark|GoreeCloud-Zorin-DeepDark)
      gsettings reset org.gnome.desktop.interface gtk-theme
      ;;
  esac

  current="$(gsettings get org.gnome.desktop.interface icon-theme 2>/dev/null | tr -d "'" || true)"
  if [[ "$current" == "$ICON_THEME" ]]; then
    gsettings reset org.gnome.desktop.interface icon-theme
  fi

  current="$(gsettings get org.gnome.desktop.interface cursor-theme 2>/dev/null | tr -d "'" || true)"
  if [[ "$current" == "$CURSOR_THEME" ]]; then
    gsettings reset org.gnome.desktop.interface cursor-theme
  fi

  if gsettings list-schemas | grep -Fxq 'org.gnome.shell.extensions.user-theme'; then
    current="$(gsettings get org.gnome.shell.extensions.user-theme name 2>/dev/null | tr -d "'" || true)"
    case "$current" in
      GoreeCloud-Zorin-Light|GoreeCloud-Zorin-Dark|GoreeCloud-Zorin-DeepDark)
        gsettings reset org.gnome.shell.extensions.user-theme name
        ;;
    esac
  fi
}

reset_if_selected

theme_moved=0
for theme in "${THEMES[@]}"; do
  target="$THEME_DEST/$theme"
  if [[ -e "$target" ]]; then
    mkdir -p -- "$THEME_RECOVERY_ROOT"
    mv -- "$target" "$THEME_RECOVERY_ROOT/$theme"
    theme_moved=1
  fi
done

asset_moved=0
for asset in "$ICON_THEME" "$CURSOR_THEME"; do
  target="$ICON_DEST/$asset"
  if [[ -e "$target" ]]; then
    mkdir -p -- "$ASSET_RECOVERY_ROOT"
    mv -- "$target" "$ASSET_RECOVERY_ROOT/$asset"
    asset_moved=1
  fi
done

if [[ "$theme_moved" -eq 1 ]]; then
  echo "Moved GoreeCloud application/Shell themes into recovery storage:"
  echo "  $THEME_RECOVERY_ROOT"
else
  echo "No installed GoreeCloud application/Shell theme folders were found."
fi

if [[ "$asset_moved" -eq 1 ]]; then
  echo "Moved GoreeCloud icon/cursor themes into recovery storage:"
  echo "  $ASSET_RECOVERY_ROOT"
else
  echo "No installed GoreeCloud icon/cursor theme folders were found."
fi
