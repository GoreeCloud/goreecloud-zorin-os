# GoreeCloud Care — Development Specification

**Lifecycle:** Development / nonconformant  
**Current source line:** `0.1.0-dev18`  
**Canonical source:** `GoreeCloud/goreecloud-zorin-os/apps/goreecloud-care/`  
**Target:** Zorin OS 17.3 and compatible GTK 3 Linux desktops

## Purpose

GoreeCloud Care is an original GoreeCloud-owned native desktop maintenance application for a person maintaining their own GoreeCloud/Zorin OS workstation. It may expand into maintenance intelligence, diagnostics, storage visibility, and guided system-health workflows only when those capabilities preserve the preview-first, least-privilege, privacy-first safety model.

## Safety model

- Preview first; cleanup never starts merely because a scan ran.
- User cache, thumbnail cache, and stale temporary files run as the logged-in user.
- Trash is a dedicated destructive action with an explicit, last-moment confirmation.
- Privilege is limited to allowlisted helper actions; the current helper exposes only `apt-clean` and `reclaim-memory`.
- Privileged helpers accept no arbitrary paths, commands, shell fragments, or free-form arguments.
- Symlinks are never followed during user-file scanning or deletion.
- Stale generic cache and temporary files use a 7-day threshold.
- Cleanup candidates are individual leaf nodes; broad recursive deletion of cache/temp directories is not used.
- Errors are surfaced and failed items are not counted as successful deletion.
- New cleanup categories begin as read-only discovery unless deletion semantics, ownership boundaries, recovery behavior, and privilege requirements are separately specified and accepted.
- Scheduled capability may scan or remind; unattended automatic deletion is excluded.

## Interface, accessibility, appearance, and GLAZE UI V1.2

Current Stable shared-design target is **GLAZE UI V1.2 / `1.2.0`**. Care must not claim conformance merely because a version string or source mapping is present.

The dev18 GTK3 mapping uses a bounded native fallback:

- ordinary material surfaces are neutral white/gray/graphite rather than default color-tinted substrate;
- blue is reserved for primary action, focus, bounded interaction response, and product-compatible accent; attention/success/error colors remain semantic;
- GTK3 does not claim compositor-wide backdrop blur or background sampling;
- system Light/Dark resolution is supported by the V1.2 provider, and Deep Dark is available as an explicit Development acceptance override until a governed native selection path exists;
- Reduced Transparency resolves ordinary translucent material to solid neutral surfaces;
- Reduced Motion honors disabled GTK animation state and removes the optional hover optical response; Care defines no nonessential CSS transition/animation dependency;
- system HighContrast removes the Care/Glaze palette providers and remains authoritative;
- effective HighContrast detection honors `Gtk.Settings:gtk-theme-name` and process-local `GTK_THEME` overrides;
- minimum interactive target contract is 48 pixels for buttons/checkbuttons in the V1.2 mapping;
- keyboard focus remains visibly perceivable in ordinary and HighContrast presentation;
- status feedback communicates changed state with text plus a recognizable symbol and semantic treatment; color alone is insufficient;
- maintenance status surfaces expose ATK status-bar semantics and update their accessible name when operation state changes;
- user cancellation is a changed/attention state, not success or destructive failure;
- interactive controls remain keyboard focusable and expose useful accessible names/descriptions;
- long status, system, description, heading, and findings text wraps instead of clipping;
- compact composition moves category amounts below category content and stacks bottom actions vertically;
- `GDK_DPI_SCALE` is included in the effective-width contract for the representative 200%-text acceptance path;
- minimum supported Development window size is 480 × 420 logical pixels.

Development acceptance environment controls are scoped to Care and do not change the desktop-wide preference:

- `GOREECLOUD_CARE_APPEARANCE=system|light|dark|deep-dark`
- `GOREECLOUD_CARE_REDUCE_TRANSPARENCY=1`
- `GOREECLOUD_CARE_REDUCE_MOTION=1`

See `GLAZE-UI-CONFORMANCE.md` for the fail-closed V1.2 evidence boundary.

