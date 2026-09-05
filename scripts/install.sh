#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${XDG_DATA_HOME:-$HOME/.local/share}/themes"
STAMP="$(date +%Y%m%d-%H%M%S)"
RECOVERY_ROOT="$DEST/.goreecloud-zorin-recovery/$STAMP"
REPLACE_STOCK=0
THEMES=(
  "GoreeCloud-Zorin-Light"
  "GoreeCloud-Zorin-Dark"
  "GoreeCloud-Zorin-DeepDark"
)

usage() {
  cat <<'EOF'
Usage:
  ./scripts/install.sh
  ./scripts/install.sh --replace-stock

The default install activates GoreeCloud-Zorin-Light and its primary light
wallpaper. --replace-stock additionally removes the audited Zorin OS 17.3
stock wallpaper packages after the recovery-backed safety checks pass.
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

python3 "$ROOT/scripts/build.py" --output "$TEMP_ROOT"

# Zorin OS 17.3's GTK 3, GTK 4, and Shell themes contain extensive
# platform-specific selectors and assets. Compose the generated GoreeCloud
# semantic overrides on top of the exact verified local Zorin 17.3 base before
# touching an existing installed GoreeCloud theme. The composer fails closed
# when package version or base hashes differ from target evidence captured
# during Development.
python3 "$ROOT/scripts/compose_zorin_base.py" "$TEMP_ROOT"

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

activate_light_theme() {
  if ! command -v gsettings >/dev/null 2>&1; then
    return 0
  fi

  gsettings set org.gnome.desktop.interface gtk-theme "'GoreeCloud-Zorin-Light'"

  if gsettings list-schemas | grep -Fxq 'org.gnome.shell.extensions.user-theme'; then
    gsettings set org.gnome.shell.extensions.user-theme name "'GoreeCloud-Zorin-Light'"
  fi

  if gsettings list-keys org.gnome.desktop.interface 2>/dev/null | grep -Fxq 'color-scheme'; then
    gsettings set org.gnome.desktop.interface color-scheme "'default'"
  fi
}

activate_light_theme
"$ROOT/scripts/wallpaper.sh" apply default

if [[ "$REPLACE_STOCK" -eq 1 ]]; then
  "$ROOT/scripts/system_wallpapers.sh" plan
  sudo "$ROOT/scripts/system_wallpapers.sh" apply
fi

echo
echo "Installed GoreeCloud Zorin themes to:"
echo "  $DEST"
echo "Activated: GoreeCloud-Zorin-Light"
echo "Applied the primary GoreeCloud light wallpaper."

echo "GTK 3, GTK 4/libadwaita, and GNOME Shell were composed from the"
echo "verified local Zorin OS 17.3 base before GoreeCloud Glaze UI overrides."

if [[ "$backed_up" -eq 1 ]]; then
  echo "Previous GoreeCloud theme folders were preserved at:"
  echo "  $RECOVERY_ROOT"
fi

if [[ "$REPLACE_STOCK" -eq 1 ]]; then
  echo "The audited Zorin stock wallpaper packages were removed."
  echo "Recovery remains available through:"
  echo "  ./scripts/wallpaper.sh replace-stock restore"
else
  echo "The complete 24-wallpaper GoreeCloud collection is installed user-locally."
  echo "To remove the audited Zorin stock wallpaper set later:"
  echo "  ./scripts/wallpaper.sh replace-stock apply"
fi
