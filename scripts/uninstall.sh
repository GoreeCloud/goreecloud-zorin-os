#!/usr/bin/env bash
set -euo pipefail

DEST="${XDG_DATA_HOME:-$HOME/.local/share}/themes"
STAMP="$(date +%Y%m%d-%H%M%S)"
RECOVERY_ROOT="$DEST/.goreecloud-zorin-recovery/uninstalled-$STAMP"
THEMES=(
  "GoreeCloud-Zorin-Light"
  "GoreeCloud-Zorin-Dark"
  "GoreeCloud-Zorin-DeepDark"
)

echo "Before uninstalling, select a different Applications and Shell theme"
echo "in Zorin Appearance so the desktop is not left pointing at a removed theme."
echo

moved=0
for theme in "${THEMES[@]}"; do
  target="$DEST/$theme"
  if [[ -e "$target" ]]; then
    mkdir -p -- "$RECOVERY_ROOT"
    mv -- "$target" "$RECOVERY_ROOT/$theme"
    moved=1
  fi
done

if [[ "$moved" -eq 1 ]]; then
  echo "Moved GoreeCloud theme folders into recovery storage:"
  echo "  $RECOVERY_ROOT"
else
  echo "No installed GoreeCloud Zorin theme folders were found in:"
  echo "  $DEST"
fi
