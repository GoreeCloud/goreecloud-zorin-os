# GoreeCloud Care

**Lifecycle:** Development  
**Version:** `0.1.0-dev18`  
**Canonical source:** `GoreeCloud/goreecloud-zorin-os` → `apps/goreecloud-care/`  
**Target:** Zorin OS 17.3 and compatible GTK 3 Linux desktops  
**License:** GPL-3.0-or-later

GoreeCloud Care is an original, local-first GoreeCloud desktop maintenance application. It previews reclaimable storage before deletion, keeps routine cache/temp cleanup unprivileged, provides privacy-safe read-only reports, has a bounded local Maintenance Insights review surface, and exposes a narrow local read-only integration API for governed GoreeCloud platform consumers.

## Current Development features

- Scan and clean application cache files older than 7 days.
- Clean the thumbnail cache.
- Scan and clean user-owned `/tmp` files older than 7 days.
- Preview Trash usage and empty Trash only after a separate permanent-deletion confirmation.
- Preview APT `.deb` cache and clean it through PolicyKit authorization.
- Display disk, available-memory, and file-cache status.
- “Memory Refresh” action that truthfully reclaims Linux file caches after a warning and PolicyKit authorization. It does **not** claim a lasting RAM/performance boost.
- Explicit cancellation, failure, partial-success, and completion reporting.
- Post-action refresh that updates scan values without replacing the final completion/exception status.
- Current-Stable GLAZE UI V1.2 native GTK3 fallback with neutral material surfaces, semantic accent/status color, system Light/Dark resolution, explicit Deep Dark Development testing, 48-pixel minimum targets, Reduced Transparency, Reduced Motion, and system-authoritative HighContrast.
- Adaptive compact layout, 200%-text effective-width behavior, vertical scrolling, and compact HeaderBar reduction.
- GTK/ATK/AT-SPI accessibility semantics, explicit Care application identity, visible focus, and HighContrast palette authority.
- Privacy-safe human/JSON maintenance reports plus local health, Privacy Shield, Wardveil-compatible security, and Everkeep continuity status output.
- Canonical GoreeCloud Care product identity sourced from `GoreeCloud/goreecloud-branding-assets/products/care/app-icon.svg` and packaged as a synchronized derivative.
- No telemetry, advertising, cloud upload, remote service, or GoreeCloud account requirement.
- Symlink-safe user cleanup and fixed privileged-action boundaries.

## Privacy-safe read-only reports

```sh
goreecloud-care --report
goreecloud-care --report-json
goreecloud-care --version
```

`--report` produces a human-readable local maintenance snapshot. `--report-json` produces schema-versioned machine-readable JSON. Both modes are read-only: they scan the same maintenance categories but never delete files, authenticate, invoke PolicyKit, or access the network.

Reports include disk headroom, memory/file-cache summary, total visible reclaimable bytes/items, per-category byte/item counts, and scan-error counts. Candidate paths, filenames, and raw scan-error strings are deliberately omitted by default so the output is safer to copy into troubleshooting or local automation workflows.

Representative-device dev13 validation is accepted at exact runtime/source head `48049b6f634a05300e01bb0e85d718284b79d7ee`: 38 tests plus XML/source validation passed, `0.1.0~dev13` built and upgraded over dev12, `dpkg-query` reported `install ok installed 0.1.0~dev13`, `--version` returned `0.1.0-dev13`, and both human and JSON reports executed successfully.

## Local platform integration API — dev18

Dev18 adds an explicit local-only command API. It does not start an HTTP server, open a listening socket, or add a network dependency.

```sh
goreecloud-care --api-version
goreecloud-care --health-json
goreecloud-care --privacy-status-json
goreecloud-care --security-status-json
goreecloud-care --continuity-status-json
```

The API version is `1`. `--health-json` produces minimized readiness/status information. `--privacy-status-json` uses the current Privacy Shield status shape and remains `development` / `production_approved=false` until runtime acceptance is completed. `--security-status-json` emits a narrowly scoped Wardveil-compatible status for Care’s installed helper/PolicyKit boundary and deliberately keeps `protected_by_wardveil=false`. `--continuity-status-json` fails closed to `attention` until representative-device package rollback has actually been accepted.

Repository-local Privacy Shield application/adapter declarations, Everkeep adoption and acceptance declarations, and the Wardveil integration boundary live in `contracts/`, `API.md`, and `WARDVEIL-INTEGRATION.md`. These source declarations are integration foundations, not production approval. The authoritative Privacy Shield-side Care adapter registration is currently proposed in Draft PR 17 and intentionally remains `production_approved=false`.

## Maintenance Insights — dev14 foundation through dev17 refinement

Launch the Development review surface with:

