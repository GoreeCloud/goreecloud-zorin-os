# GoreeCloud Care Release Acceptance

## Governing rule

GoreeCloud Care follows the GoreeCloud lifecycle:

`Development -> Release Candidate -> Stable`

The lifecycle is evidence-based. A passing build, successful package installation, working feature, or individual screenshot does not permit a lifecycle promotion by itself.

## Development exit criteria

Before a Care build may be nominated as a Release Candidate, it must have an exact immutable candidate revision and package artifact and must satisfy all applicable source-level gates. At minimum:

- all repository tests and source guards pass at the exact candidate revision;
- the Platform Contract manifest is structurally valid and records no known source-level falsehoods;
- the Privacy Shield, Wardveil Security, Everkeep, and Glaze UI repository-local integration records are current;
- all intended RC functionality is source-complete and documented;
- the official canonical Care application identity/branding exists and is consumed from the branding-assets authority;
- known release-blocking security, privacy, accessibility, compatibility, recovery, data-integrity, or visual-quality defects are resolved rather than waived;
- package build metadata, application metadata, documentation, and lifecycle records agree on the candidate version.

## Release Candidate target acceptance

The exact RC package must then receive representative Zorin OS target acceptance covering:

### Package lifecycle

- clean install;
- Development-to-RC upgrade where relevant;
- removal and reinstall;
- downgrade or rollback to the explicitly supported prior package state;
- post-rollback launch and report validation;
- package-owned helper/policy/desktop/AppStream files removed or restored as expected;
- no user data loss beyond explicitly authorized maintenance actions.

### Core maintenance task flows

- scan without deletion;
- routine selected cache/temp cleanup after explicit confirmation;
- no-selection and stale-preview handling;
- permanent Trash confirmation and cancellation boundary;
- APT authorization success, cancellation, denial/failure handling;
- file-cache reclaim warning, authorization and truthful completion language;
- post-action refresh preserving the final operation result;
- symlink-safe behavior and ownership boundary.

Testing destructive flows may use disposable fixtures or purpose-created test data. Acceptance must not require deleting unrelated personal content.

### Reports and local integration API

- `--version` and `--api-version`;
- human and JSON report output;
- local health output;
- Privacy Shield status output and data minimization;
- Wardveil-compatible security status and installed privilege-boundary verification;
- Everkeep continuity status;
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
- normal, compact, enlarged-text, HighContrast, status, confirmation, failure, empty/no-findings, and privileged-action states are visually complete;
- the current Stable GLAZE UI V1.1 mapping is accepted on the target device;
- the official canonical Care icon renders correctly in application/desktop surfaces;
- no Candidate Glaze UI V1.2 behavior is required for RC/Stable acceptance while V1.1 remains current Stable.

## Stable promotion

Stable promotion occurs only after the accepted RC revision/package completes final production-readiness review without a release blocker. The authoritative Care project specification, repository Platform Contract, changelog, release artifact record, and other material status locations must then be synchronized to Stable.

Stable additionally requires the applicable current approved contracts and application-specific acceptance for:

- GLAZE UI;
- Privacy Shield;
- Wardveil Security;
- Everkeep;
- any other Platform System classified applicable for that release scope.

Manager, Mesh, and Identity may be `not-applicable-justified` only when the released local single-user scope genuinely does not require their runtime authority or integration. Adding remote management, cross-application coordination, accounts, delegated administration, or multi-user behavior reopens those applicability decisions.

## Fail-closed promotion rule

Any unresolved required gate remains a blocker. Care must not be represented as Release Candidate-complete or Stable when required evidence is missing, stale, contradictory, failed, or not run.
