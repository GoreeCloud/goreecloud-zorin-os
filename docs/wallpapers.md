# GoreeCloud Zorin Wallpaper Collection

## Status

Development. Source implementation is identity-derived; target-device visual acceptance is pending for the redesigned artwork.

The earlier 24-wallpaper abstract collection was rejected during target review because its compositions did not match the current approved GoreeCloud, Glaze UI, Wardveil Security, and Privacy Shield artwork closely enough. That visual direction is superseded by the current identity-derived source and must not be treated as accepted wallpaper artwork.

The installed/default theme path remains the Glaze UI V1.1-compatible path while the repository carries a parallel **Glaze UI V1.2 development preview**. V1.2 is not Stable and does not inherit V1.1 acceptance automatically.

## Scope

The repository defines **24 3840×2160 SVG wallpapers** across four balanced categories:

| Category | Identity / families | Count |
| --- | --- | ---: |
| GoreeCloud | Unified Clean — Horizon, Meridian | 6 |
| Glaze UI | Facet — Aurora, Lattice | 6 |
| Wardveil Security | Sentinel Fold — Core, Veil | 6 |
| Privacy Shield | Approved Privacy Shield — Bands, Filter | 6 |
| **Total** | 8 families × Light/Dark/Deep Dark | **24** |

Every wallpaper preserves the canonical identity geometry and identity colors from the current unified branding authority. The surrounding field is intentionally environmental: neutral structure, low-frequency depth, restrained cold light, and generous quiet regions rather than a second brand mark or a semantic UI surface.

## Wallpaper visual contract

The redesigned source follows these rules:

- canonical marks keep their approved geometry and identity colors;
- GoreeCloud environmental light uses the approved platform blues rather than the theme's former Mineral Teal accent;
- Glaze UI, Wardveil Security, and Privacy Shield keep their own canonical identity color families;
- marks are subordinate to desktop work rather than oversized hero artwork;
- composition favors large calm regions, low-frequency detail, and restrained optical depth;
- wallpaper does not consume focus, selection, destructive, warning, or other semantic UI color tokens;
- changing the interactive theme accent must not silently recolor wallpaper identity artwork;
- wallpaper remains non-semantic and must not imply security, privacy, compliance, or runtime state.

This keeps family resemblance in the optical grammar while allowing every GoreeCloud identity to remain distinct.

## Branding authority and synchronization

Canonical identity authority is:

```text
GoreeCloud/goreecloud-branding-assets
```

The exact authority commit and synchronized source metadata are pinned in:

```text
config/wallpaper-identities.json
```

Synchronized consumer copies live under:

```text
assets/wallpapers/identity/
```

They are retained only so wallpaper generation works reproducibly and offline. They are not independent branding masters. The wallpaper builder verifies every synchronized SVG against its pinned SHA-256 before rendering.

Current canonical sources used by the wallpaper collection are:

- GoreeCloud Unified Clean transparent/reversed marks from `official/`;
- Glaze UI **Facet** from `systems/glaze-ui/glaze-ui-mark.svg`;
- Wardveil Security **Sentinel Fold** from `systems/wardveil-security/wardveil-security-icon.svg`;
- the approved Privacy Shield icon from `systems/privacy-shield/privacy-shield-icon.svg`.

GoreeCloud's official mark is never arbitrarily recolored or redrawn. Dark and Deep Dark wallpapers use the approved reversed variant. Glaze UI, Wardveil Security, and Privacy Shield preserve the identity colors already authored in their canonical SVGs. Glaze presentation effects may surround the marks without modifying their canonical geometry.

Wardveil Security and Privacy Shield artwork identifies those systems only. A wallpaper does not prove security protection, privacy state, runtime status, compliance, or production readiness.

## Generation

Wallpaper definitions are recorded in `config/wallpapers.json`. All 24 are generated from identity-aware templates under:

```text
assets/wallpapers/templates/
```

Build the current V1.1-compatible collection with:

