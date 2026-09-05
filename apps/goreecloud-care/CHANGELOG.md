# Changelog

## 0.1.0-dev7 — 2026-09-05
- Recorded direct representative-device negative evidence for the dev6 combined 200%-text/compact path: at the narrowest reachable `GDK_DPI_SCALE=2` window, the regular horizontal composition remained active, category amounts stayed right-aligned, and the bottom action group could not transition to the previously accepted compact stack.
- Raised the Development compact transition from 680 to 820 logical pixels so compact composition activates before the observed enlarged-text minimum-width floor.
- Reused the pure `is_compact_width()` contract in the GTK layout path and added regression coverage for the observed approximately 800-pixel enlarged-text range.
- Compact HeaderBar presentation now omits the Development subtitle instead of leaving it visibly ellipsized, reducing width pressure while preserving the product title and Scan action.
- This is a Development remediation candidate. Combined 200%-text/compact rendering remains unaccepted until the dev7 package is rebuilt, installed, and revalidated on the representative Zorin OS laptop.

## 0.1.0-dev6 — 2026-09-05
- Started the accessibility and adaptive-window acceptance phase after representative-device dev5 testing verified every current maintenance function, including controlled nonzero APT archive removal.
- Added a compact desktop composition below 680 logical pixels: category amounts move below their category content and the primary bottom actions stack vertically instead of compressing horizontally.
- Defined a 480 × 420 logical-pixel minimum Development window and retained vertical scrolling so constrained-height and larger-text layouts remain reachable.
- Added text wrapping for system status and category headings to reduce clipping risk under constrained width or large text.
- Added GTK/ATK status semantics, dynamic accessible status names, action descriptions, selector descriptions, and descriptive accessible names for scanned category amounts.
- Added high-contrast resilience: common GTK HighContrast theme names suppress the application color provider so the system high-contrast theme can take precedence over GoreeCloud Care's light Development mapping.
- Added pure adaptive/high-contrast UI contract helpers and unit coverage without importing GTK into the test boundary.
- Added an explicit `gir1.2-atk-1.0` package dependency for the new ATK accessibility mapping.
- Dev6 source work does not establish rendered, large-text, high-contrast, screen-reader, or current-Stable Glaze UI acceptance until target-device evidence is completed.

## 0.1.0-dev5 — 2026-09-05
- Fixed post-action status replacement that could hide successful privileged-action feedback behind the automatic refresh scan.
- Added an explicit completion notice after successful PolicyKit-authorized APT cache cleanup and Memory Refresh.
- Added a post-action refresh path that updates scan values without overwriting the final success/attention result.
- Applied the same status-preservation behavior to normal selected cleanup and Trash cleanup so their final result remains visible after values refresh.
- If a maintenance action completes but the follow-up scan fails, GoreeCloud Care now preserves the completed-action fact while reporting the refresh failure as an attention state instead of falsely claiming a fully refreshed result.
- Repository validation is green; representative-device successful privileged-action execution remains a required acceptance gate before success is treated as verified.

## 0.1.0-dev4 — 2026-09-05
- Changed GoreeCloud Care to open in a light appearance by default without modifying the user's desktop-wide Zorin OS appearance setting.
- Reworked the persistent maintenance-status surface into a higher-salience semantic indicator with a symbol, bold state title, stronger border/surface treatment, and explicit text so changed state is not communicated by color alone.
- Classified ordinary user cancellation as an attention/changed-state condition rather than a warning or error; cancellation now uses a prominent but non-critical presentation.
- Added distinct informational, attention, success, and error status treatments mapped from current Glaze UI V1.1 semantic roles while keeping final Glaze UI conformance/acceptance explicitly open.
- Preserved the representative-device-verified high-contrast keyboard-focus treatment.
- Added source validation checks for the light-default preference and attention-status implementation.

## 0.1.0-dev3 — 2026-09-05
- Preserved the dev2 keyboard-focus treatment after representative Zorin OS screenshots verified that focus is now visibly perceivable on checkboxes and buttons.
- Added explicit status feedback when a user cancels any GoreeCloud Care confirmation dialog, including cache cleanup, Trash emptying, APT cache cleanup, and memory-cache reclaim; cancellation now states that no corresponding changes were made.
- Hardened PolicyKit cancellation classification using the actual Zorin OS dismissal text (`Error executing command as another user: Request dismissed`) in addition to pkexec exit status 126.
- Added regression coverage proving that the observed Zorin OS `Request dismissed` result is treated as cancellation and never as success.
- Aligned the Python runtime version declaration with the Development package version.

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
