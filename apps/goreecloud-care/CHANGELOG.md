# Changelog

## 0.1.0-dev2 — 2026-09-04
- Added an explicit high-contrast keyboard focus treatment and explicit focusability for interactive controls after representative Zorin OS testing found Tab traversal was not visibly perceivable.
- Moved operation status into a persistent near-top status banner so scan and maintenance results remain visible without scrolling to the bottom of the window.
- Added explicit PolicyKit/pkexec cancellation handling: exit status 126 now produces a visible cancellation dialog and states that the privileged maintenance command was not run and no privileged changes were made.
- Added explicit non-success handling for authorization errors and helper failures, with unit coverage for success, cancellation, authorization failure, and helper failure outcomes.
- Kept confirmation dialogs fail-safe by defaulting keyboard focus to Cancel.

## 0.1.0-dev1 — 2026-09-04
- Initial GoreeCloud Care Development bootstrap.
- Added safe cache, thumbnail, stale temp, Trash, APT cache, disk/memory status, and file-cache reclaim foundations.
- Added PolicyKit boundary, tests, Debian packaging, component-local GoreeCloud documentation, and a Platform Contract v0.2 component declaration.
- Integrated source ownership into `GoreeCloud/goreecloud-zorin-os` under `apps/goreecloud-care/`; no separate Care repository is authoritative.
