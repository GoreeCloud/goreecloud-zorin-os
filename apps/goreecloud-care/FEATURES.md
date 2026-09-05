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
- Normal-text compact transition at 820 logical pixels.
- Effective-width adaptation for the `GDK_DPI_SCALE` 200%-text acceptance path.
- Compact HeaderBar reduction that omits the Development subtitle while preserving the application title and Scan action.
- GTK/ATK status, control-description, selector-description, and category-count accessibility semantics.
- Effective HighContrast detection that honors both `Gtk.Settings` theme state and process-local `GTK_THEME` overrides.
- Dev10 focus-resilience provider that uses the active GTK theme foreground color and sits one priority level below Care's normal application CSS, so HighContrast can own the palette without leaving keyboard focus visually silent.
- Local-only operation and zero telemetry.
- Conservative symlink handling and fixed privileged-action allowlist.

## Representative-device verified
- Through dev5: Zorin OS 17.3 source validation, package build, upgrade/install, launch, keyboard focus visibility, first-stage and PolicyKit cancellation, successful PolicyKit-authorized Memory Refresh and APT cleanup, controlled nonzero Application cache / Thumbnail cache / Temporary files / Trash / APT archive deletion, completion reporting, and post-action values refresh.
- Dev6: normal-text compact/minimum-window adaptive composition, vertical reachability, full-width stacked bottom actions, category-amount reflow, and visible focus at the compact bottom control path.
- Dev8: combined 200%-text/compact acceptance at exact runtime head `45b5f11a49f363ebcaf753c892245a31109bc9bb`; wide and narrow `GDK_DPI_SCALE=2` views preserve wrapping, scrolling, compact HeaderBar behavior, category-amount reflow, and the full-width vertical action stack.
- First HighContrast pass on installed dev8: focus was visibly clear on Scan, a category checkbox, and Memory Refresh, but `GTK_THEME=HighContrast` failed to displace the light Development palette.
- Fresh dev9 HighContrast pass: the system HighContrast presentation now visibly replaces the light Care palette, confirming the dev9 takeover fix. In the same state, pressing Tab produces no visibly perceivable focus response. Treat palette takeover as positive evidence but keyboard-under-HighContrast as failed/open; this does not prove whether logical focus traversal is absent or merely visually silent.

## Planned before RC
- Build/install dev10 and repeat target-device HighContrast keyboard validation at normal and constrained widths. Confirm a visible focus indicator across Scan, all three cleanup selectors, Reclaim file cache, Clean selected, Empty Trash, and Clean APT cache.
- If dev10 shows a focus ring but activation proves Tab still does not move logical focus, implement a separate native traversal remediation; do not add custom key handling without that evidence.
- Assistive-technology semantic acceptance.
- Additional supported appearance/resilience decisions and evidence, including dark/system appearance where applicable.
- Package uninstall/downgrade/rollback validation.
- Official GoreeCloud Care icon/branding from the canonical branding-assets source.
- GoreeCloud Care current-Stable Glaze UI V1.1 consumer acceptance with exact native evidence.
- Applicable Wardveil Security, Privacy Shield, Everkeep, Mesh, Manager, and Identity decisions/evidence.
