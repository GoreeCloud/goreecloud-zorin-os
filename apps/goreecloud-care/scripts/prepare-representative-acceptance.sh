#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
REPO_ROOT=$(CDPATH= cd -- "$ROOT/../.." && pwd)
OUT=${1:-"$ROOT/dist/representative-acceptance"}
EXPECTED_RUNTIME_VERSION="0.1.0-dev18"
EXPECTED_PACKAGE_VERSION="0.1.0~dev18"
EXPECTED_PACKAGE="$ROOT/dist/goreecloud-care_${EXPECTED_PACKAGE_VERSION}_all.deb"

for command_name in git python3 sha256sum dpkg-deb tee awk; do
  command -v "$command_name" >/dev/null || {
    echo "Required command not found: $command_name" >&2
    exit 2
  }
done

TRACKED_CHANGES=$(git -C "$REPO_ROOT" status --porcelain --untracked-files=no)
[ -z "$TRACKED_CHANGES" ] || {
  echo "Tracked working-tree changes are present. Commit/stash them before preparing exact-source acceptance evidence." >&2
  printf '%s\n' "$TRACKED_CHANGES" >&2
  exit 2
}

SOURCE_REVISION=$(git -C "$REPO_ROOT" rev-parse HEAD)
SOURCE_BRANCH=$(git -C "$REPO_ROOT" symbolic-ref --quiet --short HEAD 2>/dev/null || printf '%s' detached)
RUNTIME_VERSION=$(PYTHONPATH="$ROOT" python3 -c 'from goreecloud_care import __version__; print(__version__)')
[ "$RUNTIME_VERSION" = "$EXPECTED_RUNTIME_VERSION" ] || {
  echo "Representative Development harness expects runtime $EXPECTED_RUNTIME_VERSION; got $RUNTIME_VERSION" >&2
  exit 2
}

mkdir -p "$OUT"

printf '%s\n' "Preparing read-only/non-destructive representative acceptance evidence."
printf '%s\n' "Source revision: $SOURCE_REVISION"
printf '%s\n' "Source branch:   $SOURCE_BRANCH"
printf '%s\n' "Runtime version: $RUNTIME_VERSION"
printf '%s\n' "Output directory: $OUT"
printf '%s\n' "This preparation harness does not invoke Care cleanup, PolicyKit, pkexec, sudo, apt, or network operations."

(
  cd "$ROOT"
  sh ./scripts/validate.sh
) 2>&1 | tee "$OUT/source-validation.log"

(
  cd "$ROOT"
  sh ./scripts/build-deb.sh dist
) 2>&1 | tee "$OUT/package-build.log"

PACKAGE=$EXPECTED_PACKAGE
[ -f "$PACKAGE" ] || {
  echo "Expected built package not found: $PACKAGE" >&2
  exit 1
}
PACKAGE_VERSION=$(dpkg-deb -f "$PACKAGE" Version)
[ "$PACKAGE_VERSION" = "$EXPECTED_PACKAGE_VERSION" ] || {
  echo "Representative Development harness expects package $EXPECTED_PACKAGE_VERSION; got $PACKAGE_VERSION" >&2
  exit 2
}
sha256sum "$PACKAGE" > "$OUT/package.sha256"
PACKAGE_SHA256=$(awk '{print $1}' "$OUT/package.sha256")

cat > "$OUT/SOURCE_REVISION" <<EOF
source_revision=$SOURCE_REVISION
source_branch=$SOURCE_BRANCH
runtime_version=$RUNTIME_VERSION
package_version=$PACKAGE_VERSION
package_sha256=$PACKAGE_SHA256
EOF

if command -v goreecloud-care >/dev/null 2>&1; then
  {
    printf 'installed_version='
    goreecloud-care --version
    printf 'api_version='
    goreecloud-care --api-version
  } > "$OUT/installed-version.txt"

  goreecloud-care --report-json > "$OUT/report.json"
  goreecloud-care --health-json > "$OUT/health.json"
  goreecloud-care --privacy-status-json > "$OUT/privacy-status.json"
  goreecloud-care --security-status-json > "$OUT/security-status.json"
  goreecloud-care --continuity-status-json > "$OUT/continuity-status.json"
else
  printf '%s\n' "GoreeCloud Care is not currently installed; installed read-only status snapshots were skipped." > "$OUT/installed-version.txt"
fi

cat > "$OUT/MANUAL-CHECKLIST.txt" <<'EOF'
GoreeCloud Care representative-device acceptance checklist
==========================================================

Record PASS or FAIL plus notes for every exercised item. A blank item is NOT accepted evidence.
Do not use unrelated personal files for destructive-flow testing; use disposable fixtures/test data.
Do not promote lifecycle status from this checklist alone.

A. Large text / continuous resize
[ ] PASS [ ] FAIL  GDK_DPI_SCALE=2 Maintenance Insights opens in compact layout.
[ ] PASS [ ] FAIL  Drag continuously narrower/wider for at least 15 seconds; UI remains responsive and does not freeze.
[ ] PASS [ ] FAIL  Compact title remains readable; Refresh focus remains visible.
[ ] PASS [ ] FAIL  Findings remain readable and the true bottom remains reachable after resizing.
Notes:

