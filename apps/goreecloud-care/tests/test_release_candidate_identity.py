from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]


class ReleaseCandidateIdentityTests(unittest.TestCase):
    def test_platform_manifest_declares_release_candidate_without_stable_claim(self) -> None:
        manifest = (ROOT / "goreecloud.platform.yaml").read_text(encoding="utf-8")
        self.assertIn("lifecycle: release-candidate", manifest)
        self.assertIn("version: 0.1.0-dev22", manifest)
        self.assertIn("status: nonconformant", manifest)
        self.assertNotIn("lifecycle: stable", manifest)

    def test_core_gtk_identity_is_canonical_release_candidate(self) -> None:
        source = (ROOT / "goreecloud_care" / "app.py").read_text(encoding="utf-8")
        self.assertIn('APP_ID = "com.goreecloud.care"', source)
        self.assertNotIn('APP_ID = "com.goreecloud.care.dev"', source)
        self.assertIn('title="GoreeCloud Care — Release Candidate"', source)
        self.assertIn('self.header_subtitle = "Release Candidate • Adaptive Resonance preview"', source)

    def test_insights_gtk_identity_is_canonical_release_candidate(self) -> None:
        source = (ROOT / "goreecloud_care" / "insights_window.py").read_text(encoding="utf-8")
        self.assertIn('APP_ID = "com.goreecloud.care.insights"', source)
        self.assertNotIn('APP_ID = "com.goreecloud.care.dev.insights"', source)
        self.assertIn('self.header_subtitle = "Release Candidate • read-only local review"', source)

    def test_desktop_and_appstream_identity_are_canonical(self) -> None:
        desktop = (ROOT / "packaging" / "com.goreecloud.care.dev.desktop").read_text(encoding="utf-8")
        metainfo = (ROOT / "packaging" / "com.goreecloud.care.dev.metainfo.xml").read_text(encoding="utf-8")
        self.assertIn("Name=GoreeCloud Care (Release Candidate)", desktop)
        self.assertIn("StartupWMClass=com.goreecloud.care", desktop)
        self.assertNotIn("StartupWMClass=com.goreecloud.care.dev", desktop)
        self.assertIn("<id>com.goreecloud.care</id>", metainfo)
        self.assertIn("<name>GoreeCloud Care (Release Candidate)</name>", metainfo)
        self.assertIn('<launchable type="desktop-id">com.goreecloud.care.desktop</launchable>', metainfo)

    def test_package_installs_canonical_release_identity(self) -> None:
        build = (ROOT / "scripts" / "build-deb.sh").read_text(encoding="utf-8")
        installed = (ROOT / "scripts" / "validate-installed.sh").read_text(encoding="utf-8")
        self.assertIn("Description: GoreeCloud Care Release Candidate maintenance utility", build)
        self.assertIn("/usr/share/applications/com.goreecloud.care.desktop", build)
        self.assertIn("/usr/share/metainfo/com.goreecloud.care.metainfo.xml", build)
        self.assertIn("/usr/share/applications/com.goreecloud.care.desktop", installed)
        self.assertIn("/usr/share/metainfo/com.goreecloud.care.metainfo.xml", installed)
        self.assertNotIn("/usr/share/applications/com.goreecloud.care.dev.desktop", installed)

    def test_lifecycle_documents_identify_bounded_release_candidate(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        specification = (ROOT / "SPECIFICATIONS.md").read_text(encoding="utf-8")
        acceptance = (ROOT / "RELEASE-ACCEPTANCE.md").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("**Lifecycle:** Release Candidate source / nonconformant", readme)
        self.assertIn("# GoreeCloud Care — Release Candidate Specification", specification)
        self.assertIn("**Lifecycle:** Release Candidate / nonconformant", specification)
        self.assertIn("Current Release Candidate source state", acceptance)
        self.assertIn("Release Candidate source transition", changelog)
        self.assertIn("4f7aecd6fa5a6fdd6efb496e606c29457c18fefb", changelog)
        for text in (readme, specification, acceptance):
            self.assertNotIn("**Lifecycle:** Development / nonconformant", text)

    def test_ci_and_representative_harnesses_are_rc_bound(self) -> None:
        workflow = (REPO_ROOT / ".github" / "workflows" / "care-ci.yml").read_text(encoding="utf-8")
        prepare = (ROOT / "scripts" / "prepare-representative-acceptance.sh").read_text(encoding="utf-8")
        runner = (ROOT / "scripts" / "run-representative-acceptance.sh").read_text(encoding="utf-8")
        self.assertIn("name: GoreeCloud Care Release Candidate", workflow)
        self.assertIn("lifecycle=release-candidate", workflow)
        self.assertNotIn("name: GoreeCloud Care Development", workflow)
        self.assertIn("Representative Release Candidate preparation requires lifecycle: release-candidate", prepare)
        self.assertIn("lifecycle=release-candidate", prepare)
        self.assertIn("Representative RC acceptance requires lifecycle: release-candidate", runner)
        self.assertIn("lifecycle=release-candidate", runner)
        self.assertNotIn("remains Development", runner)

    def test_rc_source_does_not_claim_stable_or_platform_promotions(self) -> None:
        manifest = (ROOT / "goreecloud.platform.yaml").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("protected_by_wardveil=false", readme)
        self.assertIn("productionEligible=false", manifest)
        self.assertIn("applicable-blocked", manifest)
        self.assertIn("Stable", readme)
        self.assertNotIn("**Lifecycle:** Stable", readme)


if __name__ == "__main__":
    unittest.main()
