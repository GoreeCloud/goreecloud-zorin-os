from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BUILD = (ROOT / "scripts" / "build-deb.sh").read_text(encoding="utf-8")
VERIFY = (ROOT / "scripts" / "verify-reproducible-package.sh").read_text(encoding="utf-8")
WORKFLOW = (ROOT.parents[1] / ".github" / "workflows" / "care-ci.yml").read_text(encoding="utf-8")


class ReproduciblePackagingContractTests(unittest.TestCase):
    def test_build_uses_source_date_epoch_not_wall_clock(self):
        self.assertIn('SOURCE_DATE_EPOCH', BUILD)
        self.assertIn('git -C "$REPO_ROOT" show -s --format=%ct HEAD', BUILD)
        self.assertIn('export SOURCE_DATE_EPOCH', BUILD)
        self.assertNotIn('date +%s', BUILD)

    def test_build_normalizes_staged_mtimes(self):
        self.assertIn(
            'find "$STAGE" -exec touch -h -d "@$SOURCE_DATE_EPOCH" {} +',
            BUILD,
        )
        self.assertIn('dpkg-deb --root-owner-group', BUILD)

    def test_build_eliminates_compressor_and_locale_variability(self):
        self.assertIn('export LC_ALL=C', BUILD)
        self.assertIn('export TZ=UTC', BUILD)
        self.assertIn('--deb-format=2.0', BUILD)
        self.assertIn('-Znone', BUILD)
        self.assertNotIn('-Zxz', BUILD)
        self.assertNotIn('-Zzstd', BUILD)

    def test_verifier_compares_independent_build_to_reference(self):
        self.assertIn('SOURCE_DATE_EPOCH="$SOURCE_DATE_EPOCH" sh "$ROOT/scripts/build-deb.sh"', VERIFY)
        self.assertIn('cmp -s "$REFERENCE" "$REBUILT"', VERIFY)
        self.assertIn('sha256sum "$REFERENCE"', VERIFY)
        self.assertIn('sha256sum "$REBUILT"', VERIFY)
        self.assertIn('Reproducible package verification: passed', VERIFY)

    def test_ci_runs_same_environment_reproducibility_gate(self):
        self.assertIn('Verify reproducible GoreeCloud Care package', WORKFLOW)
        self.assertIn('sh ./scripts/verify-reproducible-package.sh', WORKFLOW)

    def test_ci_compares_jammy_and_noble_package_bytes(self):
        self.assertIn('ubuntu-22.04', WORKFLOW)
        self.assertIn('ubuntu-24.04', WORKFLOW)
        self.assertIn('Compare cross-environment package bytes', WORKFLOW)
        self.assertIn('cmp -s "$JAMMY" "$NOBLE"', WORKFLOW)
        self.assertIn('cross_environment_reproducibility=passed', WORKFLOW)


if __name__ == "__main__":
    unittest.main()
