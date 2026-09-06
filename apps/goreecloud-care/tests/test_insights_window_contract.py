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

    def test_large_text_page_and_results_remain_vertically_reachable(self):
        source = self._source()
        self.assertIn('self.page_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)', source)
        self.assertIn('self.results_scroll.set_min_content_height(RESULTS_MIN_HEIGHT)', source)
        self.assertIn('RESULTS_MIN_HEIGHT = 320', source)
        self.assertIn('self.text.set_wrap_mode(Gtk.WrapMode.CHAR)', source)

    def test_compact_insights_layout_reduces_header_and_fixed_copy(self):
        source = self._source()
        self.assertIn('compact = is_compact_width(width)', source)
        self.assertIn('self.header.set_title("Insights" if compact else "Maintenance Insights")', source)
        self.assertIn('self.header.set_subtitle(None if compact else self.header_subtitle)', source)
        self.assertIn('self.intro_compact_markup', source)
        self.assertIn('self.privacy_compact_text', source)

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
