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
# Current Development interaction invariants.
grep -F 'gtk-application-prefer-dark-theme' goreecloud_care/app.py >/dev/null
grep -F 'settings.set_property("gtk-application-prefer-dark-theme", False)' goreecloud_care/app.py >/dev/null
grep -F '.status-banner.status-attention' goreecloud_care/app.py >/dev/null
grep -F '"Action cancelled"' goreecloud_care/app.py >/dev/null
# Adaptive/accessibility invariants for dev8.
grep -F 'self.set_size_request(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)' goreecloud_care/app.py >/dev/null
grep -F 'def _apply_layout(' goreecloud_care/app.py >/dev/null
grep -F 'compact = is_compact_width(width)' goreecloud_care/app.py >/dev/null
grep -F 'self.header.set_subtitle(None if compact else self.header_subtitle)' goreecloud_care/app.py >/dev/null
grep -F 'COMPACT_WIDTH = 820' goreecloud_care/ui_contract.py >/dev/null
grep -F 'GDK_DPI_SCALE' goreecloud_care/ui_contract.py >/dev/null
grep -F 'def effective_layout_width(' goreecloud_care/ui_contract.py >/dev/null
grep -F 'Atk.Role.STATUSBAR' goreecloud_care/app.py >/dev/null
grep -F 'visible-data-changed' goreecloud_care/app.py >/dev/null
grep -F 'is_high_contrast_theme' goreecloud_care/app.py >/dev/null
grep -F 'gir1.2-atk-1.0' scripts/build-deb.sh >/dev/null
# Post-action completion must survive the automatic values refresh.
grep -F 'def _refresh_after_action(' goreecloud_care/app.py >/dev/null
grep -F 'def _refresh_after_action_done(' goreecloud_care/app.py >/dev/null
grep -F 'self._show_notice(completion_title, outcome.message, Gtk.MessageType.INFO)' goreecloud_care/app.py >/dev/null
grep -F 'self._refresh_after_action(outcome.message, "success", completion_title)' goreecloud_care/app.py >/dev/null
# Mandatory GoreeCloud component documentation.
for f in README.md SPECIFICATIONS.md FEATURES.md BENEFITS.md COMPETITIVE-OBJECTIVES.md BRANDING.md USER-MANUAL.md LICENSE CHANGELOG.md goreecloud.platform.yaml; do
  test -s "$f"
done
echo 'Local source validation: passed'
