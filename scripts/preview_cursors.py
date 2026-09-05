#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "desktop-assets.json"

CURSOR_MATRIX = (
    ("Default pointer", "left_ptr"),
    ("Link hand", "pointer"),
    ("Text I-beam", "xterm"),
    ("Crosshair", "crosshair"),
    ("Move", "move"),
    ("Horizontal resize", "size_hor"),
    ("Vertical resize", "size_ver"),
    ("NW / SE resize", "nwse-resize"),
    ("NE / SW resize", "nesw-resize"),
    ("Wait · animated", "wait"),
    ("Progress · animated", "progress"),
    ("Copy action", "copy"),
    ("Forbidden", "not-allowed"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Preview the active GoreeCloud cursor family on Light and Dark "
            "surfaces and exercise cursor hotspots."
        )
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify active runtime identity and cursor files without opening GTK",
    )
    return parser.parse_args()


def read_config() -> dict[str, object]:
    return json.loads(CONFIG.read_text(encoding="utf-8"))["cursor_theme"]


def active_cursor_theme() -> str:
    result = subprocess.run(
        ["gsettings", "get", "org.gnome.desktop.interface", "cursor-theme"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip().strip("'")


def find_runtime_root(runtime_id: str) -> Path | None:
    candidates = (
        Path.home() / ".local" / "share" / "icons" / runtime_id,
        Path.home() / ".icons" / runtime_id,
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return None


def verify_runtime() -> tuple[str, str, Path]:
    cfg = read_config()
    runtime_id = str(cfg["runtime_id"])
    active = active_cursor_theme()
    root = find_runtime_root(runtime_id)
    if active != runtime_id:
        raise SystemExit(
            "Cursor acceptance requires the revisioned GoreeCloud runtime "
            f"identity. Expected {runtime_id!r}, active theme is {active or '<unknown>'!r}."
        )
    if root is None:
        raise SystemExit(
            f"Active cursor runtime {runtime_id!r} is not discoverable under "
            "~/.local/share/icons or ~/.icons."
        )
    cursor_dir = root / "cursors"
    missing = [name for _label, name in CURSOR_MATRIX if not (cursor_dir / name).is_file()]
    if missing:
        raise SystemExit(
            "Cursor acceptance matrix is missing installed aliases: "
            + ", ".join(missing)
        )
    return runtime_id, active, root


def main() -> int:
    args = parse_args()
    runtime_id, active, runtime_root = verify_runtime()
    if args.check:
        print(f"Expected runtime: {runtime_id}")
        print(f"Active runtime:   {active}")
        print(f"Resolved theme:   {runtime_root}")
        print(f"Acceptance aliases: {len(CURSOR_MATRIX)}/{len(CURSOR_MATRIX)} present")
        return 0

    try:
        import gi

        gi.require_version("Gtk", "3.0")
        from gi.repository import Gdk, Gtk
    except (ImportError, ValueError) as exc:
        raise SystemExit(
            "GTK 3 Python bindings are required for cursor preview "
            "(python3-gi and gir1.2-gtk-3.0 on Zorin OS)."
        ) from exc

    class CursorTile(Gtk.EventBox):
        TARGET_X = 132.0
        TARGET_Y = 72.0

        def __init__(self, label: str, cursor_name: str, scene: str, status: Gtk.Label):
            super().__init__()
            self.cursor_name = cursor_name
            self.scene = scene
            self.status = status
            self.set_size_request(158, 98)
            self.set_visible_window(True)
            self.add_events(
                Gdk.EventMask.ENTER_NOTIFY_MASK
                | Gdk.EventMask.LEAVE_NOTIFY_MASK
                | Gdk.EventMask.BUTTON_PRESS_MASK
            )
            self.get_style_context().add_class(
                "cursor-tile-light" if scene == "Light" else "cursor-tile-dark"
            )

            fixed = Gtk.Fixed()
            fixed.set_size_request(158, 98)
            title = Gtk.Label(label=label)
            title.set_xalign(0.0)
            title.get_style_context().add_class("cursor-title")
            alias = Gtk.Label(label=cursor_name)
            alias.set_xalign(0.0)
            alias.get_style_context().add_class("cursor-alias")
            target = Gtk.Label(label="⊕")
            target.get_style_context().add_class("hotspot-target")
            fixed.put(title, 12, 12)
            fixed.put(alias, 12, 38)
            fixed.put(target, 124, 60)
            self.add(fixed)
            self.set_tooltip_text(
                f"{label} · {cursor_name}. Hover to preview; click the ⊕ target to assess hotspot alignment."
            )

            self.connect("enter-notify-event", self._on_enter)
            self.connect("leave-notify-event", self._on_leave)
            self.connect("button-press-event", self._on_click)

        def _cursor(self):
            display = self.get_display()
            return Gdk.Cursor.new_from_name(display, self.cursor_name)

        def _on_enter(self, _widget, _event):
            window = self.get_window()
            cursor = self._cursor()
            if window is not None and cursor is not None:
                window.set_cursor(cursor)
                self.status.set_text(
                    f"{self.scene}: {self.cursor_name} — hover active. Click the ⊕ target to check hotspot alignment."
                )
            elif cursor is None:
                self.status.set_text(
                    f"{self.scene}: {self.cursor_name} could not be resolved by GDK."
                )
            return False

        def _on_leave(self, _widget, _event):
            window = self.get_window()
            if window is not None:
                window.set_cursor(None)
            return False

        def _on_click(self, _widget, event):
            distance = math.hypot(event.x - self.TARGET_X, event.y - self.TARGET_Y)
            self.status.set_text(
                f"{self.scene}: {self.cursor_name} hotspot click offset ≈ {distance:.1f}px from target center."
            )
            return False

    class AcceptanceWindow(Gtk.Window):
        def __init__(self):
            super().__init__(title="GoreeCloud Cursor Acceptance")
            self.set_default_size(1120, 735)
            self.set_border_width(0)
            self.connect("destroy", Gtk.main_quit)
            self.get_style_context().add_class("cursor-acceptance-window")

            outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            self.add(outer)

            header = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            header.set_margin_start(24)
            header.set_margin_end(24)
            header.set_margin_top(20)
            header.set_margin_bottom(16)
            heading = Gtk.Label(label="Cursor acceptance · revision 2")
            heading.set_xalign(0.0)
            heading.get_style_context().add_class("acceptance-heading")
            intro = Gtk.Label(
                label=(
                    f"Active runtime: {runtime_id}. Move the pointer over matching Light and Dark tiles. "
                    "Wait and Progress should animate. Click each ⊕ target to assess hotspot placement."
                )
            )
            intro.set_xalign(0.0)
            intro.set_line_wrap(True)
            intro.get_style_context().add_class("acceptance-intro")
            header.pack_start(heading, False, False, 0)
            header.pack_start(intro, False, False, 0)
            outer.pack_start(header, False, False, 0)

            scenes = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=14)
            scenes.set_margin_start(18)
            scenes.set_margin_end(18)
            scenes.set_margin_bottom(12)
            outer.pack_start(scenes, True, True, 0)

            self.status = Gtk.Label(
                label="Default pointer is accepted. Review the remaining families on both backgrounds."
            )
            self.status.set_xalign(0.0)
            self.status.set_line_wrap(True)
            self.status.get_style_context().add_class("acceptance-status")

            for scene in ("Light", "Dark"):
                panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
                panel.set_margin_top(10)
                panel.set_margin_bottom(10)
                panel.set_margin_start(10)
                panel.set_margin_end(10)
                panel.get_style_context().add_class(
                    "scene-light" if scene == "Light" else "scene-dark"
                )
                title = Gtk.Label(label=f"{scene} canvas")
                title.set_xalign(0.0)
                title.get_style_context().add_class("scene-title")
                panel.pack_start(title, False, False, 0)

                grid = Gtk.Grid(column_spacing=9, row_spacing=9)
                for index, (label, cursor_name) in enumerate(CURSOR_MATRIX):
                    tile = CursorTile(label, cursor_name, scene, self.status)
                    grid.attach(tile, index % 3, index // 3, 1, 1)
                panel.pack_start(grid, True, True, 0)
                scenes.pack_start(panel, True, True, 0)

            footer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            footer.set_margin_start(24)
            footer.set_margin_end(24)
            footer.set_margin_bottom(20)
            footer.pack_start(self.status, False, False, 0)
            note = Gtk.Label(
                label=(
                    "Acceptance remains state-specific: shape, animation, Light/Dark legibility, "
                    "and practical hotspot behavior should be judged separately."
                )
            )
            note.set_xalign(0.0)
            note.set_line_wrap(True)
            note.get_style_context().add_class("acceptance-note")
            footer.pack_start(note, False, False, 0)
            outer.pack_start(footer, False, False, 0)

    css = b"""
    .cursor-acceptance-window { background-color: #F4F8FA; color: #151C22; }
    .acceptance-heading { color: #151C22; font-size: 20px; font-weight: 700; }
    .acceptance-intro, .acceptance-note { color: #61717C; }
    .acceptance-status { color: #151C22; font-weight: 600; }
    .scene-light, .scene-dark { border-radius: 18px; padding: 12px; }
    .scene-light { background-color: #EEF4F7; border: 1px solid #D3DEE6; }
    .scene-dark { background-color: #0E1419; border: 1px solid #35444F; }
    .scene-light .scene-title { color: #151C22; font-weight: 700; }
    .scene-dark .scene-title { color: #F4F8FA; font-weight: 700; }
    .cursor-tile-light, .cursor-tile-dark { border-radius: 14px; padding: 0; }
    .cursor-tile-light { background-color: #FBFDFE; border: 1px solid #D3DEE6; }
    .cursor-tile-dark { background-color: #1B252D; border: 1px solid #35444F; }
    .cursor-tile-light:hover { background-color: #E8F1FF; border-color: #8FC4E8; }
    .cursor-tile-dark:hover { background-color: #1A3A50; border-color: #68AEE0; }
    .cursor-tile-light .cursor-title { color: #151C22; font-weight: 600; }
    .cursor-tile-light .cursor-alias { color: #61717C; font-size: 11px; }
    .cursor-tile-dark .cursor-title { color: #F4F8FA; font-weight: 600; }
    .cursor-tile-dark .cursor-alias { color: #B9C5CC; font-size: 11px; }
    .cursor-tile-light .hotspot-target { color: #2563EB; font-size: 17px; font-weight: 700; }
    .cursor-tile-dark .hotspot-target { color: #8FC4E8; font-size: 17px; font-weight: 700; }
    """
    provider = Gtk.CssProvider()
    provider.load_from_data(css)
    screen = Gdk.Screen.get_default()
    if screen is not None:
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    settings = Gtk.Settings.get_default()
    if settings is not None:
        try:
            settings.set_property("gtk-application-prefer-dark-theme", False)
        except TypeError:
            pass

    window = AcceptanceWindow()
    window.show_all()
    Gtk.main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