```bash
python3 ./scripts/build_wallpapers.py --output /tmp/goreecloud-wallpapers
```

Build the same identity-derived source against the V1.2 development environmental palette with:

```bash
python3 ./scripts/build_wallpapers.py \
  --palette-config config/palettes-v1.2.json \
  --output /tmp/goreecloud-wallpapers-v1.2
```

The builder injects the verified canonical SVG interior into a nested SVG using the original canonical viewBox. It does not trace, approximate, recolor, or regenerate the logo geometry.

## V1.2 preview boundary

`config/palettes-v1.2.json` is a development contract, not a replacement for the accepted predecessor. It introduces the proposed Frost White, Ice Blue, Clear Translucency, Cool Graphite, and Blue-Black environment while preserving the current theme IDs so the same Zorin integration can be exercised in a controlled preview build.

Validate the preview contract with:

```bash
python3 ./scripts/validate_v12_preview.py
```

That check validates the V1.2 lifecycle/version metadata, the Light/Dark/Deep Dark signature colors, baseline contrast gates, and successful rendering of all theme and wallpaper variants from the preview palette. It is a source gate only; target-device visual/accessibility acceptance remains required.

## User-local install and catalog

Run:

```bash
./scripts/wallpaper.sh install
./scripts/wallpaper.sh list
```

The helper installs all 24 SVGs under:

```text
~/.local/share/backgrounds/GoreeCloud-Zorin
```

and generates the user GNOME Background Properties catalog at:

```text
~/.local/share/gnome-background-properties/goreecloud-zorin.xml
```

Target evidence already confirms Zorin OS 17.3 Settings consumes this user-scoped catalog and displays the complete 24-entry collection. That discovery result applies to the catalog mechanism, not to visual acceptance of the redesigned artwork.

Apply the primary identity-derived wallpaper matching the active GoreeCloud theme with:

```bash
./scripts/wallpaper.sh apply current
```

Or apply any exact ID shown by `./scripts/wallpaper.sh list`.

Applying a wallpaper records a GNOME settings snapshot first. Restore the latest snapshot with:

```bash
./scripts/wallpaper.sh restore
```

## Stock Zorin wallpaper replacement

The desired end state remains a GoreeCloud-only wallpaper gallery. The audited recovery-backed stock-removal tooling exists, but **privileged stock wallpaper removal is paused while the redesigned identity-derived collection is awaiting target visual acceptance**.

Do not run the privileged `apply` or `finalize` stock-removal subcommands until the redesigned 24-wallpaper set is installed, reviewed, and accepted on the target laptop.

The read-only audit/plan paths remain available for inspection without changing packages.

## Validation

`python3 ./scripts/validate_wallpapers.py` verifies:

- exactly 24 catalog entries across the four required categories;
- Light, Dark, and Deep Dark mappings;
- V1.1 manifest compatibility metadata;
- pinned branding authority and synchronized canonical SVG SHA-256 values;
- canonical identity viewBoxes;
- identity/category mapping for every wallpaper;
- presence of canonical geometry in every rendered derivative;
- wallpaper source does not consume semantic interaction/status color tokens;
- 3840×2160 rendered dimensions and viewBox;
- no script elements or remote/file/data href resources;
- generated GNOME background catalog count and filenames.

Source validation proves reproducibility and identity-source integrity. It does not prove visual quality on the target display.

## Remaining target acceptance

Install the redesigned collection on the Zorin OS 17.3 laptop, reopen Settings → Background, review the 24 thumbnails and representative full-desktop renders, and verify that Unified Clean, Facet, Sentinel Fold, and Privacy Shield are visibly faithful to their canonical artwork in Light/Dark/Deep Dark contexts.

For V1.2, review the same representative set against the Frost/Graphite preview and include bright, dark, saturated, and detailed wallpaper stress cases, increased contrast, reduced transparency where applicable, and 200% text before promoting the preview. Only after the redesigned collection is accepted should stock wallpaper removal resume.
