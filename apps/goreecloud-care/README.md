# GoreeCloud Care

**Lifecycle:** Development  
**Version:** `0.1.0-dev19`  
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
- Isolated installed Python launchers that cannot resolve a same-named package from the invoking working directory, `PYTHONPATH`, or user site.
- No telemetry, advertising, cloud upload, remote service, or GoreeCloud account requirement.
- Symlink-safe user cleanup and fixed privileged-action boundaries.

## Dev19 package/runtime isolation remediation

Representative dev18 package-lifecycle testing exposed a real packaging/security-boundary defect. After a successful dev18 install, remove, fresh reinstall, and downgrade to `0.1.0~dev17`, `dpkg-query` correctly reported dev17 installed while `goreecloud-care --version`, invoked from the dev18 source checkout, returned `0.1.0-dev18`. The installed launchers used plain `python3 -m goreecloud_care...`, so Python could import the working-tree package before the installed private package. The same ambient import path existed in the PolicyKit helper launcher. Dpkg also reported that `/usr/lib/goreecloud-care/goreecloud_care` remained non-empty after removal, consistent with private runtime bytecode residue.

Dev19 treats that result as negative lifecycle/security evidence rather than accepting rollback. Both installed launchers now use `/usr/bin/python3 -I -B -m ...`: isolated mode excludes the invoking working directory, `PYTHONPATH`, and user site from module resolution, while `-B` prevents new private bytecode writes. Debian `postinst` and `postrm` scripts remove only the fixed private `__pycache__` path so historical root-created bytecode cannot survive an upgrade/removal. Installed validation deliberately creates a fake `goreecloud_care` package in a temporary current working directory and verifies that neither the normal launcher nor the privileged helper resolves it.

This remediation advances the source/package line to dev19. It must pass exact-head CI and the full representative dev19 ↔ pinned dev17 package lifecycle before the defect or Everkeep continuity gate can be considered closed.

## Privacy-safe read-only reports

```sh
goreecloud-care --report
goreecloud-care --report-json
goreecloud-care --version
```

`--report` produces a human-readable local maintenance snapshot. `--report-json` produces schema-versioned machine-readable JSON. Both modes are read-only: they scan the same maintenance categories but never delete files, authenticate, invoke PolicyKit, or access the network. Candidate paths, filenames, and raw scan-error strings are deliberately omitted by default.

Representative-device dev13 validation remains accepted at exact runtime/source head `48049b6f634a05300e01bb0e85d718284b79d7ee`: 38 tests plus XML/source validation passed, `0.1.0~dev13` built and upgraded over dev12, `dpkg-query` reported `install ok installed 0.1.0~dev13`, `--version` returned `0.1.0-dev13`, and both report modes executed successfully.

## Local platform integration API

The current Development line exposes a local-only command API. It does not start an HTTP server, open a listening socket, or add a network dependency.

```sh
goreecloud-care --api-version
goreecloud-care --health-json
goreecloud-care --privacy-status-json
goreecloud-care --security-status-json
goreecloud-care --continuity-status-json
```

The API version is `1`. Privacy Shield remains fail-closed with `production_approved=false`; Wardveil-compatible status remains narrowly scoped and `protected_by_wardveil=false`; Everkeep continuity remains `attention` until representative rollback is accepted. The authoritative Privacy Shield-side Care adapter is still Draft PR #74.

## Maintenance Insights

Launch the read-only Development review surface with:

```sh
goreecloud-care --insights-ui
```

The engine reviews stale application-cache groups, large regular files of at least 250 MB in standard user folders, Downloads at least 30 days old, aggregate scan errors, and bounded-discovery state. Symlinks are not followed and standard-folder discovery is capped at 50,000 visited entries per refresh. Home-relative paths may appear only in the explicitly opened review UI. No finding is automatically selected for deletion and the Insights modules contain no cleanup, PolicyKit, helper, subprocess, or network execution path.

