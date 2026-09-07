from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run-representative-acceptance.sh"


class RepresentativeRuntimeRunnerContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = RUNNER.read_text(encoding="utf-8")

    def test_runner_has_valid_posix_shell_syntax(self) -> None:
        subprocess.run(["sh", "-n", str(RUNNER)], check=True)

    def test_runner_is_pinned_to_representative_zorin_target_and_normal_user(self) -> None:
        self.assertIn('"$(id -u)" -ne 0', self.source)
        self.assertIn("Run representative acceptance as the normal Zorin desktop user, not as root", self.source)
        self.assertIn('Zorin OS 17.3', self.source)
        self.assertIn('PRETTY_NAME', self.source)

    def test_runner_requires_clean_exact_rc_source_and_tree(self) -> None:
        self.assertIn('status --porcelain --untracked-files=no -- apps/goreecloud-care .github/workflows/care-ci.yml', self.source)
        self.assertIn('SOURCE_REVISION=$(git -C "$REPO_ROOT" rev-parse HEAD)', self.source)
        self.assertIn('SOURCE_TREE=$(git -C "$REPO_ROOT" rev-parse HEAD:apps/goreecloud-care)', self.source)
        self.assertIn('source_revision=$SOURCE_REVISION', self.source)
        self.assertIn('source_tree=$SOURCE_TREE', self.source)
        self.assertIn('lifecycle=release-candidate', self.source)
        self.assertIn('Representative RC acceptance requires lifecycle: release-candidate', self.source)

    def test_runner_executes_all_automatable_exact_candidate_gates(self) -> None:
        for required in (
            'sh ./scripts/validate.sh',
            'sh ./scripts/build-deb.sh dist',
            'sh ./scripts/verify-reproducible-package.sh "$CANDIDATE"',
            'sh ./scripts/build-dev17-rollback-package.sh "$ROLLBACK_DIR"',
            'sh ./scripts/validate-package-lifecycle.sh "$CANDIDATE" "$ROLLBACK"',
            'sha256sum "$CANDIDATE"',
            'dpkg-query -W',
            'goreecloud-care --version',
        ):
            self.assertIn(required, self.source)
        self.assertIn("Representative package install/remove/reinstall/downgrade/rollback acceptance: passed", self.source)
        self.assertIn("Reproducible package verification: passed", self.source)

    def test_runner_generates_schema_compatible_target_handoff_without_promotion(self) -> None:
        for required in (
            '"schema_version": 1',
            '"application": "GoreeCloud Care"',
            '"producer": "GoreeCloud/goreecloud-zorin-os/apps/goreecloud-care"',
            '"restore_capability"',
            '"migration"',
            '"documentation"',
            '"provenance"',
            '"target_runtime_status": "passed"',
            '"exact_revision_accepted": True',
            '"everkeep_integration_promoted": False',
            '"everkeep_ready_promoted": False',
        ):
            self.assertIn(required, self.source)
        self.assertIn('PACKAGE_SHA256', self.source)
        self.assertIn('LOCAL_TESTS', self.source)

    def test_runner_installs_only_care_owned_root_protected_target_record(self) -> None:
        self.assertIn(
            'REPRESENTATIVE_RECORD="/var/lib/goreecloud-care/acceptance/representative-target.json"',
            self.source,
        )
        self.assertIn('sudo install -d -o root -g root -m 0755 /var/lib/goreecloud-care/acceptance', self.source)
        self.assertIn('sudo install -o root -g root -m 0644 "$OUT/representative-target.json" "$REPRESENTATIVE_RECORD"', self.source)
        self.assertNotIn('sudo install -d -o root -g root -m 0755 /var/lib/goreecloud/everkeep', self.source)
        self.assertNotIn('sudo install -o root -g root -m 0644 "$OUT/representative-target.json" /var/lib/goreecloud/everkeep', self.source)

    def test_runner_proves_care_target_record_cannot_self_promote(self) -> None:
        self.assertIn('everkeep_acceptance_path="/nonexistent/goreecloud-care-everkeep.json"', self.source)
        self.assertIn('assert payload["state"] == "attention"', self.source)
        self.assertIn('assert payload["stage"] == "target-accepted-governance-pending"', self.source)
        self.assertIn('Everkeep promotion: not performed by this runner', self.source)

    def test_runner_reports_rc_target_acceptance_without_stable_claim(self) -> None:
        self.assertIn("Representative Release Candidate target acceptance: passed", self.source)
        self.assertIn("remains Release Candidate / nonconformant", self.source)
        self.assertNotIn("remains Development", self.source)
        self.assertNotIn("Stable / conformant", self.source)

    def test_runner_never_invokes_care_cleanup_actions(self) -> None:
        for forbidden in (
            "goreecloud-care --clean",
            "goreecloud-care --empty-trash",
            "goreecloud-care --reclaim",
            "goreecloud-care-helper clean",
        ):
            self.assertNotIn(forbidden, self.source)
        self.assertIn("never invokes a Care cleanup action", self.source)


if __name__ == "__main__":
    unittest.main()
