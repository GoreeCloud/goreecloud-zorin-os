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
- Settings now directly demonstrates that the GTK 4/libadwaita opt-in path is active: its principal application background renders as the intended Dark canvas while the application remains usable;
- Files remains only partially themed: its main grid/list surface and sidebar still use neutral charcoal surfaces rather than the intended GoreeCloud Dark canvas/surface hierarchy. Upstream Nautilus 43 uses `.nautilus-grid-view`, `.nautilus-list-view`, `gridview`, `columnview`, `listview`, and `placessidebar.sidebar`, so the current source now maps those concrete GTK 4 application classes directly and awaits target retest;
- the first GTK 3 stack-switcher contrast attempt did not resolve Zorin Appearance's **Other** label: the selected segment still renders dark text on a dark surface. The current source therefore keeps selected stack-switcher text light and uses the accent as a ring/elevated-state treatment instead of relying on an accent fill, pending target retest;
- Quick Settings is functional and its container is dark, but checked toggles still use Zorin's bright cyan accent instead of the GoreeCloud Mineral Teal token. The current Shell source now adds higher-specificity Quick Settings selectors and awaits target retest;
- the date/notification menu exposes additional Shell gaps: the outer menu is dark, but the notification card and event/world-clock/weather cards can remain light, and several calendar/date labels have poor dark-surface contrast. The current Shell source now maps the concrete GNOME Shell date-menu/message classes and awaits target retest;
- the app overview/app grid has not yet been captured in the current target-device evidence set;
- Firefox demonstrates that browser-provided/bundled chrome and content styling may remain visually independent from the GTK theme and therefore must not be treated as GTK/libadwaita acceptance evidence.

This is **partial Dark-mode acceptance evidence**, not complete visual or accessibility acceptance.

## Required target-device acceptance

Before this theme is treated as release-ready or Stable, validate it on the intended Zorin OS 17.3 laptop.

1. Build and install with `./scripts/install.sh`.
2. Close and reopen **Zorin Appearance → Themes → Other** and confirm all three variants appear under Applications and Shell.
3. If discovery fails, verify each installed variant contains `index.theme`, `gtk-2.0/gtkrc`, `gtk-3.0/gtk.css`, `gtk-4.0/gtk.css`, `gtk-4.0/.libadwaita`, and `gnome-shell/gnome-shell.css`; record the observed Zorin Appearance behavior before changing the package again.
4. Test matching Light, Dark, and Deep Dark Application + Shell combinations.
5. For GTK 4/libadwaita acceptance, confirm Files and at least one additional native libadwaita application adopt the expected GoreeCloud canvas, surface, sidebar, selected-row, headerbar, popover, button, field, and focus colors without clipping or broken controls.
6. Install/run `libadwaita-1-examples` / `adwaita-1-demo` on the target laptop when available and inspect representative controls before release qualification.
7. Inspect Settings, Terminal, dialogs, file pickers, menus, context menus, search fields, tabs, buttons, switches, checkboxes, scrollbars, progress bars, tooltips, and notifications.
8. Inspect the top panel, overview, dash, app grid, search, Quick Settings, system menu, notification/date menu, and modal dialogs.
9. Verify keyboard navigation and clearly visible focus states.
10. Verify text remains readable at normal and increased text scaling.
11. Check selected, hover, active, disabled, destructive, and suggested-action states for adequate distinction.
12. Confirm no clipping, unreadable text, invisible icons, broken separators, or unusable controls; specifically re-check the Zorin Appearance **Zorin / Other** stack switcher, the Files main/sidebar surfaces, Quick Settings checked toggles, and the date/notification menu after the current refinements.
13. Verify the theme can be switched away from cleanly and that `./scripts/uninstall.sh` preserves a recovery copy instead of deleting the installed theme folders.
14. Check representative Flatpak and Snap applications and document which ones retain bundled styling.

## Acceptance boundary

A successful build, pull request, CI run, theme-discovery fix, GTK 3 smoke-load, GTK 4 smoke-load, presence of the `.libadwaita` marker, or a visually improved screenshot does not prove the final desktop experience. Target-device rendering and accessibility acceptance are still required.
