import unittest

from goreecloud_care.ui_contract import (
    COMPACT_WIDTH,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    is_compact_width,
    is_high_contrast_theme,
)


class UIContractTests(unittest.TestCase):
    def test_compact_breakpoint_is_deterministic(self):
        self.assertTrue(is_compact_width(COMPACT_WIDTH - 1))
        self.assertFalse(is_compact_width(COMPACT_WIDTH))
        self.assertFalse(is_compact_width(COMPACT_WIDTH + 1))

    def test_compact_breakpoint_covers_large_text_narrow_range(self):
        self.assertTrue(is_compact_width(800))
        self.assertFalse(is_compact_width(900))

    def test_minimum_window_remains_usable_desktop_size(self):
        self.assertGreaterEqual(MIN_WINDOW_WIDTH, 480)
        self.assertGreaterEqual(MIN_WINDOW_HEIGHT, 420)

    def test_high_contrast_theme_variants_are_recognized(self):
        for name in (
            "HighContrast",
            "HighContrastInverse",
            "high-contrast",
            "high_contrast",
            "High Contrast",
        ):
            with self.subTest(name=name):
                self.assertTrue(is_high_contrast_theme(name))

    def test_normal_themes_are_not_high_contrast(self):
        for name in (None, "", "ZorinBlue-Light", "Adwaita", "Adwaita-dark"):
            with self.subTest(name=name):
                self.assertFalse(is_high_contrast_theme(name))


if __name__ == "__main__":
    unittest.main()
