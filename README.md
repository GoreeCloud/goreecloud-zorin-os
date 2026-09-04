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
python3 ./scripts/diagnose_gtk4_runtime.py
```

The general diagnostic reports OS/session versions, relevant package versions, active theme settings, installed GoreeCloud files, exact installed Zorin base stylesheet sizes/hashes, and targeted compatibility evidence. The GTK 4 runtime diagnostic inspects user GTK 4 configuration, installed GoreeCloud GTK 4 state rules, selected process override variables when Settings is already running, and bounded provider-path strings from the installed libadwaita library. These diagnostics change no settings and write no system files.

When `strace` is already installed and direct launch-time provider evidence is required, completely close Settings first, then run:

```bash
./scripts/trace_gtk4_runtime.sh
```

The focused trace launches a temporary `gnome-control-center search` process under `strace`, captures the complete short observation window to a temporary file, filters icon-theme noise only after capture, summarizes whether user-local or system GTK 4/GTK 3 theme paths were seen or successfully opened, and removes the temporary trace on exit. It does not install packages, copy themes into system directories, populate `~/.config/gtk-4.0`, or alter theme settings. The traced Settings process is stopped by `timeout` at the end of the observation window.

GTK 3 path activity from a traced child process is not sufficient to classify the GTK 4/libadwaita provider path. A valid provider conclusion requires direct user-local or system GTK 4 path evidence from the complete focused trace rather than a live stream truncated by unrelated icon lookups. The first manual trace on the target laptop demonstrated this limitation: it opened the user-local GoreeCloud GTK 3 stylesheet but the broad `ZorinBlue` filter filled the first 250 displayed lines with icon-path activity before decisive GTK 4 provider evidence appeared.

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

Current Dark target progress includes verified GoreeCloud canvas/surface rendering in Files, verified `#174F52` GoreeCloud selection styling in the Files sidebar, improved Shell Quick Settings/date-menu/application-menu states, and coherent overview/search rendering. Settings selected-navigation and checked-switch image-backed states remain under target-device acceptance pending direct GTK 4/libadwaita provider-path evidence.

The current draft must remain open until the documented Zorin OS 17.3 real-device visual/accessibility checks, Light/Dark/DeepDark acceptance, representative native/libadwaita application coverage, rollback verification, review/merge, and release qualification are complete.
