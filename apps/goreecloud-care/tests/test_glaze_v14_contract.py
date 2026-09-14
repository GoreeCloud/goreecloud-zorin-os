from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "goreecloud_care"


def _source(name: str) -> str:
    return (PACKAGE / name).read_text(encoding="utf-8")


def test_v14_declares_exact_target_and_source_revision() -> None:
    source = _source("glaze_v14.py")
    assert 'GLAZE_UI_TARGET_VERSION = "1.4.0"' in source
    assert 'GLAZE_UI_SOURCE_REVISION = "01c86323f8b747373d308026adc8b0881855cdc5"' in source
    assert 'GLAZE_UI_ADOPTION_STATE = "development"' in source
    assert "GLAZE_UI_CONSUMER_ELIGIBLE = False" in source


def test_v14_builds_on_v13_expressive_foundation() -> None:
    source = _source("glaze_v14.py")
    assert "CSS as V13_CSS" in source
    assert 'CSS = V13_CSS + b"\\n" + V14_CSS' in source
    assert "Functional glass is restricted to command chrome" in source


def test_v14_has_explicit_native_desktop_form_factor_states() -> None:
    source = _source("glaze_v14.py")
    for state in (
        "form-factor-compact",
        "form-factor-narrow-desktop",
        "form-factor-desktop",
        "form-factor-wide-desktop",
    ):
        assert state in source
    assert "FORM_FACTOR_NARROW_DESKTOP_MAX = 1023" in source
    assert "FORM_FACTOR_DESKTOP_MAX = 1199" in source


def test_v14_preserves_accessibility_degradation_contract() -> None:
    source = _source("glaze_v14.py")
    assert "reduced-transparency" in source
    assert "reduced-motion" in source
    assert "show-borders" in source
    assert "outline-width: 3px" in source
    assert "MIN_TARGET_PX = 48" in source


def test_v14_global_controller_is_active_entrypoint() -> None:
    main_source = _source("__main__.py")
    global_source = _source("glaze_v14_global.py")
    assert "install_glaze_v14_global_style" in main_source
    assert "install_glaze_v13_global_style" not in main_source
    assert "window-added" in global_source
    assert "size-allocate" in global_source
    assert "is_high_contrast_theme" in global_source


def test_v14_does_not_claim_downstream_acceptance() -> None:
    source = _source("glaze_v14.py")
    assert "Downstream applications are not certified" in source
    assert "application-specific validation is accepted" in source
