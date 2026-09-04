# GoreeCloud Zorin OS Themes

GoreeCloud Zorin OS Themes is the source repository for GoreeCloud desktop themes built for Zorin OS.

## Current status

**Development preview.** This repository now contains the first source implementation of a Glaze UI V1.1-inspired Zorin OS theme family. Source generation and static validation are implemented, but target-device visual and accessibility acceptance on Zorin OS 17.3 is still required before a release or Stable claim.

The current variants are:

- `GoreeCloud-Zorin-Light`
- `GoreeCloud-Zorin-Dark`
- `GoreeCloud-Zorin-DeepDark`

Each variant provides:

- a GTK 3 application theme that layers GoreeCloud styling over GTK's built-in Adwaita base;
- a small GTK 2 compatibility shim that inherits system Adwaita so classic theme-discovery paths used by Zorin/GNOME can recognize the theme package;
- a GNOME Shell custom stylesheet for panel, overview, menus, search, quick settings, dialogs, notifications, and related shell surfaces;
- Glaze UI V1.1 surface hierarchy, Deep Teal interaction accents, rounded control geometry, and light/dark/deep-dark mode mapping.

Icons and cursor themes are intentionally not replaced in this first implementation. They remain independently selectable in Zorin Appearance.

## Compatibility scope

The initial target is **Zorin OS 17.3**.

The GTK 2 shim is a compatibility/discovery layer, not a full GoreeCloud GTK 2 visual implementation. GTK 2 applications inherit the system Adwaita GTK 2 stylesheet in this preview.

This preview intentionally does **not** opt into native libadwaita theming. Zorin OS 17 and newer supports a developer opt-in mechanism for libadwaita themes, but that path requires a GTK 4 stylesheet plus extensive compatibility testing. No `gtk-4.0/.libadwaita` marker is generated until that validation is completed.

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

If the themes still do not appear, verify the generated compatibility files:

```bash
find ~/.local/share/themes/GoreeCloud-Zorin-* -maxdepth 2 -type f -print | sort
```

Each variant should include `index.theme`, `gtk-2.0/gtkrc`, `gtk-3.0/gtk.css`, and `gnome-shell/gnome-shell.css`.

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

CI additionally performs a GTK 3 smoke-load under a virtual display. This verifies that generated GTK stylesheets can be loaded on an Ubuntu 22.04-class GTK 3 environment, but it does not replace testing on the actual Zorin laptop.

See `docs/validation.md` for the target-device acceptance checklist and `docs/glaze-ui-mapping.md` for the design-system mapping.

## Repository layout

```text
config/       Machine-readable palette and variant definitions
src/          Shared GTK 2 compatibility, GTK 3, GNOME Shell, and index.theme templates
scripts/      Build, install, uninstall, and validation tooling
docs/         Design mapping and target-device validation guidance
.github/      Repository CI workflow
```

## Design-system source

The implementation target is **Glaze UI V1.1 / 1.1.0**, the current Stable Glaze UI baseline recorded by GoreeCloud. A downstream desktop theme is not considered Glaze UI-conformant merely because it looks similar; it must be independently implemented and validated for its platform.
