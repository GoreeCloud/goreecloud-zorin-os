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
        self.assertEqual(adoption["role"], "producer")
        self.assertTrue(adoption["read_only"])
        self.assertTrue(adoption["fail_closed"])

    def test_continuity_schema_blocks_unpromoted_ready(self) -> None:
        schema = json.loads((CONTRACTS / "continuity.status.schema.json").read_text(encoding="utf-8"))
        ready_rule = schema["allOf"][0]["then"]
        self.assertEqual(ready_rule["properties"]["stage"]["const"], "everkeep-promoted")
        self.assertEqual(ready_rule["properties"]["freshness"]["const"], "exact-build-bound")
        self.assertEqual(ready_rule["properties"]["limitations"]["maxItems"], 0)

    def test_acceptance_policy_cannot_self_promote(self) -> None:
        policy = json.loads((CONTRACTS / "everkeep.acceptance.json").read_text(encoding="utf-8"))
        self.assertFalse(policy["acceptance"]["everkeep_integrated"])
        self.assertFalse(policy["acceptance"]["everkeep_ready"])
        self.assertTrue(policy["acceptance"]["separate_everkeep_governance_required"])
        self.assertFalse(policy["authority"]["care_may_promote_everkeep"])

    def test_package_lifecycle_probe_reinstalls_exact_dev3_bytes(self) -> None:
        source = (ROOT / "scripts" / "validate-package-lifecycle.sh").read_text(encoding="utf-8")
        self.assertIn('candidate_version" = "0.2.0~dev3"', source)
        self.assertIn("--reinstall --allow-downgrades", source)
        self.assertIn("Reinstall 0.2.0~dev3 candidate as a fresh package state", source)
        self.assertIn('previous_version" = "0.1.0"', source)
        self.assertIn("stable-downgrade/restore acceptance: passed", source)


if __name__ == "__main__":
    unittest.main()
