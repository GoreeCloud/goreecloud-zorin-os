# GoreeCloud Themes for Zorin OS

This repository contains the Development-stage GoreeCloud desktop experience for the verified Zorin OS 17.3 target environment.

The project is now **light-first**. `GoreeCloud-Zorin-Light` is the primary experience and the installer activates it together with the GoreeCloud icon theme, cursor theme, and primary light wallpaper. Dark and Deep Dark remain secondary compatibility variants.

## Desktop assets

The repository currently provides:

- `GoreeCloud-Zorin-Light` — primary Applications/Shell theme;
- `GoreeCloud-Zorin-Dark` — secondary compatibility theme;
- `GoreeCloud-Zorin-DeepDark` — secondary compatibility theme;
- `GoreeCloud-Zorin` — light-first icon theme;
- `GoreeCloud-Zorin-Cursors` — Frost White + GoreeCloud Blue Xcursor theme;
- 24 identity-derived GoreeCloud wallpapers;
- recovery-backed replacement of the audited Zorin OS 17.3 stock wallpaper set.

The V1.1 palette remains the default compatibility build contract while the repository carries a parallel Glaze UI V1.2 Development preview in `config/palettes-v1.2.json`.

## Verified target

The installer supports the exact verified Zorin OS 17.3 theme package target. It fail-closes unless the local `zorin-desktop-themes` package and recorded GTK 3, GTK 4/libadwaita, and GNOME Shell base hashes match the tested environment.

The repository does not redistribute Zorin base-theme bytes. During installation, the composer reads and verifies the already-installed local Zorin theme files, copies them into temporary generated GoreeCloud themes, rewrites only the verified target GTK 4 selected/checked state blocks, and appends GoreeCloud semantic overrides.

## Install the GoreeCloud desktop experience

```bash
./scripts/install.sh
```

The default install:

- generates and installs all three Applications/Shell variants under `~/.local/share/themes`;
- builds and installs `GoreeCloud-Zorin` under `~/.local/share/icons`;
- builds and installs `GoreeCloud-Zorin-Cursors` under `~/.local/share/icons`;
- activates `GoreeCloud-Zorin-Light` for Applications;
- activates `GoreeCloud-Zorin-Light` for Shell when the User Themes extension schema is available;
- activates the GoreeCloud icon theme;
- activates the GoreeCloud cursor theme;
- installs the complete wallpaper collection;
- applies the primary light wallpaper.

Existing GoreeCloud theme/icon/cursor directories are moved into timestamped recovery storage before replacement.

## Replace the stock Zorin wallpapers

To install the GoreeCloud desktop experience and then remove the exact audited Zorin OS 17.3 stock wallpaper packages:

```bash
./scripts/install.sh --replace-stock
```

The replacement path verifies the target OS, exact stock wallpaper package versions, exact package-owned wallpaper/catalog paths, the complete GoreeCloud replacement catalog, and an `apt-get --simulate purge` removal set containing only the audited wallpaper packages. It creates recovery material and downloads the exact recovery `.deb` set before performing the purge.

The same workflow is available independently:

```bash
./scripts/wallpaper.sh replace-stock plan
./scripts/wallpaper.sh replace-stock apply
./scripts/wallpaper.sh replace-stock status
./scripts/wallpaper.sh replace-stock restore
./scripts/wallpaper.sh replace-stock finalize
```

`restore` reinstalls the archived exact packages/fileset. `finalize` removes recovery material only after the stock set remains absent and the GoreeCloud replacement catalog remains valid.

## Icon theme

The icon contract is recorded in:

```text
config/desktop-assets.json
```

Build the icon theme without installing it:

```bash
python3 ./scripts/build_icons.py --output /tmp/goreecloud-icons
```

The generated icon theme is named:

```text
GoreeCloud-Zorin
```

