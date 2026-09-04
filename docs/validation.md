# Validation and Acceptance

## Current verified state

The repository validation tooling verifies:

- palette JSON structure and unique theme identifiers;
- deterministic generation of all three variants;
- presence of `index.theme`, the GTK 2 discovery compatibility shim, GTK 3 CSS, GTK 4 CSS, the Zorin `.libadwaita` opt-in marker, and GNOME Shell CSS;
- the GTK 2 compatibility shim inherits the system Adwaita GTK 2 theme;
- balanced GTK 3/GTK 4/Shell stylesheet braces and no unresolved template tokens;
- a GTK 3 Adwaita compatibility-base import in each generated application theme;
- GTK 4/libadwaita color-role mappings and an empty marker at exactly `gtk-4.0/.libadwaita`;
- shell-script syntax and Python compilation;
- a basic reusable-secret scan;
- optional GTK 3 and GTK 4/libadwaita smoke-loading under a virtual display.

These checks support **source validation** only. Stock Ubuntu CI does not reproduce Zorin's patched libadwaita theme-selection path.

## Target-device evidence so far

The Zorin OS 17.3 target laptop has provided the following direct evidence during this Development cycle:

- all three theme variants installed successfully under `~/.local/share/themes`;
- the initial GTK3/Shell-only package was not enumerated by Zorin Appearance;
- adding the GTK 2 compatibility shim and reopening Zorin Appearance caused all three GoreeCloud variants to appear in the **Applications** selector;
- screenshots verify `GoreeCloud-Zorin-Dark` selected for both **Applications** and **Shell**, with Zorin Appearance itself rendering on the GoreeCloud Dark canvas without an application-launch failure;
- the GTK 4/libadwaita candidate was pulled and installed successfully on the target laptop, and `GoreeCloud-Zorin-Dark/gtk-4.0/` was directly verified to contain both `gtk.css` and the required zero-byte `.libadwaita` marker;
- Settings directly demonstrates that the GTK 4/libadwaita opt-in path is active: its principal application background renders as the intended Dark canvas while the application remains usable;
- the latest Zorin Appearance screenshot verifies the **Zorin / Other** stack-switcher contrast repair: the selected **Other** label is now readable on its dark selected surface;
- Files remains only partially themed after the current Nautilus-specific GTK 4 mappings: its main grid/list surface and sidebar still render as neutral charcoal instead of the intended GoreeCloud Dark canvas/surface hierarchy. This means further selector-only changes should not be assumed sufficient without first identifying the exact Zorin 17.3 theme/package implementation on the target laptop;
- Quick Settings remains functional and dark, but checked toggles are still visibly bright cyan rather than the GoreeCloud Mineral Teal token. Because GNOME Shell may retain the previously loaded stylesheet across a theme reinstall, this is not yet classified as a confirmed current-source selector failure until the Shell theme is explicitly reloaded or the user logs out and back in;
- the date/notification menu remains partial in the latest screenshot: the outer container is dark, while the notification and event/world-clock/weather cards remain light and several calendar/date labels have poor contrast. As with Quick Settings, a full Shell reload is required before classifying the current Shell source as failed;
- a Zorin application-menu/app-grid surface has now been captured. Its overall panel uses the dark shell surface, but the search placeholder has weak contrast and the highlighted first application tile uses a very light selection card with pale text, producing poor selected-state readability. This is a current Dark-mode visual defect that remains open;
- the GNOME overview/dash proper has not yet been separately captured if it differs from the Zorin application-menu surface;
- Firefox demonstrates that browser-provided/bundled chrome and content styling may remain visually independent from the GTK theme and therefore must not be treated as GTK/libadwaita acceptance evidence.

This is **partial Dark-mode acceptance evidence**, not complete visual or accessibility acceptance.

## Target diagnostics before deeper GTK 4 refactoring

The latest Files evidence shows that directly mapping known Nautilus classes is not enough to establish the intended surface hierarchy on this Zorin 17.3 installation. Before replacing the GTK 4 compatibility architecture or vendoring a large upstream theme, capture the exact target implementation with:

```bash
./scripts/diagnose.sh
```

The diagnostic is read-only. It reports the repository commit, Zorin/session versions, relevant installed package versions, active GTK/Shell theme settings, installed GoreeCloud theme files, and hashes/sizes of the installed ZorinBlue Light/Dark GTK 4 and Shell base stylesheets when present. This evidence is required to keep the next compatibility change bound to the actual target instead of assuming that current upstream Zorin theme internals match the installed Zorin OS 17.3 packages.

For Shell visual retesting after a reinstall, explicitly switch the Shell theme away and back or log out and back in before treating unchanged Quick Settings/date-menu rendering as current-source failure.

## Required target-device acceptance

Before this theme is treated as release-ready or Stable, validate it on the intended Zorin OS 17.3 laptop.

1. Build and install with `./scripts/install.sh`.
2. Close and reopen **Zorin Appearance → Themes → Other** and confirm all three variants appear under Applications and Shell.
3. If discovery fails, verify each installed variant contains `index.theme`, `gtk-2.0/gtkrc`, `gtk-3.0/gtk.css`, `gtk-4.0/gtk.css`, `gtk-4.0/.libadwaita`, and `gnome-shell/gnome-shell.css`; record the observed Zorin Appearance behavior before changing the package again.
4. Test matching Light, Dark, and Deep Dark Application + Shell combinations.
5. For GTK 4/libadwaita acceptance, confirm Files and at least one additional native libadwaita application adopt the expected GoreeCloud canvas, surface, sidebar, selected-row, headerbar, popover, button, field, and focus colors without clipping or broken controls.
6. Install/run `libadwaita-1-examples` / `adwaita-1-demo` on the target laptop when available and inspect representative controls before release qualification.
7. Inspect Settings, Terminal, dialogs, file pickers, menus, context menus, search fields, tabs, buttons, switches, checkboxes, scrollbars, progress bars, tooltips, and notifications.
8. Inspect the top panel, GNOME overview/dash when applicable, Zorin application menu/app grid, search, Quick Settings, system menu, notification/date menu, and modal dialogs.
9. Verify keyboard navigation and clearly visible focus states.
10. Verify text remains readable at normal and increased text scaling.
11. Check selected, hover, active, disabled, destructive, and suggested-action states for adequate distinction.
12. Confirm no clipping, unreadable text, invisible icons, broken separators, or unusable controls; the Zorin Appearance **Zorin / Other** contrast item is now visually verified in Dark mode, while Files surfaces, Quick Settings checked toggles, date/notification cards, Zorin application-menu search text, and the highlighted application tile remain open.
13. Verify the theme can be switched away from cleanly and that `./scripts/uninstall.sh` preserves a recovery copy instead of deleting the installed theme folders.
14. Check representative Flatpak and Snap applications and document which ones retain bundled styling.

## Acceptance boundary

A successful build, pull request, CI run, theme-discovery fix, GTK 3 smoke-load, GTK 4 smoke-load, presence of the `.libadwaita` marker, or a visually improved screenshot does not prove the final desktop experience. Target-device rendering and accessibility acceptance are still required.
