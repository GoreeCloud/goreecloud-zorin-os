# GoreeCloud Themes for Zorin OS

This repository contains Development-stage GoreeCloud desktop themes for the verified Zorin OS 17.3 target environment.

The current implementation provides three generated variants aligned to GLAZE UI V1.1 / 1.1.0:

- `GoreeCloud-Zorin-Light`
- `GoreeCloud-Zorin-Dark`
- `GoreeCloud-Zorin-DeepDark`

## Current target

The installer currently supports the exact verified Zorin OS 17.3 theme package target only. It fail-closes unless the local `zorin-desktop-themes` package and recorded GTK 3, GTK 4/libadwaita, and GNOME Shell base hashes match the tested environment.

The GoreeCloud repository does not redistribute Zorin base-theme bytes. During installation, the composer reads and verifies the already-installed local Zorin theme files, copies them into temporary generated GoreeCloud themes, and then appends GoreeCloud semantic overrides before replacing any currently installed GoreeCloud variants.

This preserves Zorin-specific compatibility while keeping the GoreeCloud source focused on palette, geometry, state, and compatibility overrides.

## Install

```bash
./scripts/install.sh
```

Themes are installed user-locally under:

```text
~/.local/share/themes
```

Previous GoreeCloud theme folders are preserved in timestamped recovery directories rather than deleted.

After installation, open **Zorin Appearance → Theme → Other** and select the same GoreeCloud variant for **Applications** and **Shell**.

## Target diagnostics

For read-only target evidence:

```bash
./scripts/diagnose.sh
```

The diagnostic reports OS/session versions, relevant package versions, active theme settings, installed GoreeCloud files, exact installed Zorin base stylesheet sizes/hashes, and targeted compatibility evidence. It changes no settings and writes no system files.

## Validation

Static validation:

```bash
./scripts/validate.sh
```

GTK smoke loading where the required dependencies are available:

```bash
./scripts/validate.sh --gtk
```

CI runs ShellCheck and generated-theme validation. Green CI verifies repository source/tooling only; it does not establish target-device visual or accessibility acceptance. Exact candidate SHAs and corresponding CI runs are maintained in PR #1 and the GoreeCloud task record rather than embedded in this README.

## Compatibility scope

The Development installer composes from the verified local Zorin 17.3 GTK 3, GTK 4/libadwaita, and GNOME Shell bases, then appends GoreeCloud overrides. The GTK 2 shim exists for theme discovery compatibility. The `.libadwaita` marker is present only with the tested GTK 4 compatibility stylesheet.

Target evidence has shown that some Zorin states are image-backed rather than plain `background-color` states. In particular, the verified Zorin family paints selected navigation rows and checked switches with image-backed fills. GoreeCloud therefore maps those image layers directly to the current variant's GLAZE selection/accent tokens rather than relying only on generic background colors.

Flatpak and Snap applications may retain bundled or sandboxed appearance behavior. Browser chrome and web content can also use independent themes and should not be treated as direct GTK acceptance evidence.

## Status

Development / Draft. Do not treat installation success, theme discovery, exact-base hash verification, local composition, green CI, or individual screenshots as Stable release evidence.

Current Dark target progress includes verified GoreeCloud canvas/surface rendering in Files, verified `#174F52` GoreeCloud selection styling in the Files sidebar, improved Shell Quick Settings/date-menu/application-menu states, and coherent overview/search rendering. Settings selected-navigation and checked-switch image-backed states remain under target-device acceptance after the latest GTK 4 correction.

The current draft must remain open until the documented Zorin OS 17.3 real-device visual/accessibility checks, Light/Dark/DeepDark acceptance, representative native/libadwaita application coverage, rollback verification, review/merge, and release qualification are complete.