It uses the light-first Glaze/GoreeCloud palette: Frost White, Crystal White, Ice Blue, Glacier Blue, GoreeCloud Primary Blue, Deep Blue, and graphite structure. The initial custom set covers core folders/places, home/desktop/trash, storage/devices, computer/phone/flash media, and `start-here`/GoreeCloud identity. Unoverridden icons inherit from the platform icon stack rather than disappearing.

The `start-here` and GoreeCloud identity icons preserve the synchronized canonical GoreeCloud mark already pinned by the repository branding authority.

## Cursor theme

Build the cursor theme without installing it:

```bash
python3 ./scripts/build_cursors.py --output /tmp/goreecloud-cursors
```

The generated Xcursor theme is named:

```text
GoreeCloud-Zorin-Cursors
```

It is generated with Python standard-library code and does not require `xcursorgen` at install time. The theme contains 24px, 32px, and 48px Xcursor image frames and custom Frost White / GoreeCloud Blue treatments for pointer, hand, text, crosshair, move, wait/progress, blocked, and resize cursor families, with common Xcursor aliases included.

## Wallpaper collection

The repository defines **24 3840×2160 SVG wallpapers** across GoreeCloud, Glaze UI, Wardveil Security, and Privacy Shield.

The wallpaper source is identity-derived rather than generic abstract artwork. Canonical branding authority is `GoreeCloud/goreecloud-branding-assets`; `config/wallpaper-identities.json` pins the authority commit, source path, synchronized copy, SHA-256, and viewBox used by generation.

The light variants are the primary desktop presentation. Wallpaper source is intentionally isolated from semantic interaction/status color tokens so focus, selection, warning, and destructive UI colors cannot silently recolor identity artwork.

Install or refresh wallpapers:

```bash
./scripts/wallpaper.sh install
```

Apply the default light wallpaper:

```bash
./scripts/wallpaper.sh apply default
```

List the collection:

```bash
./scripts/wallpaper.sh list
```

Wallpaper files are installed under:

```text
~/.local/share/backgrounds/GoreeCloud-Zorin
```

The generated GNOME background catalog is installed at:

```text
~/.local/share/gnome-background-properties/goreecloud-zorin.xml
```

## Uninstall

```bash
./scripts/uninstall.sh
```

If the GoreeCloud GTK, Shell, icon, or cursor themes are currently selected, uninstall resets the corresponding GNOME setting to its distro default before moving the GoreeCloud files into timestamped recovery storage. Wallpaper package recovery is managed separately through `wallpaper.sh replace-stock restore` when stock wallpapers were removed.

## Validation

Run the complete source validation set with:

```bash
./scripts/validate.sh --gtk
python3 ./scripts/validate_wallpapers.py
python3 ./scripts/validate_desktop_assets.py
python3 ./scripts/validate_v12_preview.py
python3 ./scripts/validate_system_wallpapers.py
```

Desktop-asset validation builds the icon and cursor themes in a temporary directory, validates generated SVG safety and minimum icon coverage, verifies canonical `start-here` identity preservation, parses the generated Xcursor binary format, checks all required cursor aliases, frame sizes, dimensions, and hotspots, and confirms the light-first contract.

CI runs ShellCheck plus wallpaper, icon/cursor, V1.2 preview, stock-wallpaper safety, and generated GTK theme validation.

## Target diagnostics

Read-only target evidence tools include:

```bash
./scripts/diagnose.sh
python3 ./scripts/diagnose_gtk4_runtime.py
./scripts/diagnose_settings_css.sh
./scripts/diagnose_backgrounds.sh
```

The Development installer composes from the verified local Zorin 17.3 GTK 3, GTK 4/libadwaita, and GNOME Shell bases. Flatpak and Snap applications may retain bundled or sandboxed appearance behavior; browser chrome and web content can also use independent themes.

## Status

Development / Draft. The primary product direction is the light GoreeCloud experience. Source presence, installation success, green CI, or individual screenshots do not by themselves establish Stable qualification; real-device visual/accessibility acceptance remains revision-specific.
