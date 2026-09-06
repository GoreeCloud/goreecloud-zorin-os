#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
python3 -m compileall -q goreecloud_care tests
python3 -m unittest discover -s tests -v
python3 - <<'PY'
from pathlib import Path
import json
import xml.etree.ElementTree as ET

for p in [
    Path('packaging/com.goreecloud.care.policy'),
    Path('packaging/com.goreecloud.care.dev.metainfo.xml'),
]:
    ET.parse(p)
print('XML validation: passed')

privacy_app = json.loads(Path('contracts/privacy-shield.application.json').read_text(encoding='utf-8'))
assert privacy_app['manifest_version'] == 1
assert privacy_app['application_id'] == 'goreecloud-care'
assert privacy_app['resources']
assert all(resource['processing_zones'] == ['local'] for resource in privacy_app['resources'])
assert all(resource.get('destinations', []) == [] for resource in privacy_app['resources'])
assert all(resource.get('ai_usage') is False for resource in privacy_app['resources'])

privacy_adapter = json.loads(Path('contracts/privacy-shield.adapter.json').read_text(encoding='utf-8'))
assert privacy_adapter['schema_version'] == 1
assert privacy_adapter['adapter']['id'] == 'goreecloud-care'
assert privacy_adapter['adapter']['runtime_authority'] == 'GoreeCloud/goreecloud-zorin-os'
assert privacy_adapter['acceptance']['runtime_acceptance_required'] is True
assert privacy_adapter['acceptance']['production_approved'] is False
assert set(privacy_adapter['capabilities']) == {
    'telemetry-minimization', 'data-minimization', 'privacy-status'
}
assert privacy_adapter['privacy']['local_first'] is True
assert privacy_adapter['privacy']['raw_private_activity_exported_for_status'] is False

everkeep = json.loads(Path('contracts/everkeep.adoption.json').read_text(encoding='utf-8'))
assert everkeep['schema_version'] == 1
assert everkeep['project'] == 'GoreeCloud Care'
assert everkeep['read_only'] is True
assert everkeep['fail_closed'] is True
assert 'restore_capability' in everkeep['dimensions']
assert everkeep['status_schema'] == 'contracts/continuity.status.schema.json'

everkeep_acceptance = json.loads(Path('contracts/everkeep.acceptance.json').read_text(encoding='utf-8'))
assert everkeep_acceptance['schema_version'] == 1
assert everkeep_acceptance['application'] == 'GoreeCloud Care'
assert everkeep_acceptance['freshness']['required_for_ready'] is True
assert everkeep_acceptance['acceptance']['everkeep_integrated'] is False
assert everkeep_acceptance['acceptance']['everkeep_ready'] is False
assert everkeep_acceptance['acceptance']['target_runtime_acceptance_required'] is True
assert everkeep_acceptance['acceptance']['exact_revision_acceptance_required'] is True
print('Platform integration contract validation: passed')
PY
# Exact Development version alignment.
grep -F '__version__ = "0.1.0-dev18"' goreecloud_care/__init__.py >/dev/null
grep -F 'version = "0.1.0.dev18"' pyproject.toml >/dev/null
grep -F 'VERSION="0.1.0~dev18"' scripts/build-deb.sh >/dev/null
grep -F '<release version="0.1.0-dev18"' packaging/com.goreecloud.care.dev.metainfo.xml >/dev/null
grep -F 'version: 0.1.0-dev18' goreecloud.platform.yaml >/dev/null
# Security/source invariants for the privileged boundary.
grep -F '["/usr/bin/apt-get", "clean"]' goreecloud_care/helper.py >/dev/null
! grep -R --line-number -E 'shell[[:space:]]*=[[:space:]]*True|os\.system\(' goreecloud_care packaging scripts
# Adaptive/accessibility invariants for current Development.
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
grep -F 'GTK_THEME' goreecloud_care/ui_contract.py >/dev/null
grep -F 'gtk_theme_override' goreecloud_care/ui_contract.py >/dev/null
grep -F 'GLib.set_prgname("GoreeCloud Care")' goreecloud_care/__main__.py >/dev/null
grep -F 'GLib.set_application_name("GoreeCloud Care")' goreecloud_care/__main__.py >/dev/null
grep -F 'install_focus_resilience_provider' goreecloud_care/__main__.py >/dev/null
grep -F 'Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION - 1' goreecloud_care/focus_resilience.py >/dev/null
grep -F '@theme_fg_color' goreecloud_care/focus_resilience.py >/dev/null
grep -F 'button:focus, checkbutton:focus' goreecloud_care/focus_resilience.py >/dev/null
grep -F 'gir1.2-atk-1.0' scripts/build-deb.sh >/dev/null
# Current Stable GLAZE UI V1.2 native fallback invariants.
grep -F 'GLAZE_UI_VERSION = "1.2.0"' goreecloud_care/glaze_v12.py >/dev/null
grep -F 'GLAZE_UI_LABEL = "GLAZE UI V1.2"' goreecloud_care/glaze_v12.py >/dev/null
grep -F 'MIN_TARGET_PX = 48' goreecloud_care/glaze_v12.py >/dev/null
grep -F 'button, checkbutton { min-height: 48px; }' goreecloud_care/glaze_v12.py >/dev/null
grep -F 'reduced-transparency' goreecloud_care/glaze_v12.py >/dev/null
grep -F 'reduced-motion' goreecloud_care/glaze_v12.py >/dev/null
grep -F 'install_glaze_v12_global_style' goreecloud_care/__main__.py >/dev/null
grep -F 'Gtk.STYLE_PROVIDER_PRIORITY_USER - 1' goreecloud_care/glaze_v12_global.py >/dev/null
grep -F 'is_high_contrast_theme' goreecloud_care/glaze_v12_global.py >/dev/null
! grep -E 'transition[[:space:]]*:|animation[[:space:]]*:' goreecloud_care/glaze_v12.py >/dev/null
grep -F 'version: "1.2.0"' goreecloud.platform.yaml >/dev/null
grep -F 'glaze_ui_required: "1.2.0"' goreecloud.platform.yaml >/dev/null
grep -F 'glaze-ui==1.2.0' goreecloud.platform.yaml >/dev/null
# Privacy-safe read-only report and local integration API invariants.
for flag in --report --report-json --api-version --health-json --privacy-status-json --security-status-json --continuity-status-json; do
  grep -F -- "\"$flag\"" goreecloud_care/__main__.py >/dev/null
