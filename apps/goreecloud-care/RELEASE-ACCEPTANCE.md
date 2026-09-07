# GoreeCloud Care Release Acceptance

## Governing rule

GoreeCloud Care follows the GoreeCloud lifecycle:

`Development -> Release Candidate -> Stable`

The lifecycle is evidence-based. A passing build, successful package installation, working feature, registry entry, individual screenshot, or Care-produced platform-status record does not permit a lifecycle promotion by itself.

## Development exit criteria

Before a Care build may be nominated as a Release Candidate, it must have an exact immutable candidate revision and package artifact and must satisfy all applicable source-level gates. At minimum:

- all repository tests and source guards pass at the exact candidate revision;
- the Platform Contract manifest is structurally valid and records no known source-level falsehoods;
- the Privacy Shield, Wardveil Security, Everkeep, and Glaze UI repository-local integration records are current;
- all intended RC functionality is source-complete and documented;
- the official canonical Care application identity/branding exists and is consumed from the branding-assets authority;
- known release-blocking security, privacy, accessibility, compatibility, recovery, data-integrity, packaging, reproducibility, or visual-quality defects are resolved rather than waived;
- package build metadata, application metadata, documentation, and lifecycle records agree on the candidate version;
- installed Python entrypoints are isolated from the invoking working directory, `PYTHONPATH`, and user-site package shadowing, including the privileged PolicyKit helper boundary;
- package install/remove behavior does not leave stale private Python bytecode or package-owned provenance capable of affecting a later installed revision;
- every file that can enter the Debian package is part of the exact committed Care source; untracked package inputs fail closed;
- the exact package is reproducible within one build environment and byte-identical across the supported Ubuntu 22.04 / Ubuntu 24.04 packaging boundary used to represent Zorin OS 17.3 and current CI;
- the package contains root-controlled build provenance naming the exact source revision, Care source-tree identity, runtime version, package version, and deterministic source timestamp.

The package SHA-256 is deliberately not embedded inside the package whose digest it would describe. Exact package identity is bound externally by target-runtime acceptance and governed platform evidence.

## Release Candidate target acceptance

The exact RC package must then receive representative **Zorin OS 17.3** target acceptance covering the following areas.

### Package lifecycle

- clean install;
- Development-to-RC upgrade where relevant;
- removal and reinstall;
- downgrade or rollback to the explicitly supported prior package state;
- post-rollback launch and report validation;
- package-owned helper/policy/desktop/AppStream/provenance files and directories removed or restored as expected;
- installed application and helper launchers resolve the installed package even when invoked from a working directory containing a same-named `goreecloud_care` package;
- private package bytecode/cache residue does not survive removal or cause cross-version execution;
- final installed package-owned provenance exactly matches the candidate source revision, Care source tree, runtime version, and package version;
- no user data loss beyond explicitly authorized maintenance actions.

The authoritative automated representative-device runner is `scripts/run-representative-acceptance.sh`. It must be run as the normal desktop user on Zorin OS 17.3. It runs source validation, deterministic package construction, same-environment reproducibility verification, accepted dev17 rollback-package preparation, and the complete install/remove/reinstall/downgrade/restore lifecycle. It does **not** invoke a Care cleanup action and does **not** grant Everkeep promotion.

Testing destructive flows may use disposable fixtures or purpose-created test data. Acceptance must not require deleting unrelated personal content.

### Continuity / Everkeep authority boundary

Care is an evidence producer, not the Everkeep governance authority.

After exact representative-device acceptance passes, Care may create and install only its root-controlled target handoff at:

`/var/lib/goreecloud-care/acceptance/representative-target.json`

That Care-owned record must name the exact source revision, Care source tree, runtime/package versions, package SHA-256, representative Zorin target, local test count, and package-lifecycle result. By construction it must leave:

- `everkeep_integration_promoted = false`
- `everkeep_ready_promoted = false`

A Care-owned target record by itself may advance the local continuity explanation only to `attention / target-accepted-governance-pending`. It cannot make Care Everkeep-ready.

`ready / everkeep-promoted` is allowed only when a separate root-controlled **Everkeep-owned** governance record exists at:

`/var/lib/goreecloud/everkeep/acceptance/goreecloud-care.target-runtime.json`

