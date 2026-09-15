from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUILD = (ROOT / "scripts" / "build-deb.sh").read_text(encoding="utf-8")
VERIFY = (ROOT / "scripts" / "verify-reproducible-package.sh").read_text(encoding="utf-8")
WORKFLOW = (ROOT.parents[1] / ".github" / "workflows" / "care-ci.yml").read_text(encoding="utf-8")


class ReproduciblePackagingContractTests(unittest.TestCase):
    def test_build_uses_source_date_epoch_not_wall_clock(self):
        self.assertIn('git -C "$REPO_ROOT" show -s --format=%ct HEAD', BUILD)
        self.assertIn('export SOURCE_DATE_EPOCH', BUILD)
        self.assertNotIn('date +%s', BUILD)

    def test_build_normalizes_staged_mtimes_and_modes(self):
        self.assertIn('find "$STAGE" -exec touch -h -d "@$SOURCE_DATE_EPOCH" {} +', BUILD)
        self.assertIn('find "$STAGE" -type d -exec chmod 0755 {} +', BUILD)
        self.assertIn('Caller umask is not part of package identity', BUILD)

    def test_build_eliminates_compressor_and_locale_variability(self):
        self.assertIn('export LC_ALL=C', BUILD)
        self.assertIn('export TZ=UTC', BUILD)
        self.assertIn('--deb-format=2.0', BUILD)
        self.assertIn('-Znone', BUILD)

    def test_build_embeds_exact_provenance_without_circular_hash(self):
        self.assertIn('/usr/share/goreecloud-care/build-provenance.json', BUILD)
        self.assertIn('"package_sha256_embedded": False', BUILD)
        self.assertIn("embedding a package's own hash is circular", BUILD)

    def test_artifact_package_identity_is_dev3(self):
        self.assertIn('VERSION="0.2.0~dev3"', BUILD)
        self.assertIn('RUNTIME_VERSION="0.2.0-dev3"', BUILD)
        self.assertIn('PACKAGE_NAME="goreecloud-care_0.2.0~dev3_all.deb"', VERIFY)

    def test_verifier_exercises_independent_umasks(self):
        self.assertIn('umask 0022', VERIFY)
        self.assertIn('umask 0002', VERIFY)
        self.assertIn('cmp -s "$REBUILT_022" "$REBUILT_002"', VERIFY)
        self.assertIn('Umask independence: passed (0022 == 0002)', VERIFY)

    def test_ci_records_current_glaze_and_contract_authority(self):
        self.assertIn('name: GoreeCloud Care 0.2.0-dev3 Glaze UI V1.4.1 Optical Intelligence Qualification', WORKFLOW)
        self.assertIn('package_version=0.2.0~dev3', WORKFLOW)
        self.assertIn('glaze_ui_target=1.4.1', WORKFLOW)
        self.assertIn('glaze_ui_authority=4fab9da0fad2e5c974e0e66ec88632c61745751c', WORKFLOW)
        self.assertIn('platform_contract=0.2', WORKFLOW)
        self.assertIn('stable_promotion_authorized=false', WORKFLOW)

    def test_ci_compares_jammy_and_noble_package_bytes(self):
        self.assertIn('ubuntu-22.04', WORKFLOW)
        self.assertIn('ubuntu-24.04', WORKFLOW)
        self.assertIn('Compare cross-environment package bytes', WORKFLOW)
        self.assertIn('cmp -s "$JAMMY" "$NOBLE"', WORKFLOW)
        self.assertIn('cross_environment_reproducibility=passed', WORKFLOW)


if __name__ == "__main__":
    unittest.main()
