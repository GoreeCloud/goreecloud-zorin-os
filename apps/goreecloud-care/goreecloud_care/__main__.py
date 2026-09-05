from .app import main
from .focus_resilience import install_focus_resilience_provider

install_focus_resilience_provider()
raise SystemExit(main())
