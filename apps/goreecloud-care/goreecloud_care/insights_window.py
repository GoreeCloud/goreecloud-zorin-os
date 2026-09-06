from __future__ import annotations

import sys
import threading

import gi

gi.require_version("Atk", "1.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Atk, Gio, GLib, Gtk  # noqa: E402

from .insights import InsightsSnapshot, build_insights, render_insights_text

APP_ID = "com.goreecloud.care.dev.insights"
MIN_WINDOW_WIDTH = 480
MIN_WINDOW_HEIGHT = 420


class InsightsWindow(Gtk.ApplicationWindow):
    """Read-only local maintenance-intelligence review surface."""

    def __init__(self, app: Gtk.Application) -> None:
        super().__init__(application=app, title="GoreeCloud Care — Maintenance Insights")
        self.set_default_size(780, 620)
        self.set_size_request(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.props.title = "Maintenance Insights"
        header.props.subtitle = "Development • read-only local review"
        self.set_titlebar(header)

        refresh = Gtk.Button(label="Refresh")
        refresh.set_can_focus(True)
        refresh.set_tooltip_text("Refresh read-only maintenance insights")
        refresh.get_accessible().set_description(
            "Re-scan local maintenance insights. Refreshing does not delete files or perform maintenance."
        )
        refresh.connect("clicked", self.on_refresh)
        header.pack_end(refresh)

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        root.set_border_width(16)
        self.add(root)

        intro = Gtk.Label(xalign=0)
        intro.set_line_wrap(True)
        intro.set_markup(
            "<span size='large' weight='bold'>Review storage pressure before deciding what to do</span>\n"
            "This Development view is read-only. It highlights stale application-cache groups, "
            "large files in standard user folders, and older Downloads. Nothing is selected or deleted automatically."
        )
        root.pack_start(intro, False, False, 0)

        privacy = Gtk.Label(xalign=0)
        privacy.set_line_wrap(True)
        privacy.set_text(
            "Local only • no telemetry • no network • no administrator authentication. "
            "Paths are shown only inside this local review view; default Care reports remain path-redacted."
        )
        root.pack_start(privacy, False, False, 0)

        self.status_frame = Gtk.Frame()
        self.status_frame.set_shadow_type(Gtk.ShadowType.NONE)
        self.status_accessible = self.status_frame.get_accessible()
        self.status_accessible.set_role(Atk.Role.STATUSBAR)
        self.status_accessible.set_description(
            "GoreeCloud Care Maintenance Insights read-only scan status."
        )
        root.pack_start(self.status_frame, False, False, 0)

        self.status = Gtk.Label(xalign=0)
        self.status.set_line_wrap(True)
        self.status_frame.add(self.status)
        self._set_status("Ready to analyze local maintenance insights.")

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)
        root.pack_start(scrolled, True, True, 0)

        self.text = Gtk.TextView()
        self.text.set_editable(False)
        self.text.set_cursor_visible(False)
        self.text.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.text.set_left_margin(10)
        self.text.set_right_margin(10)
        self.text.set_top_margin(10)
        self.text.set_bottom_margin(10)
        self.text.get_accessible().set_name("Maintenance Insights results")
        self.text.get_accessible().set_description(
            "Read-only maintenance findings. Review manually; nothing in this view is selected for deletion."
        )
        scrolled.add(self.text)

        GLib.idle_add(lambda: (self.on_refresh(None), False)[1])

    def _set_status(self, text: str) -> None:
        self.status.set_text(text)
        self.status_accessible.set_name(text)
        try:
            self.status_accessible.emit("visible-data-changed")
        except (TypeError, RuntimeError):
            pass

    def _run_thread(self, fn, done) -> None:
        def worker() -> None:
            try:
                value = fn()
                GLib.idle_add(done, value, None)
            except Exception as exc:
                GLib.idle_add(done, None, exc)

        threading.Thread(target=worker, daemon=True).start()

    def on_refresh(self, _button) -> None:
        self._set_status("Analyzing standard user folders and stale application cache without deleting files…")
        self._run_thread(build_insights, self._refresh_done)

    def _refresh_done(self, snapshot: InsightsSnapshot | None, error: Exception | None) -> bool:
        if error is not None or snapshot is None:
            message = f"Maintenance Insights scan failed: {error}"
            self._set_status(message)
            self.text.get_buffer().set_text(
                message + "\nNo maintenance action was performed and no files were changed."
            )
            return False

        self.text.get_buffer().set_text(render_insights_text(snapshot))
        total_findings = len(snapshot.cache_groups) + len(snapshot.large_files) + len(snapshot.stale_downloads)
        suffix = " Results are partial because the bounded discovery limit was reached." if snapshot.truncated else ""
        self._set_status(
            f"Insights ready. {total_findings} review item/group(s) shown; "
            f"{snapshot.scan_error_count} scan error(s). No files were changed.{suffix}"
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
    return app.run([sys.argv[0]])
