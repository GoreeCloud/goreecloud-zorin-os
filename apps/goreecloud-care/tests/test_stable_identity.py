from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]


class StableIdentityTests(unittest.TestCase):
    def test_platform_manifest_declares_stable_identity_without_conformance_shortcut(self) -> None:
        manifest = (ROOT / "goreecloud.platform.yaml").read_text(encoding="utf-8")
        self.assertIn("lifecycle: stable", manifest)
        self.assertIn("version: 0.1.0", manifest)
        self.assertIn("status: nonconformant", manifest)
        self.assertNotIn("lifecycle: release-candidate", manifest)
        self.assertNotIn("version: 0.1.0-dev22", manifest)

    def test_runtime_and_python_metadata_are_stable(self) -> None:
        init_source = (ROOT / "goreecloud_care" / "__init__.py").read_text(encoding="utf-8")
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('__version__ = "0.1.0"', init_source)
        self.assertIn('version = "0.1.0"', pyproject)
        self.assertIn('Development Status :: 5 - Production/Stable', pyproject)
        self.assertNotIn('0.1.0-dev22', init_source)

    def test_core_gtk_identity_is_canonical_and_lifecycle_neutral(self) -> None:
        source = (ROOT / "goreecloud_care" / "app.py").read_text(encoding="utf-8")
        self.assertIn('APP_ID = "com.goreecloud.care"', source)
        self.assertIn('title="GoreeCloud Care"', source)
        self.assertIn('self.header_subtitle = "Local maintenance • Adaptive Resonance preview"', source)
        self.assertNotIn('GoreeCloud Care — Release Candidate', source)
        self.assertNotIn('Release Candidate •', source)

    def test_insights_identity_is_canonical_and_lifecycle_neutral(self) -> None:
        source = (ROOT / "goreecloud_care" / "insights_window.py").read_text(encoding="utf-8")
        self.assertIn('APP_ID = "com.goreecloud.care.insights"', source)
        self.assertIn('self.header_subtitle = "Read-only local review"', source)
        self.assertNotIn('Release Candidate •', source)

    def test_desktop_and_appstream_sources_are_canonical_stable(self) -> None:
        desktop_path = ROOT / "packaging" / "com.goreecloud.care.desktop"
        metainfo_path = ROOT / "packaging" / "com.goreecloud.care.metainfo.xml"
        self.assertTrue(desktop_path.is_file())
        self.assertTrue(metainfo_path.is_file())
        self.assertFalse((ROOT / "packaging" / "com.goreecloud.care.dev.desktop").exists())
        self.assertFalse((ROOT / "packaging" / "com.goreecloud.care.dev.metainfo.xml").exists())
        desktop = desktop_path.read_text(encoding="utf-8")
        metainfo = metainfo_path.read_text(encoding="utf-8")
        self.assertIn("Name=GoreeCloud Care", desktop)
        self.assertNotIn("Release Candidate", desktop)
        self.assertIn("StartupWMClass=com.goreecloud.care", desktop)
        self.assertIn("<id>com.goreecloud.care</id>", metainfo)
        self.assertIn("<name>GoreeCloud Care</name>", metainfo)
        self.assertIn('<release version="0.1.0" date="2026-09-07" type="stable"/>', metainfo)

    def test_package_build_uses_stable_identity(self) -> None:
        build = (ROOT / "scripts" / "build-deb.sh").read_text(encoding="utf-8")
        self.assertIn('VERSION="0.1.0"', build)
        self.assertIn('RUNTIME_VERSION="0.1.0"', build)
        self.assertIn("Description: GoreeCloud Care local-first maintenance utility", build)
        self.assertIn("packaging/com.goreecloud.care.desktop", build)
        self.assertIn("packaging/com.goreecloud.care.metainfo.xml", build)
        self.assertNotIn("packaging/com.goreecloud.care.dev.desktop", build)
        self.assertNotIn("packaging/com.goreecloud.care.dev.metainfo.xml", build)

    def test_platform_status_package_identity_matches_stable(self) -> None:
        source = (ROOT / "goreecloud_care" / "platform_status.py").read_text(encoding="utf-8")
        self.assertIn('PACKAGE_VERSION = "0.1.0"', source)
        self.assertNotIn('PACKAGE_VERSION = "0.1.0~dev22"', source)

    def test_ci_and_representative_harnesses_are_stable_qualification_not_self_promotion(self) -> None:
        workflow = (REPO_ROOT / ".github" / "workflows" / "care-ci.yml").read_text(encoding="utf-8")
        prepare = (ROOT / "scripts" / "prepare-representative-acceptance.sh").read_text(encoding="utf-8")
        runner = (ROOT / "scripts" / "run-representative-acceptance.sh").read_text(encoding="utf-8")
        self.assertIn("name: GoreeCloud Care Stable Qualification", workflow)
        for text in (workflow, prepare, runner):
            self.assertIn("stable_promotion_authorized=false", text)
            self.assertNotIn("lifecycle=release-candidate", text)
        self.assertIn("Representative Stable qualification", prepare)
        self.assertIn("Representative Stable qualification", runner)

    def test_stable_source_does_not_self_inherit_exact_rc_platform_governance(self) -> None:
        manifest = (ROOT / "goreecloud.platform.yaml").read_text(encoding="utf-8")
        self.assertIn("status: nonconformant", manifest)
        self.assertIn("Stable identity requires exact-source", manifest)
        self.assertIn("productionEligible=false", manifest)
        self.assertIn("protected_by_wardveil=false", manifest)


if __name__ == "__main__":
    unittest.main()
