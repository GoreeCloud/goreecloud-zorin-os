from __future__ import annotations

import subprocess
import sys
import threading
from pathlib import Path

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gio, GLib, Gtk  # noqa: E402

from .core import CareEngine, CategoryScan, human_bytes, read_disk_stats, read_memory_stats

APP_ID = "com.goreecloud.care.dev"
HELPER = "/usr/lib/goreecloud-care/goreecloud-care-helper"

CSS = b"""
window { background: #101a20; color: #f3f7f8; }
headerbar { background: #18252b; color: #f3f7f8; }
.card { background: #18252b; border-radius: 14px; padding: 14px; }
.title { font-weight: 700; font-size: 18px; }
.muted { color: #9fb2bc; }
.warning { color: #f1c75b; }
button.suggested-action { background: #1c8a8d; color: #ffffff; }
"""


class CareWindow(Gtk.ApplicationWindow):
    def __init__(self, app: Gtk.Application) -> None:
        super().__init__(application=app, title="GoreeCloud Care — Development")
        self.set_default_size(900, 680)
        self.set_border_width(0)
        self.engine = CareEngine()
        self.scans: dict[str, CategoryScan] = {}
        self.rows: dict[str, tuple[Gtk.CheckButton | None, Gtk.Label]] = {}

        provider = Gtk.CssProvider()
        provider.load_from_data(CSS)
        Gtk.StyleContext.add_provider_for_screen(
            self.get_screen(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.props.title = "GoreeCloud Care"
        header.props.subtitle = "Development • local maintenance"
        self.set_titlebar(header)

        scan_btn = Gtk.Button(label="Scan")
        scan_btn.set_tooltip_text("Scan safe maintenance categories without deleting anything")
        scan_btn.connect("clicked", self.on_scan)
        header.pack_end(scan_btn)

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        root.set_border_width(18)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(root)
        self.add(scroll)

        intro = Gtk.Label()
        intro.set_xalign(0)
        intro.set_line_wrap(True)
        intro.set_markup(
            "<span size='large' weight='bold'>Safe cleanup with a preview first</span>\n"
            "GoreeCloud Care scans local files only. It does not send telemetry. "
            "Routine cache and temporary-file cleanup runs as your user account."
        )
        root.pack_start(intro, False, False, 0)

        self.system_label = Gtk.Label(xalign=0)
        self.system_label.get_style_context().add_class("muted")
        root.pack_start(self.system_label, False, False, 0)

        for key, title, desc, selectable in (
            ("cache", "Application cache", "Cache files older than 7 days in ~/.cache, excluding thumbnails.", True),
            ("thumbnails", "Thumbnail cache", "Recreatable image/video thumbnails stored for your account.", True),
            ("temp", "Temporary files", "Your own files in /tmp older than 7 days; symlinks are never followed.", True),
            ("trash", "Trash", "Items currently in your desktop Trash. Emptying is permanent and separately confirmed.", False),
            ("apt", "APT package cache", "Downloaded .deb package archives. Cleaning requires administrator authentication.", False),
        ):
            root.pack_start(self._category_card(key, title, desc, selectable), False, False, 0)

        memory = self._card()
        memory_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        memory.add(memory_box)
        label = Gtk.Label(xalign=0)
        label.set_markup("<span weight='bold' size='large'>Memory Refresh</span>")
        memory_box.pack_start(label, False, False, 0)
        explain = Gtk.Label(xalign=0)
        explain.set_line_wrap(True)
        explain.set_text(
            "Linux intentionally uses spare RAM for file caches. Reclaiming those caches can make the "
            "available-memory number rise temporarily, but it is not a lasting speed boost and may slow "
            "the next file/app loads while caches rebuild."
        )
        explain.get_style_context().add_class("muted")
        memory_box.pack_start(explain, False, False, 0)
        memory_btn = Gtk.Button(label="Reclaim file cache…")
        memory_btn.set_halign(Gtk.Align.START)
        memory_btn.connect("clicked", self.on_reclaim_memory)
        memory_box.pack_start(memory_btn, False, False, 0)
        root.pack_start(memory, False, False, 0)

        controls = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        clean = Gtk.Button(label="Clean selected")
        clean.get_style_context().add_class("suggested-action")
        clean.connect("clicked", self.on_clean_selected)
        controls.pack_start(clean, False, False, 0)

        trash = Gtk.Button(label="Empty Trash…")
        trash.connect("clicked", self.on_empty_trash)
        controls.pack_start(trash, False, False, 0)

        apt = Gtk.Button(label="Clean APT cache…")
        apt.connect("clicked", self.on_apt_clean)
        controls.pack_start(apt, False, False, 0)
        root.pack_start(controls, False, False, 0)

        self.status = Gtk.Label(xalign=0)
        self.status.set_line_wrap(True)
        self.status.set_text("Ready. Scan to preview reclaimable space.")
        root.pack_start(self.status, False, False, 0)
        self.refresh_system_status()
        GLib.idle_add(lambda: (self.on_scan(None), False)[1])

    def _card(self) -> Gtk.Frame:
        frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.NONE)
        frame.get_style_context().add_class("card")
        return frame

    def _category_card(self, key: str, title: str, desc: str, selectable: bool) -> Gtk.Widget:
        frame = self._card()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        frame.add(box)
        selector: Gtk.CheckButton | None = None
        if selectable:
            selector = Gtk.CheckButton()
            selector.set_active(True)
            selector.set_tooltip_text(f"Include {title.lower()} in Clean selected")
            box.pack_start(selector, False, False, 0)
        text = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        heading = Gtk.Label(xalign=0)
        heading.set_markup(f"<span weight='bold' size='large'>{GLib.markup_escape_text(title)}</span>")
        text.pack_start(heading, False, False, 0)
        description = Gtk.Label(label=desc, xalign=0)
        description.set_line_wrap(True)
        description.get_style_context().add_class("muted")
        text.pack_start(description, False, False, 0)
        box.pack_start(text, True, True, 0)
        amount = Gtk.Label(label="Not scanned", xalign=1)
        box.pack_end(amount, False, False, 0)
        self.rows[key] = (selector, amount)
        return frame

    def refresh_system_status(self) -> None:
        mem = read_memory_stats()
        disk = read_disk_stats()
        self.system_label.set_text(
            f"Disk: {human_bytes(disk.free)} free of {human_bytes(disk.total)}  •  "
            f"Memory: {human_bytes(mem.available)} available of {human_bytes(mem.total)}  •  "
            f"File cache: about {human_bytes(mem.cached)}"
        )

    def set_status(self, text: str) -> None:
        self.status.set_text(text)

    def run_thread(self, fn, done) -> None:
        def worker() -> None:
            try:
                value = fn()
                GLib.idle_add(done, value, None)
            except Exception as exc:  # UI boundary: surface failure, do not claim success.
                GLib.idle_add(done, None, exc)
        threading.Thread(target=worker, daemon=True).start()

    def on_scan(self, _button) -> None:
        self.set_status("Scanning without deleting files…")
        self.run_thread(self.engine.scan_all, self._scan_done)

    def _scan_done(self, scans, error) -> bool:
        if error:
            self.set_status(f"Scan failed: {error}")
            return False
        self.scans = scans
        total = 0
        for key, scan in scans.items():
            total += scan.bytes
            self.rows[key][1].set_text(f"{human_bytes(scan.bytes)} • {scan.count} items")
        self.refresh_system_status()
        self.set_status(f"Scan complete. Up to {human_bytes(total)} is visible across all maintenance categories.")
        return False

    def _confirm(self, primary: str, secondary: str, destructive: bool = False) -> bool:
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.WARNING if destructive else Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.CANCEL,
            text=primary,
        )
        dialog.format_secondary_text(secondary)
        label = "Delete permanently" if destructive else "Continue"
        response_id = Gtk.ResponseType.ACCEPT
        dialog.add_button(label, response_id)
        response = dialog.run()
        dialog.destroy()
        return response == response_id

    def on_clean_selected(self, _button) -> None:
        selected: list[str] = []
        for key in ("cache", "thumbnails", "temp"):
            selector = self.rows[key][0]
            if selector is not None and selector.get_active():
                selected.append(key)
        if not selected:
            self.set_status("Select at least one cache or temporary-file category.")
            return
        if any(key not in self.scans for key in selected):
            self.set_status("Scan first so cleanup has a current preview.")
            return
        total = sum(self.scans[key].bytes for key in selected)
        names = ", ".join(self.scans[key].label for key in selected)
        if not self._confirm(
            "Clean the selected categories?",
            f"About {human_bytes(total)} is currently eligible from: {names}. Files may be recreated by applications.",
        ):
            return
        self.set_status("Cleaning selected user-owned cache and temporary files…")

        def action():
            results = [self.engine.cleanup(self.scans[key]) for key in selected]
            return results
        self.run_thread(action, self._cleanup_done)

    def _cleanup_done(self, results, error) -> bool:
        if error:
            self.set_status(f"Cleanup failed: {error}")
            return False
        reclaimed = sum(r.reclaimed_bytes for r in results)
        failures = sum(len(r.errors) for r in results)
        msg = f"Cleanup finished: approximately {human_bytes(reclaimed)} removed."
        if failures:
            msg += f" {failures} item(s) could not be removed; no success is claimed for those items."
        self.set_status(msg)
        self.refresh_system_status()
        self.on_scan(None)
        return False

    def on_empty_trash(self, _button) -> None:
        scan = self.scans.get("trash")
        amount = human_bytes(scan.bytes) if scan else "the current contents"
        if not self._confirm(
            "Permanently empty Trash?",
            f"This will permanently delete {amount} from your Trash. This action cannot be undone by GoreeCloud Care.",
            destructive=True,
        ):
            return
        self.set_status("Permanently emptying Trash…")
        self.run_thread(self.engine.empty_trash, self._trash_done)

    def _trash_done(self, result, error) -> bool:
        if error:
            self.set_status(f"Trash cleanup failed: {error}")
            return False
        msg = f"Trash cleanup finished: approximately {human_bytes(result.reclaimed_bytes)} removed."
        if result.errors:
            msg += f" {len(result.errors)} item(s) were not removed."
        self.set_status(msg)
        self.on_scan(None)
        return False

    def _run_privileged(self, action: str):
        return subprocess.run(
            ["/usr/bin/pkexec", HELPER, action],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=150,
            check=False,
        )

    def on_apt_clean(self, _button) -> None:
        scan = self.scans.get("apt")
        amount = human_bytes(scan.bytes) if scan else "the downloaded package cache"
        if not self._confirm(
            "Clean the APT package cache?",
            f"This removes {amount} of downloaded .deb archives when present. Administrator authentication is required.",
        ):
            return
        self.set_status("Requesting administrator authorization for APT cache cleanup…")
        self.run_thread(lambda: self._run_privileged("apt-clean"), self._privileged_done)

    def on_reclaim_memory(self, _button) -> None:
        if not self._confirm(
            "Reclaim Linux file caches now?",
            "Linux normally manages these caches automatically. This can temporarily increase available RAM, "
            "but is not a lasting speed boost and may make later file/app loads slower while caches rebuild. "
            "Administrator authentication is required.",
        ):
            return
        self.set_status("Requesting administrator authorization for memory-cache reclaim…")
        self.run_thread(lambda: self._run_privileged("reclaim-memory"), self._privileged_done)

    def _privileged_done(self, result, error) -> bool:
        if error:
            self.set_status(f"Privileged action failed: {error}")
            return False
        if result.returncode != 0:
            detail = (result.stderr or "Authorization was cancelled or the action failed.").strip()
            self.set_status(f"Privileged action did not complete: {detail}")
            return False
        self.set_status("Privileged maintenance action completed successfully.")
        self.refresh_system_status()
        self.on_scan(None)
        return False


class CareApplication(Gtk.Application):
    def __init__(self) -> None:
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self) -> None:
        window = self.props.active_window
        if not window:
            window = CareWindow(self)
        window.show_all()
        window.present()


def main() -> int:
    app = CareApplication()
    return app.run(sys.argv)


if __name__ == "__main__":
    raise SystemExit(main())
