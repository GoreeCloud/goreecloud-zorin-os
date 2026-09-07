#!/bin/sh
set -eu

usage() {
  echo "Usage: $0 <candidate.deb> <previous.deb>" >&2
  exit 2
}

[ "$#" -eq 2 ] || usage
[ "$(id -u)" -ne 0 ] || {
  echo "Run this acceptance probe as the representative desktop user, not as root. The script requests sudo only for apt package operations." >&2
  exit 2
}

for command_name in sudo apt dpkg dpkg-deb dpkg-query python3 grep sed; do
  command -v "$command_name" >/dev/null || {
    echo "Required command not found: $command_name" >&2
    exit 2
  }
done

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
dpkg --compare-versions "$previous_version" lt "$candidate_version" || {
  echo "Previous package must sort older than the candidate: previous=$previous_version candidate=$candidate_version" >&2
  exit 2
}

candidate_runtime=$(printf '%s' "$candidate_version" | sed 's/~/-/')
previous_runtime=$(printf '%s' "$previous_version" | sed 's/~/-/')

case "$candidate_version" in
  0.1.0~dev19) ;;
  *) echo "This Development lifecycle probe expects candidate 0.1.0~dev19; got $candidate_version" >&2; exit 2 ;;
esac

printf '%s\n' "Package lifecycle acceptance will temporarily remove and downgrade GoreeCloud Care."
printf '%s\n' "Candidate: $candidate_version"
printf '%s\n' "Previous:  $previous_version"
printf '%s\n' "Representative user: $(id -un) (uid $(id -u))"
printf '%s\n' "The probe intentionally executes installed runtime checks from the current source working directory; dev19 must remain isolated from that source tree."
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
  [ "$installed" = "install ok installed $expected_package" ] || {
    echo "Installed package state mismatch: expected='install ok installed $expected_package' actual='$installed'" >&2
    exit 1
  }
  actual_runtime=$(goreecloud-care --version)
  [ "$actual_runtime" = "$expected_runtime" ] || {
    echo "Installed runtime mismatch: package=$expected_package expected_runtime=$expected_runtime actual_runtime=$actual_runtime" >&2
    echo "This may indicate working-directory/PYTHONPATH shadowing or stale installed bytecode." >&2
    exit 1
  }
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
[ ! -e /usr/lib/goreecloud-care/goreecloud_care/__pycache__ ] || {
  echo "Private Python bytecode remained after package removal" >&2
  exit 1
}

printf '%s\n' "[3/6] Reinstall candidate as a fresh package state"
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
printf '%s\n' "The candidate is installed at the end of the probe; no Care cleanup action was invoked."
