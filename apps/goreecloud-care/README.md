# GoreeCloud Care

**Lifecycle:** Development  
**Version:** `0.1.0-dev22`  
**Canonical source:** `GoreeCloud/goreecloud-zorin-os` → `apps/goreecloud-care/`  
**Target:** Zorin OS 17.3 and compatible GTK 3 Linux desktops  
**License:** GPL-3.0-or-later

GoreeCloud Care is an original, local-first GoreeCloud desktop maintenance application. It previews reclaimable storage before deletion, keeps routine cache/temp cleanup unprivileged, provides privacy-safe read-only reports, has a bounded local Maintenance Insights review surface, and exposes a narrow local read-only integration API for governed GoreeCloud platform consumers.

## Dev22 — Dark / Deep Dark HeaderBar contrast remediation

Dev22 follows the representative dev21 appearance pass, which exposed one concrete command-chrome defect: explicit Dark and Development Deep Dark could leave the HeaderBar Scan/native window-control surfaces very light while foreground text/glyphs were also near-white.

The Development CSS now gives Dark HeaderBar buttons an explicit `#34383f` neutral surface and Deep Dark HeaderBar buttons an explicit `#272a2f` neutral surface, both with `#f7f8fa` foreground, visible borders, no inherited background image, and bounded darker hover states. This preserves the accepted Adaptive Resonance workspace rather than redesigning it again.

The acceptance strategy is now automated so routine contrast validation no longer depends on repeated manual screenshots. Exact dev22 head `078f4b39b6c1dd8fee505182be2fb71d0cb80907` passed:

- 105 unit/source tests, including numerical contrast checks against a 4.5:1 minimum for Dark/Deep Dark normal and hover HeaderBar pairs;
- XML/platform-integration/source validation;
- the normal `GDK_DPI_SCALE=2` headless GTK runtime acceptance probe;
- a dedicated Dark headless GTK runtime pass that verifies the realized visible HeaderBar Scan control remains on an opaque surface and meets the 4.5:1 minimum;
- the same dedicated Deep Dark headless GTK runtime pass;
- Debian `0.1.0~dev22` build and package inspection;
- Platform Contract and theme-source validation.

Current exact Dev22 CI evidence:

```text
source:   078f4b39b6c1dd8fee505182be2fb71d0cb80907
Care CI:  34135667452
Contract: 34135667957
Theme:    34135667449
package:  0.1.0~dev22
sha256:   95f3cb9d2e1446a0ae31d133cc684386be14ae7571d97972cba6149f10c12194
artifact: 10023895346
```

Xvfb realizes the application-owned Scan command but not the representative Zorin desktop's full native window-control composition, so this evidence closes the automated application-owned Dark/Deep Dark command-chrome contrast gate without pretending to be a physical Zorin screenshot. Native/compositor-specific optical review can remain part of final representative release QA rather than requiring a separate manual loop for every Development revision.

## Dev21 — compact HeaderBar identity remediation

Dev21 is a focused follow-up to the dev20 **GLAZE UI V1.3 — Adaptive Resonance** revamp. Representative dev20 screenshots accepted the new wide/compact content architecture but exposed one remaining compact visual defect: `GoreeCloud Care` visibly truncated to `GoreeCloud …` beside the Scan capsule and native window controls.

The compact main HeaderBar intentionally uses the short product identity **`Care`**, matching the already-successful compact strategy used by Maintenance Insights. Medium/Expanded layouts restore the full **`GoreeCloud Care`** title and Development subtitle. Representative dev21 evidence accepted both transitions at exact head `2836a700935a019f21a4e19612a2609c21fd874c`.

## Dev20 — GLAZE UI V1.3 Adaptive Resonance revamp

Dev20 rebuilt the Care presentation around the **latest Glaze UI development line: GLAZE UI V1.3 — Adaptive Resonance**. This remains deliberately a **Development implementation**, not a conformance claim. Upstream V1.3 remains **Proposed**, `1.3.0-candidate` is not active, consumer eligibility is false, and **GLAZE UI V1.2 / `1.2.0` remains the official Stable compatibility baseline**.

Care pins the V1.3 Development architecture to Glaze qualification source `dc5ee04b09bd7d2c06d6ac1456618cbd4b1f4b80` and maps it into GTK3 without pretending that GTK3 supplies compositor-authoritative backdrop sampling or full Living Glaze parity.

The revamp changes the product structure rather than merely recoloring the old interface:

