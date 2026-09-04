# GoreeCloud Themes for Zorin OS

This repository contains Development-stage GoreeCloud desktop themes and original GoreeCloud wallpapers for the verified Zorin OS 17.3 target environment.

The current implementation provides three generated variants aligned to GLAZE UI V1.1 / 1.1.0:

- `GoreeCloud-Zorin-Light`
- `GoreeCloud-Zorin-Dark`
- `GoreeCloud-Zorin-DeepDark`

## Current target

The installer currently supports the exact verified Zorin OS 17.3 theme package target only. It fail-closes unless the local `zorin-desktop-themes` package and recorded GTK 3, GTK 4/libadwaita, and GNOME Shell base hashes match the tested environment.

The GoreeCloud repository does not redistribute Zorin base-theme or wallpaper bytes. During installation, the composer reads and verifies the already-installed local Zorin theme files, copies them into temporary generated GoreeCloud themes, and then appends GoreeCloud semantic overrides before replacing any currently installed GoreeCloud variants.

This preserves Zorin-specific compatibility while keeping the GoreeCloud source focused on palette, geometry, state, compatibility overrides, and original GoreeCloud artwork.

## Install

```bash
./scripts/install.sh
```

Themes are installed user-locally under:

```text
~/.local/share/themes
```

The repository's original GoreeCloud Horizon wallpapers are installed user-locally under:

```text
~/.local/share/backgrounds/GoreeCloud-Zorin
```

Previous GoreeCloud theme folders are preserved in timestamped recovery directories rather than deleted.

After installation, open **Zorin Appearance → Theme → Other** and select the same GoreeCloud variant for **Applications** and **Shell**.

## GoreeCloud Horizon wallpapers

The repository contains three original 3840×2160 SVG wallpapers that mirror the Light, Dark, and Deep Dark Glaze palettes without copying Zorin wallpaper artwork:

- `assets/wallpapers/goreecloud-horizon-light.svg`
- `assets/wallpapers/goreecloud-horizon-dark.svg`
- `assets/wallpapers/goreecloud-horizon-deep-dark.svg`

Wallpaper metadata is recorded in `config/wallpapers.json`.

The theme installer copies all three wallpapers user-locally but does **not** silently change the desktop background. Wallpaper activation is explicit and reversible:

```bash
./scripts/wallpaper.sh apply current
```

`current` maps the active GoreeCloud GTK theme to its matching wallpaper. You can also choose a specific variant:

```bash
./scripts/wallpaper.sh apply light
./scripts/wallpaper.sh apply dark
./scripts/wallpaper.sh apply deep-dark
```

Before changing GNOME background settings, the helper stores a restorable snapshot under:

```text
~/.local/state/goreecloud-zorin/wallpaper
```

Restore the latest saved background settings with:

```bash
./scripts/wallpaper.sh restore
```

The helper never deletes or overwrites Zorin's system wallpapers in `/usr/share`.

## Target diagnostics

For read-only target evidence:

```bash
./scripts/diagnose.sh
python3 ./scripts/diagnose_gtk4_runtime.py
./scripts/diagnose_settings_css.sh
```

The general diagnostic reports OS/session versions, relevant package versions, active theme settings, installed GoreeCloud files, exact installed Zorin base stylesheet sizes/hashes, and targeted compatibility evidence. The GTK 4 runtime diagnostic inspects user GTK 4 configuration, installed GoreeCloud GTK 4 state rules, selected process override variables when Settings is already running, and bounded provider-path strings from the installed libadwaita library. The Settings CSS diagnostic inspects the installed GNOME Control Center/libhandy package files and embedded GResource CSS for bounded selected-row, sidebar, search, switch, and pale-cyan state evidence. These diagnostics change no settings and write no system files.

When `strace` is already installed and direct launch-time provider evidence is required, completely close Settings first, then run:

```bash
./scripts/trace_gtk4_runtime.sh
```

The focused trace launches a temporary `gnome-control-center search` process under `strace`, captures the complete short observation window to a temporary file, filters icon-theme noise only after capture, summarizes whether user-local or system GTK 4/GTK 3 theme paths were seen or successfully opened, and removes the temporary trace on exit. It does not install packages, copy themes into system directories, populate `~/.config/gtk-4.0`, or alter theme settings. The traced Settings process is stopped by `timeout` at the end of the observation window.

On the verified Zorin OS 17.3 target, that focused trace and direct ELF dependency inspection establish that GNOME Settings 41.7 is a GTK 3 + libhandy application: the Settings process opens the user-local GoreeCloud GTK 3 stylesheet and links directly to `libgtk-3`, `libgdk-3`, and `libhandy-1`, with no direct GTK 4/libadwaita dependency.

## Validation

Static validation:

```bash
./scripts/validate.sh
```

GTK smoke loading where the required dependencies are available:

```bash
./scripts/validate.sh --gtk
```

Validation also checks the wallpaper manifest, expected 3840×2160 SVG dimensions/view boxes, absence of scripts or external image references, and executable syntax for `scripts/wallpaper.sh`.

CI runs ShellCheck and generated-theme validation. Green CI verifies repository source/tooling only; it does not establish target-device visual or accessibility acceptance. Exact candidate SHAs and corresponding CI runs are maintained in PR #1 and the GoreeCloud task record rather than embedded in this README.

## Compatibility scope

The Development installer composes from the verified local Zorin 17.3 GTK 3, GTK 4/libadwaita, and GNOME Shell bases, then appends GoreeCloud overrides. The GTK 2 shim exists for theme discovery compatibility. The `.libadwaita` marker is present only with the tested GTK 4 compatibility stylesheet.

Target evidence has shown that some Zorin states are image-backed rather than plain `background-color` states. GoreeCloud maps the verified GTK 3 and GTK 4 selected/checked state mechanisms to the corresponding Glaze semantic tokens rather than retaining Zorin's pale-cyan state fills.

Flatpak and Snap applications may retain bundled or sandboxed appearance behavior. Browser chrome and web content can also use independent themes and should not be treated as direct GTK acceptance evidence.

## Status

Development / Draft. Do not treat installation success, theme discovery, exact-base hash verification, local composition, green CI, wallpaper source presence, or individual screenshots as Stable release evidence.

Current Dark target progress includes verified GoreeCloud canvas/surface rendering in Files, verified `#174F52` selection styling in the Files sidebar and Settings navigation, target-verified Settings enabled-switch tracks at Mineral Teal `#1C8A8D`, improved Shell Quick Settings/date-menu/application-menu states, and coherent overview/search rendering. The Dark Settings selected-row/switch palette blocker is closed for the current candidate.

The new GoreeCloud Horizon wallpaper collection is **source-implemented but not yet target-rendered/accepted**. Target validation still needs to confirm install/apply/restore behavior, desktop cropping at the laptop's actual resolution, Light/Dark/DeepDark visual quality, icon/readability interaction, and no regression to Zorin background settings after restore.

The current draft must remain open until the documented Zorin OS 17.3 real-device visual/accessibility checks, wallpaper acceptance, Light/Dark/DeepDark acceptance, representative native/libadwaita application coverage, rollback verification, review/merge, and release qualification are complete.
