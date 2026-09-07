# GoreeCloud Care

**Lifecycle:** Development / nonconformant  
**Version:** `0.1.0-dev22`  
**Package:** `0.1.0~dev22`  
**Canonical source:** `GoreeCloud/goreecloud-zorin-os` → `apps/goreecloud-care/`  
**Representative target:** Zorin OS 17.3  
**Compatibility:** GTK 3 Linux desktops within the supported package/runtime boundary  
**License:** GPL-3.0-or-later

GoreeCloud Care is an original, local-first GoreeCloud desktop maintenance application. It previews maintenance candidates before deletion, keeps routine cache/temp cleanup unprivileged, separates consequential and privileged actions, provides privacy-safe read-only reports, includes a bounded local Maintenance Insights review surface, and exposes narrow read-only platform status interfaces for governed GoreeCloud integrations.

Care remains Development. Green CI, historical representative-device passes, package construction, platform registrations, or a Development Glaze implementation do not independently make it Release Candidate, Stable, production-approved, Protected by Wardveil, Everkeep-ready, or Glaze-conformant.

## Dev22 focus

Dev22 combines the current **GLAZE UI V1.3 Adaptive Resonance Development mapping** with release-hardening automation. The official Stable compatibility baseline remains **GLAZE UI V1.2 / `1.2.0`** because upstream V1.3 is still Proposed and consumer eligibility is not active.

Current dev22 work includes:

- explicit Dark and Development Deep Dark HeaderBar command-surface contrast remediation;
- exact-source enlarged-text GTK runtime validation;
- Dark/Deep Dark realized application-owned HeaderBar contrast acceptance with a 4.5:1 minimum;
- Clear/Balanced/Dense clarity-profile runtime geometry acceptance;
- Reduced Motion application-owned behavior acceptance;
- live core Care and Maintenance Insights AT-SPI event-delivery acceptance on a real accessibility bus;
- safe task-flow automation for selection/preview guardrails, confirmation defaults, cancellation boundaries, and PolicyKit outcome mapping without destructive side effects;
- installed package-lifecycle prequalification that installs, removes, freshly reinstalls, downgrades to immutable accepted dev17, restores dev22, and validates final state;
- installed Wardveil-compatible privilege-boundary prequalification with current/fresh/scoped/minimized evidence and an explicit `protected_by_wardveil=false` invariant;
- immutable Development package/rollback-package provenance preservation in CI artifacts.

The separate `hardening/care-reproducible-package` branch adds deterministic Debian package construction for the same Development version. It binds package timestamps to `SOURCE_DATE_EPOCH` derived from the exact Git revision when not supplied, normalizes staged filesystem mtimes, and adds a byte-for-byte independent rebuild comparison in CI. This is a hardening candidate until its exact-head workflows pass; it does not retroactively make the already accepted `a0eeac5...` package reproducible.

The exact accepted branch revision, workflow run IDs, package digest and artifact ID are maintained in PR #2 and the canonical Care project/change records so this README does not become self-stale when documentation-only commits advance a Development branch.

## Current features

- Scan and clean application cache files older than 7 days.
- Clean the thumbnail cache.
- Scan and clean user-owned `/tmp` files older than 7 days.
- Preview Trash usage and empty Trash only after a separate permanent-deletion confirmation.
- Preview APT `.deb` cache and clean it through PolicyKit authorization.
- Display disk, available-memory, and file-cache status.
- Reclaim Linux file caches only after a warning and PolicyKit authorization; no lasting speed/RAM claim is made.
- Explicit cancellation, failure, partial-success, and completion reporting.
- Post-action refresh that preserves final action outcome text.
- GTK/ATK/AT-SPI identity, status semantics, keyboard focus, enlarged-text adaptation, and system HighContrast authority.
- Privacy-safe human/JSON reports plus local health, Privacy Shield, Wardveil-compatible security, and Everkeep continuity status output.
- Canonical Care identity derived from `GoreeCloud/goreecloud-branding-assets/products/care/app-icon.svg` with a synchronized packaged derivative.
- Isolated installed Python launchers that cannot resolve a same-named package from the invoking working directory, `PYTHONPATH`, or user site.
- Symlink-safe cleanup and fixed privileged-action allowlists.
- No telemetry, advertising, cloud upload, remote service, or GoreeCloud account requirement for current local maintenance functionality.

## Safety model

Routine application-cache, thumbnail-cache, and eligible user-owned temporary-file cleanup runs without administrator privileges. Permanent Trash deletion requires a separate confirmation. APT archive cleanup and file-cache reclaim are isolated behind the fixed Care helper and PolicyKit.

