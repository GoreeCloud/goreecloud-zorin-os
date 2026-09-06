# GoreeCloud Care — GLAZE UI V1.1 Conformance Record

## Authority and status

Current required Stable consumer baseline: **GLAZE UI V1.1 / 1.1.0**.

GoreeCloud Care is a native GTK 3 application. Native GTK controls are used as the platform implementation primitives for Glaze UI semantics; they are not an exemption from the design system. This record is intentionally fail closed: Care does not claim current-Stable Glaze UI conformance until all required product-specific native, rendered, accessibility, resilience, task-flow, form-factor, and visual-quality evidence is accepted for the intended release candidate.

Lifecycle at this record: Development.

## Native mapping

### Structure and hierarchy

- `Gtk.HeaderBar` provides application identity and primary command placement.
- Primary content is vertically ordered with explicit heading/body/status hierarchy.
- Maintenance categories use bounded card-like frames rather than undifferentiated page text.
- Destructive Trash handling remains visually and behaviorally separate from routine reversible/recreatable cleanup.
- Maintenance Insights is a separate explicit read-only review surface.

### Readability and solid decision surfaces

Care uses solid high-readability content surfaces for explanatory text, maintenance categories, confirmation dialogs, findings, and destructive/privileged decisions. It does not place critical decision copy behind decorative translucent effects. The current GTK implementation therefore maps the Stable Glaze rule that explicit reading and critical decisions resolve on dependable readable surfaces.

### Semantic state and feedback

The core Care window exposes textual status titles and body copy for informational, attention, success, and error states. Semantic meaning is never color-only. Cancellation, authorization failure, partial cleanup, scan failure, and success are separate outcomes. The persistent status surface exposes ATK status-bar semantics and updates its accessible name when state changes.

### Accessibility and input

- Explicit GLib program/application identity is set before GUI startup.
- Interactive buttons and selectors are keyboard focusable.
- A theme-resilient focus provider retains perceivable focus without defining an application palette.
- System HighContrast disables Care's application CSS mapping so the system palette remains authoritative.
- Compact and enlarged-text layouts preserve vertical reachability.
- Maintenance Insights exposes accessible status/results names and an accessible symbolic Refresh action.
- Selectable findings preserve copy/read behavior while remaining read-only.

### Responsive and adaptive behavior

Care uses a shared effective-width contract that accounts for `GDK_DPI_SCALE` when deciding compact composition. At constrained widths, actions stack vertically, HeaderBar pressure is reduced, category values move below their body copy, and the page remains vertically scrollable. Maintenance Insights additionally retains an independently scrollable findings surface with a 320-pixel minimum viewport.

### Appearance

Care currently prefers a light application appearance while respecting the system HighContrast theme. This is an application-local setting only and does not modify the desktop/global appearance preference. A final supported appearance matrix must be resolved and accepted before Stable; Care must not claim unsupported dark/system behavior merely because GTK can render it.

### Motion and performance

Care does not depend on decorative animation for task completion or state communication. Long scans and maintenance operations execute off the GTK UI thread. Continuous drag-resize performance for the large-text Maintenance Insights surface remains an explicit target-device acceptance gate.

## Revision-scoped accepted evidence

The following evidence is intentionally scoped to the exact revision and behavior tested; it is not a blanket conformance grant:

- dev8 `45b5f11a49f363ebcaf753c892245a31109bc9bb` — representative target accepted combined 200%-text plus compact/minimum-width core Care layout.
- dev10 `3524a4a82da87ea51dcde08992a402190b54c130` — representative target accepted system HighContrast palette authority, perceivable focus, constrained-width composition, and requested forward/reverse keyboard traversal.
- dev12 `09c3a6bcbec094dd3cb0c828de88d084fcbd5a22` — representative target accepted `GoreeCloud Care` AT-SPI application identity and the observed static roles/names/descriptions/checked/focused-state semantic slice.
- dev17 `0fda6f90a545eaf3d1bed525aae98c6529ebbf7b` — representative target accepted the targeted Maintenance Insights compact/wide typography and reachability remediation, visible Refresh focus, and selectable findings rendering; 50 tests plus XML/source validation and package install also passed.

## Current blockers

Care remains nonconformant against the complete Stable consumer gate until all of the following are resolved and recorded at the release-candidate revision:

- continuous drag-resize responsiveness under the supported 200%-text target condition;
- complete Maintenance Insights forward/reverse keyboard traversal through and beyond selectable findings;
- broader Maintenance Insights AT-SPI/Orca behavior and dynamic core status event/announcement acceptance;
- final supported appearance matrix and native visual acceptance;
- representative task-flow acceptance for scan, routine cleanup, permanent Trash confirmation, privileged authorization/cancellation/failure, reporting, and Insights;
- official canonical GoreeCloud Care icon/branding and rendered target acceptance;
- complete visual-quality review of the supported normal, compact, enlarged-text, HighContrast, confirmation, failure, empty/no-findings, and privileged-maintenance states;
- exact release-candidate regression pass confirming no dependence on V1.2 Candidate behavior;
- product-specific production approval and synchronization with the Glaze UI consumer registry if that registry is used for Care acceptance.

## Fail-closed rule

Missing, stale, contradictory, or unverifiable Glaze UI evidence is a non-passing state. A source mapping, design-system version string, successful build, or historical screenshot does not by itself authorize GoreeCloud Care to claim Glaze UI conformance, production readiness, Release Candidate completion, or Stable status.
