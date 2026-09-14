from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
import os
import re
import stat
from typing import Any

from . import __version__

API_VERSION = "1"
PACKAGE_VERSION = "0.2.0~dev1"
BUILD_PROVENANCE_PATH = Path("/usr/share/goreecloud-care/build-provenance.json")
REPRESENTATIVE_ACCEPTANCE_PATH = Path(
    "/var/lib/goreecloud-care/acceptance/representative-target.json"
)
EVERKEEP_ACCEPTANCE_PATH = Path(
    "/var/lib/goreecloud/everkeep/acceptance/goreecloud-care.target-runtime.json"
)
REPRESENTATIVE_TARGET_TOKEN = "Zorin OS 17.3"
MAX_EVIDENCE_BYTES = 64 * 1024
_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
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
        "scope": {
            "application_id": "goreecloud-care",
            "runtime": "local",
            "network_used": False,
            "telemetry_used": False,
            "raw_private_activity_exported": False,
        },
        "limitations": [] if production_approved else [
            "Exact runtime acceptance is pending for this source/package identity."
        ],
    }
    return payload


def build_wardveil_status(now: datetime | None = None) -> dict[str, Any]:
    observed = _utc_now(now)
    return {
        "schema_version": 1,
        "producer": "GoreeCloud Care",
        "generated_at": _iso(observed),
        "scope": "local-maintenance-privilege-boundary",
        "protected_by_wardveil": False,
        "state": "evidence-available",
        "evidence": {
            "policykit_boundary": True,
            "fixed_helper_actions": True,
            "shell_execution": False,
            "remote_execution": False,
            "cross_service_authority": False,
        },
        "limitations": [
            "This local status is producer-owned evidence and does not self-assign Wardveil governance."
        ],
    }


