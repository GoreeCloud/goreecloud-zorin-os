from __future__ import annotations

from pathlib import Path
import unittest

from goreecloud_care.glaze_v14_optical import (
    MAX_MEMORY_TINT_INFLUENCE,
    care_default_optical_state,
    optical_css_classes,
    resolve_glaze_optics,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "goreecloud_care"


def _source(name: str) -> str:
    return (PACKAGE / name).read_text(encoding="utf-8")


class GlazeV14ContractTests(unittest.TestCase):
    def test_v14_declares_current_optical_intelligence_authority(self) -> None:
        source = _source("glaze_v14.py")
        self.assertIn('GLAZE_UI_LABEL = "GLAZE UI V1.4 — Optical Intelligence"', source)
        self.assertIn('GLAZE_UI_TARGET_VERSION = "1.4.0"', source)
        self.assertIn(
            'GLAZE_UI_SOURCE_REVISION = "ee057ce9e729296aeaeda182d01db89f52bd66f3"',
            source,
        )
        self.assertIn(
            'GLAZE_UI_SOURCE_INTEGRATION_ANCHOR = "a20374734dae6a119b28448f5e6b3232253b6da7"',
            source,
        )
        self.assertIn('GLAZE_UI_ADOPTION_STATE = "development"', source)
        self.assertIn("GLAZE_UI_CONSUMER_ELIGIBLE = False", source)

    def test_v14_is_additive_to_v13_but_not_defined_by_form_factor(self) -> None:
        source = _source("glaze_v14.py")
        self.assertIn("CSS as V13_CSS", source)
        self.assertIn('CSS = V13_CSS + b"\\n" + V14_CSS', source)
        self.assertIn("Optical Intelligence", source)
        self.assertIn("application-owned GTK", source)
        self.assertNotIn('GLAZE_UI_LABEL = "GLAZE UI V1.4 — Form-Factor Evolution"', source)

    def test_optical_engine_is_local_and_deterministic(self) -> None:
        source = _source("glaze_v14_optical.py")
        self.assertIn("does not collect signals", source)
        self.assertIn('"telemetry_required": False', source)
        self.assertIn('"remote_context_required": False', source)
        self.assertNotIn("requests.", source)
        self.assertNotIn("subprocess", source)

    def test_default_optics_match_current_glaze_bounds(self) -> None:
        state = resolve_glaze_optics(
            {
                "appearance": "light",
                "backgroundComplexity": "unknown",
                "backgroundLuminance": "bright",
                "semanticImportance": 0.80,
            }
        )
        self.assertEqual(state.mode, "adaptive-optical")
        self.assertAlmostEqual(state.frost_strength, 0.5566, places=4)
        self.assertAlmostEqual(state.semantic_protection, 0.868, places=4)
        self.assertAlmostEqual(state.blur_scale, 0.63544, places=5)
        self.assertTrue(state.decorative_tint_allowed)

    def test_reduced_transparency_forces_solid_accessible(self) -> None:
        state = resolve_glaze_optics(
            {
                "memoryTint": {"css": "#abcdef", "influence": 0.08},
                "accessibility": {"reducedTransparency": True},
            }
        )
        self.assertEqual(state.mode, "solid-accessible")
        self.assertEqual(state.frost_strength, 1.0)
        self.assertEqual(state.blur_scale, 0.0)
        self.assertEqual(state.semantic_protection, 1.0)
        self.assertIsNone(state.memory_tint)
        self.assertFalse(state.decorative_tint_allowed)
        self.assertEqual(optical_css_classes(state), ("optical-solid-accessible",))

    def test_forced_colors_has_same_accessibility_precedence(self) -> None:
        state = resolve_glaze_optics({"accessibility": {"forcedColors": True}})
        self.assertEqual(state.mode, "solid-accessible")
        self.assertEqual(state.warmth, 0.0)
        self.assertEqual(state.depth_hue_shift, 0.0)

    def test_increased_contrast_suppresses_decorative_tint_and_warmth(self) -> None:
        state = resolve_glaze_optics(
            {
                "daypart": "dusk",
                "memoryTint": {"css": "#abcdef", "influence": 1},
                "accessibility": {"increasedContrast": True},
            }
        )
        self.assertEqual(state.mode, "adaptive-optical")
        self.assertIsNone(state.memory_tint)
        self.assertEqual(state.warmth, 0.0)
        self.assertFalse(state.decorative_tint_allowed)
        self.assertIn("optical-no-decorative-tint", optical_css_classes(state))

    def test_memory_tint_is_bounded_to_eight_percent(self) -> None:
        state = resolve_glaze_optics(
            {"memoryTint": {"css": "#abcdef", "influence": 99}}
        )
        self.assertIsNotNone(state.memory_tint)
        assert state.memory_tint is not None
        self.assertEqual(MAX_MEMORY_TINT_INFLUENCE, 0.08)
        self.assertEqual(state.memory_tint.influence, 0.08)

    def test_malformed_context_fails_to_bounded_defaults(self) -> None:
        state = resolve_glaze_optics(
            {
                "appearance": "invalid",
                "backgroundComplexity": object(),
                "backgroundLuminance": None,
                "depth": "impossible",
                "daypart": 123,
                "baseFrost": "not-a-number",
            }
        )
        self.assertEqual(state.appearance, "light")
        self.assertEqual(state.background_complexity, "unknown")
        self.assertEqual(state.background_luminance, "unknown")
        self.assertEqual(state.depth, "base")
        self.assertEqual(state.daypart, "unknown")
        self.assertGreaterEqual(state.frost_strength, 0.20)
        self.assertLessEqual(state.frost_strength, 0.88)

    def test_care_default_adapter_does_not_collect_environment_context(self) -> None:
        state = care_default_optical_state(
            appearance="dark",
            reduced_transparency=False,
            reduced_motion=False,
        )
        self.assertEqual(state.background_complexity, "unknown")
        self.assertEqual(state.background_luminance, "dark")
        self.assertEqual(state.daypart, "unknown")
        self.assertIsNone(state.memory_tint)

    def test_v14_preserves_native_desktop_responsiveness(self) -> None:
        source = _source("glaze_v14.py")
        for state in (
            "form-factor-compact",
            "form-factor-narrow-desktop",
            "form-factor-desktop",
            "form-factor-wide-desktop",
        ):
            self.assertIn(state, source)
        self.assertIn("effective_layout_width", source)
        self.assertIn("is_compact_width", source)
        self.assertIn("MIN_TARGET_PX = 48", source)

    def test_v14_global_controller_applies_optical_and_accessibility_state(self) -> None:
        global_source = _source("glaze_v14_global.py")
        self.assertIn("OPTICAL_CLASSES", global_source)
        self.assertIn("window_optical_classes", global_source)
        self.assertIn("increased_contrast_requested", global_source)
        self.assertIn("is_high_contrast_theme", global_source)
        self.assertLess(
            global_source.index("self.sync()"),
            global_source.index("GLib.timeout_add(100, self._attach_application)"),
        )

    def test_v14_global_controller_is_active_entrypoint(self) -> None:
        main_source = _source("__main__.py")
        self.assertIn("from .glaze_v14_global import install_glaze_v14_global_style", main_source)
        self.assertIn("install_glaze_v14_global_style()", main_source)
        self.assertNotIn("from .glaze_v13_global import", main_source)


if __name__ == "__main__":
    unittest.main()
