#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
REPO_ROOT=$(CDPATH= cd -- "$ROOT/../.." && pwd)
VERSION="0.1.0~dev22"
ARCH="all"
PKG="goreecloud-care"
OUT=${1:-"$ROOT/dist"}

# Debian package output must be reproducible for an exact source revision. Use an
# explicit SOURCE_DATE_EPOCH when supplied; otherwise bind the package timestamp
# to the exact repository HEAD being built. Outside a Git checkout, callers must
# provide SOURCE_DATE_EPOCH rather than falling back to wall-clock time.
if [ -z "${SOURCE_DATE_EPOCH:-}" ]; then
  if command -v git >/dev/null 2>&1 && git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    SOURCE_DATE_EPOCH=$(git -C "$REPO_ROOT" show -s --format=%ct HEAD)
  else
    echo "SOURCE_DATE_EPOCH is required when building outside a Git checkout." >&2
    exit 2
  fi
fi
case "$SOURCE_DATE_EPOCH" in
  ''|*[!0-9]*)
    echo "SOURCE_DATE_EPOCH must be a non-negative integer Unix timestamp." >&2
    exit 2
    ;;
esac
export SOURCE_DATE_EPOCH

STAGE=$(mktemp -d)
chmod 0755 "$STAGE"
trap 'rm -rf "$STAGE"' EXIT INT TERM
mkdir -p "$OUT" \
  "$STAGE/DEBIAN" \
  "$STAGE/usr/bin" \
  "$STAGE/usr/lib/goreecloud-care/goreecloud_care" \
  "$STAGE/usr/share/applications" \
  "$STAGE/usr/share/icons/hicolor/scalable/apps" \
  "$STAGE/usr/share/metainfo" \
  "$STAGE/usr/share/polkit-1/actions" \
  "$STAGE/usr/share/doc/goreecloud-care"
cat > "$STAGE/DEBIAN/control" <<CONTROL
Package: $PKG
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Maintainer: GoreeCloud <support@goreecloud.com>
Depends: python3, python3-gi, gir1.2-gtk-3.0, gir1.2-atk-1.0, policykit-1
Homepage: https://goreecloud.com/
Description: GoreeCloud Care Development maintenance utility
 Local-first GTK maintenance utility for Zorin OS and compatible Linux systems.
CONTROL
install -m 0755 "$ROOT/packaging/postinst" "$STAGE/DEBIAN/postinst"
install -m 0755 "$ROOT/packaging/postrm" "$STAGE/DEBIAN/postrm"
install -m 0755 "$ROOT/packaging/goreecloud-care" "$STAGE/usr/bin/goreecloud-care"
install -m 0755 "$ROOT/packaging/goreecloud-care-helper" "$STAGE/usr/lib/goreecloud-care/goreecloud-care-helper"
install -m 0644 "$ROOT/goreecloud_care/"*.py "$STAGE/usr/lib/goreecloud-care/goreecloud_care/"
install -m 0644 "$ROOT/packaging/com.goreecloud.care.dev.desktop" "$STAGE/usr/share/applications/"
install -m 0644 "$ROOT/packaging/icons/com.goreecloud.care.svg" "$STAGE/usr/share/icons/hicolor/scalable/apps/com.goreecloud.care.svg"
install -m 0644 "$ROOT/packaging/com.goreecloud.care.dev.metainfo.xml" "$STAGE/usr/share/metainfo/"
install -m 0644 "$ROOT/packaging/com.goreecloud.care.policy" "$STAGE/usr/share/polkit-1/actions/"
install -m 0644 "$ROOT/LICENSE" "$STAGE/usr/share/doc/goreecloud-care/copyright"
install -m 0644 "$ROOT/API.md" "$STAGE/usr/share/doc/goreecloud-care/API.md"
install -m 0644 "$ROOT/WARDVEIL-INTEGRATION.md" "$STAGE/usr/share/doc/goreecloud-care/WARDVEIL-INTEGRATION.md"
cat > "$STAGE/usr/lib/goreecloud-care/goreecloud_care.pth" <<'PTH'
/usr/lib/goreecloud-care
PTH
mkdir -p "$STAGE/usr/lib/python3/dist-packages"
install -m 0644 "$STAGE/usr/lib/goreecloud-care/goreecloud_care.pth" "$STAGE/usr/lib/python3/dist-packages/goreecloud_care.pth"

# Normalize every staged filesystem timestamp before dpkg-deb sees it. GNU
# coreutils touch supports -h so any future staged symlink metadata is normalized
# without dereferencing it. dpkg-deb also consumes SOURCE_DATE_EPOCH for archive
# metadata, eliminating wall-clock timestamps from the .deb container.
find "$STAGE" -exec touch -h -d "@$SOURCE_DATE_EPOCH" {} +

dpkg-deb --root-owner-group --build "$STAGE" "$OUT/${PKG}_${VERSION}_${ARCH}.deb" >/dev/null
printf '%s\n' "$OUT/${PKG}_${VERSION}_${ARCH}.deb"
