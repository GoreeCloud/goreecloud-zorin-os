from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"


class EverkeepContractTests(unittest.TestCase):
    def test_adoption_manifest_is_read_only_and_fail_closed(self) -> None:
        adoption = json.loads((CONTRACTS / "everkeep.adoption.json").read_text(encoding="utf-8"))
        self.assertEqual(adoption["schema_version"], 1)
        self.assertEqual(adoption["project"], "GoreeCloud Care")
        self.assertEqual(adoption["role"], "producer")
        self.assertTrue(adoption["read_only"])
        self.assertTrue(adoption["fail_closed"])
        self.assertEqual(adoption["status_schema"], "contracts/continuity.status.schema.json")
        self.assertIn("restore_capability", adoption["dimensions"])
        self.assertIn("provenance", adoption["dimensions"])

    def test_acceptance_policy_cannot_claim_ready_before_target_acceptance(self) -> None:
        policy = json.loads((CONTRACTS / "everkeep.acceptance.json").read_text(encoding="utf-8"))
        self.assertEqual(policy["schema_version"], 1)
        self.assertEqual(policy["application"], "GoreeCloud Care")
        self.assertEqual(policy["status_schema"], "contracts/continuity.status.schema.json")
        self.assertTrue(policy["freshness"]["required_for_ready"])
        self.assertIn("exact immutable Care candidate", policy["freshness"]["rule"])
        self.assertFalse(policy["acceptance"]["everkeep_integrated"])
        self.assertFalse(policy["acceptance"]["everkeep_ready"])
        self.assertTrue(policy["acceptance"]["target_runtime_acceptance_required"])
        self.assertTrue(policy["acceptance"]["exact_revision_acceptance_required"])

    def test_restore_ready_requires_full_package_lifecycle_and_provenance(self) -> None:
        policy = json.loads((CONTRACTS / "everkeep.acceptance.json").read_text(encoding="utf-8"))
        restore = "\n".join(policy["required_ready_evidence"]["restore_capability"]).lower()
        provenance = "\n".join(policy["required_ready_evidence"]["provenance"]).lower()
        for required in ("installs", "removal", "reinstalls", "downgrade", "restored", "sha-256"):
            self.assertIn(required, restore)
        for required in ("source revision", "sha-256", "ci workflow", "goreecloud/goreecloud-zorin-os"):
            self.assertIn(required, provenance)

    def test_sensitive_recovery_material_is_forbidden(self) -> None:
        policy = json.loads((CONTRACTS / "everkeep.acceptance.json").read_text(encoding="utf-8"))
        forbidden = {item.lower() for item in policy["sensitive_evidence"]["forbidden"]}
        self.assertIn("passwords", forbidden)
        self.assertIn("authentication tokens", forbidden)
        self.assertIn("private keys", forbidden)
        self.assertIn("recovery codes", forbidden)
        self.assertIn("reusable credentials", forbidden)


if __name__ == "__main__":
    unittest.main()
