# GoreeCloud Care — Development Specification

**Lifecycle:** Development / nonconformant  
**Current source line:** `0.1.0-dev22`  
**Package line:** `0.1.0~dev22`  
**Canonical source:** `GoreeCloud/goreecloud-zorin-os/apps/goreecloud-care/`  
**Representative target:** Zorin OS 17.3  
**Official Stable design baseline:** GLAZE UI V1.2 / `1.2.0`  
**Forward Development design target:** GLAZE UI V1.3 Adaptive Resonance (Proposed; consumer eligibility inactive)

## Purpose

GoreeCloud Care is an original GoreeCloud-owned native desktop maintenance application for a person maintaining their own GoreeCloud/Zorin OS workstation. It may expand into maintenance intelligence, diagnostics, storage visibility, and guided system-health workflows only when those capabilities preserve the preview-first, least-privilege, privacy-first safety model.

## Safety model

- Preview first; cleanup never starts merely because a scan ran.
- User cache, thumbnail cache, and stale temporary files run as the logged-in user.
- Trash is a dedicated destructive action with an explicit last-moment confirmation.
- Privilege is limited to allowlisted helper actions; the current helper exposes only `apt-clean` and `reclaim-memory`.
- Privileged helpers accept no arbitrary paths, commands, shell fragments, or free-form arguments.
- Symlinks are never followed during user-file scanning or deletion.
- Stale generic cache and temporary files use a 7-day threshold.
- Cleanup candidates are individual leaf nodes; broad recursive deletion of cache/temp directories is not used.
- Errors are surfaced and failed items are not counted as successful deletion.
- New cleanup categories begin as read-only discovery unless deletion semantics, ownership boundaries, recovery behavior, and privilege requirements are separately specified and accepted.
- Scheduled capability may scan or remind; unattended automatic deletion is excluded.
- Cancellation, PolicyKit denial, helper failure, and partial failure are never represented as success.

## Interface, accessibility, and Glaze UI

The official Stable shared-design target remains **GLAZE UI V1.2 / `1.2.0`**. Dev22 additionally carries a forward Development implementation of Proposed **GLAZE UI V1.3 Adaptive Resonance**. That implementation is not a claim that V1.3 Candidate is active or that Care is an eligible/conformant V1.3 consumer.

Current native GTK3 behavior includes:

- neutral material surfaces with semantic/accent color separated from substrate color;
- compact and expanded layout environments that reorganize content instead of merely scaling it;
- 48-pixel minimum target intent for interactive controls in the Glaze mappings;
- `GDK_DPI_SCALE`-aware effective-width behavior for the representative enlarged-text path;
- readable Light, Dark, Development Deep Dark, and HighContrast acceptance surfaces where claimed;
- system-authoritative HighContrast and a separate focus-resilience provider;
- Reduced Transparency, Reduced Motion, Show Borders, expression-profile, and clarity-profile Development controls;
- accessible application identity set before GUI startup;
- status surfaces with ATK status-bar semantics and dynamic accessible-name/state updates;
- keyboard-focus visibility, forward/reverse traversal requirements, wrapped text, and true-bottom reachability;
- Maintenance Insights using selectable Pango findings with `WORD_CHAR` wrapping and synthetic-hyphen suppression.

Representative visual, Orca speech-quality, continuous-resize, native compositor, and desktop PolicyKit-agent judgments remain target/human release evidence rather than source-level assumptions.

## Read-only report contract

- `goreecloud-care --report` provides a human-readable local maintenance report.
- `goreecloud-care --report-json` provides schema-versioned JSON.
- `goreecloud-care --version` provides the installed application version.
- Report generation may read the same local filesystem metadata, disk usage, and `/proc/meminfo` used by normal Care scanning.
- Report generation must not delete files, request PolicyKit authorization, invoke the helper, use telemetry, or access the network.
- Reports omit candidate file paths, local filenames, and raw scan-error strings by default.
- Reports may expose aggregate/per-category byte and item counts, scan-error counts, disk headroom, memory availability, file-cache estimates, and explicit mode/privacy declarations.
- Disk-headroom classification is informational only and is not filesystem-health certification, failure prediction, or an automatic cleanup trigger.

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

## Local platform integration API

Dev22 exposes read-only local command endpoints. They do not create an HTTP listener or perform maintenance:

- `--api-version` → local API version `1`.
- `--health-json` → minimized local readiness/version status.
- `--privacy-status-json` → Privacy Shield-shaped adapter status.
- `--security-status-json` → Wardveil-compatible scoped status for Care’s installed privilege boundary.
- `--continuity-status-json` → evidence-derived Everkeep continuity status for exact package restore/rollback readiness.

All status modes remain GUI-lazy and must not delete files, request PolicyKit authorization, invoke the privileged helper, send telemetry, or access the network.

### Privacy Shield boundary

Repository-local declarations are `contracts/privacy-shield.application.json` and `contracts/privacy-shield.adapter.json`. Current declared capabilities are `telemetry-minimization`, `data-minimization`, and `privacy-status`. The application is local-first; status output includes no raw private activity, credentials, or identifiers. Runtime acceptance remains exact-revision-scoped and `production_approved` stays false until a separate governed production approval exists for an eligible release candidate.

### Wardveil Security boundary

`WARDVEIL-INTEGRATION.md` defines the scoped producer model. Care is authoritative only for Care-owned installation/control facts such as the fixed helper and PolicyKit policy files. A passing local record requires secure fixed-file ownership/write permissions and executable `pkexec`; evidence fails closed otherwise. The record deliberately keeps `protected_by_wardveil=false`; a compatible status shape does not authorize a broad Wardveil protection claim or cross-service execution authority.

### Everkeep / continuity boundary