B. Keyboard traversal
[ ] PASS [ ] FAIL  Forward Tab reaches Refresh, selectable findings, and subsequent focusable controls without a trap.
[ ] PASS [ ] FAIL  Reverse Shift+Tab traverses back through the same region without a trap.
[ ] PASS [ ] FAIL  Focus indication is perceivable in normal and HighContrast presentation.
Notes:

C. Assistive technology
[ ] PASS [ ] FAIL  AT-SPI application identity is GoreeCloud Care.
[ ] PASS [ ] FAIL  Roles/names/descriptions/checked/focused state are useful.
[ ] PASS [ ] FAIL  Dynamic status value changes are observable after Scan/Refresh.
[ ] PASS [ ] FAIL  Orca announcements for completion/cancellation/failure are understandable and not misleading.
Notes:

D. Appearance / resilience
[ ] PASS [ ] FAIL  System Light presentation claimed by Care is readable and visually complete.
[ ] PASS [ ] FAIL  System/Dark presentation claimed by Care is readable and visually complete.
[ ] PASS [ ] FAIL  HighContrast remains system-authoritative and focus is visible.
[ ] PASS [ ] FAIL  Reduced Transparency remains readable with solid neutral surfaces.
[ ] PASS [ ] FAIL  Reduced Motion does not remove required state feedback.
[ ] PASS [ ] FAIL  Deep Dark Development override, if reviewed, is clearly treated as Development evidence rather than an automatically released mode.
Notes:

E. Visual / branding
[ ] PASS [ ] FAIL  Canonical Care icon renders correctly in launcher/desktop/application surfaces.
[ ] PASS [ ] FAIL  Normal, compact, enlarged-text, status, empty/no-findings, confirmation, failure, and privileged-action states have no clipping/overlap/unreadable text.
Notes:

F. Representative task flows
[ ] PASS [ ] FAIL  Scan is read-only and does not delete files.
[ ] PASS [ ] FAIL  Routine selected cleanup requires explicit confirmation and reports completion truthfully.
[ ] PASS [ ] FAIL  No-selection/stale-preview behavior is safe and understandable.
[ ] PASS [ ] FAIL  Permanent Trash flow has a separate irreversible-action confirmation and cancellation path.
[ ] PASS [ ] FAIL  APT authorization success/cancellation/denial/failure are distinguishable.
[ ] PASS [ ] FAIL  File-cache reclaim warning and completion language are truthful and do not claim a lasting RAM/performance boost.
[ ] PASS [ ] FAIL  Post-action refresh preserves the final operation result.
Notes:

G. Package lifecycle / continuity
Run the separate package lifecycle probe as the normal desktop user, with a retained genuinely older Development package.
[ ] PASS [ ] FAIL  install/remove/reinstall/downgrade/restore/final-state probe passed.
Candidate package:
Previous package:
Lifecycle log/evidence:

H. Platform-system acceptance
[ ] PASS [ ] FAIL  Privacy Shield exact-candidate runtime/application review complete (production_approved must remain false until governed approval).
[ ] PASS [ ] FAIL  Wardveil scoped adoption/runtime review complete (do not claim broad protection unless separately accepted).
[ ] PASS [ ] FAIL  Everkeep continuity evidence is complete and provenance matches the exact candidate package.
[ ] PASS [ ] FAIL  GLAZE UI V1.2 product-specific acceptance is complete; only then may the registry be considered for accepted-v1.
Notes:
EOF

cat > "$OUT/MANUAL-COMMANDS.txt" <<'EOF'
# Run one mode at a time from the representative desktop session.

# Normal Care
  goreecloud-care

# Maintenance Insights at the large-text acceptance condition
  GDK_DPI_SCALE=2 goreecloud-care --insights-ui

# HighContrast
  GTK_THEME=HighContrast goreecloud-care
  GTK_THEME=HighContrast GDK_DPI_SCALE=2 goreecloud-care --insights-ui

# Explicit Development appearance/resilience probes
  GOREECLOUD_CARE_APPEARANCE=light goreecloud-care
  GOREECLOUD_CARE_APPEARANCE=dark goreecloud-care
  GOREECLOUD_CARE_APPEARANCE=deep-dark goreecloud-care
  GOREECLOUD_CARE_REDUCE_TRANSPARENCY=1 goreecloud-care
  GOREECLOUD_CARE_REDUCE_MOTION=1 goreecloud-care

# Installed read-only status probes
  goreecloud-care --version
  goreecloud-care --api-version
  goreecloud-care --report
  goreecloud-care --report-json
  goreecloud-care --health-json
  goreecloud-care --privacy-status-json
  goreecloud-care --security-status-json
  goreecloud-care --continuity-status-json

# Package lifecycle (run as the normal desktop user; the script requests sudo only for apt operations)
  sh ./scripts/validate-package-lifecycle.sh ./dist/goreecloud-care_0.1.0~dev18_all.deb /path/to/retained/older-development-package.deb
EOF

printf '%s\n' "Representative acceptance preparation: passed"
printf '%s\n' "Package: $PACKAGE_VERSION"
printf '%s\n' "SHA-256: $PACKAGE_SHA256"
printf '%s\n' "Manual checklist: $OUT/MANUAL-CHECKLIST.txt"
printf '%s\n' "Manual commands:  $OUT/MANUAL-COMMANDS.txt"
printf '%s\n' "No manual item is accepted until a representative-device result is explicitly recorded."
