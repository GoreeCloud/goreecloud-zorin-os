# GoreeCloud Zorin Wallpaper Collection

## Status

Development. The collection source is implemented; target-device acceptance is partial.

The target laptop has rendered **GoreeCloud Horizon Dark** successfully at its current desktop resolution with readable panel/dock chrome and no obvious crop failure in the supplied full-desktop screenshot. Zorin Settings now also visibly consumes the generated user-scoped catalog: the supplied Background view shows the 24 GoreeCloud wallpapers ahead of the still-present stock Zorin set. This verifies catalog discovery and thumbnail rendering for the collection as a gallery, but it does not yet visually accept every wallpaper individually.

## Scope

This repository defines **24 original 3840×2160 SVG wallpapers** across four balanced categories:

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
config/zorin-stock-wallpapers-17.3.json
scripts/build_background_catalog.py
scripts/validate_wallpapers.py
scripts/validate_system_wallpapers.py
scripts/wallpaper.sh
scripts/diagnose_backgrounds.sh
scripts/system_wallpapers.py
scripts/system_wallpapers.sh
```

`config/wallpapers.json` keeps the three Horizon wallpapers as the primary Light/Dark/DeepDark mapping for `apply current`, while the full `catalog` contains all 24 options.

`config/zorin-stock-wallpapers-17.3.json` is the evidence-bound removal manifest for the verified Zorin OS 17.3 laptop. It is intentionally pinned to the audited package versions, three system background catalogs, and 28 package-owned stock JPEG paths. If those facts change, the privileged removal workflow must fail closed until new target evidence is captured.

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

Target evidence now verifies that Zorin OS 17.3 Settings consumes this user-scoped catalog and renders all 24 GoreeCloud thumbnails in the Background gallery.

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

The target audit is complete. It identifies the stock wallpaper set as package-owned by exactly:

```text
zorin-os-wallpapers          17.1
zorin-os-wallpapers-17       17.1
zorin-os-pro-wallpapers      17
zorin-os-pro-wallpapers-17   17
```

The audited active stock set consists of three GNOME Background Properties XML catalogs and 28 JPEG files under `/usr/share/backgrounds`. The exact paths and expected owners are recorded in `config/zorin-stock-wallpapers-17.3.json`.

The ordinary theme/wallpaper installer still never modifies or deletes system wallpaper packages. Privileged removal is isolated in `scripts/system_wallpapers.sh`.

### Controlled removal sequence

First run the read-only plan:

```bash
./scripts/system_wallpapers.sh plan
```

`plan` verifies:

1. the host is the verified Zorin OS 17.3 target;
2. all four audited wallpaper packages are installed at the exact recorded versions;
3. every audited stock path exists and has the expected package owner;
4. the 24-wallpaper GoreeCloud user catalog and all referenced SVGs are ready;
5. `apt-get --simulate purge` proposes removal of exactly the four audited wallpaper packages and no other package.

Only after the plan output is reviewed should privileged removal run:

```bash
sudo ./scripts/system_wallpapers.sh apply
```

Before package removal, `apply` captures the exact stock files in a root-owned recovery archive, records checksums and package state, saves the apt simulation, and downloads the exact four `.deb` packages into the recovery transaction. It then re-runs all preconditions and purges only the audited wallpaper packages. Any package-version, ownership, path, replacement-catalog, recovery-download, or apt-removal-set mismatch aborts the operation.

After `apply`, reopen Settings → Background and verify that only the intended GoreeCloud collection remains. Keep the recovery transaction until this screenshot/visual acceptance is complete.

Rollback remains available with:

```bash
sudo ./scripts/system_wallpapers.sh restore
```

`restore` reinstalls the archived exact wallpaper packages, restores the captured stock files, checks the recorded SHA-256 values, and verifies the package/path state.

Only after removal is visually accepted and rollback is no longer required should the recovery copy be irreversibly deleted:

```bash
sudo ./scripts/system_wallpapers.sh finalize
```

`finalize` is deliberately separate from `apply`. It is refused unless the stock packages and audited stock paths remain absent and the 24-wallpaper GoreeCloud replacement catalog is still ready.

Do not use broad recursive deletion of `/usr/share/backgrounds`, manually remove unrelated files, or purge wallpaper packages outside this evidence-bound workflow.

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
- the exact Zorin OS 17.3 stock-package/version/catalog/path manifest;
- the four-package no-collateral purge safety contract;
- recovery/restore/finalize workflow presence;
- executable/syntax/ShellCheck validation for wallpaper helpers.

Static checks do not establish actual package-removal success or visual acceptance.

## Remaining target acceptance

Before release qualification, complete the read-only system-removal plan, then the controlled removal and post-removal Settings verification if the plan is clean. Keep recovery until the post-removal gallery is accepted. Also verify representative Light/Dark/DeepDark wallpapers, panel/dock/icon readability, wallpaper settings restore, package-removal rollback, and the broader theme acceptance gates. The PR remains Draft until those checks are complete.
