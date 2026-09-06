# GoreeCloud Care — Wardveil Security Integration

## Scope

GoreeCloud Care uses the current Wardveil Security status semantics for a narrowly scoped security-evidence producer covering the installed Care privileged-maintenance boundary. This integration does not make Wardveil the executor of Care maintenance and does not grant Wardveil arbitrary command authority.

## Authoritative producer

GoreeCloud Care is authoritative only for these Care-owned facts:

- the installed fixed helper location;
- the installed Care PolicyKit policy location;
- whether those fixed files satisfy the expected root-ownership and write-permission constraints;
- whether `/usr/bin/pkexec` is available for the existing PolicyKit flow;
- the source-enforced helper action allowlist and no-arbitrary-shell/path boundary.

PolicyKit, the operating system, and APT remain authoritative for their own behavior. Wardveil Security remains authoritative for Wardveil security semantics and any future Wardveil-native policy, scanning, quarantine, incident, or audit service.

## Local status API

`goreecloud-care --security-status-json` returns a record shaped to `contracts/wardveil.status.schema.json` from the current Wardveil Security authority.

A passing result requires the fixed helper and policy files to be regular files owned by the expected root UID, neither file to be group/world writable, the helper to be owner-executable, and `/usr/bin/pkexec` to be executable. Missing or non-passing evidence produces `attention` rather than a passing status.

The record deliberately sets `claim.protected_by_wardveil` to `false`. Care must not display or advertise `Protected by Wardveil` merely because it emits a Wardveil-compatible status record.

## Privacy boundary

The shared record omits user identity, arbitrary local file paths, raw privileged command output, credentials, secrets, and unrestricted diagnostics. It reports only the scoped normalized state, observation/freshness data, and a short summary.

## Failure and freshness behavior

Missing helper/policy/pkexec evidence fails closed to a non-passing state. A passing record receives a short validity interval so stale evidence cannot remain indefinitely reassuring. Consumers must re-evaluate after expiry.

## High-impact actions

Care does not currently accept Wardveil runtime-authorization envelopes for `apt-clean`, file-cache reclaim, user-file cleanup, or Trash deletion. Existing Care actions retain their explicit local user confirmation, PolicyKit, ownership, fixed-allowlist, and application-specific authorization boundaries. Therefore Wardveil's high-impact cross-service executor requirements are not claimed as implemented by this integration.

## Acceptance boundary

Source-level tests must cover passing and non-passing installation evidence, sensitive-field minimization, normalized state, freshness, and the absence of a false `Protected by Wardveil` claim. Exact-revision target-device acceptance remains required before Care may mark Wardveil integration as production-conformant in `goreecloud.platform.yaml`.
