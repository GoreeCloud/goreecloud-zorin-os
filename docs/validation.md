# Validation and Acceptance

## Current verified state

The repository validation tooling verifies:

- palette JSON structure and unique theme identifiers;
- deterministic generation of all three GoreeCloud override variants;
- presence of `index.theme`, the GTK 2 discovery compatibility shim, GTK 3 CSS, GTK 4 CSS, the Zorin `.libadwaita` opt-in marker, and GNOME Shell CSS in standalone generated output;
- the GTK 2 compatibility shim inherits the system Adwaita GTK 2 theme;
- balanced GTK 3/GTK 4/Shell stylesheet braces and no unresolved template tokens;
- a GTK 3 Adwaita compatibility-base import in each generated application theme;
- GTK 4/libadwaita color-role mappings and an empty marker at exactly `gtk-4.0/.libadwaita`;
- shell-script syntax, Python compilation, and expected executable bits for executable repository tools;
- presence of the exact Zorin OS 17.3 target package/version and base stylesheet size/SHA-256 evidence in the composition implementation;
- a basic reusable-secret scan;
- optional GTK 3 and standalone GTK 4/libadwaita override smoke-loading under a virtual display.

These checks support **source validation** only. Stock Ubuntu CI does not reproduce Zorin's patched libadwaita theme-selection path, the verified Zorin 17.3 base-theme bytes, or a live Zorin GNOME Shell session.

## Target-device evidence so far

The Zorin OS 17.3 target laptop has provided the following direct evidence during this Development cycle:

- all three theme variants installed successfully under `~/.local/share/themes`;
- the initial GTK3/Shell-only package was not enumerated by Zorin Appearance;
- adding the GTK 2 compatibility shim and reopening Zorin Appearance caused all three GoreeCloud variants to appear in the **Applications** selector;
- screenshots verify `GoreeCloud-Zorin-Dark` selected for both **Applications** and **Shell**, with Zorin Appearance itself rendering on the GoreeCloud Dark canvas without an application-launch failure;
- the GTK 4/libadwaita candidate was pulled and installed successfully on the target laptop, and `GoreeCloud-Zorin-Dark/gtk-4.0/` was directly verified to contain both `gtk.css` and the required zero-byte `.libadwaita` marker;
- Settings directly demonstrates that the GTK 4/libadwaita opt-in path is active: its principal application background renders as the intended Dark canvas while the application remains usable;
- the latest Zorin Appearance screenshot verifies the **Zorin / Other** stack-switcher contrast repair: the selected **Other** label is readable on its dark selected surface;
- Files remains only partially themed after the standalone Nautilus-specific GTK 4 mappings: its main grid/list surface and sidebar still render as neutral charcoal instead of the intended GoreeCloud Dark canvas/surface hierarchy;
- Quick Settings remains functional and dark, but checked toggles are still visibly bright cyan rather than the GoreeCloud Mineral Teal token. A full Shell reload is still required after the next composed-base installation before this is classified as a current-source failure;
- the date/notification menu remains partial in the latest screenshot: the outer container is dark, while notification and event/world-clock/weather cards remain light and several calendar/date labels have poor contrast. A full Shell reload is likewise required after the next composed-base installation;
- a Zorin application-menu/app-grid surface has been captured. Its overall panel uses the dark shell surface, but the search placeholder has weak contrast and the highlighted first application tile uses a very light selection card with pale text, producing poor selected-state readability;
- the GNOME overview/dash proper has not yet been separately captured if it differs from the Zorin application-menu surface;
- Firefox demonstrates that browser-provided/bundled chrome and content styling may remain visually independent from the GTK theme and therefore must not be treated as GTK/libadwaita acceptance evidence.

This is **partial Dark-mode acceptance evidence**, not complete visual or accessibility acceptance.

## Captured Zorin OS 17.3 implementation evidence

The read-only target diagnostic successfully ran at repository commit `b82c2acea0e90ca5ea16460ce9caffccdd786465` and established this exact environment:

- Zorin OS 17.3 (`VERSION_ID=17`);
- Wayland session, `zorin:GNOME`, GNOME Shell 43.9;
- Nautilus 42.6 (`1:42.6-0ubuntu2`);
- `zorin-desktop-themes` 4.2.2;
- `zorin-appearance` 5.3.8;
- `libadwaita-1-0` `1.3.3-0ubuntu0.23.04.1+zorin2`;
- `gnome-shell` `43.9-0+deb12u2+zorin3`;
- GTK theme `GoreeCloud-Zorin-Dark`, color scheme `prefer-dark`, Shell user theme `GoreeCloud-Zorin-Dark`.

The exact locally installed Zorin base stylesheet evidence is:

| Base file | Bytes | SHA-256 |
| --- | ---: | --- |
| `ZorinBlue-Light/gtk-4.0/gtk.css` | 196060 | `b29cfbaa713955b14517798e2c15a67184136d9913944c1d0cf22fce0d1b3e0c` |
| `ZorinBlue-Light/gtk-4.0/gtk-dark.css` | 195469 | `90ffa76c872443d1549f09c814be8c22d68169a0dfb19e0508339e3613add77d` |
| `ZorinBlue-Light/gnome-shell/gnome-shell.css` | 110634 | `3d94563d7c680be4ac0632b95bb0c205954377488c774a653d8655dbc2ca0823` |
| `ZorinBlue-Dark/gtk-4.0/gtk.css` | 195469 | `90ffa76c872443d1549f09c814be8c22d68169a0dfb19e0508339e3613add77d` |
| `ZorinBlue-Dark/gtk-4.0/gtk-dark.css` | 195469 | `90ffa76c872443d1549f09c814be8c22d68169a0dfb19e0508339e3613add77d` |
| `ZorinBlue-Dark/gnome-shell/gnome-shell.css` | 111171 | `e36202095055bda8de6f225227a91911623775aa0896c24b8568c0d52982f8d7` |

