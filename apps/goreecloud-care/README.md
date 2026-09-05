# GoreeCloud Care

**Lifecycle:** Development  
**Version:** `0.1.0-dev10`  
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
- Large-text-aware compact selection: `GDK_DPI_SCALE` is converted into an effective layout width before the compact contract is evaluated.
- Compact HeaderBar behavior that omits the Development subtitle when the compact composition is active.
- GTK/ATK status semantics, category-count accessible names, and action/selector descriptions.
- HighContrast takeover detection through both `Gtk.Settings:gtk-theme-name` and a process-local `GTK_THEME` override.
- Dev10 theme-resilient keyboard-focus fallback: a focus-only GTK provider remains below Care's normal application CSS and uses the active theme foreground color, preserving the established normal Care focus treatment while ensuring HighContrast does not lose visible keyboard focus when the normal palette provider is suppressed.
- A minimum supported Development window size plus vertical scrolling and wrapping for long/status/system text.
- No telemetry, advertising, cloud upload, or network requirement.
- Symlink-safe user cleanup: links are unlinked, never traversed.

## Build and test

```sh
sh ./scripts/validate.sh
sh ./scripts/build-deb.sh
```

Representative Zorin OS 17.3 testing through dev5 verifies the current maintenance functions, including controlled nonzero cache/temp/Trash/APT deletion and privileged success/cancellation reporting. Dev6 verified normal-text compact/minimum-window behavior; dev8 closed the combined 200%-text + compact/minimum-width adaptive-layout blocker on exact runtime head `45b5f11a49f363ebcaf753c892245a31109bc9bb`.

HighContrast target work remains in progress. The first pass showed visible focus but failed palette takeover. Dev9 corrected the takeover detection. A fresh dev9 target screenshot now provides positive evidence that the system HighContrast presentation replaces Care's light Development palette, but pressing **Tab** produces no visibly perceivable focus response. Because the explicit Care focus CSS is intentionally removed together with the normal palette provider in HighContrast, dev10 adds a separate theme-derived focus-only fallback beneath the ordinary Care CSS. This is a source remediation candidate, not target acceptance; the dev10 package must be installed and revalidated on the representative laptop.

The generated Debian package is Development software. HighContrast keyboard/resilience acceptance, assistive-technology acceptance, package rollback, official GoreeCloud Care visual assets, full current-Stable Glaze UI V1.1 acceptance, and broader GoreeCloud platform-system acceptance remain required before Release Candidate consideration.

## Install or upgrade a locally built Development package

```sh
sudo apt install ./dist/goreecloud-care_0.1.0~dev10_all.deb
```

Uninstall with:

```sh
sudo apt remove goreecloud-care
```

The canonical source-control authority is `GoreeCloud/goreecloud-zorin-os`. GoreeCloud Care is maintained as the `apps/goreecloud-care/` component so its Zorin OS packaging, desktop integration, and target-device acceptance remain coupled to the GoreeCloud Zorin OS development surface while preserving a distinct application boundary.
