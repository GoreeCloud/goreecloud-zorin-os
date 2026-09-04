# GoreeCloud Zorin OS Themes

GoreeCloud Zorin OS Themes is the source repository for GoreeCloud desktop themes built for Zorin OS.

## Current status

**Development preview.** This repository contains a Glaze UI V1.1-inspired Zorin OS theme family. Source generation and automated smoke validation are implemented, and target-device testing is in progress on Zorin OS 17.3. A release or Stable claim still requires completion of rendered visual and accessibility acceptance.

The current variants are:

- `GoreeCloud-Zorin-Light`
- `GoreeCloud-Zorin-Dark`
- `GoreeCloud-Zorin-DeepDark`

Each variant provides:

- a GTK 3 application theme that layers GoreeCloud styling over GTK's built-in Adwaita base;
- a small GTK 2 compatibility shim that inherits system Adwaita so classic theme-discovery paths used by Zorin/GNOME can recognize the theme package;
- a GTK 4 stylesheet that maps Glaze UI color roles and common widget states into GTK 4/libadwaita surfaces;
- Zorin's required empty `gtk-4.0/.libadwaita` opt-in marker so native libadwaita applications can participate in target-device validation;
- a GNOME Shell custom stylesheet for panel, overview, menus, search, quick settings, dialogs, notifications, and related shell surfaces;
- Glaze UI V1.1 surface hierarchy, Deep Teal interaction accents, rounded control geometry, and light/dark/deep-dark mode mapping.

Icons and cursor themes are intentionally not replaced in this implementation. They remain independently selectable in Zorin Appearance.

## Compatibility scope

The initial target is **Zorin OS 17.3**.

The GTK 2 shim is a compatibility/discovery layer, not a full GoreeCloud GTK 2 visual implementation. GTK 2 applications inherit the system Adwaita GTK 2 stylesheet in this preview.

The GTK 4/libadwaita path is a **Development acceptance candidate**. Zorin OS 17 and newer patches libadwaita to permit explicit third-party theme opt-in when a compatible `gtk-4.0/gtk.css` and sibling `.libadwaita` marker are present. The files are now generated so real-device testing can cover native libadwaita applications. Their presence does not by itself prove compatibility or release readiness.

Flatpak and Snap applications may retain styling bundled by their developers.

## Build

The theme files are generated from shared source templates and palette data so the three variants do not maintain duplicated authoritative CSS.

```bash
python3 scripts/build.py
```

Generated output is written to `build/themes/` by default and is not committed.

## Install on Zorin OS

Run:

```bash
./scripts/install.sh
```

The installer builds the themes, backs up any existing GoreeCloud theme folders into a timestamped recovery directory, and installs the generated variants under:

```text
~/.local/share/themes/
```

Then close and reopen **Zorin Appearance**, navigate to **Themes → Other**, and choose a GoreeCloud variant in the **Applications** and **Shell** drop-downs.

You can mix variants if desired, although matching Application and Shell modes are the intended combinations.

If the themes still do not appear or a new candidate appears stale, verify the generated files:

```bash
find ~/.local/share/themes/GoreeCloud-Zorin-* -maxdepth 2 -type f -print | sort
```

Each variant should include `index.theme`, `gtk-2.0/gtkrc`, `gtk-3.0/gtk.css`, `gtk-4.0/gtk.css`, `gtk-4.0/.libadwaita`, and `gnome-shell/gnome-shell.css`.

## Target diagnostics

When target-device rendering differs from the generated palette or a Zorin-specific compatibility change is being considered, run the read-only diagnostic helper:

```bash
./scripts/diagnose.sh
```

It reports the repository revision, operating-system/session information, relevant package versions, active GTK/Shell theme settings, installed GoreeCloud theme files, and hashes/sizes of installed ZorinBlue Light/Dark GTK 4 and Shell base stylesheets when available. It does not modify settings or system files. This evidence keeps compatibility work tied to the actual Zorin OS 17.3 implementation rather than assuming that another Zorin release or current upstream theme source is identical.

GNOME Shell can retain a previously loaded stylesheet across a theme reinstall. When validating Shell-only visual changes, switch the Shell theme away and back or log out and back in before classifying unchanged rendering as a current-source failure.

## Uninstall / rollback

First switch **Applications** and **Shell** to another theme in Zorin Appearance. Then run:

```bash
./scripts/uninstall.sh
```

The uninstaller moves GoreeCloud theme folders into a timestamped recovery directory instead of permanently deleting them.

## Validation

Run the repository checks with:

```bash
./scripts/validate.sh
```

CI additionally performs GTK 3 and GTK 4/libadwaita smoke-loads under a virtual display. These checks verify generated stylesheet parsing and representative widget loading on an Ubuntu 22.04-class environment; they do not replace testing on the actual Zorin laptop or Zorin's patched libadwaita theme-selection path.

See `docs/validation.md` for the target-device acceptance checklist and `docs/glaze-ui-mapping.md` for the design-system mapping.

## Repository layout

```text
config/       Machine-readable palette and variant definitions
src/          Shared GTK 2, GTK 3, GTK 4/libadwaita, GNOME Shell, and index.theme templates
scripts/      Build, install, uninstall, target diagnostics, and validation tooling
docs/         Design mapping and target-device validation guidance
.github/      Repository CI workflow
```

## Design-system source

The implementation target is **Glaze UI V1.1 / 1.1.0**, the baseline recorded for this Development task. A downstream desktop theme is not considered Glaze UI-conformant merely because it looks similar; it must be independently implemented and validated for its platform.
