from __future__ import annotations

import os
import sys
import time
from pathlib import Path

os.environ.setdefault("GDK_DPI_SCALE", "2")

# This file is intentionally runnable both from the repository root and directly
# from tests/. Python otherwise puts tests/ rather than the Care source root on
# sys.path when invoked as `python3 tests/runtime_ui_acceptance.py`.
SOURCE_ROOT = Path(__file__).resolve().parents[1]
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gio, Gtk  # noqa: E402

from goreecloud_care.app import CareWindow
from goreecloud_care.glaze_v12 import GLAZE_UI_VERSION
from goreecloud_care.glaze_v12_global import install_glaze_v12_global_style
from goreecloud_care.insights import CacheGroupInsight, FileInsight, InsightsSnapshot
import goreecloud_care.insights_window as insights_window


def drain_events(limit: int = 500) -> None:
    count = 0
    while Gtk.events_pending() and count < limit:
        Gtk.main_iteration_do(False)
        count += 1


def make_app() -> Gtk.Application:
    # No application ID means the headless CI probe does not require a session
    # D-Bus name. NON_UNIQUE keeps the test isolated from desktop registration.
    app = Gtk.Application(
        application_id=None,
        flags=Gio.ApplicationFlags.NON_UNIQUE,
    )
    app.register(None)
    return app


def test_core_status_accessible_mutation(app: Gtk.Application) -> None:
    window = CareWindow(app)
    window.set_status("Synthetic completion state.", "success", "Completed")
    name = window.status_accessible.get_name()
    assert name == "Completed. Synthetic completion state.", name
    window.destroy()


def test_insights_focus_resize_and_rendering(app: Gtk.Application) -> None:
    snapshot = InsightsSnapshot(
        cache_groups=(CacheGroupInsight("example-cache", 1024, 2),),
        large_files=(
            FileInsight(
                "~/Pictures/a-very-long-path-component-without-synthetic-hyphenation/example-video.mp4",
                512 * 1024 * 1024,
                35,
            ),
        ),
        stale_downloads=(),
        scan_error_count=0,
        visited_entries=42,
        truncated=False,
    )
    insights_window.build_insights = lambda: snapshot

    window = insights_window.InsightsWindow(app)
    window.show_all()
    drain_events()

    window._set_results_text(insights_window.render_insights_text(snapshot))
    assert window.results.get_selectable()
    assert window.results.get_can_focus()
    assert "example-video.mp4" in window.results.get_text()
    assert "synthetic-hyphenation" in window.results.get_text()

    # At GDK_DPI_SCALE=2 the effective layout width is half the allocated width.
    # 480 therefore exercises compact mode while 1800 crosses back into regular
    # mode above the 820 effective-width breakpoint.
    window._apply_layout(480)
    assert window.header.get_title() == "Insights"
    assert window.header.get_subtitle() is None
    window._apply_layout(1800)
    assert window.header.get_title() == "Maintenance Insights"
    assert window.header.get_subtitle() == window.header_subtitle

    window.refresh.grab_focus()
    drain_events()
    assert window.get_focus() is window.refresh
    moved_forward = window.child_focus(Gtk.DirectionType.TAB_FORWARD)
    drain_events()
    assert moved_forward
    assert window.get_focus() is window.results, type(window.get_focus()).__name__

    moved_backward = window.child_focus(Gtk.DirectionType.TAB_BACKWARD)
    drain_events()
    assert moved_backward
    assert window.get_focus() is window.refresh, type(window.get_focus()).__name__

    start = time.monotonic()
    for _ in range(20):
        window.resize(480, 620)
        drain_events()
        window.resize(1800, 720)
        drain_events()
    elapsed = time.monotonic() - start
    assert elapsed < 5.0, f"synthetic continuous resize took {elapsed:.3f}s"

    window.destroy()


def main() -> int:
    ok, _argv = Gtk.init_check(None)
    if not ok:
        raise SystemExit("GTK could not initialize; run this probe under Xvfb or a desktop session")

    glaze = install_glaze_v12_global_style()
    assert GLAZE_UI_VERSION == "1.2.0"
    assert glaze.provider_attached, "GLAZE UI V1.2 provider was not attached"

    app = make_app()
    test_core_status_accessible_mutation(app)
    test_insights_focus_resize_and_rendering(app)
    print("Headless GTK runtime acceptance probe: passed (GLAZE UI V1.2 native fallback)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
