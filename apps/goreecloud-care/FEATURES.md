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
- Dev9 HighContrast pass: the system HighContrast presentation visibly replaced the light Care palette, confirming the takeover fix, but pressing Tab produced no visibly perceivable focus response.
- Dev10 representative focus checkpoint: exact runtime head `3524a4a82da87ea51dcde08992a402190b54c130` passed 30 local tests plus XML/source validation, built and installed `0.1.0~dev10`, and fresh `GTK_THEME=HighContrast` screenshots show visible focus on Scan, the Thumbnail cache checkbutton, and Reclaim file cache while system HighContrast remains authoritative. Treat the dev9 no-visible-focus defect as closed for these sampled controls.

## Planned before RC
- Complete the remaining HighContrast keyboard path at normal and constrained widths: verify visible focus on the remaining cleanup selectors and bottom actions, complete forward traversal, and reverse `Shift+Tab` traversal.
- Assistive-technology semantic acceptance.
- Additional supported appearance/resilience decisions and evidence, including dark/system appearance where applicable.
- Package uninstall/downgrade/rollback validation.
- Official GoreeCloud Care icon/branding from the canonical branding-assets source.
- GoreeCloud Care current-Stable Glaze UI V1.1 consumer acceptance with exact native evidence.
- Applicable Wardveil Security, Privacy Shield, Everkeep, Mesh, Manager, and Identity decisions/evidence.
