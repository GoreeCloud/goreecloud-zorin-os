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
        self.assertIn(
            "read-only/non-destructive representative acceptance evidence",
            self.source,
        )
        self.assertIn(
            "does not invoke Care cleanup, PolicyKit, pkexec, sudo, apt, or network operations",
            self.source,
        )
        forbidden_invocations = (
            "sudo apt ",
            "pkexec ",
            "apt remove ",
            "apt install ",
            "goreecloud-care-helper ",
        )
        for forbidden in forbidden_invocations:
            self.assertNotIn(forbidden, self.source)

        self.assertNotIn("goreecloud-care --clean", self.source)
        self.assertNotIn("goreecloud-care --empty-trash", self.source)
        self.assertNotIn("goreecloud-care --reclaim", self.source)

    def test_preparation_harness_requires_clean_exact_source(self) -> None:
        self.assertIn('git -C "$REPO_ROOT" status --porcelain --untracked-files=no', self.source)
        self.assertIn("Tracked working-tree changes are present", self.source)
        self.assertIn('git -C "$REPO_ROOT" rev-parse HEAD', self.source)
        self.assertIn('source_branch=$SOURCE_BRANCH', self.source)

    def test_preparation_harness_records_exact_source_and_package_provenance(self) -> None:
        self.assertIn('EXPECTED_RUNTIME_VERSION="0.1.0-dev18"', self.source)
        self.assertIn('EXPECTED_PACKAGE_VERSION="0.1.0~dev18"', self.source)
        self.assertIn('"$RUNTIME_VERSION" = "$EXPECTED_RUNTIME_VERSION"', self.source)
        self.assertIn('"$PACKAGE_VERSION" = "$EXPECTED_PACKAGE_VERSION"', self.source)
        self.assertIn('sha256sum "$PACKAGE"', self.source)
        self.assertIn("source_revision=$SOURCE_REVISION", self.source)
        self.assertIn("package_sha256=$PACKAGE_SHA256", self.source)
        self.assertIn("SOURCE_REVISION", self.source)

    def test_preparation_harness_selects_exact_expected_package(self) -> None:
        self.assertIn(
            'EXPECTED_PACKAGE="$ROOT/dist/goreecloud-care_${EXPECTED_PACKAGE_VERSION}_all.deb"',
            self.source,
        )
        self.assertIn("PACKAGE=$EXPECTED_PACKAGE", self.source)
        self.assertIn("Expected built package not found", self.source)
        self.assertNotIn('find "$ROOT/dist"', self.source)
        self.assertNotIn("sort | tail", self.source)

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
            "build-dev17-rollback-package.sh",
            "GLAZE UI V1.2 product-specific acceptance",
            "No manual item is accepted until a representative-device result is explicitly recorded.",
        ):
            self.assertIn(required, self.source)


if __name__ == "__main__":
    unittest.main()
