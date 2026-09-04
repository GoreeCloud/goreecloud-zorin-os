# GoreeCloud Zorin OS Themes

GoreeCloud Zorin OS Themes is the source repository for GoreeCloud desktop themes built for Zorin OS.

## Current status

**Development preview.** This repository contains a Glaze UI V1.1-targeted Zorin OS theme family. Source generation and automated smoke validation are implemented, and target-device testing is in progress on Zorin OS 17.3. A release or Stable claim still requires completion of rendered visual and accessibility acceptance.

The current variants are:

- `GoreeCloud-Zorin-Light`
- `GoreeCloud-Zorin-Dark`
- `GoreeCloud-Zorin-DeepDark`

Each variant provides:

- a GTK 3 application theme whose Development installation is composed over the exact verified local Zorin OS 17.3 GTK 3 base before GoreeCloud semantic overrides are appended;
- a small GTK 2 compatibility shim that inherits system Adwaita so classic theme-discovery paths used by Zorin/GNOME can recognize the theme package;
- a GTK 4/libadwaita stylesheet whose Development installation is composed over the exact verified local Zorin OS 17.3 base before GoreeCloud semantic overrides are appended;
- Zorin's required empty `gtk-4.0/.libadwaita` opt-in marker so native libadwaita applications can participate in target-device validation;
- a GNOME Shell stylesheet whose Development installation is likewise composed over the verified local Zorin OS 17.3 Shell base before GoreeCloud overrides are appended;
- Glaze UI V1.1 surface hierarchy, Deep Teal interaction accents, rounded control geometry, and light/dark/deep-dark mode mapping.

Icons and cursor themes are intentionally not replaced in this implementation. They remain independently selectable in Zorin Appearance.

## Compatibility scope

The current Development target is **Zorin OS 17.3** with `zorin-desktop-themes` **4.2.2**.

Target-device diagnostics established that the installed Zorin 17.3 GTK 3, GTK 4, and GNOME Shell stylesheets are substantial platform-specific bases. The installer therefore composes generated GoreeCloud overrides over the exact verified local `ZorinBlue-Light` or `ZorinBlue-Dark` GTK 3, GTK 4, and Shell bases, including their supporting assets, before installation.

This composition is intentionally fail-closed in Development. Before any existing GoreeCloud theme folder is moved or replaced, the installer verifies the local `zorin-desktop-themes` package version and the exact byte size/SHA-256 evidence captured from the accepted Zorin OS 17.3 target. If that base has changed, installation stops and requests a fresh `./scripts/diagnose.sh` result instead of assuming compatibility.

The repository does **not** redistribute Zorin's base-theme bytes. They are copied locally from `/usr/share/themes` on the target device after verification. When available, the installed package's copyright record is also copied into each locally composed theme as `ZORIN_BASE_COPYRIGHT`, and `goreecloud-base.json` records the verified local base provenance.

The GTK 2 shim is a compatibility/discovery layer, not a full GoreeCloud GTK 2 visual implementation. GTK 2 applications inherit the system Adwaita GTK 2 stylesheet in this preview.

The GTK 4/libadwaita path remains a **Development acceptance candidate**. Zorin OS 17 and newer patches libadwaita to permit explicit third-party theme opt-in when a compatible `gtk-4.0/gtk.css` and sibling `.libadwaita` marker are present. Successful local composition does not by itself prove visual compatibility or release readiness.

Current Dark target evidence now verifies that Files / Nautilus 42.6 uses the intended GoreeCloud Dark `#101A20` main canvas and `#18252B` sidebar after exact Zorin GTK 3 composition. A narrower selected-state pass remains open because the captured Files selected row and Settings selected/checked states still showed pale Zorin cyan instead of the configured Dark selection/accent roles; current Development source contains target-specific selected/checked-state overrides that still require laptop retest.

Flatpak and Snap applications may retain styling bundled by their developers.

## Build

The GoreeCloud override files are generated from shared source templates and palette data so the three variants do not maintain duplicated authoritative GoreeCloud CSS.

```bash
python3 scripts/build.py
```

Generated standalone override output is written to `build/themes/` by default and is not committed. The target-specific Zorin base composition occurs during installation, not during ordinary source generation.

## Install on the verified Zorin OS 17.3 target

Run:

```bash
./scripts/install.sh
```

The installer:

1. generates all three GoreeCloud variants into temporary storage;
2. verifies `zorin-desktop-themes` 4.2.2 and the recorded ZorinBlue Light/Dark GTK 3, GTK 4, and Shell base hashes;
3. locally copies the matching Zorin base directories and assets into the temporary themes;
4. appends the generated GoreeCloud Glaze UI semantic overrides;
5. only after successful composition, backs up any existing GoreeCloud theme folders into a timestamped recovery directory and installs the new variants under `~/.local/share/themes/`.

Then close and reopen **Zorin Appearance**, navigate to **Themes → Other**, and choose a GoreeCloud variant in the **Applications** and **Shell** drop-downs.

You can mix variants if desired, although matching Application and Shell modes are the intended combinations.

Verify the installed package with:

```bash
find ~/.local/share/themes/GoreeCloud-Zorin-* -maxdepth 2 -type f -print | sort
```

In addition to the generated compatibility files, locally composed variants include copied Zorin base assets/files, `goreecloud-base.json`, and `goreecloud-overrides.css` copies used for traceability.

## Target diagnostics

When target-device rendering differs from the generated palette or a Zorin-specific compatibility change is being considered, run the read-only diagnostic helper:

```bash
./scripts/diagnose.sh
```

It reports the repository revision, operating-system/session information, relevant package versions, active GTK/Shell theme settings, installed GoreeCloud theme files, hashes/sizes of installed ZorinBlue Light/Dark GTK 3, GTK 4, and Shell base stylesheets, and bounded target selector evidence. It does not modify settings or system files. This evidence keeps compatibility work tied to the actual Zorin OS 17.3 implementation rather than assuming that another Zorin release or current upstream theme source is identical.

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

CI additionally performs GTK 3 and standalone GTK 4/libadwaita override smoke-loads under a virtual display. These checks verify generated stylesheet parsing and representative widget loading on an Ubuntu 22.04-class environment. CI also compiles and statically checks the target-composition tooling and pinned target evidence. It cannot reproduce the locally installed Zorin 17.3 base composition, Zorin's patched libadwaita theme-selection path, or the real GNOME Shell session; those remain target-device acceptance requirements.

See `docs/validation.md` for the target-device acceptance checklist and `docs/glaze-ui-mapping.md` for the design-system mapping.

## Repository layout

```text
config/       Machine-readable palette and variant definitions
src/          Shared GTK 2, GTK 3, GTK 4/libadwaita, GNOME Shell, and index.theme templates
scripts/      Build, target-base composition, install, uninstall, diagnostics, and validation tooling
docs/         Design mapping and target-device validation guidance
.github/      Repository CI workflow
```

## Design-system source

The implementation target is **Glaze UI V1.1 / 1.1.0**, the current baseline recorded for this Development task. A downstream desktop theme is not considered Glaze UI-conformant merely because it looks similar; it must be independently implemented and validated for its platform.
