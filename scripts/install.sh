#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${XDG_DATA_HOME:-$HOME/.local/share}/themes"
STAMP="$(date +%Y%m%d-%H%M%S)"
RECOVERY_ROOT="$DEST/.goreecloud-zorin-recovery/$STAMP"
THEMES=(
  "GoreeCloud-Zorin-Light"
  "GoreeCloud-Zorin-Dark"
  "GoreeCloud-Zorin-DeepDark"
)

TEMP_ROOT="$(mktemp -d)"
cleanup() {
  rm -rf -- "$TEMP_ROOT"
}
trap cleanup EXIT

python3 "$ROOT/scripts/build.py" --output "$TEMP_ROOT"
mkdir -p -- "$DEST"

backed_up=0
for theme in "${THEMES[@]}"; do
  target="$DEST/$theme"
  if [[ -e "$target" ]]; then
    mkdir -p -- "$RECOVERY_ROOT"
    mv -- "$target" "$RECOVERY_ROOT/$theme"
    backed_up=1
  fi
  cp -a -- "$TEMP_ROOT/$theme" "$target"
done

echo
echo "Installed GoreeCloud Zorin themes to:"
echo "  $DEST"

if [[ "$backed_up" -eq 1 ]]; then
  echo "Previous GoreeCloud theme folders were preserved at:"
  echo "  $RECOVERY_ROOT"
fi

echo
echo "Next: open Zorin Appearance -> Themes -> Other, then select"
echo "a GoreeCloud variant for Applications and Shell."
