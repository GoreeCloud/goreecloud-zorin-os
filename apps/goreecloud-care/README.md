# GoreeCloud Care

**Lifecycle:** Development  
**Version:** `0.1.0-dev8`  
**Canonical source:** `GoreeCloud/goreecloud-zorin-os` → `apps/goreecloud-care/`  
**Target:** Zorin OS 17.3 and compatible GTK 3 Linux desktops  
**License:** GPL-3.0-or-later

GoreeCloud Care is an original, local-first GoreeCloud desktop maintenance application. It previews reclaimable storage before deletion and keeps normal cache/temp cleanup unprivileged.

## Current Development features

- Scan and clean application cache files older than 7 days.
- Clean the thumbnail cache.
- Scan and clean user-owned `/tmp` files older than 7 days.
- Preview Trash usage and empty Trash only after a separate permanent-deletion confirmation.
- Preview APT `.deb` cache and clean it through PolicyKit authorization.
- Display disk, available-memory, and file-cache status.
- “Memory Refresh” action that truthfully reclaims Linux file caches after a warning and PolicyKit authorization. It does **not** claim a lasting RAM/performance boost.
- Explicit keyboard-focus presentation for interactive controls and fail-safe Cancel-first confirmation dialogs.
- Explicit cancellation status for GoreeCloud Care confirmation dialogs so cancelling an operation never fails silently.
- More prominent semantic status presentation with a symbol, bold state label, stronger surface/border treatment, and text so changed state does not depend on color alone.
- Light appearance by default inside GoreeCloud Care without changing the user's Zorin OS desktop-wide appearance setting.
- Explicit PolicyKit cancellation/error reporting, including the observed Zorin OS `Request dismissed` result, so a dismissed authentication request is never presented as success.
- Explicit completion notice for successful privileged APT cache cleanup and Memory Refresh.
- Post-action refresh that updates scan values without replacing the final completion/exception status.
- Adaptive desktop composition: category amounts move below their content and primary actions stack vertically before constrained or enlarged-text layouts become horizontally compressed.
- Dev8 large-text-aware compact selection: the GTK `GDK_DPI_SCALE` used by the 200%-text acceptance harness is converted into an effective layout width before the 820-logical-pixel compact contract is evaluated, preventing the text-scaled allocation from hiding a physically narrow window.
- Compact HeaderBar behavior that omits the Development subtitle when the compact composition is active instead of relying on visible ellipsis.
- GTK/ATK status semantics: the maintenance status surface exposes a status role and updated accessible name, category counts expose descriptive accessible names, and action controls include clearer assistive descriptions.
- High-contrast resilience: common GTK HighContrast theme names suppress the application color provider so the system high-contrast presentation can take precedence.
- A minimum supported Development window size plus vertical scrolling and wrapping for long/status/system text to improve large-text and constrained-window behavior.
- No telemetry, advertising, cloud upload, or network requirement.
- Symlink-safe user cleanup: links are unlinked, never traversed.

## Build and test

```sh
sh ./scripts/validate.sh
sh ./scripts/build-deb.sh
```

Representative Zorin OS 17.3 testing through dev5 verifies light-default rendering, visible keyboard focus, both first-stage and PolicyKit cancellation paths, successful privileged Memory Refresh and APT cleanup, nonzero APT archive removal, controlled application-cache deletion, thumbnail-cache deletion, stale user-owned `/tmp` deletion, permanent Trash deletion, completion reporting, and post-action refresh behavior. Dev6 target testing verified the normal-text compact/minimum-window composition but exposed a combined 200%-text defect. Dev7 raised the normal-text compact threshold to 820 logical pixels and passed exact-head CI plus local dev7 source/package validation on the representative laptop, yet direct `GDK_DPI_SCALE=2` screenshots still showed the regular composition at the narrowest reachable window: the HeaderBar subtitle remained visible, category amounts stayed right-aligned, and the bottom actions remained horizontal. Dev8 addresses that verified target-device failure by evaluating an effective width adjusted for the 200%-text DPI scale. Dev8 still requires fresh repository validation and representative-device rendered acceptance before combined 200%-text/compact acceptance is claimed.

The generated Debian package is Development software. Package rollback, official GoreeCloud Care visual assets, HighContrast/assistive-technology acceptance, full current-Stable Glaze UI acceptance, and broader GoreeCloud platform-system acceptance remain required before Release Candidate consideration.

## Install or upgrade a locally built Development package

```sh
sudo apt install ./dist/goreecloud-care_0.1.0~dev8_all.deb
```

Uninstall with:

```sh
sudo apt remove goreecloud-care
```

The canonical source-control authority is `GoreeCloud/goreecloud-zorin-os`. GoreeCloud Care is maintained as the `apps/goreecloud-care/` component so its Zorin OS packaging, desktop integration, and target-device acceptance remain coupled to the GoreeCloud Zorin OS development surface while preserving a distinct application boundary.