Everkeep owns continuity governance. Care may produce evidence but cannot promote itself.

The continuity chain is:

1. **Package-owned build provenance** — `/usr/share/goreecloud-care/build-provenance.json`
   - root-controlled package file;
   - exact repository source revision;
   - exact Care source-tree SHA;
   - runtime version;
   - package version;
   - deterministic source timestamp;
   - no embedded package SHA because embedding a package's own digest is circular.

2. **Care-owned representative-target record** — `/var/lib/goreecloud-care/acceptance/representative-target.json`
   - produced only after exact Zorin OS 17.3 representative lifecycle acceptance;
   - records exact candidate package SHA-256 externally;
   - records source validation, local test count, and package lifecycle pass;
   - keeps `everkeep_integration_promoted=false` and `everkeep_ready_promoted=false`.

3. **Everkeep-owned governance record** — `/var/lib/goreecloud/everkeep/acceptance/goreecloud-care.target-runtime.json`
   - separate authority;
   - must match installed source revision/tree/runtime/package;
   - must identify Zorin OS 17.3 as the representative target;
   - must carry the same exact package SHA-256 as the Care target record;
   - must explicitly promote both Everkeep integration and readiness.

Continuity state is fail-closed:

- missing/untrusted package provenance → `attention / provenance-unavailable`;
- no matching Zorin target record → `attention / target-acceptance-required`;
- matching Care target record but no matching promoted Everkeep record → `attention / target-accepted-governance-pending`;
- only the complete exact-match promoted chain → `ready / everkeep-promoted`, with `freshness=exact-build-bound`.

Regular evidence files and their immediate parent directories must be root-owned and not group/other writable. Symlinked, malformed, oversized, writable, source-mismatched, target-mismatched, package-mismatched, or unpromoted evidence cannot produce `ready`.

`contracts/continuity.status.schema.json` defines the machine-readable status contract. `contracts/everkeep.acceptance.json` defines the local authority/failure policy.

### Manager, Mesh, and Identity applicability

For the intended first Stable scope, Care is a local single-user maintenance utility and does not require central administration, cross-application coordination, an account, multi-user behavior, or delegated authorization. Manager, Mesh, and Identity may therefore remain `not-applicable-justified` only while that bounded scope remains true. Any remote management, coordination, account, multi-user, or delegated-administration scope reopens these applicability decisions.

## Packaging and exact provenance

The Development Debian package is architecture `all` and is built by `scripts/build-deb.sh`.

Packaging requirements:

- authoritative Git checkout required;
- tracked Care changes must be committed/stashed;
- every file that can enter the package must be tracked; untracked glob inputs fail closed;
- source revision and Care source-tree SHA are embedded in package provenance;
- `SOURCE_DATE_EPOCH` defaults to exact `HEAD` commit time when not explicitly supplied;
- locale/timezone are deterministic (`C`, UTC);
- all staged mtimes are normalized;
- Debian format 2.0 is used with `-Znone` to remove compressor-version variation;
- same-environment rebuild must compare byte-for-byte equal;
- independent Ubuntu 22.04 and Ubuntu 24.04 builds must compare byte-for-byte equal in CI;
- package removal must remove package-owned provenance as well as application/helper/policy/desktop/icon/AppStream/private-runtime paths.

## Representative target acceptance

`scripts/run-representative-acceptance.sh` is the exact automated Zorin OS 17.3 target handoff runner. Run as the normal desktop user, it requires a clean exact candidate, performs source validation, builds and verifies the reproducible candidate, builds the immutable accepted dev17 rollback package, executes the full install/remove/reinstall/downgrade/restore package lifecycle, verifies final installed source provenance, computes the package SHA-256, generates the Care-owned target record, installs that record root-controlled, and proves that it cannot self-promote without Everkeep governance.

The runner does not invoke Care cleanup actions and does not write an Everkeep governance record.

## Branding authority

The canonical Care product icon is `GoreeCloud/goreecloud-branding-assets/products/care/app-icon.svg`. The Debian package carries a synchronized derivative at `packaging/icons/com.goreecloud.care.svg` and installs it under the freedesktop hicolor application-icon path. The consumer copy is not a branding authority. Target desktop rendering and visual-quality acceptance remain required before release qualification.

## Data and privacy

Care reads local filesystem metadata, `/proc/meminfo`, disk usage, and fixed installation metadata for status checks. It sends nothing over the network and contains no telemetry. Default reports/status are minimized. Maintenance Insights may show home-relative paths only inside the explicitly opened local review surface. Future diagnostic bundles exposing more local detail require explicit user approval, redaction rules, and separate governance.

## Platform and toolkit

- Python 3.10+
- GTK 3 / PyGObject
- ATK / AT-SPI
- Pango for findings layout
- PolicyKit / `pkexec` only for the two fixed privileged maintenance actions
- Debian `all` Development packaging
- GLAZE UI V1.2 Stable compatibility baseline plus a bounded Proposed V1.3 Development mapping

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

GoreeCloud Care remains **Development / nonconformant**. Dev22 includes automated source/runtime/accessibility/package hardening, deterministic cross-environment packaging, exact package provenance, and a governed continuity evidence boundary. None of those changes promotes Care to Release Candidate or Stable by themselves.

The remaining promotion requirements are governed by `RELEASE-ACCEPTANCE.md` and include a frozen exact candidate with green CI, fresh exact-source Zorin OS 17.3 representative acceptance, remaining human visual/Orca/desktop PolicyKit judgments, exact-candidate Privacy Shield/Wardveil/Everkeep acceptance where required, current approved Glaze acceptance, immutable RC regression evidence, synchronized canonical Drive specification/change records, and explicit lifecycle promotion.
