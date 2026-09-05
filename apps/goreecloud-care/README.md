# GoreeCloud Care

**Lifecycle:** Development  
**Version:** `0.1.0-dev3`  
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
- Explicit PolicyKit cancellation/error reporting, including the observed Zorin OS `Request dismissed` result, so a dismissed authentication request is never presented as success.
- No telemetry, advertising, cloud upload, or network requirement.
- Symlink-safe user cleanup: links are unlinked, never traversed.

## Build and test

```sh
sh ./scripts/validate.sh
sh ./scripts/build-deb.sh
```

The generated Debian package is Development software. Representative Zorin OS 17.3 source validation, build, installation, launch, initial rendering, and keyboard-focus visibility have been exercised. The dev3 cancellation-feedback changes still require target-device revalidation. Actual privileged-success behavior, cleanup acceptance, package rollback, official GoreeCloud Care visual assets, Glaze UI acceptance, and broader GoreeCloud platform-system acceptance remain required before Release Candidate consideration.

## Install or upgrade a locally built Development package

```sh
sudo apt install ./dist/goreecloud-care_0.1.0~dev3_all.deb
```

Uninstall with:

```sh
sudo apt remove goreecloud-care
```

The canonical source-control authority is `GoreeCloud/goreecloud-zorin-os`. GoreeCloud Care is maintained as the `apps/goreecloud-care/` component so its Zorin OS packaging, desktop integration, and target-device acceptance remain coupled to the GoreeCloud Zorin OS development surface while preserving a distinct application boundary.