```sh
goreecloud-care --insights-ui
```

The installed desktop entry also exposes **Maintenance Insights (Read-only)** as a desktop action.

The Insights engine is deliberately bounded and read-only. It currently reviews largest stale application-cache groups using the same >7-day policy as routine Care cleanup, large files of at least 250 MB in standard user folders, Downloads at least 30 days old, aggregate scan-error count, and bounded-discovery truncation state. Symlinks are not followed. The standard-folder crawl is capped at 50,000 visited entries per refresh. Local file paths may be shown only inside the explicitly requested review window; default reports remain path-redacted. No finding is automatically selected for deletion and the Insights modules contain no cleanup, PolicyKit, privileged-helper, subprocess, or network execution path.

Dev16 representative-device screenshots verified the compact `Insights` title, visible Refresh focus, and true-bottom findings reachability. Dev17 then replaced the synthetic-hyphen-prone character-wrapped `Gtk.TextView` with a selectable Pango-backed `Gtk.Label` using `WORD_CHAR` and `insert_hyphens='false'`. On the representative Zorin OS laptop, exact dev17 head `0fda6f90a545eaf3d1bed525aae98c6529ebbf7b` passed all 50 tests plus XML/source validation, built and installed `0.1.0~dev17`, eliminated the observed synthetic mid-word hyphens, retained compact/wide readability and visible Refresh focus, and reached the true bottom with 24,247 inspected user-folder entries and 0 scan errors. Those values are run-specific evidence, not product guarantees.

Dev18 adds automated headless GTK acceptance for enlarged-text compact/regular composition, selectable-results focus traversal, repeated resize behavior, accessible status mutation, and the process-level GLAZE UI V1.2 native fallback. This remains automated Linux evidence; it does not substitute for representative-device drag-resize or live AT-SPI/Orca acceptance.

## Current GLAZE UI V1.2 boundary

The required current Stable consumer target is **GLAZE UI V1.2 / `1.2.0`**. Care’s Development mapping follows the governing material rule **Neutral glass is the material. Color is an accent.** GTK3 does not claim compositor-wide backdrop blur, so Care intentionally uses a bounded V1.2 degradation path: neutral translucent/solid material, semantic blue/status color, no nonessential animation dependency, and accessibility behavior that outranks optical effects.

Development acceptance overrides support reproducible Light/Dark/Deep Dark, Reduced Transparency, and Reduced Motion checks without changing desktop-wide preferences. HighContrast removes the Care/Glaze palette provider so the system remains authoritative.

Historical V1.1-era evidence remains valid only for the exact behaviors and revisions it exercised. Full product-specific V1.2 conformance is not yet complete. See `GLAZE-UI-CONFORMANCE.md` for the fail-closed mapping and remaining exact-candidate gates.

## Build and test

```sh
sh ./scripts/validate.sh
sh ./scripts/build-deb.sh
```

The Development CI also runs the GTK runtime probe under Xvfb, inspects the Debian package, generates a SHA-256 file, and preserves the exact package/checksum as a short-lived workflow artifact. A successful Development artifact remains evidence only; it is not a Release Candidate or Stable release by itself.

## Package lifecycle acceptance

The representative target can exercise the recovery gate with:

```sh
sudo sh ./scripts/validate-package-lifecycle.sh \
  ./dist/goreecloud-care_0.1.0~dev18_all.deb \
  /path/to/retained/previous-development-package.deb
```

The script validates candidate install, removal, reinstall, explicit downgrade, candidate restoration, and final installed state without invoking Care cleanup actions. Everkeep continuity remains non-ready until this exact-candidate lifecycle evidence is actually accepted on the supported target.

## Install or upgrade a locally built Development package

```sh
sudo apt install ./dist/goreecloud-care_0.1.0~dev18_all.deb
```

Uninstall with:

```sh
sudo apt remove goreecloud-care
```

## Release boundary

The generated Debian package remains Development software. Exact-head dev18 V1.2 regression CI, representative appearance/resilience and drag-resize checks, live keyboard/AT-SPI/Orca acceptance, package rollback, canonical icon target rendering, current-Stable GLAZE UI V1.2 consumer acceptance, Privacy Shield runtime acceptance, Wardveil adoption/runtime acceptance, Everkeep continuity acceptance, and governed immutable Release Candidate qualification remain required before Stable consideration.

The canonical source-control authority is `GoreeCloud/goreecloud-zorin-os`. GoreeCloud Care is maintained as the `apps/goreecloud-care/` component so its Zorin OS packaging, desktop integration, target-device acceptance, and Platform Contract evidence remain coupled to the GoreeCloud Zorin OS development surface while preserving a distinct application boundary.