## Read-only report contract

- `goreecloud-care --report` provides a human-readable local maintenance report.
- `goreecloud-care --report-json` provides schema-versioned JSON.
- `goreecloud-care --version` provides the installed application version.
- Report generation may read the same local filesystem metadata, disk usage, and `/proc/meminfo` used by normal Care scanning.
- Report generation must not delete files, request PolicyKit authorization, invoke the helper, use telemetry, or access the network.
- Reports omit candidate file paths, local filenames, and raw scan-error strings by default.
- Reports may expose aggregate/per-category byte and item counts, scan-error counts, disk headroom, memory availability, file-cache estimates, and explicit mode/privacy declarations.
- Disk-headroom classification is informational only and is not filesystem-health certification, failure prediction, or an automatic cleanup trigger.

Representative-device dev13 exact head `48049b6f634a05300e01bb0e85d718284b79d7ee` is accepted for this reporting slice.

## Maintenance Insights contract

- `goreecloud-care --insights-ui` opens a dedicated local read-only GTK review surface. The desktop entry exposes **Maintenance Insights (Read-only)**.
- The engine groups stale application-cache candidates by top-level cache namespace using the established >7-day policy; thumbnails remain excluded.
- Large-file discovery is limited to regular user-owned files of at least 250 MB under `Downloads`, `Desktop`, `Documents`, `Pictures`, `Videos`, and `Music`.
- Stale Downloads review is limited to regular user-owned files at least 30 days old.
- Discovery does not follow symlinks and remains lexically inside configured standard roots.
- Each refresh is bounded to at most 50,000 visited standard-folder entries and discloses partial results if the limit is reached.
- The interactive review may show home-relative file paths; default report modes remain path-redacted.
- Findings are informational only and are never automatically selected for deletion, movement, quarantine, package action, or privileged operation.
- The Insights engine/window contains no deletion, PolicyKit, privileged-helper, subprocess, or network execution path.
- The whole page is vertically scrollable and findings have an independent scroller with a 320-pixel minimum viewport.
- Compact mode reduces HeaderBar/fixed-copy pressure and uses a symbolic Refresh control with explicit accessible name, description, tooltip, and focusability.
- Dev17 findings use a selectable Pango-backed `Gtk.Label`, `Pango.WrapMode.WORD_CHAR`, `insert_hyphens='false'`, and markup escaping. No zero-width break characters are inserted to obtain wrapping.

Representative-device exact dev17 head `0fda6f90a545eaf3d1bed525aae98c6529ebbf7b` is accepted for the targeted build/install/rendering slice: 50 tests plus XML/source validation passed, the package upgraded successfully, compact/wide readability and Refresh focus were preserved, the prior synthetic mid-word hyphens were absent, and the findings true bottom was reached. Continuous drag-resize responsiveness and exact-candidate live accessibility remain open despite newer automated headless evidence.

## Dev18 local platform integration API

Dev18 adds read-only local command endpoints. They do not create an HTTP listener or perform maintenance:

- `--api-version` → local API version `1`.
- `--health-json` → minimized local readiness/version status.
- `--privacy-status-json` → Privacy Shield-shaped adapter status.
- `--security-status-json` → Wardveil-compatible scoped status for Care’s installed privilege boundary.
- `--continuity-status-json` → Everkeep continuity status for package restore/rollback evidence.

All status modes remain GUI-lazy and must not delete files, request PolicyKit authorization, invoke the privileged helper, send telemetry, or access the network.

### Privacy Shield boundary

Repository-local declarations are `contracts/privacy-shield.application.json` and `contracts/privacy-shield.adapter.json`. Current declared capabilities are `telemetry-minimization`, `data-minimization`, and `privacy-status`. The application is local-first; status output includes no raw private activity, credentials, or identifiers. The authoritative Privacy Shield-side Care registration is proposed in Draft PR 17. Runtime acceptance remains required and `production_approved` stays false until accepted exact-candidate evidence exists.

### Wardveil Security boundary

