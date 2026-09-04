# GoreeCloud Horizon Wallpapers

## Status

Development / source-implemented. Target-device visual acceptance is still required.

## Purpose

`GoreeCloud Horizon` is an original wallpaper family for the GoreeCloud Zorin OS theme. The artwork is stored directly in this repository as scalable SVG source and is designed to replace the visual role of the stock desktop wallpaper without copying or redistributing Zorin wallpaper assets.

The collection follows the current GLAZE UI V1.1 / 1.1.0 palette used by this repository.

## Variants

| Wallpaper | Theme | Native canvas | Primary palette |
| --- | --- | --- | --- |
| `goreecloud-horizon-light.svg` | `GoreeCloud-Zorin-Light` | 3840×2160 | `#F4F7F8`, `#0F6B6F`, `#8FD6D2` |
| `goreecloud-horizon-dark.svg` | `GoreeCloud-Zorin-Dark` | 3840×2160 | `#101A20`, `#1C8A8D`, `#8FD6D2` |
| `goreecloud-horizon-deep-dark.svg` | `GoreeCloud-Zorin-DeepDark` | 3840×2160 | `#081016`, `#1C8A8D`, `#8FD6D2` |

All three use a restrained horizon/ridge composition, mineral-teal atmospheric treatment, and a small amber atmosphere token. They contain no external images, scripts, remote resources, or Zorin artwork.

## Repository layout

```text
assets/wallpapers/
  goreecloud-horizon-light.svg
  goreecloud-horizon-dark.svg
  goreecloud-horizon-deep-dark.svg
config/wallpapers.json
scripts/wallpaper.sh
```

## User-local installation

The main theme installer copies the wallpaper files to:

```text
~/.local/share/backgrounds/GoreeCloud-Zorin
```

It does not remove or overwrite files under `/usr/share/backgrounds`.

The current desktop wallpaper changes only when explicitly requested:

```bash
./scripts/wallpaper.sh apply current
```

The `current` mode maps the active GoreeCloud GTK theme to the matching wallpaper. Explicit modes are also supported:

```bash
./scripts/wallpaper.sh apply light
./scripts/wallpaper.sh apply dark
./scripts/wallpaper.sh apply deep-dark
```

Before modifying GNOME background settings, the helper stores a snapshot under `${XDG_STATE_HOME:-~/.local/state}/goreecloud-zorin/wallpaper`. Restore the newest snapshot with:

```bash
./scripts/wallpaper.sh restore
```

## Validation boundary

Source validation checks:

- exactly three wallpaper variants are declared;
- each entry maps to an existing GoreeCloud theme and matching Glaze palette roles;
- each asset is valid SVG XML with `3840×2160` dimensions and `0 0 3840 2160` view box;
- no SVG scripts or external/embedded href resources are present;
- `scripts/wallpaper.sh` is executable and shell-syntax valid.

Source validation does not prove desktop composition quality.

## Required target acceptance

Before release qualification:

1. Install all three wallpapers on the target Zorin OS 17.3 laptop.
2. Apply each wallpaper with its matching Light, Dark, or Deep Dark theme.
3. Capture full-desktop screenshots at the laptop's actual native resolution.
4. Check cropping/zoom behavior, panel/dock readability, desktop-icon readability where enabled, lock-screen/background compatibility if used, and visual balance behind representative windows.
5. Verify `./scripts/wallpaper.sh restore` returns to the prior GNOME background settings.
6. Verify no Zorin system wallpaper files were modified or deleted.

Until these checks are complete, the wallpaper collection remains Development and must not be treated as Stable wallpaper acceptance.
