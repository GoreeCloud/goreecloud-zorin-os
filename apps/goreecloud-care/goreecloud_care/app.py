from __future__ import annotations

import subprocess
import sys
import threading

import gi

gi.require_version("Atk", "1.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Atk, Gio, GLib, Gtk  # noqa: E402

from .core import CareEngine, CategoryScan, human_bytes, read_disk_stats, read_memory_stats
from .glaze_v14 import layout_environment
from .privilege import interpret_pkexec_result
from .ui_contract import (
    COMPACT_BORDER,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    REGULAR_BORDER,
    effective_layout_width,
    is_compact_width,
)

APP_ID = "com.goreecloud.care"
HELPER = "/usr/lib/goreecloud-care/goreecloud-care-helper"

STATUS_STYLES = ("status-info", "status-attention", "status-success", "status-error")
STATUS_ICONS = {
    "info": "dialog-information-symbolic",
    "attention": "process-stop-symbolic",
    "success": "emblem-ok-symbolic",
    "error": "dialog-error-symbolic",
}
STATUS_TITLES = {
    "info": "Status",
    "attention": "Action needs attention",
    "success": "Completed",
    "error": "Action failed",
}


class CareWindow(Gtk.ApplicationWindow):
    """Content-first GoreeCloud Care maintenance surface."""

    def __init__(self, app: Gtk.Application) -> None:
        super().__init__(application=app, title="GoreeCloud Care")
        self.set_default_size(1060, 720)
        self.set_size_request(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.set_border_width(0)
        self.engine = CareEngine()
        self.scans: dict[str, CategoryScan] = {}
        self.rows: dict[str, tuple[Gtk.CheckButton | None, Gtk.Label]] = {}
        self.category_layouts: dict[str, tuple[Gtk.Box, Gtk.Label]] = {}
        self._layout_environment: str | None = None

        # Chrome Plane: identity plus one transient scan command. The command is
        # the deliberate capsule; ordinary controls use the standard shape role.
        self.header_subtitle = "Local maintenance • Glaze UI V1.4"
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = "GoreeCloud Care"
        self.header.props.subtitle = self.header_subtitle
        self.header.get_style_context().add_class("chrome-plane")
        self.set_titlebar(self.header)

        self.scan_btn = Gtk.Button(label="Scan")
        self.scan_btn.get_style_context().add_class("command-capsule")
        self.scan_btn.set_can_focus(True)
        self.scan_btn.set_tooltip_text("Scan safe maintenance categories without deleting anything")
        self.scan_btn.get_accessible().set_description(
            "Preview maintenance categories. Scanning does not delete files."
        )
        self.scan_btn.connect("clicked", self.on_scan)
        self.header.pack_end(self.scan_btn)

        self.page_scroll = Gtk.ScrolledWindow()
        self.page_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.page_scroll.set_hexpand(True)
        self.page_scroll.set_vexpand(True)
        self.add(self.page_scroll)

        self.root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.root.set_border_width(REGULAR_BORDER)
        self.page_scroll.add(self.root)

        # A single signature surface establishes hierarchy without turning every
        # section into a floating card. It remains neutral and informational.
        self.hero = Gtk.Frame()
        self.hero.set_shadow_type(Gtk.ShadowType.NONE)
        self.hero.get_style_context().add_class("hero-surface")
        hero_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=7)
        self.hero.add(hero_box)

        eyebrow = Gtk.Label(xalign=0)
        eyebrow.set_text("LOCAL MAINTENANCE • PREVIEW FIRST")
        eyebrow.get_style_context().add_class("eyebrow")
        hero_box.pack_start(eyebrow, False, False, 0)

        hero_title = Gtk.Label(xalign=0)
        hero_title.set_line_wrap(True)
        hero_title.set_markup(
            "<span size='x-large' weight='bold'>Keep your system clear, safely.</span>"
        )
        hero_title.get_style_context().add_class("hero-mark")
        hero_box.pack_start(hero_title, False, False, 0)

        intro = Gtk.Label(xalign=0)
        intro.set_line_wrap(True)
        intro.set_text(
            "Care scans local files only and shows a preview before routine cleanup. "
            "No telemetry is sent, and routine cache or temporary-file cleanup runs as your user account."
        )
        intro.get_style_context().add_class("muted")
        hero_box.pack_start(intro, False, False, 0)

        self.system_label = Gtk.Label(xalign=0)
        self.system_label.set_line_wrap(True)
        self.system_label.get_style_context().add_class("metric-line")
        hero_box.pack_start(self.system_label, False, False, 0)

        self.root.pack_start(self.hero, False, False, 0)

        section_title = Gtk.Label(xalign=0)
        section_title.set_text("Maintenance")
        section_title.get_style_context().add_class("section-title")
        self.root.pack_start(section_title, False, False, 0)

        self.maintenance_collection = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=0
        )
        self.maintenance_collection.get_style_context().add_class("maintenance-collection")
        self.root.pack_start(self.maintenance_collection, False, False, 0)

        self._add_category(
            "cache",
            "Application cache",
            "Stale files in ~/.cache. Fresh files are preserved.",
            selectable=True,
        )
        self._add_category(
            "thumbnails",
            "Thumbnails",
            "Cached thumbnail previews older than the safety threshold.",
            selectable=True,
        )
        self._add_category(
            "temp",
            "Temporary files",
            "Owned stale files in the system temporary directory. Symlinks are never followed.",
            selectable=True,
        )
        self._add_category(
            "trash",
            "Trash",
            "Files currently in the desktop Trash. Emptying Trash is permanent.",
            selectable=False,
        )

        actions_title = Gtk.Label(xalign=0)
        actions_title.set_text("System actions")
        actions_title.get_style_context().add_class("section-title")
        self.root.pack_start(actions_title, False, False, 0)

        self.system_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.system_panel.get_style_context().add_class("system-panel")
        self.root.pack_start(self.system_panel, False, False, 0)

        self.clean = Gtk.Button(label="Clean selected")
        self.clean.get_style_context().add_class("resonant-action")
        self.clean.set_can_focus(True)
        self.clean.set_tooltip_text("Review and clean selected routine maintenance categories")
        self.clean.connect("clicked", self.on_clean)
        self._add_system_action(
            self.clean,
            "Clean selected",
            "Deletes only the currently selected routine categories after confirmation.",
        )

        self.trash = Gtk.Button(label="Empty Trash")
        self.trash.set_can_focus(True)
        self.trash.set_tooltip_text("Permanently empty your desktop Trash after confirmation")
        self.trash.connect("clicked", self.on_empty_trash)
        self._add_system_action(
            self.trash,
            "Empty Trash",
            "Permanent. Care asks for confirmation before deleting files in Trash.",
            destructive=True,
        )

        self.apt = Gtk.Button(label="Clean package cache")
        self.apt.set_can_focus(True)
        self.apt.set_tooltip_text("Authorize APT package-cache cleanup")
        self.apt.connect("clicked", self.on_apt_clean)
        self._add_system_action(
            self.apt,
            "Clean package cache",
            "Requires PolicyKit authorization and runs only the fixed apt-get clean helper action.",
            privileged=True,
        )

        self.memory_btn = Gtk.Button(label="Reclaim file cache")
        self.memory_btn.set_can_focus(True)
        self.memory_btn.set_tooltip_text("Authorize Linux file-cache reclaim")
        self.memory_btn.connect("clicked", self.on_reclaim_memory)
        self._add_system_action(
            self.memory_btn,
            "Reclaim file cache",
            "Requires PolicyKit authorization and asks Linux to drop reclaimable file cache.",
            privileged=True,
        )

        self.workspace = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.workspace.pack_start(self.maintenance_collection, True, True, 0)
        self.workspace.pack_start(self.system_panel, False, False, 0)

        self.status_frame = Gtk.Frame()
        self.status_frame.set_shadow_type(Gtk.ShadowType.NONE)
        self.status_frame.get_style_context().add_class("status-banner")
        self.status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.status_frame.add(self.status_box)
        self.status_icon = Gtk.Image.new_from_icon_name(
            STATUS_ICONS["info"], Gtk.IconSize.BUTTON
        )
        self.status_box.pack_start(self.status_icon, False, False, 0)
        self.status = Gtk.Label(xalign=0)
        self.status.set_line_wrap(True)
        self.status.set_selectable(True)
        self.status_box.pack_start(self.status, True, True, 0)
        self.status_accessible = self.status_frame.get_accessible()
        self.status_accessible.set_role(Atk.Role.STATUSBAR)
        self.root.pack_end(self.status_frame, False, False, 0)

        self.connect("size-allocate", self._on_size_allocate)
        self.connect("key-press-event", self._on_key_press)
        GLib.idle_add(self.on_scan, None)

    def _add_category(
        self,
        key: str,
        title: str,
        description: str,
        *,
        selectable: bool,
    ) -> None:
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row.get_style_context().add_class("maintenance-row")
        row.set_border_width(12)

        check: Gtk.CheckButton | None
        if selectable:
            check = Gtk.CheckButton()
            check.set_active(True)
            check.set_can_focus(True)
            check.set_tooltip_text(f"Include {title.lower()} in routine cleanup")
            check.get_accessible().set_name(f"Select {title}")
            row.pack_start(check, False, False, 0)
        else:
            check = None

        copy = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        title_label = Gtk.Label(xalign=0)
        title_label.set_markup(f"<b>{GLib.markup_escape_text(title)}</b>")
        copy.pack_start(title_label, False, False, 0)
        detail = Gtk.Label(xalign=0)
        detail.set_line_wrap(True)
        detail.set_text(description)
        detail.get_style_context().add_class("muted")
        copy.pack_start(detail, False, False, 0)
        row.pack_start(copy, True, True, 0)

        size = Gtk.Label(xalign=1)
        size.get_style_context().add_class("metric")
        row.pack_end(size, False, False, 0)

        self.maintenance_collection.pack_start(row, False, False, 0)
        self.rows[key] = (check, size)
        self.category_layouts[key] = (row, detail)

    def _add_system_action(
        self,
        button: Gtk.Button,
        title: str,
        description: str,
        *,
        destructive: bool = False,
        privileged: bool = False,
    ) -> None:
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row.get_style_context().add_class("system-action-row")
        row.set_border_width(12)
        if destructive:
            row.get_style_context().add_class("destructive-row")
        if privileged:
            row.get_style_context().add_class("privileged-row")

        copy = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        title_label = Gtk.Label(xalign=0)
        title_label.set_markup(f"<b>{GLib.markup_escape_text(title)}</b>")
        copy.pack_start(title_label, False, False, 0)
        detail = Gtk.Label(xalign=0)
        detail.set_line_wrap(True)
        detail.set_text(description)
        detail.get_style_context().add_class("muted")
        copy.pack_start(detail, False, False, 0)
        row.pack_start(copy, True, True, 0)

        row.pack_end(button, False, False, 0)
        self.system_panel.pack_start(row, False, False, 0)

    def _on_size_allocate(self, _widget, allocation) -> None:
        self._apply_layout(int(allocation.width))

    def _apply_layout(self, width: int) -> None:
        compact = is_compact_width(width)
        environment = layout_environment(
            int(effective_layout_width(width)), compact=compact
        )
        if environment == self._layout_environment:
            return
        self._layout_environment = environment

        self.header.set_title("Care" if compact else "GoreeCloud Care")
        self.header.set_subtitle(None if compact else self.header_subtitle)
        self.root.set_border_width(COMPACT_BORDER if compact else REGULAR_BORDER)

        if environment == "expanded":
            self.workspace.set_orientation(Gtk.Orientation.HORIZONTAL)
            self.workspace.set_spacing(20)
            self.maintenance_collection.set_hexpand(True)
            self.system_panel.set_hexpand(True)
        else:
            self.workspace.set_orientation(Gtk.Orientation.VERTICAL)
            self.workspace.set_spacing(12 if environment == "medium" else 8)
            self.maintenance_collection.set_hexpand(False)
            self.system_panel.set_hexpand(False)

        for row, detail in self.category_layouts.values():
            detail.set_max_width_chars(88 if environment == "expanded" else 64 if environment == "medium" else 42)
            row.set_border_width(14 if environment == "expanded" else 12 if environment == "medium" else 9)

    def _on_key_press(self, _widget, event) -> bool:
        if event.keyval == 0xFF1B:  # Escape
            self.scan_btn.grab_focus()
            return True
        return False

    def set_status(self, message: str, style: str, title: str | None = None) -> None:
        style = style if style in STATUS_ICONS else "info"
        semantic_title = title or STATUS_TITLES[style]
        self.status.set_text(message)
        self.status_icon.set_from_icon_name(STATUS_ICONS[style], Gtk.IconSize.BUTTON)
        context = self.status_frame.get_style_context()
        for class_name in STATUS_STYLES:
            context.remove_class(class_name)
        context.add_class(f"status-{style}")
        accessible_name = f"{semantic_title}. {message}"
        self.status_accessible.set_name(accessible_name)
        self.status_accessible.emit("visible-data-changed")

    def on_scan(self, _button) -> bool:
        self.set_status("Scanning without deleting files…", "info", "Scanning")
        self.scan_btn.set_sensitive(False)

        def work() -> None:
            try:
                scans = self.engine.scan()
                disk = read_disk_stats()
                memory = read_memory_stats()
            except Exception as exc:  # pragma: no cover - defensive UI boundary
                GLib.idle_add(self._scan_failed, str(exc))
                return
            GLib.idle_add(self._scan_ready, scans, disk, memory)

        threading.Thread(target=work, daemon=True).start()
        return False

    def _scan_failed(self, detail: str) -> bool:
        self.scan_btn.set_sensitive(True)
        self.set_status(
            "The maintenance scan could not finish. No files were deleted.",
            "error",
            "Scan failed",
        )
        print(f"goreecloud-care scan failure: {detail}", file=sys.stderr)
        return False

    def _scan_ready(self, scans, disk, memory) -> bool:
        self.scans = scans
        for key, (_check, label) in self.rows.items():
            scan = scans.get(key)
            label.set_text(human_bytes(scan.total_bytes if scan else 0))
        self.system_label.set_text(
            f"Disk free: {human_bytes(disk.free_bytes)} • Memory available: {human_bytes(memory.available_bytes)}"
        )
        total = sum(scan.total_bytes for scan in scans.values())
        self.set_status(
            f"Up to {human_bytes(total)} is visible across all maintenance categories.",
            "success",
            "Scan complete",
        )
        self.scan_btn.set_sensitive(True)
        return False

    def _confirm(self, title: str, body: str, *, destructive: bool = False) -> bool:
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.WARNING if destructive else Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.NONE,
            text=title,
        )
        dialog.format_secondary_text(body)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Continue", Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.CANCEL)
        response = dialog.run()
        dialog.destroy()
        return response == Gtk.ResponseType.OK

    def on_clean(self, _button) -> None:
        selected = [
            key
            for key, (check, _label) in self.rows.items()
            if check is not None and check.get_active()
        ]
        if not selected:
            self.set_status("Select at least one routine maintenance category first.", "attention")
            return
        preview = sum(self.scans.get(key, CategoryScan(key, (), 0)).total_bytes for key in selected)
        if not self._confirm(
            "Clean selected categories?",
            f"Care will remove only the currently selected stale files, up to {human_bytes(preview)} based on the latest scan.",
        ):
            self.set_status("Routine cleanup was cancelled before any files were removed.", "info", "Cancelled")
            return
        try:
            removed = self.engine.clean_selected(selected)
        except Exception as exc:  # pragma: no cover - defensive UI boundary
            self.set_status("Routine cleanup failed before completion.", "error")
            print(f"goreecloud-care cleanup failure: {exc}", file=sys.stderr)
            return
        self.set_status(f"Removed {human_bytes(removed)} of selected stale data.", "success")
        self.on_scan(None)

    def on_empty_trash(self, _button) -> None:
        if not self._confirm(
            "Empty Trash permanently?",
            "Files in Trash will be permanently deleted. This cannot be undone by GoreeCloud Care.",
            destructive=True,
        ):
            self.set_status("Trash was not changed.", "info", "Cancelled")
            return
        try:
            removed = self.engine.empty_trash()
        except Exception as exc:  # pragma: no cover
            self.set_status("Trash could not be emptied completely.", "error")
            print(f"goreecloud-care trash failure: {exc}", file=sys.stderr)
            return
        self.set_status(f"Emptied Trash and removed {human_bytes(removed)}.", "success")
        self.on_scan(None)

    def _run_privileged(self, action: str, label: str) -> None:
        self.set_status(f"Requesting authorization to {label.lower()}…", "info", "Authorization required")

        def work() -> None:
            try:
                completed = subprocess.run(
                    ["pkexec", HELPER, action],
                    capture_output=True,
                    text=True,
                    check=False,
                )
            except OSError as exc:
                GLib.idle_add(self._privileged_result, label, None, str(exc))
                return
            GLib.idle_add(self._privileged_result, label, completed, None)

        threading.Thread(target=work, daemon=True).start()

    def _privileged_result(self, label, completed, launch_error) -> bool:
        outcome = interpret_pkexec_result(completed, launch_error=launch_error)
        if outcome.state == "success":
            self.set_status(f"{label} completed.", "success")
        elif outcome.state == "cancelled":
            self.set_status(f"{label} was cancelled before authorization completed.", "info", "Cancelled")
        else:
            self.set_status(
                f"{label} did not complete. No success is claimed.",
                "error",
                "Privileged action failed",
            )
            if outcome.diagnostic:
                print(f"goreecloud-care privileged failure: {outcome.diagnostic}", file=sys.stderr)
        return False

    def on_apt_clean(self, _button) -> None:
        if not self._confirm(
            "Clean package cache?",
            "This uses PolicyKit to run the fixed apt-get clean helper action. Installed packages are not removed.",
        ):
            self.set_status("Package-cache cleanup was cancelled before authorization.", "info", "Cancelled")
            return
        self._run_privileged("apt-clean", "Package cache cleanup")

    def on_reclaim_memory(self, _button) -> None:
        if not self._confirm(
            "Reclaim Linux file cache?",
            "This uses PolicyKit to ask Linux to drop reclaimable file cache. Running applications are not force-closed.",
        ):
            self.set_status("File-cache reclaim was cancelled before authorization.", "info", "Cancelled")
            return
        self._run_privileged("reclaim-memory", "File-cache reclaim")


def main() -> int:
    app = Gtk.Application(application_id=APP_ID, flags=Gio.ApplicationFlags.FLAGS_NONE)

    def activate(application: Gtk.Application) -> None:
        window = CareWindow(application)
        window.show_all()

    app.connect("activate", activate)
    return app.run([])
