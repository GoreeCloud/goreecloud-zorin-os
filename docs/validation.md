# Validation and Acceptance

## Current verified state

The repository validation tooling verifies:

- palette JSON structure and unique theme identifiers;
- deterministic generation of all three variants;
- presence of `index.theme`, the GTK 2 discovery compatibility shim, GTK 3 CSS, and GNOME Shell CSS;
- the GTK 2 compatibility shim inherits the system Adwaita GTK 2 theme;
- balanced GTK 3/Shell stylesheet braces and no unresolved template tokens;
- a GTK 3 Adwaita compatibility-base import in each generated application theme;
- absence of an unvalidated GTK 4 directory or `.libadwaita` opt-in marker;
- shell-script syntax and Python compilation;
- a basic reusable-secret scan;
- optional GTK 3 smoke-loading under a virtual display.

These checks support **source validation** only.

## Required target-device acceptance

Before this theme is treated as release-ready or Stable, validate it on the intended Zorin OS 17.3 laptop.

1. Build and install with `./scripts/install.sh`.
2. Close and reopen **Zorin Appearance → Themes → Other** and confirm all three variants appear under Applications and Shell.
3. If discovery fails, verify each installed variant contains `index.theme`, `gtk-2.0/gtkrc`, `gtk-3.0/gtk.css`, and `gnome-shell/gnome-shell.css`; record the observed Zorin Appearance behavior before changing the package again.
4. Test matching Light, Dark, and Deep Dark Application + Shell combinations.
5. Inspect Files, Settings, Terminal, dialogs, file pickers, menus, context menus, search fields, tabs, buttons, switches, checkboxes, scrollbars, progress bars, tooltips, and notifications.
6. Inspect the top panel, overview, dash, app grid, search, quick settings, system menu, notifications, and modal dialogs.
7. Verify keyboard navigation and clearly visible focus states.
8. Verify text remains readable at normal and increased text scaling.
9. Check selected, hover, active, disabled, destructive, and suggested-action states for adequate distinction.
10. Confirm no clipping, unreadable text, invisible icons, broken separators, or unusable controls.
11. Verify the theme can be switched away from cleanly and that `./scripts/uninstall.sh` preserves a recovery copy instead of deleting the installed theme folders.
12. Check representative Flatpak and Snap applications and document which ones retain bundled styling.
13. Do not add `gtk-4.0/.libadwaita` until a GTK 4/libadwaita stylesheet has been developed and extensively tested with Zorin's required opt-in process.

## Acceptance boundary

A successful build, pull request, CI run, theme-discovery fix, or GTK 3 smoke-load does not prove the final desktop experience. Target-device rendering and accessibility acceptance are still required.
