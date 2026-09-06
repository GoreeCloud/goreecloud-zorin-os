from gi.repository import GLib

from .app import main
from .focus_resilience import install_focus_resilience_provider

# Ensure AT-SPI/Orca expose the product name instead of the Python module basename.
GLib.set_application_name("GoreeCloud Care")
install_focus_resilience_provider()
raise SystemExit(main())