- **Content Plane vs Chrome Plane.** Reading, findings, status, and consequential decisions stay optically stable; restrained neutral Glaze is concentrated in HeaderBar/command/signature chrome.
- **Grouped maintenance plan.** Application cache, thumbnail cache, and temporary files are one coherent selectable collection instead of a stack of repetitive floating cards.
- **Separate system actions.** Trash, APT cache, and Memory Refresh are visually and behaviorally separated from routine recreatable cleanup.
- **One dominant primary action.** `Clean selected` is the resonant primary action; destructive Trash and privileged/system actions remain lower-emphasis or danger roles.
- **Semantic shape roles.** Ordinary controls use rounded control geometry; capsule geometry is reserved for compact command chrome such as Scan/Refresh rather than applied to every button.
- **Adaptive workspace.** Compact and Medium layouts prioritize vertical reachability; Expanded layouts expose a useful two-column maintenance/system workspace instead of simply stretching content.
- **Expression and clarity are independent.** Development acceptance can exercise Calm/Balanced/Expressive expression separately from Clear/Balanced/Dense clarity.
- **Accessibility-first degradation.** HighContrast stays system-authoritative; Reduced Transparency resolves optical surfaces to solid equivalents; Reduced Motion removes nonessential optical emphasis; Show Borders strengthens boundaries without requiring extra saturation.
- **Maintenance Insights is part of the same system.** Its read-only summary, semantic status, stable findings plane, command-capsule Refresh, selectable Pango findings, and true-bottom scrolling share the Adaptive Resonance hierarchy while preserving dev17 copy-integrity behavior.

Representative dev20 evidence already accepted the package lifecycle/rollback and launcher-isolation slice, Maintenance Insights/main Care visual slices, continuous `GDK_DPI_SCALE=2` narrow↔wide resizing, and complete forward/reverse keyboard traversal through the redesigned core controls and through/beyond selectable findings without a focus trap.

## Current Development features

- Scan and clean application cache files older than 7 days.
- Clean the thumbnail cache.
- Scan and clean user-owned `/tmp` files older than 7 days.
- Preview Trash usage and empty Trash only after a separate permanent-deletion confirmation.
- Preview APT `.deb` cache and clean it through PolicyKit authorization.
- Display disk, available-memory, and file-cache status.
- “Memory Refresh” truthfully reclaims Linux file caches after a warning and PolicyKit authorization; it does **not** claim a lasting RAM/performance boost.
- Explicit cancellation, failure, partial-success, and completion reporting.
- Post-action refresh updates scan values without replacing the final completion/exception status.
- GTK/ATK/AT-SPI identity, status semantics, keyboard focus, enlarged-text adaptation, and system HighContrast authority.
- Privacy-safe human/JSON reports plus local health, Privacy Shield, Wardveil-compatible security, and Everkeep continuity status output.
- Canonical Care identity from `GoreeCloud/goreecloud-branding-assets/products/care/app-icon.svg` with a synchronized packaged derivative.
- Isolated installed Python launchers that cannot resolve a same-named package from the invoking working directory, `PYTHONPATH`, or user site.
- No telemetry, advertising, cloud upload, remote service, or GoreeCloud account requirement.
- Symlink-safe user cleanup and fixed privileged-action boundaries.

## Package/runtime isolation retained from dev19

Representative dev18 package-lifecycle testing exposed a real packaging/security-boundary defect: after downgrade, `dpkg-query` reported dev17 while a pre-dev19 ambient `python3 -m` launcher invoked from the dev18 source checkout resolved dev18. Removal also left private Python residue. Dev19 corrected both normal and PolicyKit helper launchers to `/usr/bin/python3 -I -B -m ...`, added fixed private `__pycache__` cleanup, and added working-directory shadowing regression probes.

Dev20 preserved and representative-device validated that boundary through the full dev20 ↔ pinned dev17 install/remove/reinstall/downgrade/restore/final-state lifecycle. Dev22 retains the same package/runtime isolation implementation.

## Privacy-safe read-only reports

```sh
goreecloud-care --report
goreecloud-care --report-json
goreecloud-care --version
```

Both report modes are read-only: they scan the same maintenance categories but never delete files, authenticate, invoke PolicyKit, or access the network. Candidate paths, filenames, and raw scan-error strings are omitted by default.

## Local platform integration API

```sh
goreecloud-care --api-version
goreecloud-care --health-json
goreecloud-care --privacy-status-json
goreecloud-care --security-status-json
goreecloud-care --continuity-status-json
```

The API version is `1`. Privacy Shield remains fail-closed with `production_approved=false`; Wardveil-compatible status remains narrowly scoped and `protected_by_wardveil=false`; Everkeep restore evidence passed on dev20 but governed readiness remains fail-closed until explicitly promoted.

## Maintenance Insights

```sh
goreecloud-care --insights-ui
```

Maintenance Insights reviews stale application-cache groups, large regular files of at least 250 MB in standard user folders, Downloads at least 30 days old, aggregate scan errors, and bounded-discovery state. Symlinks are not followed and standard-folder discovery is capped at 50,000 visited entries per refresh. Home-relative paths appear only in this explicit local review surface. No finding is automatically selected for deletion and the Insights modules contain no cleanup, PolicyKit, helper, subprocess, or network execution path.

