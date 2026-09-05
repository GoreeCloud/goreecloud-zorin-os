#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
THEME_DEST="$DATA_HOME/themes"
ICON_DEST="$DATA_HOME/icons"
STAMP="$(date +%Y%m%d-%H%M%S)"
THEME_RECOVERY_ROOT="$THEME_DEST/.goreecloud-zorin-recovery/$STAMP"
ASSET_RECOVERY_ROOT="$ICON_DEST/.goreecloud-zorin-recovery/$STAMP"
REPLACE_STOCK=0
THEMES=(
  "GoreeCloud-Zorin-Light"
  "GoreeCloud-Zorin-Dark"
  "GoreeCloud-Zorin-DeepDark"
)
ICON_THEME="GoreeCloud-Zorin"
CURSOR_THEME="GoreeCloud-Zorin-Cursors"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/install.sh
  ./scripts/install.sh --replace-stock

The install activates the light-first GoreeCloud desktop experience:
Applications theme, Shell theme, GoreeCloud icons, GoreeCloud cursors, and the
primary light wallpaper. --replace-stock additionally removes the audited
Zorin OS 17.3 stock wallpaper packages after recovery-backed checks pass.
EOF
}

case "${1:-}" in
  "") ;;
  --replace-stock) REPLACE_STOCK=1 ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    usage >&2
    exit 64
    ;;
esac
[[ $# -le 1 ]] || { usage >&2; exit 64; }

TEMP_ROOT="$(mktemp -d)"
cleanup() {
  rm -rf -- "$TEMP_ROOT"
}
trap cleanup EXIT

python3 "$ROOT/scripts/build.py" --output "$TEMP_ROOT/themes"
python3 "$ROOT/scripts/build_icons.py" --output "$TEMP_ROOT/icons"
python3 "$ROOT/scripts/build_cursors.py" --output "$TEMP_ROOT/cursors"

# Zorin OS 17.3's GTK 3, GTK 4, and Shell themes contain extensive
# platform-specific selectors and assets. Compose the generated GoreeCloud
# semantic overrides on top of the exact verified local Zorin 17.3 base before
# touching an existing installed GoreeCloud theme.
python3 "$ROOT/scripts/compose_zorin_base.py" "$TEMP_ROOT/themes"

mkdir -p -- "$THEME_DEST" "$ICON_DEST"

theme_backed_up=0
for theme in "${THEMES[@]}"; do
  target="$THEME_DEST/$theme"
  if [[ -e "$target" ]]; then
    mkdir -p -- "$THEME_RECOVERY_ROOT"
    mv -- "$target" "$THEME_RECOVERY_ROOT/$theme"
    theme_backed_up=1
  fi
  cp -a -- "$TEMP_ROOT/themes/$theme" "$target"
done

asset_backed_up=0
for asset in "$ICON_THEME" "$CURSOR_THEME"; do
  target="$ICON_DEST/$asset"
  if [[ -e "$target" ]]; then
    mkdir -p -- "$ASSET_RECOVERY_ROOT"
    mv -- "$target" "$ASSET_RECOVERY_ROOT/$asset"
    asset_backed_up=1
  fi
done
cp -a -- "$TEMP_ROOT/icons/$ICON_THEME" "$ICON_DEST/$ICON_THEME"
cp -a -- "$TEMP_ROOT/cursors/$CURSOR_THEME" "$ICON_DEST/$CURSOR_THEME"

if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache -f "$ICON_DEST/$ICON_THEME" >/dev/null 2>&1 || true
fi

activate_light_experience() {
  if ! command -v gsettings >/dev/null 2>&1; then
    return 0
  fi

  gsettings set org.gnome.desktop.interface gtk-theme "'GoreeCloud-Zorin-Light'"
  gsettings set org.gnome.desktop.interface icon-theme "'$ICON_THEME'"
  gsettings set org.gnome.desktop.interface cursor-theme "'$CURSOR_THEME'"

  if gsettings list-schemas | grep -Fxq 'org.gnome.shell.extensions.user-theme'; then
    gsettings set org.gnome.shell.extensions.user-theme name "'GoreeCloud-Zorin-Light'"
  fi

  if gsettings list-keys org.gnome.desktop.interface 2>/dev/null | grep -Fxq 'color-scheme'; then
    gsettings set org.gnome.desktop.interface color-scheme "'default'"
  fi
}

activate_light_experience
"$ROOT/scripts/wallpaper.sh" apply default

if [[ "$REPLACE_STOCK" -eq 1 ]]; then
  "$ROOT/scripts/system_wallpapers.sh" plan
  sudo "$ROOT/scripts/system_wallpapers.sh" apply
fi

echo
echo "Installed and activated GoreeCloud desktop assets:"
echo "  Applications: GoreeCloud-Zorin-Light"
echo "  Shell:        GoreeCloud-Zorin-Light"
echo "  Icons:        $ICON_THEME"
echo "  Cursor:       $CURSOR_THEME"
echo "  Wallpaper:    primary GoreeCloud light wallpaper"
echo
echo "Theme directory:"
echo "  $THEME_DEST"
echo "Icon/cursor directory:"
echo "  $ICON_DEST"

if [[ "$theme_backed_up" -eq 1 ]]; then
  echo "Previous GoreeCloud theme folders were preserved at:"
  echo "  $THEME_RECOVERY_ROOT"
fi
if [[ "$asset_backed_up" -eq 1 ]]; then
  echo "Previous GoreeCloud icon/cursor folders were preserved at:"
  echo "  $ASSET_RECOVERY_ROOT"
fi

if [[ "$REPLACE_STOCK" -eq 1 ]]; then
  echo "The audited Zorin stock wallpaper packages were removed."
  echo "Recovery remains available through:"
  echo "  ./scripts/wallpaper.sh replace-stock restore"
else
  echo "The complete GoreeCloud wallpaper collection is installed user-locally."
  echo "To remove the audited Zorin stock wallpaper set later:"
  echo "  ./scripts/wallpaper.sh replace-stock apply"
fi
