from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "prepare-representative-acceptance.sh"


class RepresentativeAcceptanceContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = SCRIPT.read_text(encoding="utf-8")

    def test_preparation_harness_has_valid_posix_shell_syntax(self) -> None:
        subprocess.run(["sh", "-n", str(SCRIPT)], check=True)

    def test_preparation_harness_is_non_destructive_and_unprivileged(self) -> None:
        self.assertIn("read-only/non-destructive representative acceptance evidence", self.source)
        for forbidden in (
            "sudo apt",
            "pkexec",
            "apt remove",
            "apt install",
            "empty_trash",
            "clean_selected",
            "reclaim-memory",
            "apt-clean",
        ):
            self.assertNotIn(forbidden, self.source)

    def test_preparation_harness_records_exact_source_and_package_provenance(self) -> None:
        self.assertIn('git -C "$REPO_ROOT" rev-parse HEAD', self.source)
        self.assertIn('sha256sum "$PACKAGE"', self.source)
        self.assertIn("source_revision=$SOURCE_REVISION", self.source)
        self.assertIn("package_sha256=$PACKAGE_SHA256", self.source)
        self.assertIn("SOURCE_REVISION", self.source)

    def test_preparation_harness_uses_only_read_only_installed_status_modes(self) -> None:
        for mode in (
            "--version",
            "--api-version",
            "--report-json",
            "--health-json",
            "--privacy-status-json",
            "--security-status-json",
            "--continuity-status-json",
        ):
            self.assertIn(mode, self.source)

    def test_manual_checklist_keeps_human_only_gates_explicit(self) -> None:
        for required in (
            "Drag continuously narrower/wider",
            "Reverse Shift+Tab",
            "Dynamic status value changes",
            "Orca announcements",
            "HighContrast",
            "Reduced Transparency",
            "Reduced Motion",
            "Canonical Care icon",
            "Package lifecycle / continuity",
            "GLAZE UI V1.2 product-specific acceptance",
            "No manual item is accepted until a representative-device result is explicitly recorded.",
        ):
            self.assertIn(required, self.source)


if __name__ == "__main__":
    unittest.main()
