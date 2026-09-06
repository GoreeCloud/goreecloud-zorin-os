from pathlib import Path
import unittest


class InsightsWindowContractTests(unittest.TestCase):
    def _source(self) -> str:
        return (
            Path(__file__).resolve().parents[1]
            / "goreecloud_care"
            / "insights_window.py"
        ).read_text(encoding="utf-8")

    def test_window_is_explicitly_read_only(self):
        source = self._source()
        self.assertIn('self.text.set_editable(False)', source)
        self.assertIn('Nothing is selected or deleted automatically', source)
        self.assertNotIn('.unlink(', source)
        self.assertNotIn('shutil.rmtree', source)
        self.assertNotIn('pkexec', source)
        self.assertNotIn('subprocess', source)

    def test_window_exposes_accessible_status_and_results(self):
        source = self._source()
        self.assertIn('Atk.Role.STATUSBAR', source)
        self.assertIn('Maintenance Insights results', source)
        self.assertIn('visible-data-changed', source)

    def test_entrypoint_has_dedicated_insights_ui_mode(self):
        entrypoint = (
            Path(__file__).resolve().parents[1]
            / "goreecloud_care"
            / "__main__.py"
        ).read_text(encoding="utf-8")
        self.assertIn('"--insights-ui"', entrypoint)
        self.assertIn('from .insights_window import main as insights_main', entrypoint)


if __name__ == "__main__":
    unittest.main()
