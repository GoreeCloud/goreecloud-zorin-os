from pathlib import Path
import unittest


class AccessibilityIdentityTests(unittest.TestCase):
    def test_entrypoint_sets_product_application_name_before_main(self):
        entrypoint = (
            Path(__file__).resolve().parents[1]
            / "goreecloud_care"
            / "__main__.py"
        ).read_text(encoding="utf-8")

        identity = 'GLib.set_application_name("GoreeCloud Care")'
        launch = "raise SystemExit(main())"
        self.assertIn(identity, entrypoint)
        self.assertIn(launch, entrypoint)
        self.assertLess(entrypoint.index(identity), entrypoint.index(launch))


if __name__ == "__main__":
    unittest.main()
