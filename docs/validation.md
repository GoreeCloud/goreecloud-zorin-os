# Validation and Acceptance

## Current verified state

The repository validation tooling verifies:

- palette JSON structure and unique theme identifiers;
- deterministic generation of all three GoreeCloud override variants;
- presence of `index.theme`, the GTK 2 discovery compatibility shim, GTK 3 CSS, GTK 4 CSS, the Zorin `.libadwaita` opt-in marker, and GNOME Shell CSS in standalone generated output;
- the GTK 2 compatibility shim inherits the system Adwaita GTK 2 theme;
- balanced GTK 3/GTK 4/Shell stylesheet braces and no unresolved template tokens;
- a GTK 3 Adwaita compatibility-base import in each standalone generated application theme;
- GTK 3 legacy symbolic color mappings used by application-provided CSS such as Nautilus 42.6;
- an exact Nautilus 42.6 `.nautilus-window .sidebar-row:selected` override in GTK 3;
- GTK 4/libadwaita color-role mappings, exact `navigation-sidebar` selected/activatable states, checked-switch state coverage, and an empty marker at exactly `gtk-4.0/.libadwaita`;
- shell-script syntax, Python compilation, and expected executable bits for executable repository tools;
- presence of the exact Zorin OS 17.3 target package/version and pinned GTK 3, GTK 4, and GNOME Shell base stylesheet size/SHA-256 evidence in the composition implementation;
- source evidence that target installation copies the verified local Zorin GTK 3 base and removes the standalone GTK 3 Adwaita import before appending GoreeCloud overrides;
- a basic reusable-secret scan;
- optional GTK 3 and standalone GTK 4/libadwaita override smoke-loading under a virtual display.

These checks support **source validation** only. Stock Ubuntu CI does not reproduce Zorin's patched libadwaita theme-selection path, the verified Zorin 17.3 base-theme bytes, or a live Zorin GNOME Shell session.

## Target-device evidence so far

The Zorin OS 17.3 target laptop has provided the following direct evidence during this Development cycle:

- all three theme variants install successfully under `~/.local/share/themes` and remain discoverable in Zorin Appearance;
- the GTK 2 compatibility shim resolved Applications-theme enumeration;
- `GoreeCloud-Zorin-Dark` is selectable for both **Applications** and **Shell**;
- Settings demonstrates that Zorin's patched GTK 4/libadwaita opt-in path is active;
- the Zorin Appearance **Zorin / Other** stack-switcher contrast repair is visually verified;
- exact-base composition is installed and provenance-verified for GTK 3, GTK 4, and GNOME Shell;
- after a full Shell reload, Quick Settings checked toggles use the GoreeCloud Mineral Teal family rather than the original bright Zorin cyan;
- the date/notification menu uses coherent dark cards and readable calendar/date text;
- the Zorin application-menu selected tile is readable and its tooltip is readable; the empty search placeholder still needs a dedicated contrast check;
- representative GNOME overview/search rendering is coherent dark with a visible teal focus treatment;
- the exact GTK 3 base-composition candidate is now visually effective in **Files / Nautilus 42.6**: the main Home view renders at the intended Dark canvas `#101A20`, and the sidebar renders at the intended Dark surface `#18252B`. This resolves the prior neutral-charcoal surface defect for the captured Dark state;
- the same Files screenshot exposes a narrower remaining state defect: the selected Home row renders pale cyan near `#BDE6FB` instead of the Dark Glaze selection token `#174F52`;
- **Settings → Search** likewise no longer shows the earlier saturated Zorin-blue selected row, but the selected Search row and checked switches render pale cyan near `#BDE6FB` rather than the intended Dark selection/accent roles (`#174F52` selection and `#1C8A8D` accent). The main Settings canvas/sidebar remain coherent with the Dark GoreeCloud surface hierarchy;
- the pale selected/checked states are therefore tracked as target-specific specificity/background-image state defects, not as failures of the exact-base composition architecture;
- current Development source adds the exact Nautilus 42.6 selected-sidebar selector, expands Settings `navigation-sidebar` selected/activatable/focus coverage, and clears inherited GTK 4 checked-switch background images before applying the GoreeCloud accent. These latest changes are source-validated but still require target-device reinstall/retest;
- Firefox demonstrates that browser-provided/bundled chrome and content styling may remain visually independent from the GTK theme and therefore must not be treated as GTK/libadwaita acceptance evidence.

This is **partial Dark-mode acceptance evidence**, not complete visual or accessibility acceptance.

## Captured Zorin OS 17.3 implementation evidence

The target diagnostics establish this environment:

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
| `ZorinBlue-Light/gtk-3.0/gtk.css` | 215389 | `bc06ff2fac92e56951b8f4141b8324acc1e38db783ec3a0b3cf438e8c87d9fe6` |
| `ZorinBlue-Light/gtk-4.0/gtk.css` | 196060 | `b29cfbaa713955b14517798e2c15a67184136d9913944c1d0cf22fce0d1b3e0c` |
| `ZorinBlue-Light/gtk-4.0/gtk-dark.css` | 195469 | `90ffa76c872443d1549f09c814be8c22d68169a0dfb19e0508339e3613add77d` |
| `ZorinBlue-Light/gnome-shell/gnome-shell.css` | 110634 | `3d94563d7c680be4ac0632b95bb0c205954377488c774a653d8655dbc2ca0823` |
| `ZorinBlue-Dark/gtk-3.0/gtk.css` | 214797 | `71e9d93ad1e58f75e52bb7b724fa38409961368b5d9edda4c3b921fac6e44604` |
| `ZorinBlue-Dark/gtk-4.0/gtk.css` | 195469 | `90ffa76c872443d1549f09c814be8c22d68169a0dfb19e0508339e3613add77d` |
| `ZorinBlue-Dark/gtk-4.0/gtk-dark.css` | 195469 | `90ffa76c872443d1549f09c814be8c22d68169a0dfb19e0508339e3613add77d` |
| `ZorinBlue-Dark/gnome-shell/gnome-shell.css` | 111171 | `e36202095055bda8de6f225227a91911623775aa0896c24b8568c0d52982f8d7` |

