#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
REPO_ROOT=$(CDPATH= cd -- "$ROOT/../.." && pwd)
PACKAGE_NAME="goreecloud-care_0.1.0~dev22_all.deb"
REFERENCE=${1:-"$ROOT/dist/$PACKAGE_NAME"}

for command_name in git cmp sha256sum mktemp rm sh; do
  command -v "$command_name" >/dev/null || {
    echo "Required command not found: $command_name" >&2
    exit 2
  }
done

[ -f "$REFERENCE" ] || {
  echo "Reference package not found: $REFERENCE" >&2
  exit 2
}

if [ -z "${SOURCE_DATE_EPOCH:-}" ]; then
  SOURCE_DATE_EPOCH=$(git -C "$REPO_ROOT" show -s --format=%ct HEAD)
fi
case "$SOURCE_DATE_EPOCH" in
  ''|*[!0-9]*)
    echo "SOURCE_DATE_EPOCH must be a non-negative integer Unix timestamp." >&2
    exit 2
    ;;
esac
export SOURCE_DATE_EPOCH

TMP=$(mktemp -d)
cleanup() {
  rm -rf "$TMP"
}
trap cleanup EXIT INT TERM
REBUILD_OUT="$TMP/rebuild"
mkdir -p "$REBUILD_OUT"

SOURCE_DATE_EPOCH="$SOURCE_DATE_EPOCH" sh "$ROOT/scripts/build-deb.sh" "$REBUILD_OUT" >/dev/null
REBUILT="$REBUILD_OUT/$PACKAGE_NAME"
[ -f "$REBUILT" ] || {
  echo "Rebuilt package not found: $REBUILT" >&2
  exit 1
}

REFERENCE_SHA=$(sha256sum "$REFERENCE" | awk '{print $1}')
REBUILT_SHA=$(sha256sum "$REBUILT" | awk '{print $1}')

if ! cmp -s "$REFERENCE" "$REBUILT"; then
  echo "Reproducible package verification failed." >&2
  echo "Reference SHA-256: $REFERENCE_SHA" >&2
  echo "Rebuilt SHA-256:   $REBUILT_SHA" >&2
  echo "SOURCE_DATE_EPOCH: $SOURCE_DATE_EPOCH" >&2
  exit 1
fi

printf '%s\n' "Reproducible package verification: passed"
printf '%s\n' "SOURCE_DATE_EPOCH: $SOURCE_DATE_EPOCH"
printf '%s\n' "SHA-256: $REFERENCE_SHA"
