#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
python3 -m compileall -q goreecloud_care tests
python3 -m unittest discover -s tests -v
python3 - <<'PY'
from pathlib import Path
import xml.etree.ElementTree as ET
for p in [
    Path('packaging/com.goreecloud.care.policy'),
    Path('packaging/com.goreecloud.care.dev.metainfo.xml'),
]:
    ET.parse(p)
print('XML validation: passed')
PY
# Security/source invariants for the privileged boundary.
grep -F '["/usr/bin/apt-get", "clean"]' goreecloud_care/helper.py >/dev/null
! grep -R --line-number -E 'shell[[:space:]]*=[[:space:]]*True|os\.system\(' goreecloud_care packaging scripts
# Mandatory GoreeCloud component documentation.
for f in README.md SPECIFICATIONS.md FEATURES.md BENEFITS.md COMPETITIVE-OBJECTIVES.md BRANDING.md USER-MANUAL.md LICENSE CHANGELOG.md goreecloud.platform.yaml; do
  test -s "$f"
done
echo 'Local source validation: passed'
