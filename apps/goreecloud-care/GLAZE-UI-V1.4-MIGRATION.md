# GoreeCloud Care — Glaze UI V1.4 Migration

**Status:** Implementation Candidate  
**Target:** Glaze UI 1.4.0  
**Care branch:** `feat/goreecloud-care-glaze-ui-v1.4`  
**Glaze UI source revision:** `01c86323f8b747373d308026adc8b0881855cdc5`  
**Production / Stable claim:** Not granted

## Purpose

This migration revamps GoreeCloud Care around Glaze UI V1.4 while preserving Care's maintenance safety, privacy, accessibility, and fail-closed status semantics.

Glaze UI 1.4.0 is a form-factor evolution release built on the V1.3 expressive/material foundation. Care therefore retains the established V1.3 semantic material mapping and adds an application-specific V1.4 native desktop composition layer instead of replacing proven controls with unrelated visual effects.

## Native Care mapping

GoreeCloud Care is a GTK3 desktop application. V1.4 is mapped into four resizable native window composition states:

- `compact` — narrow Care windows with reduced surface radius and visual density while retaining every task.
- `narrow-desktop` — single-reading-column composition before multi-pane presentation is appropriate.
- `desktop` — canonical Care desktop composition.
- `wide-desktop` — increased breathing room and hierarchy without inflating targets or text merely to consume width.

These are window composition states. They do not claim that the desktop Care binary is a Mobile, Tablet, or TV product.

## Visual and interaction changes

The V1.4 layer introduces:

- Functional-glass treatment restricted to command/navigation chrome.
- Stable, opaque or near-opaque reading and consequential-action surfaces.
- More deliberate hero, status, maintenance, and system-action surface geometry.
- Desktop and Wide Desktop responsive state classes.
- Compact-window simplification without task loss or focus-order changes.
- A 48 px minimum target contract inherited and enforced at the Care mapping boundary.
- Strong visible focus treatment independent of material effects.
- Reduced-transparency, reduced-motion, border-emphasis, and HighContrast precedence.
- Application/window binding through the GTK application `window-added` lifecycle and `size-allocate` updates.

## Source architecture

New runtime modules:

- `goreecloud_care/glaze_v14.py` — V1.4 semantic mapping, form-factor resolution, CSS, and per-window controller.
- `goreecloud_care/glaze_v14_global.py` — process-level provider and window lifecycle synchronization.

The package entrypoint now installs the V1.4 process controller instead of the V1.3 global provider.

The V1.3 implementation remains in-tree as the immediately preceding compatibility/reference layer and provides the expressive/material foundation inherited by V1.4.

## Acceptance policy

This migration must not be marked Stable or Glaze UI V1.4 conformant solely because the Glaze UI design-system release was Stable.

Care requires fresh application-specific evidence for this new source identity. At minimum, promotion should require:

1. Static V1.4 contract tests.
2. Full existing GoreeCloud Care test suite.
3. GTK CSS parse/runtime validation on the representative Zorin OS image.
4. Rendered review at compact, narrow-desktop, desktop, and wide-desktop window sizes.
5. Keyboard-only and visible-focus validation.
6. HighContrast validation with the Care provider removed from palette authority.
7. Reduced-motion and reduced-transparency validation.
8. Light, Dark, and Deep Dark appearance review.
9. Scan, cleanup preview, confirmation, cancellation, privilege-denial, success, and failure-state regression checks.
10. Install/upgrade/rollback and packaging validation before any production claim.

Until those gates pass for the exact migration head, the correct state is **Implementation Candidate / Development adoption**.

## Follow-up improvements

After V1.4 acceptance, the next Care design work should focus on improving information architecture and system-health orchestration without weakening the product boundary between maintenance truth and presentation. Any later Glaze UI migration should create a new application-specific evidence identity rather than inheriting this migration's acceptance automatically.
