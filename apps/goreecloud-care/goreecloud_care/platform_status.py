from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
import os
import stat
from typing import Any

from . import __version__

API_VERSION = "1"
PRIVACY_CAPABILITIES = (
    "telemetry-minimization",
    "data-minimization",
    "privacy-status",
)


def _utc_now(now: datetime | None = None) -> datetime:
    value = now or datetime.now(timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _iso(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def render_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


def build_health_status(now: datetime | None = None) -> dict[str, Any]:
    observed = _utc_now(now)
    return {
        "schema_version": API_VERSION,
        "product": "GoreeCloud Care",
        "version": __version__,
        "state": "ready",
        "observed_at": _iso(observed),
        "local_only": True,
        "network_used": False,
        "telemetry_used": False,
        "privileged_action_performed": False,
    }


def build_privacy_status(
    now: datetime | None = None,
    *,
    production_approved: bool = False,
) -> dict[str, Any]:
    observed = _utc_now(now)
    state = "protected" if production_approved else "development"
    capability_state = "active" if production_approved else "pending-acceptance"
    payload: dict[str, Any] = {
        "schema_version": 1,
        "producer": {
            "adapter_id": "goreecloud-care",
            "product": "GoreeCloud Care",
            "runtime_authority": "GoreeCloud/goreecloud-zorin-os",
            "adapter_contract_version": 1,
        },
        "generated_at": _iso(observed),
        "state": state,
        "capabilities": [
            {"id": capability, "state": capability_state}
            for capability in PRIVACY_CAPABILITIES
        ],
        "privacy": {
            "raw_private_activity_included": False,
            "contains_credentials": False,
            "contains_identifiers": False,
        },
        "acceptance": {
            "runtime_acceptance_required": True,
            "production_approved": production_approved,
        },
    }
    if production_approved:
        payload["valid_until"] = _iso(observed + timedelta(minutes=15))
    return payload


def _secure_root_owned_file(path: Path, *, expected_uid: int = 0, executable: bool = False) -> bool:
    try:
        st = path.stat()
    except OSError:
        return False
    if not stat.S_ISREG(st.st_mode) or st.st_uid != expected_uid:
        return False
    if st.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        return False
    if executable and not (st.st_mode & stat.S_IXUSR):
        return False
    return True


def evaluate_privileged_boundary(
    helper_path: str | Path = "/usr/lib/goreecloud-care/goreecloud-care-helper",
    policy_path: str | Path = "/usr/share/polkit-1/actions/com.goreecloud.care.policy",
    pkexec_path: str | Path = "/usr/bin/pkexec",
    *,
    expected_uid: int = 0,
) -> dict[str, bool]:
    helper = Path(helper_path)
    policy = Path(policy_path)
    pkexec = Path(pkexec_path)
    return {
        "helper_root_owned_nonwritable": _secure_root_owned_file(
            helper, expected_uid=expected_uid, executable=True
        ),
        "policy_root_owned_nonwritable": _secure_root_owned_file(
            policy, expected_uid=expected_uid, executable=False
        ),
        "pkexec_available": pkexec.is_file() and os.access(pkexec, os.X_OK),
    }


def build_wardveil_status(
    now: datetime | None = None,
    *,
    helper_path: str | Path = "/usr/lib/goreecloud-care/goreecloud-care-helper",
    policy_path: str | Path = "/usr/share/polkit-1/actions/com.goreecloud.care.policy",
    pkexec_path: str | Path = "/usr/bin/pkexec",
    expected_uid: int = 0,
) -> dict[str, Any]:
    observed = _utc_now(now)
    checks = evaluate_privileged_boundary(
        helper_path,
        policy_path,
        pkexec_path,
        expected_uid=expected_uid,
    )
    passing = all(checks.values())
    summary = (
        "Installed Care privileged boundary passed root-ownership, write-permission, and pkexec checks."
        if passing
        else "Care privileged-boundary evidence is incomplete or non-passing."
    )
    payload: dict[str, Any] = {
        "contract_version": "0.1.0",
        "scope": {
            "kind": "application",
            "id": "goreecloud-care",
            "display_name": "GoreeCloud Care",
        },
        "authority": {
            "system": "GoreeCloud Care",
            "control": "local-maintenance-privilege-boundary",
            "authoritative": True,
        },
        "state": "protected" if passing else "attention",
        "source_state": "passing" if passing else "non-passing",
        "evidence": {
            "status": "current",
            "observed_at": _iso(observed),
            "summary": summary,
            "reference": "local-cli://goreecloud-care/security-status",
        },
        "claim": {"protected_by_wardveil": False},
        "privacy": {
            "details_withheld": True,
            "redactions": [
                "local filesystem paths beyond fixed installation locations",
                "user identity",
                "raw privileged command output",
            ],
        },
    }
    if passing:
        payload["evidence"]["valid_until"] = _iso(observed + timedelta(minutes=15))
    return payload


def build_continuity_status(
    now: datetime | None = None,
    *,
    rollback_verified: bool = False,
    evidence_reference: str | None = None,
) -> dict[str, Any]:
    observed = _utc_now(now)
    state = "ready" if rollback_verified else "attention"
    payload: dict[str, Any] = {
        "record_id": f"goreecloud-care-package-rollback-{observed.strftime('%Y%m%dT%H%M%SZ')}",
        "producer": "GoreeCloud Care",
        "scope": "goreecloud-care Debian package lifecycle",
        "dimension": "restore_capability",
        "state": state,
        "observed_at": _iso(observed),
        "required_evidence": True,
        "verification_method": (
            "Representative-device install, upgrade, uninstall/reinstall, downgrade, and rollback validation."
        ),
        "evidence_reference": evidence_reference,
        "reason": (
            "Package rollback evidence is current and accepted."
            if rollback_verified
            else "Representative-device uninstall/downgrade/rollback acceptance is still required."
        ),
        "limitations": [] if rollback_verified else [
            "Source validation and package construction do not prove target-device rollback."
        ],
    }
    if rollback_verified:
        payload["fresh_until"] = _iso(observed + timedelta(days=30))
    return payload
