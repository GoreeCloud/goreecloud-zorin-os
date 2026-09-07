# GoreeCloud Care — Wardveil Security Integration

## Scope

GoreeCloud Care uses the current Wardveil Security status semantics for a narrowly scoped security-evidence producer covering the installed Care privileged-maintenance boundary. This integration does not make Wardveil the executor of Care maintenance and does not grant Wardveil arbitrary command authority.

## Authoritative producer

GoreeCloud Care is authoritative only for these Care-owned facts:

- the installed fixed helper location;
- the installed Care PolicyKit policy location;
- whether those fixed files satisfy the expected root-ownership and write-permission constraints;
- whether `/usr/bin/pkexec` is available for the existing PolicyKit flow;
- the source-enforced helper action allowlist and no-arbitrary-shell/path boundary;
- whether the installed application/helper launchers use isolated Python path semantics so a user-controlled working directory, `PYTHONPATH`, or user site cannot shadow the installed Care package;
- whether the fixed private Care Python package directory is free of stale runtime bytecode that could affect cross-version execution.

PolicyKit, the operating system, and APT remain authoritative for their own behavior. Wardveil Security remains authoritative for Wardveil security semantics and any future Wardveil-native policy, scanning, quarantine, incident, or audit service.

## Installed launcher isolation

Dev18 representative package-lifecycle testing found that the pre-dev19 launchers used plain `python3 -m goreecloud_care...`. When the installed package had been downgraded to dev17 but the command was launched from the dev18 source directory, Python resolved the working-tree dev18 package and reported the wrong runtime version. The privileged helper used the same ambient import pattern, so this is treated as a security-boundary defect rather than merely a test-harness issue.

Dev19 requires both installed entrypoints to use `/usr/bin/python3 -I -B -m ...`. `-I` excludes the current working directory, `PYTHONPATH`, and user site from import resolution; `-B` prevents new runtime bytecode writes. Debian `postinst`/`postrm` scripts remove only the fixed private Care `__pycache__` path so bytecode created by earlier Development versions cannot survive an install/remove transition. Installed acceptance deliberately attempts same-named working-directory shadowing against both entrypoints.

This hardening is Care-owned evidence only. It does not authorize a `Protected by Wardveil` claim and remains target-unaccepted until the exact dev19 candidate completes representative lifecycle/runtime validation.

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

Source-level tests must cover passing and non-passing installation evidence, sensitive-field minimization, normalized state, freshness, launcher isolation, private bytecode cleanup, and the absence of a false `Protected by Wardveil` claim. Exact-revision target-device acceptance remains required before Care may mark Wardveil integration as production-conformant in `goreecloud.platform.yaml`.
