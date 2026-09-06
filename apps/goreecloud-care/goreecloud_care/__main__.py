from __future__ import annotations

import sys

from gi.repository import GLib

from . import __version__

# Keep both GLib identities explicit before Gtk.Application startup. AT-SPI on
# the representative Zorin OS desktop derives the application-root name from
# the GLib program name, while user-facing GTK surfaces use the application
# name. Setting both prevents Python's module basename (__main__.py) from
# leaking into assistive-technology discovery.
GLib.set_prgname("GoreeCloud Care")
GLib.set_application_name("GoreeCloud Care")


def _run() -> int:
    args = sys.argv[1:]
    report_requested = "--report" in args
    json_report_requested = "--report-json" in args

    if report_requested and json_report_requested:
        print("goreecloud-care: choose either --report or --report-json, not both", file=sys.stderr)
        return 2

    if "--version" in args:
        print(__version__)
        return 0

    if report_requested or json_report_requested:
        unexpected = [arg for arg in args if arg not in {"--report", "--report-json"}]
        if unexpected:
            print(
                "goreecloud-care: report mode does not accept additional arguments: "
                + " ".join(unexpected),
                file=sys.stderr,
            )
            return 2

        from .reporting import build_snapshot, render_json_report, render_text_report

        snapshot = build_snapshot()
        print(render_json_report(snapshot) if json_report_requested else render_text_report(snapshot))
        return 0

    from .app import main
    from .focus_resilience import install_focus_resilience_provider

    install_focus_resilience_provider()
    return main()


raise SystemExit(_run())