This evidence confirms that the target GTK 3, GTK 4, and Shell implementations are substantial Zorin-specific bases rather than tiny semantic overlays. Current upstream Zorin theme source must not be substituted for the installed 17.3 package without verification.

## Development base-composition architecture

The Development installer uses an evidence-bound composition step instead of attempting to replace the Zorin compatibility foundation:

1. `scripts/build.py` generates standalone GoreeCloud GTK 3, GTK 4, and Shell semantic override stylesheets.
2. `scripts/compose_zorin_base.py` requires `zorin-desktop-themes` 4.2.2 and verifies the recorded ZorinBlue Light/Dark GTK 3, GTK 4, and Shell base file sizes/SHA-256 hashes before making a composed theme.
3. Light uses the verified local `ZorinBlue-Light` base. Dark and Deep Dark use the verified local `ZorinBlue-Dark` base.
4. The compositor copies the complete local GTK 3, GTK 4, and GNOME Shell base directories, including supporting assets, into temporary generated theme folders.
5. The standalone GTK 3 Adwaita import is removed only for target-base composition, preventing a second compatibility base from being imported after the verified Zorin GTK 3 foundation.
6. GoreeCloud Glaze UI V1.1 semantic overrides are appended after each verified local base.
7. `gtk-dark.css` is composed to the explicit selected GoreeCloud variant where applicable so a separate dark-preference path does not silently replace the selected Applications variant during this acceptance cycle.
8. The empty `.libadwaita` opt-in marker is restored after GTK 4 composition.
9. `goreecloud-base.json` records local base provenance; the installed package copyright record is copied as `ZORIN_BASE_COPYRIGHT` when available.
10. The GoreeCloud repository does not redistribute Zorin base-theme bytes; composition copies them locally from the already-installed Zorin package.
11. The installer performs all verification and temporary composition **before** moving or replacing an existing installed GoreeCloud theme. A package/hash mismatch therefore fails closed without disturbing the current installed theme.

The exact-base architecture is target-verified for the captured Dark Files surfaces. The latest selected/checked-state tightening remains a **Development candidate** until target-device rendering is retested.

## Required target-device acceptance

Before this theme is treated as release-ready or Stable, validate it on the intended Zorin OS 17.3 laptop.

1. Pull the current Development branch and run `./scripts/install.sh` after each source candidate that changes application or Shell styling.
2. Confirm the installer reports successful composition against verified `ZorinBlue-Light` / `ZorinBlue-Dark` GTK 3, GTK 4, and Shell bases before installation.
3. Confirm `goreecloud-base.json` records `gtk3_css`, `gtk_css`, and `shell_css` evidence for the selected base, and confirm `gtk-3.0/goreecloud-overrides.css` exists in the composed theme.
4. Close/relaunch Files (`nautilus -q` before reopening is sufficient) and verify that the already-correct `#101A20` main canvas and `#18252B` sidebar are preserved while the selected Home/Pictures sidebar row moves from pale `#BDE6FB` to the Dark Glaze selection treatment.
5. Fully close/reopen Settings, then re-test **Settings → Search** and verify that the selected navigation row no longer uses pale `#BDE6FB` and that checked switches return to the Dark Mineral Teal accent instead of pale cyan.
6. Close and reopen **Zorin Appearance → Themes → Other** and confirm all three variants remain available under Applications and Shell.
7. Test matching Light, Dark, and Deep Dark Application + Shell combinations.
8. For GTK 4/libadwaita acceptance, confirm at least one additional native libadwaita application adopts expected GoreeCloud canvas, surface, sidebar, selected-row, headerbar, popover, button, field, and focus colors without clipping or broken controls.
9. Install/run `libadwaita-1-examples` / `adwaita-1-demo` on the target laptop when available and inspect representative controls before release qualification.
10. Inspect Terminal, dialogs, file pickers, menus, context menus, search fields, tabs, buttons, switches, checkboxes, scrollbars, progress bars, tooltips, and notifications.
11. After each Shell-theme update, switch the Shell theme away and back or log out and back in, then inspect the top panel, GNOME overview/dash when applicable, Zorin application menu/app grid, search, Quick Settings, system menu, notification/date menu, and modal dialogs.
12. Re-check the Zorin application-menu search placeholder for sufficient contrast.
13. Verify keyboard navigation and clearly visible focus states.
14. Verify text remains readable at normal and increased text scaling.
15. Check selected, hover, active, disabled, destructive, and suggested-action states for adequate distinction.
16. Confirm no clipping, unreadable text, invisible icons, broken separators, or unusable controls.
17. Verify the theme can be switched away from cleanly and that `./scripts/uninstall.sh` preserves a recovery copy instead of deleting installed theme folders.
18. Check representative Flatpak and Snap applications and document which ones retain bundled styling.

## Acceptance boundary

A successful build, pull request, CI run, theme-discovery fix, base hash match, local composition, GTK 3 smoke-load, GTK 4 smoke-load, presence of the `.libadwaita` marker, or a visually improved screenshot does not prove the final desktop experience. Target-device rendering and accessibility acceptance are still required.
