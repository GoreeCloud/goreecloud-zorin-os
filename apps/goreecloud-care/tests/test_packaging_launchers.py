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
STABLE_ROLLBACK = ROOT / "scripts" / "build-stable-0.1.0-rollback-package.sh"


class PackagingLauncherIsolationTests(unittest.TestCase):
    def test_shell_entrypoints_have_valid_posix_syntax(self) -> None:
        for path in (APP, HELPER, POSTINST, POSTRM, BUILD, LIFECYCLE, STABLE_ROLLBACK):
            subprocess.run(["sh", "-n", str(path)], check=True)

    def test_application_launcher_uses_isolated_no_bytecode_python(self) -> None:
        source = APP.read_text(encoding="utf-8")
        self.assertIn('exec /usr/bin/python3 -I -B -m goreecloud_care "$@"', source)
        self.assertNotIn("PYTHONPATH=", source)

    def test_privileged_helper_uses_same_isolation_boundary(self) -> None:
        source = HELPER.read_text(encoding="utf-8")
        self.assertIn('exec /usr/bin/python3 -I -B -m goreecloud_care.helper "$@"', source)
        self.assertIn("PolicyKit", source)
        self.assertNotIn("PYTHONPATH=", source)

    def test_postinst_repairs_fixed_provenance_trust_path(self) -> None:
        source = POSTINST.read_text(encoding="utf-8")
        self.assertIn("chown root:root /usr/share/goreecloud-care", source)
        self.assertIn("chmod 0755 /usr/share/goreecloud-care", source)
        self.assertIn("chmod 0644 /usr/share/goreecloud-care/build-provenance.json", source)

    def test_debian_build_installs_dev3_identity(self) -> None:
        source = BUILD.read_text(encoding="utf-8")
        self.assertIn('VERSION="0.2.0~dev3"', source)
        self.assertIn('RUNTIME_VERSION="0.2.0-dev3"', source)
        self.assertIn("packaging/com.goreecloud.care.metainfo.xml", source)
        self.assertNotIn('VERSION="0.1.0"', source)

    def test_lifecycle_probe_keeps_candidate_isolation_regression_gate(self) -> None:
        source = LIFECYCLE.read_text(encoding="utf-8")
        self.assertIn("working-directory/PYTHONPATH shadowing", source)
        self.assertIn("Private Python bytecode remained after package removal", source)
        self.assertIn("0.2.0~dev3", source)
        self.assertIn("Downgrade to immutable Stable 0.1.0", source)

    def test_stable_rollback_builder_verifies_accepted_package_bytes(self) -> None:
        source = STABLE_ROLLBACK.read_text(encoding="utf-8")
        self.assertIn('EXPECTED_VERSION="0.1.0"', source)
        self.assertIn('EXPECTED_SHA256="819cff6e0132bf6b09df0986682995c25b14c39e74982f725efd0b5a21b71160"', source)


if __name__ == "__main__":
    unittest.main()
