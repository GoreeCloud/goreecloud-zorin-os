# GoreeCloud Care — GLAZE UI V1.2 Conformance Record

## Authority and status

Current required Stable consumer baseline: **GLAZE UI V1.2 / 1.2.0**.

The current Glaze UI consumer authority is `GoreeCloud/goreecloud-glaze-ui/consumers/registry.json`; its official baseline is `1.2.0` and its product label is `GLAZE UI V1.2`. Historical Care V1.1 evidence remains useful provenance for unchanged accessibility/adaptive behavior, but it does not automatically establish V1.2 conformance.

GoreeCloud Care is a native GTK 3 application. Native GTK controls are the platform implementation primitives for Glaze UI semantics; they are not an exemption from the design system. This record is intentionally fail closed: Care does not claim current-Stable Glaze UI conformance until the exact intended release candidate has product-specific native, rendered, accessibility, resilience, task-flow, form-factor, visual-quality, and registry acceptance evidence.

Lifecycle at this record: **Development / nonconformant**.

## V1.2 native material strategy

Care implements a bounded GTK3 V1.2 fallback rather than claiming compositor-wide backdrop-blur fidelity.

- `goreecloud_care/glaze_v12.py` defines the current-Stable version identity, neutral material mapping, Light/Dark/Deep Dark palettes, 48-pixel minimum interactive targets, Reduced Transparency solid-surface fallback, and Reduced Motion behavior.
- `goreecloud_care/glaze_v12_global.py` installs one process-local provider for both the core Care and Maintenance Insights windows at a priority above the historical Development palette provider.
- System HighContrast remains authoritative: when HighContrast is effective, the V1.2 provider is removed rather than recoloring the system palette.
- GTK3 does not claim compositor background sampling or Wayland-wide backdrop blur. Care therefore uses the V1.2 degradation principle: reduce optical complexity before correctness, accessibility, or task completion.
- Living Glaze is bounded to immediate, subtle interaction-state feedback. Care defines no cursor-following geometry, animated opacity drift, nonessential travel, CSS transitions, or animation dependency.
- Reduced Transparency removes translucent application material surfaces by resolving them to solid neutral surfaces rather than merely lowering alpha.
- Reduced Motion respects disabled GTK animations and the Care-scoped Development acceptance override. Hover optical feedback becomes static/instant and is not required for semantic state.

Development-only environment overrides used for reproducible native acceptance are product-scoped:

- `GOREECLOUD_CARE_APPEARANCE=system|light|dark|deep-dark`
- `GOREECLOUD_CARE_REDUCE_TRANSPARENCY=1`
- `GOREECLOUD_CARE_REDUCE_MOTION=1`

These do not change desktop-wide settings and do not by themselves constitute a user-facing Personalization implementation.

## Native mapping

### Structure and hierarchy

- `Gtk.HeaderBar` provides application identity and primary command placement.
- Primary content is vertically ordered with explicit heading/body/status hierarchy.
- Maintenance categories use bounded neutral material cards rather than undifferentiated page text.
- Destructive Trash handling remains visually and behaviorally separate from routine recreatable cleanup.
- Maintenance Insights is a separate explicit read-only review surface.

### Neutral material and semantic color

The governing V1.2 rule is **Neutral glass is the material. Color is an accent.** Care's ordinary cards and header surfaces therefore resolve first as white/neutral or graphite material. Blue is reserved for primary action, focus, and bounded interaction feedback; attention/success/error colors remain semantic rather than decorative substrate.

Critical maintenance decisions and status outcomes remain opaque/readable. Care does not put destructive warnings, authentication boundaries, or state meaning behind an optical effect that is required for comprehension.

### Semantic state and feedback

The core Care window exposes textual status titles and body copy for informational, attention, success, and error states. Semantic meaning is never color-only. Cancellation, authorization failure, partial cleanup, scan failure, and success are separate outcomes. The persistent status surface exposes ATK status-bar semantics and updates its accessible name when state changes.

### Accessibility and input

- Explicit GLib program/application identity is set before GUI startup.
- Interactive buttons and selectors are keyboard focusable and the V1.2 mapping establishes a 48-pixel minimum target contract.
- A theme-resilient focus provider retains perceivable focus without defining an application palette.
- System HighContrast removes the ordinary Care/V1.2 palette providers so the system palette remains authoritative.
- Compact and enlarged-text layouts preserve vertical reachability.
- Maintenance Insights exposes accessible status/results names and an accessible symbolic Refresh action.
- Selectable findings preserve copy/read behavior while remaining read-only.
- Historical static AT-SPI acceptance is retained as provenance; exact-candidate dynamic event/Orca quality is still separately required.

### Responsive and adaptive behavior

Care uses a shared effective-width contract that accounts for `GDK_DPI_SCALE` when deciding compact composition. At constrained widths, actions stack vertically, HeaderBar pressure is reduced, category values move below body copy, and the page remains vertically scrollable. Maintenance Insights additionally retains an independently scrollable findings surface with a 320-pixel minimum viewport.

The headless Development acceptance harness repeatedly resizes Maintenance Insights between compact and regular allocations under `GDK_DPI_SCALE=2`, verifies compact/regular title transitions, and verifies forward/reverse focus movement through the selectable results surface. This is useful automated native evidence but does not replace human representative-device drag-resize or assistive-technology acceptance.

### Appearance and resilience