`WARDVEIL-INTEGRATION.md` defines the scoped producer model. Care is authoritative only for Care-owned installation/control facts such as the fixed helper and PolicyKit policy files. A passing local record requires secure fixed-file ownership/write permissions and executable `pkexec`; evidence fails closed otherwise. The record deliberately keeps `protected_by_wardveil=false`; a compatible status shape does not authorize a broad Wardveil protection claim or cross-service execution authority.

### Everkeep boundary

`contracts/everkeep.adoption.json` declares a read-only/fail-closed producer role for restore capability, migration, documentation, and provenance. `contracts/everkeep.acceptance.json` additionally requires exact immutable candidate/package provenance and representative install/remove/reinstall/downgrade/restore evidence before ready. Care currently persists no substantial durable application-owned user dataset. Continuity therefore remains `attention` until the package lifecycle gate actually passes.

### Manager, Mesh, and Identity applicability

For the intended first Stable scope, Care is a local single-user maintenance utility and does not require central administration, cross-application coordination, an account, multi-user behavior, or delegated authorization. Manager, Mesh, and Identity may therefore remain `not-applicable-justified` for that bounded release scope. The local API intentionally leaves a future read-only integration path. Any remote management, coordination, account, multi-user, or delegated-administration scope must reopen these applicability decisions.

## Branding authority

The canonical Care product icon is `GoreeCloud/goreecloud-branding-assets/products/care/app-icon.svg`. The Debian package carries an exact synchronized derivative at `packaging/icons/com.goreecloud.care.svg` and installs it under the freedesktop hicolor application-icon path. The consumer copy is not a branding authority. Target desktop rendering and visual-quality acceptance remain required before release qualification.

## Data and privacy

Care reads local filesystem metadata, `/proc/meminfo`, disk usage, and fixed installation metadata for status checks. It sends nothing over the network and contains no telemetry. Default reports/status are minimized. Maintenance Insights may show home-relative paths only inside the explicitly opened local review surface. Future diagnostic bundles exposing more local detail require explicit user approval, redaction rules, and separate governance.

## Platform and toolkit

- Python 3.10+
- GTK 3 / PyGObject
- ATK / AT-SPI
- Pango for dev17+ findings layout
- PolicyKit / `pkexec` only for the two fixed privileged maintenance actions
- Debian `all` Development packaging
- GLAZE UI V1.2 native GTK3 fallback layered above the historical Development palette while preserving system-authoritative HighContrast

The report, Insights, and local status layers add no mandatory remote runtime dependency.

## Exclusions

- No automatic scheduled deletion.
- No browser-history, cookie, password, or credential deletion.
- No process killer or “one-click optimizer.”
- No swap manipulation.
- No automatic package autoremove or old-kernel removal.
- No registry-style tuning, CPU overclocking, or arbitrary kernel-parameter tuning.
- No claim that dropping file caches permanently boosts RAM or performance.
- No arbitrary root shell execution.
- No unbounded whole-home or whole-filesystem Insights discovery.
- No GoreeCloud account, remote management, or cross-application execution authority in the intended first release scope.
- No claim of compositor-wide GTK3 backdrop-blur fidelity.
- No Stable/production Glaze, Privacy Shield, Wardveil, or Everkeep acceptance before exact-candidate evidence actually passes.

## Release status

GoreeCloud Care remains **Development / nonconformant**. Dev18 now includes the local platform integration foundation, fail-closed Everkeep acceptance policy, canonical Care branding derivative, and current-Stable GLAZE UI V1.2 source/runtime mapping. It does not itself qualify Care for Release Candidate or Stable. Remaining gates are defined in `RELEASE-ACCEPTANCE.md` and include exact-head dev18 V1.2 regression validation, representative status/API checks, Privacy Shield/Wardveil/Everkeep acceptance, governed GLAZE UI V1.2 registry/product acceptance, representative appearance/resilience and continuous large-text resize validation, complete keyboard/AT-SPI/Orca acceptance, package lifecycle rollback evidence, representative task-flow/icon/visual-quality review, immutable candidate provenance, and governed lifecycle promotion.
