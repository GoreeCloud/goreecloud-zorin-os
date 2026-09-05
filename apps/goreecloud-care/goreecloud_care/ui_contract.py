"""Pure UI-contract helpers for GoreeCloud Care Development."""

# Switch before constrained/large-text layouts reach the point where the regular
# horizontal composition can no longer transition into its compact form.
COMPACT_WIDTH = 820
MIN_WINDOW_WIDTH = 480
MIN_WINDOW_HEIGHT = 420
REGULAR_BORDER = 18
COMPACT_BORDER = 12


def is_compact_width(width: int) -> bool:
    """Return whether the Care window should use its compact desktop composition."""
    return width < COMPACT_WIDTH


def is_high_contrast_theme(theme_name: str | None) -> bool:
    """Recognize common GTK high-contrast theme names without toolkit imports."""
    normalized = (theme_name or "").lower()
    normalized = normalized.replace("-", "").replace("_", "").replace(" ", "")
    return "highcontrast" in normalized
