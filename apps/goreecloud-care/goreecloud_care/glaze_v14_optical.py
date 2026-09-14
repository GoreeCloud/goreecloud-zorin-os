"""Deterministic GoreeCloud Care adapter for GLAZE UI V1.4 Optical Intelligence.

This module mirrors the bounded resolver contract in the current Glaze UI
``js/glaze-v1.4-optical-engine.mjs`` authority. It does not collect signals.
Callers may provide already-derived local context only through independently
approved Privacy Shield / Wardveil boundaries. Care's default adapter uses no
camera, wallpaper inspection, telemetry, analytics, network, or remote context.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

LUMINANCE = frozenset({"dark", "mid", "bright", "unknown"})
COMPLEXITY = frozenset({"simple", "moderate", "complex", "unknown"})
DEPTH = frozenset({"base", "raised", "overlay", "modal"})
DAYPART = frozenset({"dawn", "day", "dusk", "night", "unknown"})
APPEARANCE = frozenset({"light", "dark", "deep-dark"})
MAX_MEMORY_TINT_INFLUENCE = 0.08


def _clamp(value: Any, minimum: float = 0.0, maximum: float = 1.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return minimum
    if number != number or number in (float("inf"), float("-inf")):
        return minimum
    return min(maximum, max(minimum, number))


def _bounded(value: Any, allowed: frozenset[str], fallback: str) -> str:
    return value if isinstance(value, str) and value in allowed else fallback


def _complexity_variance(value: str) -> float:
    return {"complex": 0.90, "moderate": 0.55, "simple": 0.18}.get(value, 0.45)


def _luminance_variance(value: str) -> float:
    return {"bright": 0.12, "dark": 0.06, "mid": 0.02}.get(value, 0.04)


def _depth_hue_shift(value: str) -> float:
    return {"raised": 0.012, "overlay": 0.022, "modal": 0.030}.get(value, 0.0)


def _warmth_for_daypart(value: str) -> float:
    return {"dawn": 0.035, "dusk": 0.045, "night": -0.018}.get(value, 0.0)


@dataclass(frozen=True)
class OpticalAccessibility:
    forced_colors: bool = False
    reduced_transparency: bool = False
    increased_contrast: bool = False
    reduced_motion: bool = False


@dataclass(frozen=True)
class MemoryTint:
    css: str
    influence: float


@dataclass(frozen=True)
class OpticalState:
    mode: str
    appearance: str
    background_complexity: str
    background_luminance: str
    depth: str
    daypart: str
    frost_strength: float
    blur_scale: float
    semantic_protection: float
    depth_hue_shift: float
    warmth: float
    memory_tint: MemoryTint | None
    decorative_tint_allowed: bool
    accessibility: OpticalAccessibility


def _normalize_accessibility(value: Any) -> OpticalAccessibility:
    source = value if isinstance(value, Mapping) else {}
    return OpticalAccessibility(
        forced_colors=bool(source.get("forcedColors", source.get("forced_colors", False))),
        reduced_transparency=bool(
            source.get("reducedTransparency", source.get("reduced_transparency", False))
        ),
        increased_contrast=bool(
            source.get("increasedContrast", source.get("increased_contrast", False))
        ),
        reduced_motion=bool(source.get("reducedMotion", source.get("reduced_motion", False))),
    )


def _normalize_memory_tint(value: Any) -> MemoryTint | None:
    if not isinstance(value, Mapping):
        return None
    css = value.get("css")
    if not isinstance(css, str) or not 1 <= len(css) <= 160:
        return None
    influence = _clamp(value.get("influence", 0.04), 0.0, MAX_MEMORY_TINT_INFLUENCE)
    if influence == 0:
        return None
    return MemoryTint(css=css, influence=influence)


def resolve_glaze_optics(options: Mapping[str, Any] | None = None) -> OpticalState:
    """Resolve the bounded V1.4 optical state without collecting any context."""
    source: Mapping[str, Any] = options if isinstance(options, Mapping) else {}
    complexity = _bounded(source.get("backgroundComplexity"), COMPLEXITY, "unknown")
    luminance = _bounded(source.get("backgroundLuminance"), LUMINANCE, "unknown")
    depth = _bounded(source.get("depth"), DEPTH, "base")
    daypart = _bounded(source.get("daypart"), DAYPART, "unknown")
    appearance = _bounded(source.get("appearance"), APPEARANCE, "light")
    accessibility = _normalize_accessibility(source.get("accessibility"))

    if accessibility.forced_colors or accessibility.reduced_transparency:
        return OpticalState(
            mode="solid-accessible",
            appearance=appearance,
            background_complexity=complexity,
            background_luminance=luminance,
            depth=depth,
            daypart=daypart,
            frost_strength=1.0,
            blur_scale=0.0,
            semantic_protection=1.0,
            depth_hue_shift=0.0,
            warmth=0.0,
            memory_tint=None,
            decorative_tint_allowed=False,
            accessibility=accessibility,
        )

    base_frost = _clamp(source.get("baseFrost", 0.34), 0.20, 0.72)
    sensitivity = _clamp(source.get("sensitivityFactor", 0.38), 0.0, 0.55)
    variance = _clamp(_complexity_variance(complexity) + _luminance_variance(luminance))
    frost_strength = _clamp(base_frost + variance * sensitivity, 0.20, 0.88)
    if accessibility.increased_contrast:
        frost_strength = _clamp(frost_strength + 0.10, 0.20, 0.92)

    semantic_importance = _clamp(source.get("semanticImportance", 0.65))
    semantic_protection = _clamp(
        0.50 + semantic_importance * 0.46 + (0.04 if accessibility.increased_contrast else 0.0),
        0.50,
        1.0,
    )
    blur_scale = _clamp(1.0 - semantic_protection * 0.42, 0.50, 0.80)
    memory_tint = None if accessibility.increased_contrast else _normalize_memory_tint(
        source.get("memoryTint")
    )
    warmth = 0.0 if accessibility.increased_contrast else _warmth_for_daypart(daypart)

    return OpticalState(
        mode="adaptive-optical",
        appearance=appearance,
        background_complexity=complexity,
        background_luminance=luminance,
        depth=depth,
        daypart=daypart,
        frost_strength=frost_strength,
        blur_scale=blur_scale,
        semantic_protection=semantic_protection,
        depth_hue_shift=_depth_hue_shift(depth),
        warmth=warmth,
        memory_tint=memory_tint,
        decorative_tint_allowed=not accessibility.increased_contrast,
        accessibility=accessibility,
    )


def care_default_optical_state(
    *,
    appearance: str,
    reduced_transparency: bool,
    reduced_motion: bool,
    increased_contrast: bool = False,
    forced_colors: bool = False,
    depth: str = "base",
    semantic_importance: float = 0.80,
) -> OpticalState:
    """Resolve Care's privacy-safe default state from already-known local UI state.

    Background complexity, wallpaper/content luminance, daypart, and memory tint
    intentionally remain unknown/disabled unless a separately governed adapter is
    introduced later. This keeps the default implementation local, deterministic,
    minimized, and independent from environmental data collection.
    """
    return resolve_glaze_optics(
        {
            "appearance": appearance,
            "backgroundComplexity": "unknown",
            "backgroundLuminance": "dark" if appearance in {"dark", "deep-dark"} else "bright",
            "depth": depth,
            "daypart": "unknown",
            "semanticImportance": semantic_importance,
            "accessibility": {
                "forcedColors": forced_colors,
                "reducedTransparency": reduced_transparency,
                "increasedContrast": increased_contrast,
                "reducedMotion": reduced_motion,
            },
        }
    )


def optical_css_classes(state: OpticalState) -> tuple[str, ...]:
    """Map numeric optical state to bounded native GTK semantic classes."""
    classes = [f"optical-{state.mode}"]
    if state.mode == "solid-accessible":
        return tuple(classes)
    if state.frost_strength < 0.45:
        classes.append("optical-frost-soft")
    elif state.frost_strength < 0.65:
        classes.append("optical-frost-balanced")
    else:
        classes.append("optical-frost-strong")
    if state.semantic_protection >= 0.80:
        classes.append("optical-semantic-protected")
    classes.append(f"optical-depth-{state.depth}")
    if not state.decorative_tint_allowed:
        classes.append("optical-no-decorative-tint")
    return tuple(classes)


GLAZE_OPTICAL_ENGINE_V14 = {
    "version": "1.4.0",
    "lifecycle": "stable",
    "telemetry_required": False,
    "remote_context_required": False,
    "preserves_token_system": True,
    "additive_component_api": True,
    "max_memory_tint_influence": MAX_MEMORY_TINT_INFLUENCE,
    "accessibility_precedence": (
        "forced-colors",
        "reduced-transparency",
        "increased-contrast",
    ),
}
