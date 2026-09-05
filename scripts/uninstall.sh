#!/usr/bin/env bash
set -euo pipefail

DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
THEME_DEST="$DATA_HOME/themes"
ICON_DEST="$DATA_HOME/icons"
LEGACY_ICON_DEST="$HOME/.icons"
STAMP="$(date +%Y%m%d-%H%M%S)"
THEME_RECOVERY_ROOT="$THEME_DEST/.goreecloud-zorin-recovery/uninstalled-$STAMP"
ASSET_RECOVERY_ROOT="$ICON_DEST/.goreecloud-zorin-recovery/uninstalled-$STAMP"
THEMES=(
  "GoreeCloud-Zorin-Light"
  "GoreeCloud-Zorin-Dark"
  "GoreeCloud-Zorin-DeepDark"
)
ASSETS=(
  "GoreeCloud-Zorin"
  "GoreeCloud-Zorin-Cursors"
)

echo "Before uninstalling, select a different Applications, Shell, Icons, and Cursor theme"
echo "so the desktop is not left pointing at removed GoreeCloud assets."
echo

moved=0
for theme in "${THEMES[@]}"; do
  target="$THEME_DEST/$theme"
  if [[ -e "$target" || -L "$target" ]]; then
    mkdir -p -- "$THEME_RECOVERY_ROOT"
    mv -- "$target" "$THEME_RECOVERY_ROOT/$theme"
    moved=1
  fi
done

asset_moved=0
for asset in "${ASSETS[@]}"; do
  target="$ICON_DEST/$asset"
  if [[ -e "$target" || -L "$target" ]]; then
    mkdir -p -- "$ASSET_RECOVERY_ROOT"
    mv -- "$target" "$ASSET_RECOVERY_ROOT/$asset"
    asset_moved=1
  fi

  legacy="$LEGACY_ICON_DEST/$asset"
  if [[ -L "$legacy" ]]; then
    link_target="$(readlink -- "$legacy")"
    if [[ "$link_target" == "$ICON_DEST/$asset" ]]; then
      rm -f -- "$legacy"
    fi
  fi
done

if [[ "$moved" -eq 1 ]]; then
  echo "Moved GoreeCloud theme folders into recovery storage:"
  echo "  $THEME_RECOVERY_ROOT"
else
  echo "No installed GoreeCloud Zorin theme folders were found in:"
  echo "  $THEME_DEST"
fi

if [[ "$asset_moved" -eq 1 ]]; then
  echo "Moved GoreeCloud icon/cursor folders into recovery storage:"
  echo "  $ASSET_RECOVERY_ROOT"
else
  echo "No installed GoreeCloud icon/cursor folders were found in:"
  echo "  $ICON_DEST"
fi