Historical representative evidence remains revision-scoped. Dev17 exact head `0fda6f90a545eaf3d1bed525aae98c6529ebbf7b` accepted the submitted compact/wide typography, synthetic-hyphen remediation, true-bottom reachability, visible Refresh focus, and selectable findings rendering. Dev20 exact head `9da1107527bb4d7627e4940bd5b1b752cf318e83` accepted the submitted Adaptive Resonance visual slices, continuous enlarged-text resizing, and complete keyboard traversal. Dev21 exact head `2836a700935a019f21a4e19612a2609c21fd874c` accepted the compact/full HeaderBar identity remediation.

## Glaze UI lifecycle boundary

The required platform compatibility baseline remains:

```text
GLAZE UI V1.2 / 1.2.0 — Stable
```

The active Care Development design target is:

```text
GLAZE UI V1.3 — Adaptive Resonance
planned machine target: 1.3.0-candidate
upstream lifecycle: Proposed
Candidate active: no
consumer eligible: no
pinned development source: dc5ee04b09bd7d2c06d6ac1456618cbd4b1f4b80
```

The authoritative Glaze consumer registry still contains GoreeCloud Care as `adoption-required` with no accepted target/reference/evidence and `productionEligible=false`. Dev22 therefore does **not** claim `accepted-v1`, V1.3 Candidate status, V1.3 consumer conformance, Release Candidate status, Stable status, or production eligibility.

Development-only acceptance controls are product-scoped:

```sh
GOREECLOUD_CARE_APPEARANCE=light|dark|deep-dark goreecloud-care
GOREECLOUD_CARE_GLAZE_EXPRESSION=calm|balanced|expressive goreecloud-care
GOREECLOUD_CARE_GLAZE_CLARITY=clear|balanced|dense goreecloud-care
GOREECLOUD_CARE_REDUCE_TRANSPARENCY=1 goreecloud-care
GOREECLOUD_CARE_REDUCE_MOTION=1 goreecloud-care
GOREECLOUD_CARE_SHOW_BORDERS=1 goreecloud-care
```

These are reproducible Development acceptance controls, not a claim that GoreeCloud Personalization or cross-device preference synchronization is implemented.

## Build and test

```sh
sh ./scripts/validate.sh
sh ./scripts/build-deb.sh
```

Development CI verifies the exact PR source revision, runs unit/source validation and enlarged-text headless GTK runtime acceptance, now exercises Dark and Deep Dark realized HeaderBar contrast under Xvfb, builds/inspects the Debian package, records SHA-256 provenance, and preserves the package/checksum/source-revision artifact. Green CI is evidence only; it does not manufacture live screen-reader, physical-device compositor, destructive-flow, or governance acceptance.

## Representative-device acceptance preparation

```sh
sh ./scripts/prepare-representative-acceptance.sh
```

The harness requires a clean tracked tree, records exact dev22 source/package/checksum provenance, performs only read-only installed snapshots when the installed runtime exactly matches `0.1.0-dev22`, and generates explicit human/manual checklists. Routine Development contrast checks are now automated in CI rather than requiring repeated screenshot submissions.

## Package lifecycle acceptance

```sh
sh ./scripts/build-dev17-rollback-package.sh
sh ./scripts/validate-package-lifecycle.sh \
  ./dist/goreecloud-care_0.1.0~dev22_all.deb \
  ./dist/rollback/goreecloud-care_0.1.0~dev17_all.deb
```

The lifecycle probe can perform candidate install, removal, fresh reinstall, downgrade to the pinned accepted dev17 package, dev22 restoration, and final-state validation. Dev20 already accepted the underlying package/runtime boundary; exact-candidate reruns remain available when governed qualification requires them.

## Install or upgrade a locally built Development package

```sh
sudo apt install ./dist/goreecloud-care_0.1.0~dev22_all.deb
```

Uninstall with:

```sh
sudo apt remove goreecloud-care
```

## Release boundary

GoreeCloud Care remains **Development / nonconformant**. The application-owned Dark/Deep Dark HeaderBar contrast remediation now has automated exact-source numerical and realized GTK runtime evidence, so no additional manual screenshot loop is required for that narrow Development gate. Remaining release work includes live AT-SPI/Orca, behavioral Reduced Motion, clarity-profile acceptance, final representative optical/compositor QA, status/confirmation/empty/failure-state review, destructive/PolicyKit task-flow acceptance, exact-candidate Privacy Shield/Wardveil/Everkeep governance, the applicable future governed Glaze consumer gate, immutable Release Candidate evidence, and governed lifecycle promotion. V1.3’s upstream Proposed status must not be bypassed by a downstream Care claim.