This evidence confirms that the target's GTK 4 and Shell implementation is a substantial Zorin-specific base rather than a tiny semantic overlay. It also confirms that the current upstream `ZorinOS/zorin-desktop-themes` `master` must not be substituted for the target package without verification: upstream `master` currently reports a `ZorinBlue-Dark/gtk-4.0/gtk.css` size of 486443 bytes and a `ZorinBlue-Dark/gnome-shell/gnome-shell.css` size of 159259 bytes, which do not match the installed Zorin OS 17.3 package evidence.

## Development base-composition architecture

The next Development installer candidate therefore uses an evidence-bound composition step instead of additional standalone selector guessing:

1. `scripts/build.py` generates the GoreeCloud GTK 4 and Shell semantic override stylesheets as before.
2. `scripts/compose_zorin_base.py` requires `zorin-desktop-themes` 4.2.2 and verifies the recorded ZorinBlue Light/Dark base file sizes and SHA-256 hashes before making a composed theme.
3. Light uses the verified local `ZorinBlue-Light` base. Dark and Deep Dark use the verified local `ZorinBlue-Dark` base.
4. The compositor copies the complete local GTK 4 and GNOME Shell base directories, including supporting assets, into temporary generated theme folders and then appends GoreeCloud Glaze UI V1.1 semantic overrides.
5. `gtk-dark.css` is composed to the explicit selected GoreeCloud variant as well, so a desktop color-scheme preference does not silently replace the selected Applications variant during this acceptance cycle.
6. The empty `.libadwaita` opt-in marker is restored after composition.
7. `goreecloud-base.json` records local base provenance; the installed package copyright record is copied as `ZORIN_BASE_COPYRIGHT` when available.
8. The GoreeCloud repository itself does not redistribute Zorin base-theme bytes; composition copies them locally from the already-installed Zorin package.
9. The installer performs all verification and temporary composition **before** moving or replacing an existing installed GoreeCloud theme. A package/hash mismatch therefore fails closed without disturbing the current installed theme.

This architecture is still **unaccepted Development work** until it is installed and rendered on the target laptop.

## Required target-device acceptance

Before this theme is treated as release-ready or Stable, validate it on the intended Zorin OS 17.3 laptop.

1. Pull the current Development branch and run `./scripts/install.sh`.
2. Confirm the installer reports successful composition against verified `ZorinBlue-Light` / `ZorinBlue-Dark` bases before installation.
3. Confirm each installed variant contains `goreecloud-base.json`, the expected `gtk-4.0/goreecloud-overrides.css` and `gnome-shell/goreecloud-overrides.css`, the copied base assets, and the zero-byte `gtk-4.0/.libadwaita` marker.
4. Close and reopen **Zorin Appearance → Themes → Other** and confirm all three variants remain available under Applications and Shell.
5. Test matching Light, Dark, and Deep Dark Application + Shell combinations.
6. For GTK 4/libadwaita acceptance, confirm Files and at least one additional native libadwaita application adopt the expected GoreeCloud canvas, surface, sidebar, selected-row, headerbar, popover, button, field, and focus colors without clipping or broken controls.
7. Install/run `libadwaita-1-examples` / `adwaita-1-demo` on the target laptop when available and inspect representative controls before release qualification.
8. Inspect Settings, Terminal, dialogs, file pickers, menus, context menus, search fields, tabs, buttons, switches, checkboxes, scrollbars, progress bars, tooltips, and notifications.
9. After each Shell-theme update, switch the Shell theme away and back or log out and back in, then inspect the top panel, GNOME overview/dash when applicable, Zorin application menu/app grid, search, Quick Settings, system menu, notification/date menu, and modal dialogs.
10. Verify keyboard navigation and clearly visible focus states.
11. Verify text remains readable at normal and increased text scaling.
12. Check selected, hover, active, disabled, destructive, and suggested-action states for adequate distinction.
13. Confirm no clipping, unreadable text, invisible icons, broken separators, or unusable controls. The Zorin Appearance **Zorin / Other** contrast item is already visually verified in Dark mode; Files surfaces, Quick Settings checked toggles, date/notification cards, Zorin application-menu search text, and highlighted application tile remain open until retested against the composed-base candidate.
14. Verify the theme can be switched away from cleanly and that `./scripts/uninstall.sh` preserves a recovery copy instead of deleting the installed theme folders.
15. Check representative Flatpak and Snap applications and document which ones retain bundled styling.

## Acceptance boundary

A successful build, pull request, CI run, theme-discovery fix, base hash match, local composition, GTK 3 smoke-load, GTK 4 smoke-load, presence of the `.libadwaita` marker, or a visually improved screenshot does not prove the final desktop experience. Target-device rendering and accessibility acceptance are still required.
