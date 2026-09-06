#!/bin/sh
set -eu

usage() {
  echo "Usage: $0 <candidate.deb> <previous.deb>" >&2
  exit 2
}

[ "$#" -eq 2 ] || usage
CANDIDATE=$1
PREVIOUS=$2
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

[ -f "$CANDIDATE" ] || { echo "Candidate package not found: $CANDIDATE" >&2; exit 2; }
[ -f "$PREVIOUS" ] || { echo "Previous package not found: $PREVIOUS" >&2; exit 2; }

candidate_name=$(dpkg-deb -f "$CANDIDATE" Package)
previous_name=$(dpkg-deb -f "$PREVIOUS" Package)
[ "$candidate_name" = "goreecloud-care" ]
[ "$previous_name" = "goreecloud-care" ]

candidate_version=$(dpkg-deb -f "$CANDIDATE" Version)
previous_version=$(dpkg-deb -f "$PREVIOUS" Version)
[ "$candidate_version" != "$previous_version" ]

candidate_runtime=$(printf '%s' "$candidate_version" | sed 's/~/-/')
previous_runtime=$(printf '%s' "$previous_version" | sed 's/~/-/')

case "$candidate_version" in
  0.1.0~dev18) ;;
  *) echo "This Development lifecycle probe expects candidate 0.1.0~dev18; got $candidate_version" >&2; exit 2 ;;
esac

printf '%s\n' "Package lifecycle acceptance will temporarily remove and downgrade GoreeCloud Care."
printf '%s\n' "Candidate: $candidate_version"
printf '%s\n' "Previous:  $previous_version"
printf '%s\n' "No Care-owned user data is expected to be removed; this script does not invoke Care cleanup actions."
printf '%s\n' "Administrator authentication may be requested by apt."

install_package() {
  package_path=$1
  sudo apt install -y --allow-downgrades "$package_path"
}

assert_version() {
  expected_package=$1
  expected_runtime=$2
  installed=$(dpkg-query -W -f='${Status} ${Version}' goreecloud-care)
  [ "$installed" = "install ok installed $expected_package" ]
  [ "$(goreecloud-care --version)" = "$expected_runtime" ]
}

printf '%s\n' "[1/6] Install/upgrade candidate"
install_package "$CANDIDATE"
sh "$ROOT/scripts/validate-installed.sh" "$candidate_version" "$candidate_runtime"

printf '%s\n' "[2/6] Remove candidate"
sudo apt remove -y goreecloud-care
if dpkg-query -W -f='${Status}' goreecloud-care 2>/dev/null | grep -qx 'install ok installed'; then
  echo "Package still installed after removal" >&2
  exit 1
fi
for path in \
  /usr/bin/goreecloud-care \
  /usr/lib/goreecloud-care/goreecloud-care-helper \
  /usr/share/polkit-1/actions/com.goreecloud.care.policy \
  /usr/share/applications/com.goreecloud.care.dev.desktop \
  /usr/share/icons/hicolor/scalable/apps/com.goreecloud.care.svg; do
  [ ! -e "$path" ] || { echo "Package-owned path remained after removal: $path" >&2; exit 1; }
done

printf '%s\n' "[3/6] Reinstall candidate"
install_package "$CANDIDATE"
sh "$ROOT/scripts/validate-installed.sh" "$candidate_version" "$candidate_runtime"

printf '%s\n' "[4/6] Downgrade to previous Development package"
install_package "$PREVIOUS"
assert_version "$previous_version" "$previous_runtime"
goreecloud-care --report-json >/dev/null

printf '%s\n' "[5/6] Restore candidate after downgrade"
install_package "$CANDIDATE"
sh "$ROOT/scripts/validate-installed.sh" "$candidate_version" "$candidate_runtime"

printf '%s\n' "[6/6] Final package state"
assert_version "$candidate_version" "$candidate_runtime"
printf '%s\n' "Representative package install/remove/reinstall/downgrade/rollback acceptance: passed"
