# GoreeCloud Care — GLAZE UI consumer record

## Current development authority

GoreeCloud Care `0.2.0-dev1` is the active **Glaze UI V1.4 / `1.4.0` implementation candidate**.

It is not yet a Stable or accepted-v1.4 consumer. The exact V1.4 implementation must earn new application-specific evidence because its source, runtime/package identity, responsive composition, and active design-system provider differ from the immutable Stable `0.1.0` release.

Current V1.4 design-system source authority:

- Glaze UI target version: `1.4.0`
- Glaze UI source revision: `01c86323f8b747373d308026adc8b0881855cdc5`
- Care runtime identity: `0.2.0-dev1`
- Care Debian identity: `0.2.0~dev1`
- Care adoption state: Development / Implementation Candidate
- consumer eligibility: false until exact Care acceptance is promoted

The active Care entrypoint installs the V1.4 process controller. The main Care layout resolves through `glaze_v14.layout_environment`; V1.3 remains in-tree only as the expressive/material foundation inherited by V1.4 and as historical compatibility context.

## V1.4 native GTK3 mapping

Care is a GTK3 desktop application. Its V1.4 adaptation therefore maps Glaze form-factor semantics into native resizable desktop composition rather than pretending the application is a Mobile, Tablet, or TV client.

The mapping defines:

- Compact — narrow Care windows with reduced radius and density while preserving every task;
- Narrow Desktop — single-reading-column composition before multi-pane presentation is appropriate;
- Desktop — canonical Care desktop composition;
- Wide Desktop — increased breathing room and hierarchy without inflating targets or text merely to fill width.

The form-factor classifier uses Care's DPI-aware effective-width contract. Raw physical pixel width is not treated as logical composition width.

## Material, hierarchy, and interaction boundary

V1.4 preserves the accepted content-first principles while evolving the shell:

- functional glass is restricted to command/navigation chrome;
- reading, status, findings, and consequential-action surfaces remain opaque or near-opaque;
- one signature hero surface establishes product hierarchy without repetitive cardification;
- maintenance collections and system actions stay semantically grouped;
- destructive and privileged actions remain visually and behaviorally distinct;
- semantic shape roles are used instead of universal pills;
- focus indication remains independent of material effects;
- minimum interactive target intent remains 48 pixels;
- keyboard traversal and task order do not change merely because the window changes form-factor state.

GTK3 does not claim compositor-authoritative Living Glaze backdrop sampling or physical parity with rendering capabilities it does not provide.

## Accessibility precedence

Care's V1.4 provider must degrade embellishment before hierarchy, meaning, focus, or task completion.

Required precedence remains:

- HighContrast is system-authoritative and removes Care palette authority;
- Reduced Transparency removes decorative translucency/elevation before content distinction;
- Reduced Motion removes nonessential application-owned motion/elevation;
- Show Borders strengthens surface boundaries without requiring saturation;
- enlarged text reflows through the effective-width contract;
- visible focus remains explicit and non-color-only;
- AT-SPI status delivery and read-only Maintenance Insights remain first-class acceptance gates.

Safety-critical appearance/accessibility state is resolved before asynchronous window binding. Form-factor geometry remains allocation-driven.

## Current automated evidence

The V1.4 migration has already demonstrated green automated evidence for its pre-version-split implementation head, including:

- V1.4 static contract coverage;
- DPI-aware V1.4 headless GTK runtime acceptance;
- safe maintenance task-flow acceptance;
- live core and Maintenance Insights AT-SPI acceptance;
- Dark and Deep Dark HeaderBar contrast checks;
- Clear, Balanced, and Dense clarity geometry;
- Reduced Motion behavior;
- deterministic package construction;
- installed package lifecycle and Wardveil privilege-boundary prequalification;
- Ubuntu 22.04 / Ubuntu 24.04 byte-for-byte reproducibility.

That evidence does not automatically accept `0.2.0-dev1`. The artifact identity split intentionally requires the same gates to pass again for the exact new candidate bytes.

## Required V1.4 human/native acceptance

Before Care can claim V1.4 consumer acceptance or Stable eligibility, the exact `0.2.0` candidate must pass representative Zorin OS review covering at least:

1. Orca scan/completion announcement quality;
2. Orca cancellation/failure/success announcement quality;
3. Maintenance Insights status/results announcement quality;
4. Compact, Narrow Desktop, Desktop, and Wide Desktop rendered composition;
5. native window-control/compositor optical quality;
6. Light, Dark, Deep Dark, and HighContrast physical presentation;
7. Reduced Transparency, Reduced Motion, Show Borders, and enlarged-text behavior;
8. keyboard-only traversal, visible focus, and task order across resize states;
9. canonical Care icon and launcher rendering;
10. confirmation, empty, failure, success, and controlled privileged-task UX.

A blank, inferred, inherited, or screenshot-only result is not accepted evidence for an observation that requires physical/native review.

## Historical Stable 0.1.0 authority

Stable GoreeCloud Care `0.1.0` remains an accepted-v1 consumer of **Glaze UI V1.2 / `1.2.0`**.

That immutable historical authority remains:

- release source: `bbc4779454c2887b810aa0ddc9e8a686a4c68ebd`
- Care tree: `ebe028347c978b6d09fb1d2af011729249f63bc3`
- package SHA-256: `819cff6e0132bf6b09df0986682995c25b14c39e74982f725efd0b5a21b71160`
- representative target: Zorin OS 17.3
- Glaze authority: `c3b077cd454825cd5a74cf21ba9e5dd4c25f94ae`
- consumer status: `accepted-v1`
- target version: `1.2.0`
- evidence: `acceptance/goreecloud-care-v1.2-0.1.0-exact-source-bridge.json`

The old acceptance is retained as release history, not as authority for the V1.4 development line.

## Fail-closed rule

Glaze acceptance is exact-source and exact-artifact scoped. Any change to Care presentation behavior, canonical icon, focus/accessibility behavior, supported target/form factor, required Glaze version, runtime/package identity, or active Glaze provider invalidates assumptions that earlier acceptance transfers automatically.

`0.2.0-dev1` must therefore remain Development / nonconformant for Glaze promotion purposes until its own exact candidate evidence is complete and explicitly governed.
