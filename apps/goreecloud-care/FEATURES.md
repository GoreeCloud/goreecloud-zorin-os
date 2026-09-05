# Features

## Implemented in Development source
- User cache scan/cleanup (>7 days).
- Thumbnail cache scan/cleanup.
- User-owned stale `/tmp` scan/cleanup (>7 days).
- Trash scan plus separately confirmed permanent emptying.
- APT archive-cache preview and PolicyKit-authorized `apt-get clean`.
- Disk and memory status.
- PolicyKit-authorized Linux page/dentry/inode cache reclaim with a truthful warning.
- Explicit cancellation, failure, and completion reporting for privileged maintenance.
- Persistent semantic status presentation with non-color-only state communication.
- Visible keyboard-focus treatment and fail-safe Cancel-first confirmation dialogs.
- Light application appearance by default without changing the desktop-wide Zorin OS appearance.
- Adaptive compact-window composition for constrained desktop widths.
- Dev7 compact transition at 820 logical pixels so the compact category/action composition is reachable before the observed 200%-text minimum-width floor.
- Dev7 compact HeaderBar reduction that omits the Development subtitle while preserving the application title and Scan action.
- GTK/ATK status, control-description, selector-description, and category-count accessibility semantics.
- High-contrast fallback that yields application color styling to common GTK HighContrast themes.
- Local-only operation and zero telemetry.
- Conservative symlink handling and fixed privileged-action allowlist.

## Representative-device verified
- Through dev5: Zorin OS 17.3 source validation, package build, upgrade/install, launch, keyboard focus visibility, first-stage and PolicyKit cancellation, successful PolicyKit-authorized Memory Refresh and APT cleanup, controlled nonzero Application cache / Thumbnail cache / Temporary files / Trash / APT archive deletion, completion reporting, and post-action values refresh.
- Dev6: normal-text compact/minimum-window adaptive composition, vertical reachability, full-width stacked bottom actions, category-amount reflow, and visible focus at the compact bottom control path.
- Dev6 negative evidence: at the narrowest `GDK_DPI_SCALE=2` window, the old 680-pixel compact transition was not reachable; the regular count/action composition remained active.

## Planned before RC
- Target-device dev7 revalidation proving combined 200%-text + compact/minimum-window behavior after the breakpoint/HeaderBar remediation.
- Target-device HighContrast and assistive-technology acceptance, including keyboard focus through the full resilience-mode control path.
- Additional supported appearance/resilience decisions and evidence, including dark/system appearance where applicable.
- Package uninstall/downgrade/rollback validation.
- Official GoreeCloud Care icon/branding from the canonical branding-assets source.
- GoreeCloud Care current-Stable Glaze UI V1.1 consumer acceptance with exact native evidence.
- Applicable Wardveil Security, Privacy Shield, Everkeep, Mesh, Manager, and Identity decisions/evidence.
