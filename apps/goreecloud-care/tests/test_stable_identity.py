from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
STABLE_SOURCE = "bbc4779454c2887b810aa0ddc9e8a686a4c68ebd"
STABLE_PACKAGE_SHA = "819cff6e0132bf6b09df0986682995c25b14c39e74982f725efd0b5a21b71160"


class DevelopmentArtifactIdentityTests(unittest.TestCase):
    def test_platform_manifest_declares_nonconformant_dev3_contract_0_2_line(self) -> None:
        manifest = (ROOT / "goreecloud.platform.yaml").read_text(encoding="utf-8")
        self.assertIn('schema_version: "0.2"', manifest)
        self.assertIn('\nlifecycle: development\n', manifest)
        self.assertIn('version: 0.2.0-dev3', manifest)
        self.assertIn('status: nonconformant', manifest)
        self.assertIn('glaze_ui_required: "1.4.1"', manifest)
        self.assertIn('platform_contract: "0.2"', manifest)
        self.assertNotIn('\n  sync:\n', manifest)
        for system in ("manager","privacy_shield","wardveil_security","everkeep","glaze_ui","mesh","identity"):
            self.assertIn(f'\n  {system}:\n', manifest)
        self.assertIn('GoreeCloud Sync is separately governed application/service functionality', manifest)

    def test_runtime_and_python_metadata_are_dev3_identity(self) -> None:
        init_source = (ROOT / "goreecloud_care" / "__init__.py").read_text(encoding="utf-8")
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('__version__ = "0.2.0-dev3"', init_source)
        self.assertIn('version = "0.2.0-dev3"', pyproject)
        self.assertIn('Development Status :: 3 - Alpha', pyproject)

    def test_appstream_preserves_stable_history_and_adds_dev3(self) -> None:
        metainfo = (ROOT / "packaging" / "com.goreecloud.care.metainfo.xml").read_text(encoding="utf-8")
        self.assertIn('<release version="0.2.0-dev3" date="2026-09-15" type="development"/>', metainfo)
        self.assertIn('<release version="0.1.0" date="2026-09-07" type="stable"/>', metainfo)

    def test_package_and_platform_status_identity_match_dev3(self) -> None:
        build = (ROOT / "scripts" / "build-deb.sh").read_text(encoding="utf-8")
        status = (ROOT / "goreecloud_care" / "platform_status.py").read_text(encoding="utf-8")
        self.assertIn('VERSION="0.2.0~dev3"', build)
        self.assertIn('RUNTIME_VERSION="0.2.0-dev3"', build)
        self.assertIn('PACKAGE_VERSION = "0.2.0~dev3"', status)

    def test_stable_0_1_0_evidence_is_historical_only(self) -> None:
        manifest = (ROOT / "goreecloud.platform.yaml").read_text(encoding="utf-8")
        self.assertIn(STABLE_SOURCE, manifest)
        self.assertIn(STABLE_PACKAGE_SHA, manifest)
        self.assertIn('Historical Stable 0.1.0 evidence', manifest)

    def test_dev3_does_not_inherit_external_platform_acceptance(self) -> None:
        manifest = (ROOT / "goreecloud.platform.yaml").read_text(encoding="utf-8")
        for system in ("privacy_shield", "wardveil_security", "everkeep"):
            self.assertIn(f'  {system}:\n    result: applicable-nonconformant', manifest)
        self.assertIn('  glaze_ui:\n    result: applicable-migration-required', manifest)
        self.assertIn('Stable promotion requires a later explicit exact-candidate decision', manifest)

    def test_local_status_producers_do_not_self_assign_external_governance(self) -> None:
        source = (ROOT / "goreecloud_care" / "platform_status.py").read_text(encoding="utf-8")
        self.assertIn('"protected_by_wardveil": False', source)
        self.assertIn('production_approved: bool = False', source)

    def test_ci_is_v141_candidate_qualification_not_stable_republication(self) -> None:
        workflow = (REPO_ROOT / ".github" / "workflows" / "care-ci.yml").read_text(encoding="utf-8")
        self.assertIn('name: GoreeCloud Care 0.2.0-dev3 Glaze UI V1.4.1 Optical Intelligence Qualification', workflow)
        self.assertIn('glaze_ui_target=1.4.1', workflow)
        self.assertIn('platform_contract=0.2', workflow)
        self.assertIn('stable_promotion_authorized=false', workflow)
        self.assertIn('build-stable-0.1.0-rollback-package.sh', workflow)


if __name__ == "__main__":
    unittest.main()