done
grep -F 'contains_file_paths' goreecloud_care/reporting.py >/dev/null
grep -F 'contains_raw_scan_errors' goreecloud_care/reporting.py >/dev/null
grep -F 'read-only-local-maintenance-report' goreecloud_care/reporting.py >/dev/null
grep -F 'classify_disk_headroom' goreecloud_care/reporting.py >/dev/null
grep -F 'production_approved: bool = False' goreecloud_care/platform_status.py >/dev/null
grep -F 'rollback_verified: bool = False' goreecloud_care/platform_status.py >/dev/null
grep -F '"protected_by_wardveil": False' goreecloud_care/platform_status.py >/dev/null
grep -F 'stat.S_IWGRP | stat.S_IWOTH' goreecloud_care/platform_status.py >/dev/null
# Maintenance Insights must remain bounded, local, review-only, and large-text reachable.
grep -F -- '"--insights-ui"' goreecloud_care/__main__.py >/dev/null
grep -F 'MAX_VISITED_ENTRIES = 50_000' goreecloud_care/insights.py >/dev/null
grep -F 'STANDARD_USER_DIRS' goreecloud_care/insights.py >/dev/null
grep -F 'def build_insights(' goreecloud_care/insights.py >/dev/null
grep -F 'self.results = Gtk.Label(xalign=0, yalign=0)' goreecloud_care/insights_window.py >/dev/null
grep -F 'self.results.set_selectable(True)' goreecloud_care/insights_window.py >/dev/null
grep -F 'Atk.Role.STATUSBAR' goreecloud_care/insights_window.py >/dev/null
grep -F 'self.page_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)' goreecloud_care/insights_window.py >/dev/null
grep -F 'self.results_scroll.set_min_content_height(RESULTS_MIN_HEIGHT)' goreecloud_care/insights_window.py >/dev/null
grep -F 'self.results.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)' goreecloud_care/insights_window.py >/dev/null
grep -F "<span insert_hyphens='false'>{escaped}</span>" goreecloud_care/insights_window.py >/dev/null
! grep -F 'Gtk.WrapMode.CHAR' goreecloud_care/insights_window.py >/dev/null
grep -F 'compact = is_compact_width(width)' goreecloud_care/insights_window.py >/dev/null
grep -F 'self.header.set_subtitle(None if compact else self.header_subtitle)' goreecloud_care/insights_window.py >/dev/null
grep -F 'self.root.set_spacing(COMPACT_SPACING if compact else REGULAR_SPACING)' goreecloud_care/insights_window.py >/dev/null
grep -F 'view-refresh-symbolic' goreecloud_care/insights_window.py >/dev/null
grep -F 'self.refresh.get_accessible().set_name("Refresh")' goreecloud_care/insights_window.py >/dev/null
grep -F "<span weight='bold'>Review storage safely</span>" goreecloud_care/insights_window.py >/dev/null
grep -F 'Refreshing read-only insights…' goreecloud_care/insights_window.py >/dev/null
grep -F 'Maintenance Insights (Read-only)' packaging/com.goreecloud.care.dev.desktop >/dev/null
! grep -R --line-number -E '\.unlink\(|shutil\.rmtree|os\.remove|subprocess|pkexec' goreecloud_care/insights.py goreecloud_care/insights_window.py
# Post-action completion must survive the automatic values refresh.
grep -F 'def _refresh_after_action(' goreecloud_care/app.py >/dev/null
grep -F 'def _refresh_after_action_done(' goreecloud_care/app.py >/dev/null
grep -F 'self._show_notice(completion_title, outcome.message, Gtk.MessageType.INFO)' goreecloud_care/app.py >/dev/null
grep -F 'self._refresh_after_action(outcome.message, "success", completion_title)' goreecloud_care/app.py >/dev/null
# Mandatory GoreeCloud component documentation and integration records.
for f in README.md SPECIFICATIONS.md FEATURES.md BENEFITS.md CAPABILITIES.md COMPETITIVE-OBJECTIVES.md BRANDING.md USER-MANUAL.md LICENSE CHANGELOG.md API.md WARDVEIL-INTEGRATION.md GLAZE-UI-CONFORMANCE.md RELEASE-ACCEPTANCE.md goreecloud.platform.yaml contracts/privacy-shield.application.json contracts/privacy-shield.adapter.json contracts/everkeep.adoption.json contracts/everkeep.acceptance.json scripts/validate-installed.sh scripts/validate-package-lifecycle.sh; do
  test -s "$f"
done
echo 'Local source validation: passed'