and that record:

- matches the installed package provenance source revision, Care source tree, runtime version, and package version;
- names Zorin OS 17.3 as the representative target and records a passing target lifecycle;
- has the same exact package SHA-256 as the Care-owned representative-target record;
- explicitly promotes both Everkeep integration and Everkeep readiness;
- is a regular root-owned file in a root-owned directory with neither file nor immediate parent group/other writable.

Missing, malformed, oversized, writable, symlinked, source-mismatched, target-mismatched, package-mismatched, or unpromoted evidence fails closed. `contracts/continuity.status.schema.json` defines the machine-readable Care continuity status boundary.

### Core maintenance task flows

- scan without deletion;
- routine selected cache/temp cleanup after explicit confirmation;
- no-selection and stale-preview handling;
- permanent Trash confirmation and cancellation boundary;
- APT authorization success, cancellation, denial/failure handling;
- file-cache reclaim warning, authorization and truthful completion language;
- post-action refresh preserving the final operation result;
- symlink-safe behavior and ownership boundary.

### Reports and local integration API

- `--version` and `--api-version`;
- human and JSON report output;
- local health output;
- Privacy Shield status output and data minimization;
- Wardveil-compatible security status and installed privilege-boundary verification;
- evidence-derived Everkeep continuity status;
- malformed/unexpected CLI combinations fail without falling through to the GUI or performing maintenance.

### Accessibility and adaptive behavior

- normal and constrained desktop layout;
- 200% text / effective large-text layout;
- HighContrast system palette authority;
- visible keyboard focus;
- complete forward and reverse keyboard traversal for core Care and Maintenance Insights;
- no focus trap in selectable findings;
- AT-SPI application identity, roles, names, descriptions, checked/focused state, and dynamic status state mutation;
- Orca announcement quality for scan completion, cancellation/failure, successful completion, and Maintenance Insights status where applicable;
- true-bottom reachability for page and findings surfaces.

### Performance and resilience

- continuous narrow/wide window resizing at the supported large-text condition is responsive enough for ordinary desktop use and does not freeze the UI;
- scans and maintenance operations do not block GTK interaction for an unreasonable duration;
- bounded Insights discovery remains bounded and discloses partial results;
- malformed or unavailable local integration evidence fails closed rather than becoming a passing state.

### Appearance and visual quality

- final supported appearance matrix is explicitly documented;
- normal, compact, enlarged-text, Light/Dark where claimed, HighContrast, Reduced Transparency, Reduced Motion, status, confirmation, failure, empty/no-findings, and privileged-action states are visually complete;
- the current Stable **GLAZE UI V1.2 / `1.2.0`** native mapping is accepted on the target device for every Care appearance/resilience mode claimed by the release;
- Proposed GLAZE UI V1.3 Adaptive Resonance development work may be reviewed as forward-looking evidence but cannot be represented as Candidate/Stable conformance until upstream governance activates it and Care becomes eligible;
- the official canonical Care icon renders correctly in application/desktop surfaces;
- the authoritative Glaze consumer registry records Care only at the state justified by product-specific evidence. Registration as `adoption-required` is not conformance; promotion requires complete exact-candidate Care acceptance.

## Stable promotion

Stable promotion occurs only after the accepted RC revision/package completes final production-readiness review without a release blocker. The authoritative Care project specification, repository Platform Contract, changelog, release artifact record, and other material status locations must then be synchronized to Stable.

Stable additionally requires the applicable current approved contracts and application-specific acceptance for:

- GLAZE UI V1.2 / `1.2.0` (or a newer current Stable contract only if governance changes before the candidate is qualified);
- Privacy Shield;
- Wardveil Security;
- Everkeep;
- any other Platform System classified applicable for that release scope.

Manager, Mesh, and Identity may be `not-applicable-justified` only when the released local single-user scope genuinely does not require their runtime authority or integration. Adding remote management, cross-application coordination, accounts, delegated administration, or multi-user behavior reopens those applicability decisions.

## Fail-closed promotion rule

Any unresolved required gate remains a blocker. Care must not be represented as Release Candidate-complete or Stable when required evidence is missing, stale, contradictory, failed, mismatched, untrusted, or not run.
