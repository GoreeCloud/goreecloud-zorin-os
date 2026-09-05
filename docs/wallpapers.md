# GoreeCloud Zorin Wallpaper Collection

## Status

Development. The collection source is implemented; target-device acceptance is partial.

The target laptop has rendered **GoreeCloud Horizon Dark** successfully at its current desktop resolution with readable panel/dock chrome and no obvious crop failure in the supplied full-desktop screenshot. That evidence applies only to this wallpaper and view. The remaining 23 wallpapers, user-catalog discovery, restore behavior, and any system-wide stock-wallpaper replacement still require direct target verification.

## Scope

This repository now defines **24 original 3840×2160 SVG wallpapers** across four balanced categories:

| Category | Families | Count |
| --- | --- | ---: |
| GoreeCloud | Horizon, Meridian | 6 |
| Glaze UI | Aurora, Lattice | 6 |
| Wardveil Security | Core, Fold | 6 |
| Privacy Shield | Bands, Filter | 6 |
| **Total** | 8 families × Light/Dark/Deep Dark | **24** |

Every family has Light, Dark, and Deep Dark variants mapped to the same GLAZE UI V1.1 / 1.1.0 palette roles used by the desktop theme.

Wardveil Security and Privacy Shield wallpapers are **supporting abstract identity artwork**, not canonical product marks and not security/privacy status indicators. Wardveil compositions use calm paired veil/core geometry; Privacy Shield compositions use layered privacy-band/filter geometry. They intentionally avoid generic padlocks, checkmarks, hacker imagery, neon threat graphics, and other misleading security/privacy symbolism.

## Source

```text
assets/wallpapers/
config/wallpapers.json
scripts/build_background_catalog.py
scripts/validate_wallpapers.py
scripts/wallpaper.sh
scripts/diagnose_backgrounds.sh
```

`config/wallpapers.json` keeps the three Horizon wallpapers as the primary Light/Dark/DeepDark mapping for `apply current`, while the full `catalog` contains all 24 options.

## User-local install and catalog

Run:

```bash
./scripts/wallpaper.sh install
./scripts/wallpaper.sh list
```

The helper copies all 24 SVGs to:

```text
~/.local/share/backgrounds/GoreeCloud-Zorin
```

and generates a user-scoped GNOME Background Properties catalog at:

```text
~/.local/share/gnome-background-properties/goreecloud-zorin.xml
```

Whether Zorin OS 17.3 Settings consumes the user-scoped catalog is a target-runtime behavior and must be verified; source generation alone does not prove the 24 thumbnails will appear in Settings.

Apply the primary wallpaper matching the active GoreeCloud theme:

```bash
./scripts/wallpaper.sh apply current
```

Or apply any exact ID from `./scripts/wallpaper.sh list`, for example:

```bash
./scripts/wallpaper.sh apply glaze-aurora-dark
./scripts/wallpaper.sh apply wardveil-core-dark
./scripts/wallpaper.sh apply privacy-bands-dark
./scripts/wallpaper.sh apply goreecloud-meridian-dark
```

Applying a wallpaper records a GNOME settings snapshot first. Restore the latest snapshot with:

```bash
./scripts/wallpaper.sh restore
```

## Stock Zorin wallpaper replacement

The project requirement is to replace the stock Zorin wallpaper set with the GoreeCloud collection. Permanently deleting package-owned system files is a privileged destructive operation and is not performed by the ordinary theme or wallpaper installer.

Before a system replacement implementation is accepted, run the read-only target audit:

```bash
./scripts/diagnose_backgrounds.sh
```

The audit reports the actual Zorin 17.3 background-property catalogs, wallpaper roots, package ownership, wallpaper-related packages, and current GNOME background settings. This evidence is required before defining the exact files/packages to remove or divert.

The intended controlled migration is:

1. identify the exact stock catalogs/files and owning packages on the target;
2. preserve a restorable system recovery copy;
3. install the 24 GoreeCloud assets and a system background catalog;
4. remove the stock entries from the Settings gallery;
5. verify Settings shows only the intended GoreeCloud set;
6. verify desktop, login/lock/background behavior and package-update behavior;
7. only after acceptance, permanently purge the preserved stock recovery material if still desired.

Do not use broad recursive deletion of `/usr/share/backgrounds` or guess wallpaper package names. Package updates may also recreate package-owned wallpaper files, so “permanent” replacement must be verified against the actual package ownership/update model.

## Validation

Source validation covers:

- at least 20 assets, currently exactly 24;
- all four required categories with at least five options each;
- unique IDs and Light/Dark/DeepDark mappings;
- exact Glaze palette-role mapping;
- 3840×2160 SVG size/viewBox;
- no script elements;
- no remote, file, or embedded-data href resources;
- generated GNOME catalog count and filenames;
- executable/syntax validation for wallpaper helpers.

Static checks do not establish visual quality or system replacement success.

## Remaining target acceptance

Before release qualification, verify all 24 wallpapers in representative desktop views, the generated user catalog, Light/Dark/DeepDark visual balance, panel/dock/icon readability, wallpaper restore, and the eventual system replacement/rollback path. The PR remains Draft until those and the broader theme acceptance gates are complete.
