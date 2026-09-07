from __future__ import annotations

import unittest
from unittest.mock import patch

from goreecloud_care.glaze_v13 import (
    APPEARANCE_ENV,
    CLARITY_ENV,
    CSS,
    EXPRESSION_ENV,
    GLAZE_UI_CONSUMER_ELIGIBLE,
    GLAZE_UI_LABEL,
    GLAZE_UI_LIFECYCLE,
    GLAZE_UI_SOURCE_REVISION,
    GLAZE_UI_STABLE_BASELINE,
    GLAZE_UI_TARGET_VERSION,
    MIN_TARGET_PX,
    REDUCE_MOTION_ENV,
    REDUCE_TRANSPARENCY_ENV,
    SHOW_BORDERS_ENV,
    appearance_from_theme,
    clarity_profile,
    expression_profile,
    layout_environment,
    reduced_motion_requested,
    reduced_transparency_requested,
    show_borders_requested,
)
from goreecloud_care.glaze_v13_global import _runtime_css


class GlazeV13ContractTests(unittest.TestCase):
    def test_latest_development_identity_is_truthful(self) -> None:
        self.assertEqual(GLAZE_UI_LABEL, "GLAZE UI V1.3 — Adaptive Resonance")
        self.assertEqual(GLAZE_UI_TARGET_VERSION, "1.3.0-candidate")
        self.assertEqual(GLAZE_UI_LIFECYCLE, "proposed")
        self.assertFalse(GLAZE_UI_CONSUMER_ELIGIBLE)
        self.assertEqual(GLAZE_UI_STABLE_BASELINE, "1.2.0")
        self.assertEqual(
            GLAZE_UI_SOURCE_REVISION,
            "dc5ee04b09bd7d2c06d6ac1456618cbd4b1f4b80",
        )
        self.assertEqual(MIN_TARGET_PX, 48)

    def test_expression_and_clarity_are_separate_dimensions(self) -> None:
        self.assertEqual(expression_profile(None), "balanced")
        self.assertEqual(clarity_profile(None), "balanced")
        self.assertEqual(expression_profile("calm"), "calm")
        self.assertEqual(expression_profile("expressive"), "expressive")
        self.assertEqual(clarity_profile("clear"), "clear")
        self.assertEqual(clarity_profile("dense"), "dense")
        self.assertEqual(expression_profile("invalid"), "balanced")
        self.assertEqual(clarity_profile("invalid"), "balanced")

    def test_material_and_shape_roles_are_semantic_and_restrained(self) -> None:
        text = CSS.decode("utf-8")
        self.assertIn(".chrome-plane", text)
        self.assertIn(".content-plane", text)
        self.assertIn(".maintenance-collection", text)
        self.assertIn(".findings-plane", text)
        self.assertIn("button.command-capsule { border-radius: 999px; }", text)
        self.assertIn("button.resonant-action", text)
        self.assertIn("border-radius: 12px", text)
        self.assertIn("button,\nwindow.care-shell checkbutton { min-height: 48px; }", text)
        self.assertNotIn("button {\n  border-radius: 999px", text)
        self.assertNotIn("transition:", text)
        self.assertNotIn("animation:", text)

    def test_accessibility_degradation_is_explicit(self) -> None:
        self.assertTrue(reduced_transparency_requested("1"))
        self.assertTrue(reduced_motion_requested(False, value="0"))
        self.assertTrue(reduced_motion_requested(True, value="1"))
        self.assertFalse(reduced_motion_requested(True, value="0"))
        self.assertTrue(show_borders_requested("yes"))
        text = CSS.decode("utf-8")
        self.assertIn("reduced-transparency", text)
        self.assertIn("reduced-motion", text)
        self.assertIn("show-borders", text)

    def test_appearance_remains_bounded_and_system_aware(self) -> None:
        self.assertEqual(
            appearance_from_theme(
                "ZorinBlue-Light", appearance_override="system", gtk_theme_override=""
            ),
            "light",
        )
        self.assertEqual(
            appearance_from_theme(
                "Adwaita-dark", appearance_override="system", gtk_theme_override=""
            ),
            "dark",
        )
        with patch.dict("os.environ", {APPEARANCE_ENV: "deep-dark"}, clear=False):
            self.assertEqual(appearance_from_theme("Adwaita"), "deep-dark")

    def test_layout_environments_add_context_instead_of_stretching(self) -> None:
        self.assertEqual(layout_environment(600, compact=True), "compact")
        self.assertEqual(layout_environment(900, compact=False), "medium")
        self.assertEqual(layout_environment(1200, compact=False), "expanded")

    def test_runtime_css_promotes_only_resolved_development_state(self) -> None:
        data = _runtime_css(
            "dark",
            expression="balanced",
            clarity="clear",
            reduced_transparency=True,
            reduced_motion=True,
            show_borders=True,
        ).decode("utf-8")
        self.assertIn("window {\n  background: #17191c", data)
        self.assertIn("window .hero-surface", data)
        self.assertIn("window .maintenance-row", data)

    def test_development_environment_names_are_product_scoped(self) -> None:
        for name in (
            APPEARANCE_ENV,
            EXPRESSION_ENV,
            CLARITY_ENV,
            REDUCE_TRANSPARENCY_ENV,
            REDUCE_MOTION_ENV,
            SHOW_BORDERS_ENV,
        ):
            self.assertTrue(name.startswith("GOREECLOUD_CARE_"))


if __name__ == "__main__":
    unittest.main()
