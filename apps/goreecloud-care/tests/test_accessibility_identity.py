from pathlib import Path
import unittest


class AccessibilityIdentityTests(unittest.TestCase):
    def _entrypoint(self):
        return (
            Path(__file__).resolve().parents[1]
            / "goreecloud_care"
            / "__main__.py"
        ).read_text(encoding="utf-8")

    def test_entrypoint_sets_product_program_name_before_main(self):
        entrypoint = self._entrypoint()
        identity = 'GLib.set_prgname("GoreeCloud Care")'
        launch = "raise SystemExit(main())"
        self.assertIn(identity, entrypoint)
        self.assertIn(launch, entrypoint)
        self.assertLess(entrypoint.index(identity), entrypoint.index(launch))

    def test_entrypoint_sets_product_application_name_before_main(self):
        entrypoint = self._entrypoint()
        identity = 'GLib.set_application_name("GoreeCloud Care")'
        launch = "raise SystemExit(main())"
        self.assertIn(identity, entrypoint)
        self.assertIn(launch, entrypoint)
        self.assertLess(entrypoint.index(identity), entrypoint.index(launch))

    def test_program_identity_precedes_application_identity(self):
        entrypoint = self._entrypoint()
        program_identity = 'GLib.set_prgname("GoreeCloud Care")'
        application_identity = 'GLib.set_application_name("GoreeCloud Care")'
        self.assertLess(
            entrypoint.index(program_identity),
            entrypoint.index(application_identity),
        )


if __name__ == "__main__":
    unittest.main()