Accepted representative slices remain revision-scoped. Dev16 verified the compact `Insights` title, visible Refresh focus, and true-bottom reachability. Dev17 exact head `0fda6f90a545eaf3d1bed525aae98c6529ebbf7b` passed 50 tests plus XML/source validation, built/installed `0.1.0~dev17`, removed synthetic mid-word hyphenation, retained compact/wide readability and visible Refresh focus, and reached the true bottom. Continuous drag-resize, complete selectable-results Tab/Shift+Tab traversal, and live AT-SPI/Orca remain separate open gates.

## GLAZE UI V1.2 boundary

The required current Stable consumer target is **GLAZE UI V1.2 / `1.2.0`**, following **Neutral glass is the material. Color is an accent.** GTK3 does not claim compositor-wide backdrop blur, so Care intentionally uses a bounded native fallback emphasizing neutral material, semantic color, accessibility, reduced-transparency resilience, and reduced-motion behavior.

The authoritative Glaze registry contains GoreeCloud Care as `adoption-required`, registered at merged revision `f88aa45b4d012dcfcd04a938cb71e96f9bb107d6`. `targetVersion`, accepted reference/evidence, and `productionEligible` remain unset/false. Registration is not product-specific `accepted-v1` conformance and does not create Release Candidate or Stable eligibility.

## Build and test

```sh
sh ./scripts/validate.sh
sh ./scripts/build-deb.sh
```

Development CI verifies the exact PR source revision, runs unit/source validation and the headless GTK enlarged-text probe, builds/inspects the Debian package, generates SHA-256 provenance, and preserves the package/checksum/source-revision artifact. A green Development artifact is evidence only; it is not a Release Candidate or Stable release.

## Representative-device acceptance preparation

```sh
sh ./scripts/prepare-representative-acceptance.sh
```

The harness requires a clean tracked tree, records exact source/package/checksum provenance, performs only read-only installed snapshots when the installed runtime exactly matches `0.1.0-dev19`, and generates explicit human/manual checklists. It never invokes Care cleanup, PolicyKit, `pkexec`, `sudo`, `apt`, or network operations and never marks a manual item passed.

## Package lifecycle acceptance

Build the pinned accepted dev17 rollback package locally:

```sh
sh ./scripts/build-dev17-rollback-package.sh
```

Then exercise the lifecycle as the normal desktop user:

```sh
sh ./scripts/validate-package-lifecycle.sh \
  ./dist/goreecloud-care_0.1.0~dev19_all.deb \
  ./dist/rollback/goreecloud-care_0.1.0~dev17_all.deb
```

The lifecycle probe verifies that the previous package genuinely sorts older, then performs candidate install, removal, fresh reinstall, downgrade to dev17, dev19 restoration, and final-state validation. Runtime checks intentionally occur while the process is launched from the current Care source working directory so dev19 launcher isolation is tested directly. Removal also verifies that the private bytecode cache does not remain. No Care cleanup action is invoked by the lifecycle probe.

## Install or upgrade a locally built Development package

```sh
sudo apt install ./dist/goreecloud-care_0.1.0~dev19_all.deb
```

Uninstall with:

```sh
sudo apt remove goreecloud-care
```

## Release boundary

GoreeCloud Care remains **Development / nonconformant**. Dev18 produced accepted repository/headless evidence and a successful representative preparation pass, but its package lifecycle produced negative runtime-isolation evidence and was not accepted. Dev19 is the remediation line. Before Release Candidate consideration it still requires exact-head repository/CI success, representative dev19 lifecycle success, continuous enlarged-text drag-resize, complete Insights keyboard traversal, live AT-SPI/Orca, appearance/resilience and icon rendering, representative maintenance/task-flow acceptance, exact-candidate Privacy Shield/Wardveil/Everkeep acceptance, governed GLAZE UI V1.2 `accepted-v1`, and immutable RC regression/promotion evidence.

The canonical source-control authority is `GoreeCloud/goreecloud-zorin-os`; Care remains the `apps/goreecloud-care/` component so Zorin OS packaging, desktop integration, target-device acceptance, and Platform Contract evidence remain coupled while preserving a distinct application boundary.
