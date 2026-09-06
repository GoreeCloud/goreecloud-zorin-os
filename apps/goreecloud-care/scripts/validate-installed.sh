#!/bin/sh
set -eu
EXPECTED_PACKAGE_VERSION=${1:-0.1.0~dev18}
EXPECTED_RUNTIME_VERSION=${2:-0.1.0-dev18}

command -v goreecloud-care >/dev/null
command -v dpkg-query >/dev/null

installed=$(dpkg-query -W -f='${Status} ${Version}' goreecloud-care)
[ "$installed" = "install ok installed $EXPECTED_PACKAGE_VERSION" ]
[ "$(goreecloud-care --version)" = "$EXPECTED_RUNTIME_VERSION" ]
[ "$(goreecloud-care --api-version)" = "1" ]

report_json=$(goreecloud-care --report-json)
health_json=$(goreecloud-care --health-json)
privacy_json=$(goreecloud-care --privacy-status-json)
security_json=$(goreecloud-care --security-status-json)
continuity_json=$(goreecloud-care --continuity-status-json)

REPORT_JSON=$report_json \
HEALTH_JSON=$health_json \
PRIVACY_JSON=$privacy_json \
SECURITY_JSON=$security_json \
CONTINUITY_JSON=$continuity_json \
python3 - <<'PY'
import json
import os

report = json.loads(os.environ['REPORT_JSON'])
health = json.loads(os.environ['HEALTH_JSON'])
privacy = json.loads(os.environ['PRIVACY_JSON'])
security = json.loads(os.environ['SECURITY_JSON'])
continuity = json.loads(os.environ['CONTINUITY_JSON'])

assert report['product'] == 'GoreeCloud Care'
assert report['privacy']['contains_file_paths'] is False
assert report['privacy']['contains_raw_scan_errors'] is False
assert report['privacy']['network_used'] is False

assert health['product'] == 'GoreeCloud Care'
assert health['state'] == 'ready'
assert health['local_only'] is True
assert health['network_used'] is False
assert health['telemetry_used'] is False
assert health['privileged_action_performed'] is False

assert privacy['producer']['adapter_id'] == 'goreecloud-care'
assert privacy['privacy']['raw_private_activity_included'] is False
assert privacy['privacy']['contains_credentials'] is False
assert privacy['privacy']['contains_identifiers'] is False
assert privacy['acceptance']['runtime_acceptance_required'] is True
assert privacy['acceptance']['production_approved'] is False
assert privacy['state'] == 'development'

assert security['scope']['id'] == 'goreecloud-care'
assert security['claim']['protected_by_wardveil'] is False
assert security['state'] in {'protected', 'attention'}
if security['state'] != 'protected':
    raise SystemExit('installed privileged-boundary security evidence is non-passing')

assert continuity['producer'] == 'GoreeCloud Care'
assert continuity['dimension'] == 'restore_capability'
assert continuity['state'] == 'attention'
PY

test -f /usr/lib/goreecloud-care/goreecloud-care-helper
test -f /usr/share/polkit-1/actions/com.goreecloud.care.policy
test -f /usr/share/applications/com.goreecloud.care.dev.desktop
test -f /usr/share/metainfo/com.goreecloud.care.dev.metainfo.xml
test -f /usr/share/doc/goreecloud-care/API.md
test -f /usr/share/doc/goreecloud-care/WARDVEIL-INTEGRATION.md

printf '%s\n' "Installed GoreeCloud Care $EXPECTED_PACKAGE_VERSION safe acceptance probe: passed"
printf '%s\n' "Continuity remains attention until destructive package lifecycle rollback testing is separately completed."
