from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "packaging" / "goreecloud-care"
HELPER = ROOT / "packaging" / "goreecloud-care-helper"
POSTINST = ROOT / "packaging" / "postinst"
POSTRM = ROOT / "packaging" / "postrm"
BUILD = ROOT / "scripts" / "build-deb.sh"
LIFECYCLE = ROOT / "scripts" / "validate-package-lifecycle.sh"


class PackagingLauncherIsolationTests(unittest.TestCase):
    def test_shell_entrypoints_have_valid_posix_syntax(self) -> None:
        for path in (APP, HELPER, POSTINST, POSTRM, BUILD, LIFECYCLE):
            subprocess.run(["sh", "-n", str(path)], check=True)

    def test_application_launcher_uses_isolated_no_bytecode_python(self) -> None:
        source = APP.read_text(encoding="utf-8")
        self.assertIn(
            'exec /usr/bin/python3 -I -B -m goreecloud_care "$@"',
            source,
        )
        self.assertIn("working directory", source)
        self.assertNotIn("PYTHONPATH=", source)

    def test_privileged_helper_launcher_uses_same_isolation_boundary(self) -> None:
        source = HELPER.read_text(encoding="utf-8")
        self.assertIn(
            'exec /usr/bin/python3 -I -B -m goreecloud_care.helper "$@"',
            source,
        )
        self.assertIn("user-controlled working directory", source)
        self.assertIn("PolicyKit", source)
        self.assertNotIn("PYTHONPATH=", source)

    def test_package_maintainer_scripts_only_clean_fixed_private_bytecode(self) -> None:
        for path in (POSTINST, POSTRM):
            source = path.read_text(encoding="utf-8")
            self.assertIn(
                "/usr/lib/goreecloud-care/goreecloud_care/__pycache__",
                source,
            )
            self.assertNotIn("$HOME", source)
            self.assertNotIn("/home/", source)
            self.assertNotIn("find ", source)

    def test_debian_build_installs_bytecode_cleanup_maintainer_scripts(self) -> None:
        source = BUILD.read_text(encoding="utf-8")
        self.assertIn(
            'install -m 0755 "$ROOT/packaging/postinst" "$STAGE/DEBIAN/postinst"',
            source,
        )
        self.assertIn(
            'install -m 0755 "$ROOT/packaging/postrm" "$STAGE/DEBIAN/postrm"',
            source,
        )
        self.assertIn('VERSION="0.1.0~dev20"', source)

    def test_lifecycle_probe_keeps_candidate_shadowing_as_a_regression_gate(self) -> None:
        source = LIFECYCLE.read_text(encoding="utf-8")
        self.assertIn("Dev20 candidate checks deliberately exercise source/working-directory shadow resistance", source)
        self.assertIn("working-directory/PYTHONPATH shadowing", source)
        self.assertIn("Private Python bytecode remained after package removal", source)
        self.assertIn("0.1.0~dev20", source)

    def test_historical_rollback_is_checked_from_a_clean_neutral_directory(self) -> None:
        source = LIFECYCLE.read_text(encoding="utf-8")
        self.assertIn("dev17 predates that isolation contract", source)
        self.assertIn("PREVIOUS_PROBE_DIR=$(mktemp -d)", source)
        self.assertIn('assert_version_from "$previous_version" "$previous_runtime" "$PREVIOUS_PROBE_DIR"', source)
        self.assertIn('(cd "$PREVIOUS_PROBE_DIR" && goreecloud-care --report-json >/dev/null)', source)
        self.assertIn('assert_version_from "$candidate_version" "$candidate_runtime" "$ROOT"', source)


if __name__ == "__main__":
    unittest.main()