Confirmation dialogs are fail-safe by default: Cancel is present, initially focused, and the default response. Cancellation must not cross the filesystem or privileged execution boundary. PolicyKit cancellation/failure is never represented as success.

The installed normal application and helper launchers use isolated Python path semantics. Package maintainer scripts remove only the fixed Care private bytecode cache so an older Development version cannot affect a later install/downgrade/restore execution path.

## Privacy-safe read-only reports

```sh
goreecloud-care --version
goreecloud-care --report
goreecloud-care --report-json
```

Report modes are read-only. They never delete files, authenticate, invoke PolicyKit, call the privileged helper, or access the network. Candidate paths, filenames, and raw scan-error strings are omitted by default.

## Local platform integration API

```sh
goreecloud-care --api-version
goreecloud-care --health-json
goreecloud-care --privacy-status-json
goreecloud-care --security-status-json
goreecloud-care --continuity-status-json
```

API version is `1`.

### Privacy Shield

Care declares only the bounded local-first adapter capabilities required for telemetry minimization, data minimization, and privacy status. The authoritative adapter remains fail-closed with:

```text
runtime_acceptance_required=true
production_approved=false
```

Exact dev22 representative runtime acceptance is centrally recorded for the accepted revision, but production approval remains a separate governed release gate. A later hardening revision does not inherit exact-revision acceptance automatically.

### Wardveil Security

`--security-status-json` describes only the Care-owned installed privilege boundary. Passing evidence requires the fixed helper/policy installation constraints and `pkexec` availability; missing, writable, or otherwise non-passing evidence fails closed.

The record is scoped, timestamped, short-lived when passing, minimized, and text-semantic. It deliberately keeps:

```text
protected_by_wardveil=false
```

Care does not accept Wardveil runtime-authorization envelopes for its maintenance actions. Wardveil therefore remains evidence/governance authority for its status semantics, not the executor of Care cleanup.

See [`WARDVEIL-INTEGRATION.md`](WARDVEIL-INTEGRATION.md).

### Everkeep

Care has package-lifecycle and restore-path evidence, including accepted representative dev20 history, exact dev22 representative lifecycle evidence, and repeatable CI prequalification. Governed Everkeep readiness remains fail-closed until the exact release candidate satisfies the authoritative target-runtime acceptance policy and is explicitly promoted. `--continuity-status-json` therefore remains `attention` in Development.

## Maintenance Insights

```sh
goreecloud-care --insights-ui
```

Maintenance Insights reviews:

- stale application-cache groups;
- large regular files of at least 250 MB in standard user folders;
- Downloads at least 30 days old;
- aggregate scan errors;
- bounded-discovery state.

Symlinks are not followed and standard-folder discovery is capped at 50,000 visited entries per refresh. Home-relative paths appear only in this explicit local review surface. No finding is automatically selected for deletion and the Insights modules contain no cleanup, PolicyKit, helper, subprocess, or network execution path.

Historical representative evidence is revision-scoped. Dev17 exact head `0fda6f90a545eaf3d1bed525aae98c6529ebbf7b` accepted the submitted compact/wide typography, synthetic-hyphen remediation, true-bottom reachability, visible Refresh focus, and selectable findings rendering. Dev20 exact head `9da1107527bb4d7627e4940bd5b1b752cf318e83` accepted the submitted Adaptive Resonance visual slices, continuous enlarged-text resizing, complete keyboard traversal, package lifecycle and launcher isolation. Dev21 exact head `2836a700935a019f21a4e19612a2609c21fd874c` accepted the compact/wide HeaderBar identity transition; its Dark/Deep Dark screenshots provided the defect evidence remediated in dev22.

## Accessibility automation

Development CI runs a real AT-SPI session bus and validates dynamic accessible-name and `visible-data-changed` delivery for both core Care and Maintenance Insights. It also validates the accessible application identity, status surfaces, commands and Insights results exposure.

This establishes AT-SPI delivery, not final screen-reader speech quality. Representative Orca announcement-quality acceptance remains a human release boundary.

## Appearance and Adaptive Resonance

Official Stable compatibility baseline:

```text
GLAZE UI V1.2 / 1.2.0 — Stable
```

Active Care Development design target:

```text
GLAZE UI V1.3 — Adaptive Resonance
planned machine target: 1.3.0-candidate
upstream lifecycle: Proposed
Candidate active: no
consumer eligible: no
pinned development source: dc5ee04b09bd7d2c06d6ac1456618cbd4b1f4b80
```