def _safe_json_file(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        stat_result = path.lstat()
    except OSError as exc:
        return None, f"missing-or-unreadable:{exc.__class__.__name__}"
    if stat.S_ISLNK(stat_result.st_mode):
        return None, "symlink-not-accepted"
    if not stat.S_ISREG(stat_result.st_mode):
        return None, "not-regular-file"
    if stat_result.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        return None, "writable-by-group-or-other"
    if stat_result.st_size > MAX_EVIDENCE_BYTES:
        return None, "evidence-too-large"
    try:
        raw = path.read_text(encoding="utf-8")
        payload = json.loads(raw)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, f"invalid-evidence:{exc.__class__.__name__}"
    if not isinstance(payload, dict):
        return None, "evidence-not-object"
    return payload, None


def _package_provenance(
    path: Path = BUILD_PROVENANCE_PATH,
) -> tuple[dict[str, Any] | None, str | None]:
    payload, error = _safe_json_file(path)
    if payload is None:
        return None, error
    if payload.get("schema_version") != 1:
        return None, "provenance-schema-mismatch"
    if payload.get("application") != "GoreeCloud Care":
        return None, "provenance-application-mismatch"
    if payload.get("package_version") != PACKAGE_VERSION:
        return None, "provenance-package-version-mismatch"
    source_revision = payload.get("source_revision")
    source_tree = payload.get("source_tree")
    if not isinstance(source_revision, str) or not _SHA1_RE.fullmatch(source_revision):
        return None, "provenance-source-revision-invalid"
    if not isinstance(source_tree, str) or not _SHA1_RE.fullmatch(source_tree):
        return None, "provenance-source-tree-invalid"
    return payload, None


def _representative_acceptance(
    path: Path = REPRESENTATIVE_ACCEPTANCE_PATH,
) -> tuple[dict[str, Any] | None, str | None]:
    payload, error = _safe_json_file(path)
    if payload is None:
        return None, error
    try:
        candidate = payload["candidate"]
        target = payload["target"]
        acceptance = payload["acceptance"]
    except KeyError:
        return None, "representative-evidence-missing-fields"
    if payload.get("schema_version") != 1:
        return None, "representative-schema-mismatch"
    if payload.get("application") != "GoreeCloud Care":
        return None, "representative-application-mismatch"
    if target.get("representative") is not True or target.get("status") != "passed":
        return None, "representative-target-not-passed"
    if REPRESENTATIVE_TARGET_TOKEN not in str(target.get("name", "")):
        return None, "representative-target-mismatch"
    if acceptance.get("target_runtime_status") != "passed":
        return None, "representative-runtime-not-passed"
    if acceptance.get("exact_revision_accepted") is not True:
        return None, "representative-revision-not-accepted"
    if candidate.get("package_version") != PACKAGE_VERSION:
        return None, "representative-package-version-mismatch"
    package_sha = candidate.get("package_sha256")
    if not isinstance(package_sha, str) or not _SHA256_RE.fullmatch(package_sha):
        return None, "representative-package-sha-invalid"
    return payload, None


def build_continuity_status(
    now: datetime | None = None,
    *,
    build_provenance_path: str | Path = BUILD_PROVENANCE_PATH,
    representative_acceptance_path: str | Path = REPRESENTATIVE_ACCEPTANCE_PATH,
    everkeep_acceptance_path: str | Path = EVERKEEP_ACCEPTANCE_PATH,
) -> dict[str, Any]:
    observed = _utc_now(now)
    provenance, provenance_error = _package_provenance(Path(build_provenance_path))
    representative, representative_error = _representative_acceptance(
        Path(representative_acceptance_path)
    )

    evidence_reference: str | None = None
    limitations: list[str] = []
    stage = "package-evidence-pending"
    state = "attention"

    if provenance is None:
        limitations.append(f"Installed package provenance is not accepted: {provenance_error}.")
    elif representative is None:
        limitations.append(
            f"Representative target acceptance is not accepted: {representative_error}."
        )
    else:
        candidate = representative["candidate"]
        if candidate.get("source_revision") != provenance.get("source_revision"):
            limitations.append("Representative source revision does not match installed provenance.")
        if candidate.get("source_tree") != provenance.get("source_tree"):
            limitations.append("Representative source tree does not match installed provenance.")
        if not limitations:
            evidence_reference = f"file://{Path(representative_acceptance_path)}"
            stage = "target-accepted-governance-pending"

    everkeep, everkeep_error = _safe_json_file(Path(everkeep_acceptance_path))
    if stage == "target-accepted-governance-pending":
        if everkeep is None:
            limitations.append(
                f"Everkeep governance is not accepted for this exact build: {everkeep_error}."
            )
        else:
            decision = everkeep.get("acceptance", {})
            bound_candidate = everkeep.get("candidate", {})
            if everkeep.get("schema_version") != 1:
                limitations.append("Everkeep acceptance schema does not match.")
            if everkeep.get("application") != "GoreeCloud Care":
                limitations.append("Everkeep acceptance application does not match.")
            if decision.get("everkeep_integration_promoted") is not True:
                limitations.append("Everkeep integration has not been promoted.")
            if decision.get("everkeep_ready_promoted") is not True:
                limitations.append("Everkeep readiness has not been promoted.")
            if provenance is not None:
                for key in ("source_revision", "source_tree", "package_version"):
                    if bound_candidate.get(key) != provenance.get(key):
                        limitations.append(f"Everkeep candidate {key} does not match installed provenance.")
                rep_sha = representative["candidate"].get("package_sha256") if representative else None
                if bound_candidate.get("package_sha256") != rep_sha:
                    limitations.append("Everkeep package SHA-256 does not match representative evidence.")
            if not limitations:
                state = "ready"
                stage = "everkeep-promoted"
                evidence_reference = f"file://{Path(everkeep_acceptance_path)}"

    payload: dict[str, Any] = {
        "schema_version": 1,
        "producer": "GoreeCloud Care",
        "generated_at": _iso(observed),
        "dimension": "restore_capability",
        "state": state,
        "stage": stage,
        "freshness": "exact-build-bound",
        "evidence_reference": evidence_reference,
        "limitations": limitations,
    }
    return payload
