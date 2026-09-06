from gi.repository import GLib

from .app import main
from .focus_resilience import install_focus_resilience_provider

# Keep both GLib identities explicit before Gtk.Application startup.  AT-SPI on
# the representative Zorin OS desktop derives the application-root name from
# the GLib program name, while user-facing GTK surfaces use the application
# name.  Setting both prevents Python's module basename (__main__.py) from
# leaking into assistive-technology discovery.
GLib.set_prgname("GoreeCloud Care")
GLib.set_application_name("GoreeCloud Care")
install_focus_resilience_provider()
raise SystemExit(main())
