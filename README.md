# GoreeCloud Themes for Zorin OS

This repository contains Development-stage GoreeCloud desktop themes and an original GoreeCloud wallpaper collection for the verified Zorin OS 17.3 target environment.

The current theme implementation provides three generated variants aligned to GLAZE UI V1.1 / 1.1.0:

- `GoreeCloud-Zorin-Light`
- `GoreeCloud-Zorin-Dark`
- `GoreeCloud-Zorin-DeepDark`

## Current target

The installer currently supports the exact verified Zorin OS 17.3 theme package target only. It fail-closes unless the local `zorin-desktop-themes` package and recorded GTK 3, GTK 4/libadwaita, and GNOME Shell base hashes match the tested environment.

The GoreeCloud repository does not redistribute Zorin base-theme or wallpaper bytes. During installation, the composer reads and verifies the already-installed local Zorin theme files, copies them into temporary generated GoreeCloud themes, and then appends GoreeCloud semantic overrides before replacing any currently installed GoreeCloud variants.

This preserves Zorin-specific compatibility while keeping GoreeCloud source focused on palette, geometry, state, compatibility overrides, and original/authorized GoreeCloud artwork.

## Theme install

```bash
./scripts/install.sh
```

Themes are installed user-locally under:

```text
~/.local/share/themes
```

Previous GoreeCloud theme folders are preserved in timestamped recovery directories rather than deleted.

After installation, open **Zorin Appearance → Theme → Other** and select the same GoreeCloud variant for **Applications** and **Shell**.

## Identity-derived wallpaper collection

The repository defines **24 3840×2160 SVG wallpapers** across GoreeCloud, Glaze UI, Wardveil Security, and Privacy Shield.

The earlier abstract wallpaper direction was rejected during target review because it did not match the current logos/artwork closely enough. The current source is therefore derived directly from the approved canonical identities rather than merely borrowing their themes or colors.

Canonical branding authority is `GoreeCloud/goreecloud-branding-assets`. `config/wallpaper-identities.json` pins the exact authority commit, canonical path, Git blob, local synchronized copy, SHA-256, and viewBox used by wallpaper generation. Current identities are:

- GoreeCloud **Unified Clean**;
- Glaze UI **Facet**;
- Wardveil Security **Sentinel Fold**;
- the approved **Privacy Shield** artwork.

The canonical artwork is embedded without tracing, approximating, arbitrary recoloring, or geometry changes. The surrounding wallpaper field uses the GoreeCloud Zorin Glaze palette and presentation language. Dark GoreeCloud wallpapers use the approved reversed Unified Clean mark rather than recoloring the full-color mark.

Install or refresh all wallpapers with:

```bash
./scripts/wallpaper.sh install
```

They are installed user-locally under:

```text
~/.local/share/backgrounds/GoreeCloud-Zorin
```

The generated GNOME Background Properties catalog is installed at:

```text
~/.local/share/gnome-background-properties/goreecloud-zorin.xml
```

List exact IDs with:

```bash
./scripts/wallpaper.sh list
```

Apply the primary wallpaper matching the active GoreeCloud GTK theme:

```bash
./scripts/wallpaper.sh apply current
```

Or apply a specific wallpaper ID. Before changing GNOME background settings, the helper stores a restorable snapshot under:

```text
~/.local/state/goreecloud-zorin/wallpaper
```

Restore the latest saved settings with:

```bash
./scripts/wallpaper.sh restore
```

See `docs/wallpapers.md` for identity authority, synchronization, validation, and acceptance details.

### Stock Zorin wallpapers

Target evidence identifies the exact package-owned Zorin OS 17.3 wallpaper set and a recovery-backed removal workflow is implemented. However, privileged stock-wallpaper removal is **paused until the redesigned identity-derived 24-wallpaper collection is visually accepted on the target laptop**.

Do not run the privileged stock removal/finalization path merely because source validation passes. The redesigned replacements must be installed and reviewed first.

## Target diagnostics

For read-only target evidence:

```bash
./scripts/diagnose.sh
python3 ./scripts/diagnose_gtk4_runtime.py
./scripts/diagnose_settings_css.sh
./scripts/diagnose_backgrounds.sh
```

The general diagnostic reports OS/session versions, relevant package versions, active theme settings, installed GoreeCloud files, exact installed Zorin base stylesheet sizes/hashes, and targeted compatibility evidence. The Settings/runtime diagnostics are evidence tools and do not change theme settings.

When `strace` is already installed and direct launch-time provider evidence is required, completely close Settings first, then run:

```bash
./scripts/trace_gtk4_runtime.sh
```

On the verified Zorin OS 17.3 target, the focused trace and direct ELF dependency inspection establish that GNOME Settings 41.7 is a GTK 3 + libhandy application: the Settings process opens the user-local GoreeCloud GTK 3 stylesheet and links directly to `libgtk-3`, `libgdk-3`, and `libhandy-1`, with no direct GTK 4/libadwaita dependency.

## Validation

Static validation:

```bash
./scripts/validate.sh
python3 ./scripts/validate_wallpapers.py
```

GTK smoke loading where required dependencies are available:

```bash
./scripts/validate.sh --gtk
```

Wallpaper validation verifies the 24-entry catalog, the exact synchronized canonical identity SHA-256 values and viewBoxes, identity/category mapping, preservation of canonical geometry in every rendered derivative, Glaze palette mappings, 3840×2160 SVG dimensions, and absence of scripts or external resources.

CI runs ShellCheck, wallpaper/source integrity validation, stock-wallpaper replacement safety validation, and generated-theme validation. Green CI verifies repository source/tooling only; it does not establish target-device visual or accessibility acceptance.

## Compatibility scope

The Development installer composes from the verified local Zorin 17.3 GTK 3, GTK 4/libadwaita, and GNOME Shell bases, then appends GoreeCloud overrides. The GTK 2 shim exists for theme discovery compatibility. The `.libadwaita` marker is present only with the tested GTK 4 compatibility stylesheet.

Target evidence has shown that some Zorin states are image-backed rather than plain `background-color` states. GoreeCloud maps the verified GTK 3 and GTK 4 selected/checked mechanisms to corresponding Glaze semantic tokens rather than retaining Zorin's pale-cyan state fills.

Flatpak and Snap applications may retain bundled or sandboxed appearance behavior. Browser chrome and web content can also use independent themes and should not be treated as direct GTK acceptance evidence.

## Status

Development / Draft. Do not treat installation success, theme discovery, exact-base hash verification, local composition, green CI, wallpaper source presence, user-catalog discovery, or individual screenshots as Stable release evidence.

Current Dark target progress includes verified GoreeCloud canvas/surface rendering in Files, verified `#174F52` selection styling in Files and Settings, target-verified Settings enabled-switch tracks at Mineral Teal `#1C8A8D`, improved Shell Quick Settings/date-menu/application-menu states, and coherent overview/search rendering.

The wallpaper catalog mechanism is target-verified to appear in Zorin Settings, but the **new identity-derived artwork itself is target-unverified** until the refreshed collection is installed and visually reviewed. The previous abstract wallpaper artwork is superseded by the current redesign and is not accepted evidence.

The draft remains open until documented Zorin OS 17.3 real-device visual/accessibility checks, identity-derived wallpaper acceptance, Light/Dark/DeepDark acceptance, representative native/libadwaita application coverage, rollback verification, review/merge, and release qualification are complete.