The authoritative Glaze consumer registry keeps GoreeCloud Care `adoption-required`, without accepted target/reference/evidence and with `productionEligible=false`. Dev22 does not claim `accepted-v1`, V1.3 Candidate status, V1.3 consumer conformance, Release Candidate status, Stable status, or production eligibility.

Development-only acceptance controls:

```sh
GOREECLOUD_CARE_APPEARANCE=light|dark|deep-dark goreecloud-care
GOREECLOUD_CARE_GLAZE_EXPRESSION=calm|balanced|expressive goreecloud-care
GOREECLOUD_CARE_GLAZE_CLARITY=clear|balanced|dense goreecloud-care
GOREECLOUD_CARE_REDUCE_TRANSPARENCY=1 goreecloud-care
GOREECLOUD_CARE_REDUCE_MOTION=1 goreecloud-care
GOREECLOUD_CARE_SHOW_BORDERS=1 goreecloud-care
```

These are reproducible Development controls, not a claim that cross-device Personalization synchronization is implemented.

## Build and test

```sh
sh ./scripts/validate.sh
sh ./scripts/build-deb.sh
sh ./scripts/verify-reproducible-package.sh ./dist/goreecloud-care_0.1.0~dev22_all.deb
```

`build-deb.sh` never uses the wall clock for package metadata. In a Git checkout it derives `SOURCE_DATE_EPOCH` from the exact repository `HEAD`; outside a Git checkout an explicit `SOURCE_DATE_EPOCH` is required. The staged package tree is normalized to that timestamp before `dpkg-deb` builds the archive. The verifier independently rebuilds with the same epoch and requires byte-for-byte identity with the reference package.

Development CI verifies the exact PR head and currently exercises:

- unit/source contracts;
- XML and platform integration validation;
- enlarged-text GTK runtime behavior;
- safe task flows;
- live core and Insights AT-SPI delivery;
- Dark/Deep Dark command contrast;
- clarity profiles;
- Reduced Motion behavior;
- Debian package construction and inspection;
- byte-for-byte reproducible-package verification on the hardening branch;
- immutable dev17 rollback construction;
- full installed dev22↔dev17 lifecycle prequalification;
- installed Wardveil-compatible boundary prequalification;
- package/source/checksum provenance preservation.

Green CI is evidence only. It does not manufacture representative Zorin compositor rendering, Orca speech quality, desktop PolicyKit-agent UX, or governed platform acceptance.

## Representative-device acceptance preparation

```sh
sh ./scripts/prepare-representative-acceptance.sh
```

The preparation harness requires a clean tracked tree, records exact source/package/checksum provenance, captures only supported read-only installed snapshots, and keeps human-only gates explicit.

## Package lifecycle acceptance

Build the immutable accepted dev17 rollback package:

```sh
sh ./scripts/build-dev17-rollback-package.sh
```

Then run:

```sh
sh ./scripts/validate-package-lifecycle.sh \
  ./dist/goreecloud-care_0.1.0~dev22_all.deb \
  ./dist/rollback/goreecloud-care_0.1.0~dev17_all.deb
```

The probe performs candidate install/upgrade, installed validation, removal, fresh reinstall, downgrade to accepted dev17, restoration to dev22, repeated installed validation, and final-state verification. It does not invoke Care cleanup actions.

## Install a local Development package

```sh
sudo apt install ./dist/goreecloud-care_0.1.0~dev22_all.deb
```

Uninstall:

```sh
sudo apt remove goreecloud-care
```

## Release boundary

Care remains **Development / nonconformant**. Automated Development evidence has substantially reduced the remaining human-only surface, but the release process is not complete.

Remaining release boundaries include:

- exact-head validation of the deterministic package hardening branch and, if integrated, exact-candidate representative target acceptance for the resulting new source revision;
- final representative Orca speech/announcement-quality acceptance;
- final physical Zorin optical/compositor review for native window controls and canonical Care icon rendering, including Dark/Deep Dark;
- actual desktop PolicyKit-agent success/cancellation/failure UX and any controlled destructive-flow evidence required by release policy;
- Privacy Shield governed production approval for an eligible exact candidate;
- governed Wardveil runtime/adoption promotion while `protected_by_wardveil=false` remains authoritative until accepted;
- governed Everkeep integration/readiness promotion after the exact candidate satisfies the required evidence;
- applicable future Glaze consumer acceptance only when upstream V1.3 lifecycle permits it;
- immutable Release Candidate regression/evidence and explicit governed lifecycle promotion.

No downstream Care document or CI result may bypass those authorities.
