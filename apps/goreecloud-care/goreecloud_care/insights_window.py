from __future__ import annotations

import sys
import threading

import gi

gi.require_version("Atk", "1.0")
gi.require_version("Gtk", "3.0")
gi.require_version("Pango", "1.0")
from gi.repository import Atk, Gio, GLib, Gtk, Pango  # noqa: E402

from .insights import InsightsSnapshot, build_insights, render_insights_text
from .ui_contract import (
    COMPACT_BORDER,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    REGULAR_BORDER,
    is_compact_width,
)

APP_ID = "com.goreecloud.care.insights"
RESULTS_MIN_HEIGHT = 320
REGULAR_SPACING = 12
COMPACT_SPACING = 8
RESULTS_MARGIN = 12


class InsightsWindow(Gtk.ApplicationWindow):
    """Read-only GoreeCloud Care maintenance review surface."""

    def __init__(self, app: Gtk.Application) -> None:
        super().__init__(application=app, title="GoreeCloud Care — Maintenance Insights")
        self.set_default_size(860, 660)
        self.set_size_request(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self._compact_layout: bool | None = None

        self.header_subtitle = "Read-only local review"
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = "Maintenance Insights"
        self.header.props.subtitle = self.header_subtitle
        self.header.get_style_context().add_class("chrome-plane")
        self.set_titlebar(self.header)

        self.refresh = Gtk.Button()
        self.refresh.get_style_context().add_class("command-capsule")
        self.refresh_icon = Gtk.Image.new_from_icon_name(
            "view-refresh-symbolic", Gtk.IconSize.BUTTON
        )
        self.refresh.add(self.refresh_icon)
        self.refresh.set_can_focus(True)
        self.refresh.set_tooltip_text("Refresh read-only maintenance insights")
        self.refresh.get_accessible().set_name("Refresh")
        self.refresh.get_accessible().set_description(
            "Re-scan local maintenance insights. Refreshing does not delete files or perform maintenance."
        )
        self.refresh.connect("clicked", self.on_refresh)
        self.header.pack_end(self.refresh)

        self.page_scroll = Gtk.ScrolledWindow()
        self.page_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.page_scroll.set_hexpand(True)
        self.page_scroll.set_vexpand(True)
        self.add(self.page_scroll)

        self.root = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=REGULAR_SPACING
        )
        self.root.set_border_width(REGULAR_BORDER)
        self.page_scroll.add(self.root)

        self.summary = Gtk.Frame()
        self.summary.set_shadow_type(Gtk.ShadowType.NONE)
        self.summary.get_style_context().add_class("hero-surface")
        summary_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.summary.add(summary_box)

        eyebrow = Gtk.Label(xalign=0)
        eyebrow.set_text("READ-ONLY REVIEW • LOCAL ONLY")
        eyebrow.get_style_context().add_class("eyebrow")
        summary_box.pack_start(eyebrow, False, False, 0)

        self.intro_regular_markup = (
            "<span size='x-large' weight='bold'>See storage pressure before deciding what to do.</span>\n"
            "Maintenance Insights highlights stale application-cache groups, large files in standard user folders, "
            "and older Downloads. Nothing is selected or deleted automatically."
        )
        self.intro_compact_markup = (
            "<span weight='bold'>Review storage safely</span>\n"
            "Stale cache, large files, and older Downloads are shown read-only."
        )
        self.intro = Gtk.Label(xalign=0, yalign=0)
        self.intro.set_line_wrap(True)
        self.intro.set_use_markup(True)
        self.intro.set_markup(self.intro_regular_markup)
        summary_box.pack_start(self.intro, False, False, 0)
        self.root.pack_start(self.summary, False, False, 0)

        self.status_frame = Gtk.Frame()
        self.status_frame.set_shadow_type(Gtk.ShadowType.NONE)
        self.status_frame.get_style_context().add_class("status-banner")
        self.status_frame.get_style_context().add_class("status-info")
        self.status_accessible = self.status_frame.get_accessible()
        self.status_accessible.set_role(Atk.Role.STATUSBAR)
        self.status_accessible.set_name("Ready. Refresh to review local maintenance insights.")
        self.status_accessible.set_description(
            "GoreeCloud Care Maintenance Insights read-only status."
        )
        status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=11)
        self.status_frame.add(status_box)
        self.status_icon = Gtk.Image.new_from_icon_name(
            "dialog-information-symbolic", Gtk.IconSize.BUTTON
        )
        status_box.pack_start(self.status_icon, False, False, 0)
        self.status_title = Gtk.Label(xalign=0)
        self.status_title.set_text("Ready")
        self.status_title.get_style_context().add_class("status-title")
        status_box.pack_start(self.status_title, False, False, 0)
        self.status = Gtk.Label(xalign=0)
        self.status.set_line_wrap(True)
        self.status.set_text("Refresh to review local maintenance insights.")
        status_box.pack_start(self.status, True, True, 0)
        self.root.pack_start(self.status_frame, False, False, 0)

        self.results_frame = Gtk.Frame()
        self.results_frame.set_shadow_type(Gtk.ShadowType.NONE)
        self.results_frame.get_style_context().add_class("findings-plane")
        findings_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.results_frame.add(findings_box)
        results_title = Gtk.Label(xalign=0)
        results_title.set_text("Findings")
        results_title.get_style_context().add_class("section-title")
        findings_box.pack_start(results_title, False, False, 0)
        results_desc = Gtk.Label(xalign=0)
        results_desc.set_line_wrap(True)
        results_desc.set_text(
            "Paths are shown only in this local review window. Standard-folder scanning is bounded and symlinks are not followed."
        )
        results_desc.get_style_context().add_class("muted")
        findings_box.pack_start(results_desc, False, False, 0)

        self.results_scroll = Gtk.ScrolledWindow()
        self.results_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.results_scroll.set_min_content_height(RESULTS_MIN_HEIGHT)
        self.results_scroll.set_hexpand(True)
        self.results_scroll.set_vexpand(True)
        findings_box.pack_start(self.results_scroll, True, True, 0)

        self.results = Gtk.Label(xalign=0, yalign=0)
        self.results.set_selectable(True)
        self.results.set_line_wrap(True)
        self.results.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        self.results.set_margin_start(RESULTS_MARGIN)
        self.results.set_margin_end(RESULTS_MARGIN)
        self.results.set_margin_top(RESULTS_MARGIN)
        self.results.set_margin_bottom(RESULTS_MARGIN)
        self.results.get_accessible().set_name("Maintenance insight findings")
        self.results.get_accessible().set_description(
            "Read-only local paths and storage findings. Nothing here is selected or deleted automatically."
        )
        self.results_scroll.add(self.results)
        self.root.pack_start(self.results_frame, True, True, 0)

        self.connect("size-allocate", self._on_size_allocate)
        self._apply_layout(860)
        GLib.idle_add(lambda: (self.on_refresh(None), False)[1])

    def _on_size_allocate(self, _widget, allocation) -> None:
        self._apply_layout(allocation.width)

    def _apply_layout(self, width: int) -> None:
        compact = is_compact_width(width)
        if compact == self._compact_layout:
            return
        self._compact_layout = compact
        self.header.set_title("Insights" if compact else "Maintenance Insights")
        self.header.set_subtitle(None if compact else self.header_subtitle)
        self.root.set_border_width(COMPACT_BORDER if compact else REGULAR_BORDER)
        self.root.set_spacing(COMPACT_SPACING if compact else REGULAR_SPACING)
        self.intro.set_markup(
            self.intro_compact_markup if compact else self.intro_regular_markup
        )

    def set_status(self, title: str, message: str, state: str = "info") -> None:
        context = self.status_frame.get_style_context()
        for style in ("status-info", "status-attention", "status-success", "status-error"):
            context.remove_class(style)
        context.add_class(f"status-{state}")
        icon = {
            "info": "dialog-information-symbolic",
            "attention": "process-stop-symbolic",
            "success": "emblem-ok-symbolic",
            "error": "dialog-error-symbolic",
        }.get(state, "dialog-information-symbolic")
        self.status_icon.set_from_icon_name(icon, Gtk.IconSize.BUTTON)
        self.status_title.set_text(title)
        self.status.set_text(message)
        self.status_accessible.set_name(f"{title}. {message}".strip())
        self.status_accessible.notify("accessible-name")
        self.status_accessible.emit("visible-data-changed")

    def on_refresh(self, _button) -> None:
        self.refresh.set_sensitive(False)
        self.set_status("Refreshing", "Reviewing local maintenance insights…")

        def worker() -> None:
            snapshot = None
            error = None
            try:
                snapshot = build_insights()
            except Exception as exc:
                error = exc
            GLib.idle_add(self._refresh_done, snapshot, error)

        threading.Thread(target=worker, daemon=True).start()

    def _refresh_done(self, snapshot: InsightsSnapshot | None, error: Exception | None) -> bool:
        self.refresh.set_sensitive(True)
        if error or snapshot is None:
            message = f"Maintenance Insights refresh failed: {error or 'unknown error'}"
            self.results.set_text("No findings are shown because the refresh did not complete.")
            self.set_status("Refresh failed", message, "error")
            return False

        text = render_insights_text(snapshot)
        escaped = GLib.markup_escape_text(text)
        self.results.set_markup(f"<span insert_hyphens='false'>{escaped}</span>")
        count = len(snapshot.large_files) + len(snapshot.stale_cache_groups) + len(snapshot.old_downloads)
        if snapshot.partial:
            self.set_status(
                "Partial findings",
                f"Review refreshed with {count} finding(s); scan limits were reached, so results are explicitly partial.",
                "attention",
            )
        else:
            self.set_status(
                "Review refreshed",
                f"Review refreshed with {count} finding(s). Nothing was selected or deleted.",
                "success",
            )
        return False


class InsightsApplication(Gtk.Application):
    def __init__(self) -> None:
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self) -> None:
        window = self.props.active_window
        if not window:
            window = InsightsWindow(self)
        window.show_all()
        window.present()


def main() -> int:
    app = InsightsApplication()
    return app.run(sys.argv)


if __name__ == "__main__":
    raise SystemExit(main())
