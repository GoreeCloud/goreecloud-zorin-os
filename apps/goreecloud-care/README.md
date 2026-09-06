# GoreeCloud Care

**Lifecycle:** Development  
**Version:** `0.1.0-dev13`  
**Canonical source:** `GoreeCloud/goreecloud-zorin-os` → `apps/goreecloud-care/`  
**Target:** Zorin OS 17.3 and compatible GTK 3 Linux desktops  
**License:** GPL-3.0-or-later

GoreeCloud Care is an original, local-first GoreeCloud desktop maintenance application. It previews reclaimable storage before deletion, keeps routine cache/temp cleanup unprivileged, and now includes privacy-safe read-only maintenance reporting for local diagnostics and future governed GoreeCloud integrations.

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
- Light appearance by default inside Care without changing the desktop-wide appearance setting.
- Adaptive compact layout, 200%-text effective-width behavior, vertical scrolling, and compact HeaderBar reduction.
- GTK/ATK/AT-SPI accessibility semantics, explicit Care application identity, visible focus, and HighContrast palette authority.
- No telemetry, advertising, cloud upload, remote service, or GoreeCloud account requirement.
- Symlink-safe user cleanup and fixed privileged-action boundaries.

## New in dev13: privacy-safe read-only reports

```sh
goreecloud-care --report
goreecloud-care --report-json
goreecloud-care --version
```

`--report` produces a human-readable local maintenance snapshot. `--report-json` produces schema-versioned machine-readable JSON. Both modes are read-only: they scan the same maintenance categories but never delete files, authenticate, invoke PolicyKit, or access the network.

Reports include disk headroom, memory/file-cache summary, total visible reclaimable bytes/items, per-category byte/item counts, and scan-error counts. Candidate paths, filenames, and raw scan-error strings are deliberately omitted by default so the output is safer to copy into troubleshooting or local automation workflows.

See `CAPABILITIES.md` for the expanded current and planned capability set and `BENEFITS.md` for product/user benefits.

## Build and test

```sh
sh ./scripts/validate.sh
sh ./scripts/build-deb.sh
```

Representative Zorin OS testing through dev5 verifies the core cleanup and privileged-maintenance functions. Dev8 accepted the combined 200%-text + compact/minimum-width adaptive-layout slice. Dev10 accepted system HighContrast palette authority, visible focus, constrained-width composition, and complete requested forward/reverse keyboard traversal. Dev12 accepted the AT-SPI `GoreeCloud Care` application-root identity and the current static roles/names/descriptions/checked/focused-state semantic slice on exact runtime head `09c3a6bcbec094dd3cb0c828de88d084fcbd5a22`.

Dynamic assistive-technology event/announcement behavior remains open. A property-change listener did not receive status events in a session that also reported an unavailable/stale AT-SPI socket. The subsequent polling harness confirmed all three routine selectors were unchecked and successfully read the initial Care status, but the submitted output did not yet include a post-click status mutation result.

Dev13 adds the read-only reporting layer, report CLI modes, disk-headroom classification, privacy-redaction tests, capability documentation, and aligned Development package metadata. Dev13 target-device build/install/report execution is not accepted until the representative laptop updates to the exact dev13 head and runs the report modes.

The generated Debian package remains Development software. Dynamic assistive-technology acceptance, package rollback, official GoreeCloud Care visual assets, full current-Stable Glaze UI V1.1 acceptance, and broader GoreeCloud platform-system acceptance remain required before Release Candidate consideration.

## Install or upgrade a locally built Development package

```sh
sudo apt install ./dist/goreecloud-care_0.1.0~dev13_all.deb
```

Uninstall with:

```sh
sudo apt remove goreecloud-care
```

The canonical source-control authority is `GoreeCloud/goreecloud-zorin-os`. GoreeCloud Care is maintained as the `apps/goreecloud-care/` component so its Zorin OS packaging, desktop integration, target-device acceptance, and Platform Contract evidence remain coupled to the GoreeCloud Zorin OS development surface while preserving a distinct application boundary.
