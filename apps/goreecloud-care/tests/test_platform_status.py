import json
import os
from datetime import datetime, timezone
from pathlib import Path
import stat
import tempfile
import unittest

from goreecloud_care.platform_status import (
    API_VERSION,
    build_continuity_status,
    build_health_status,
    build_privacy_status,
    build_wardveil_status,
    evaluate_privileged_boundary,
    render_json,
)


NOW = datetime(2026, 9, 6, 18, 30, tzinfo=timezone.utc)


class PlatformStatusTests(unittest.TestCase):
    def test_health_status_is_minimized_local_and_read_only(self):
        payload = build_health_status(NOW)
        self.assertEqual(payload["schema_version"], API_VERSION)
        self.assertEqual(payload["product"], "GoreeCloud Care")
        self.assertEqual(payload["state"], "ready")
        self.assertTrue(payload["local_only"])
        self.assertFalse(payload["network_used"])
        self.assertFalse(payload["telemetry_used"])
        self.assertFalse(payload["privileged_action_performed"])

    def test_privacy_status_fails_closed_to_pending_acceptance(self):
        payload = build_privacy_status(NOW)
        self.assertEqual(payload["state"], "development")
        self.assertFalse(payload["acceptance"]["production_approved"])
        self.assertTrue(payload["acceptance"]["runtime_acceptance_required"])
        self.assertNotIn("valid_until", payload)
        self.assertTrue(all(item["state"] == "pending-acceptance" for item in payload["capabilities"]))
        self.assertFalse(payload["privacy"]["raw_private_activity_included"])
        self.assertFalse(payload["privacy"]["contains_credentials"])
        self.assertFalse(payload["privacy"]["contains_identifiers"])

    def test_privacy_status_can_represent_explicit_future_acceptance(self):
        payload = build_privacy_status(NOW, production_approved=True)
        self.assertEqual(payload["state"], "protected")
        self.assertTrue(payload["acceptance"]["production_approved"])
        self.assertIn("valid_until", payload)
        self.assertTrue(all(item["state"] == "active" for item in payload["capabilities"]))

    def _make_file(self, path: Path, mode: int) -> None:
        path.write_text("fixture\n", encoding="utf-8")
        path.chmod(mode)

    def test_privileged_boundary_passes_only_with_secure_fixed_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            helper = root / "helper"
            policy = root / "policy"
            pkexec = root / "pkexec"
            self._make_file(helper, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
            self._make_file(policy, stat.S_IRUSR | stat.S_IWUSR)
            self._make_file(pkexec, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
            checks = evaluate_privileged_boundary(
                helper,
                policy,
                pkexec,
                expected_uid=os.geteuid(),
            )
            self.assertTrue(all(checks.values()))

            payload = build_wardveil_status(
                NOW,
                helper_path=helper,
                policy_path=policy,
                pkexec_path=pkexec,
                expected_uid=os.geteuid(),
            )
            self.assertEqual(payload["state"], "protected")
            self.assertEqual(payload["evidence"]["status"], "current")
            self.assertIn("valid_until", payload["evidence"])
            self.assertTrue(payload["authority"]["authoritative"])
            self.assertFalse(payload["claim"]["protected_by_wardveil"])

    def test_privileged_boundary_fails_closed_on_writable_or_missing_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            helper = root / "helper"
            policy = root / "policy"
            pkexec = root / "pkexec"
            self._make_file(helper, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IWGRP)
            self._make_file(policy, stat.S_IRUSR | stat.S_IWUSR)
            self._make_file(pkexec, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
            payload = build_wardveil_status(
                NOW,
                helper_path=helper,
                policy_path=policy,
                pkexec_path=pkexec,
                expected_uid=os.geteuid(),
            )
            self.assertEqual(payload["state"], "attention")
            self.assertFalse(payload["claim"]["protected_by_wardveil"])
            self.assertNotIn("valid_until", payload["evidence"])

            helper.unlink()
            checks = evaluate_privileged_boundary(
                helper,
                policy,
                pkexec,
                expected_uid=os.geteuid(),
            )
            self.assertFalse(checks["helper_root_owned_nonwritable"])

    def test_continuity_status_is_non_ready_until_rollback_is_verified(self):
        pending = build_continuity_status(NOW)
        self.assertEqual(pending["state"], "attention")
        self.assertTrue(pending["required_evidence"])
        self.assertNotIn("fresh_until", pending)
        self.assertIn("rollback", pending["reason"].lower())

        ready = build_continuity_status(
            NOW,
            rollback_verified=True,
            evidence_reference="evidence://care/rollback/accepted",
        )
        self.assertEqual(ready["state"], "ready")
        self.assertIn("fresh_until", ready)
        self.assertEqual(ready["evidence_reference"], "evidence://care/rollback/accepted")

    def test_render_json_is_machine_readable(self):
        payload = build_health_status(NOW)
        self.assertEqual(json.loads(render_json(payload)), payload)


if __name__ == "__main__":
    unittest.main()