The V1.2 Development provider can resolve Light, Dark, and Deep Dark material mappings. `system` is the default resolution strategy for the new provider, with system theme naming used to distinguish ordinary Light/Dark presentation. Deep Dark remains an explicit Development acceptance override until a native platform/user-facing selector is governed.

HighContrast is a separate system-authoritative path, not a Care dark-mode substitute. Reduced Transparency and Reduced Motion are separately testable degradation paths. Final release claims must name only the appearance/resilience modes actually accepted on the supported target.

### Motion and performance

Care does not depend on decorative animation for task completion or state communication. Long scans and maintenance operations execute off the GTK UI thread. V1.2 interaction feedback is immediate rather than continuously animated. Repository CI includes bounded repeated resize timing under Xvfb; representative continuous drag-resize on the target laptop remains a human/native acceptance gate.

## Revision-scoped evidence retained from earlier Development

These older passes remain evidence for the behavior they actually exercised, not a blanket V1.2 grant:

- dev8 `45b5f11a49f363ebcaf753c892245a31109bc9bb` — representative target accepted combined 200%-text plus compact/minimum-width core Care layout.
- dev10 `3524a4a82da87ea51dcde08992a402190b54c130` — representative target accepted system HighContrast palette authority, perceivable focus, constrained-width composition, and requested forward/reverse keyboard traversal.
- dev12 `09c3a6bcbec094dd3cb0c828de88d084fcbd5a22` — representative target accepted `GoreeCloud Care` AT-SPI application identity and the observed static roles/names/descriptions/checked/focused-state semantic slice.
- dev17 `0fda6f90a545eaf3d1bed525aae98c6529ebbf7b` — representative target accepted the targeted Maintenance Insights compact/wide typography and reachability remediation, visible Refresh focus, and selectable findings rendering.

## Current V1.2 Development evidence

The dev18 source line adds automated evidence for:

- exact Glaze target identity `1.2.0`;
- neutral V1.2 material source contract;
- 48-pixel minimum native target contract;
- Light/Dark/Deep Dark state resolution;
- Reduced Transparency and Reduced Motion source/runtime paths;
- system HighContrast failover boundary;
- absence of CSS transitions/animations in the Care V1.2 material mapping;
- process-level activation across both Care GTK windows;
- headless enlarged-text compact/regular adaptation and focus traversal.

The latest accepted exact-source Development checkpoint before this documentation synchronization is `ba646235dd12df251a02d728b096d8398a515ab7`. Care Development run `34071691286` explicitly checked out and verified that immutable revision before testing, passed all 73 tests, XML/platform-integration/source validation, the `GDK_DPI_SCALE=2` headless GTK V1.2 runtime probe, Debian `0.1.0~dev18` build and package inspection, and preserved `SOURCE_REVISION` with the artifact. Platform Contract run `34071691586` passed against the synchronized central V1.2 baseline pinned at `c941ce1d8d1eff3c9df994d1e16f83147eadae00`, and theme-source run `34071691321` passed. The exact-source package checksum is `85e4b04847d40c51654d65b06c7daee48db1cd7eac79e8433f789fe07088cf0c`, artifact ID `10000667917`. This is repository/headless CI evidence only and does not replace representative-device visual, input, assistive-technology, resilience, or package-lifecycle acceptance.

The upstream consumer-registry mechanics are now complete. `GoreeCloud/goreecloud-glaze-ui` PR #161 repaired the schemaVersion 6 consumer-registry schema, validator, guidance, and dedicated exact-source CI guard and merged at `8a0e21056acd8012a6e7482bf591027359067c81`. Follow-up PR #162 registered GoreeCloud Care in the authoritative `consumers/registry.json` and merged at `f88aa45b4d012dcfcd04a938cb71e96f9bb107d6` after all applicable Glaze workflows passed. Care is intentionally registered as `adoption-required` with `targetVersion=null`, `referenceRevision=null`, `evidence=null`, and `productionEligible=false`. Registration therefore does not establish `accepted-v1`, product conformance, Release Candidate, Stable, or production eligibility.

## Current blockers

Care remains nonconformant against the complete Stable V1.2 consumer gate until all required exact-candidate evidence is resolved and recorded, including:

- representative continuous drag-resize responsiveness under the supported 200%-text condition;
- complete Maintenance Insights forward/reverse keyboard traversal through and beyond selectable findings on the representative target;
- broader Maintenance Insights AT-SPI/Orca behavior and dynamic core status event/announcement acceptance;
- representative accepted appearance/resilience matrix, including ordinary Light/Dark behavior actually claimed, HighContrast, Reduced Transparency, and Reduced Motion;
- representative task-flow acceptance for scan, routine cleanup, permanent Trash confirmation, privileged authorization/cancellation/failure, reporting, and Insights;
- canonical Care icon target rendering and visual-quality acceptance;
- visual-quality review of supported normal, compact, enlarged-text, semantic status, empty/no-findings, confirmation, failure, and privileged-maintenance states;
- exact release-candidate regression pass against GLAZE UI V1.2 / `1.2.0`;
- governed product-specific promotion from the current registry state `adoption-required` to `accepted-v1` only after the complete Care acceptance evidence exists.

## Fail-closed rule

Missing, stale, contradictory, or unverifiable Glaze UI evidence is non-passing. A source mapping, version string, successful build, historical screenshot, registry entry, or Glaze platform-level Stable status does not by itself authorize GoreeCloud Care to claim Glaze UI conformance, production readiness, Release Candidate completion, or Stable status.
