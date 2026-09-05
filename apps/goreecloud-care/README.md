# GoreeCloud Care

**Lifecycle:** Development  
**Version:** `0.1.0-dev1`  
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
- No telemetry, advertising, cloud upload, or network requirement.
- Symlink-safe user cleanup: links are unlinked, never traversed.

## Build and test

```sh
sh ./scripts/validate.sh
sh ./scripts/build-deb.sh
```

The generated Debian package is Development software. Installing it on a representative Zorin OS 17.3 device, visual/accessibility review, PolicyKit behavior, package upgrade/rollback, and broader GoreeCloud platform-system acceptance are still required before Release Candidate consideration.

## Install a locally built Development package

```sh
sudo apt install ./dist/goreecloud-care_0.1.0~dev1_all.deb
```

Uninstall with:

```sh
sudo apt remove goreecloud-care
```

The canonical source-control authority is `GoreeCloud/goreecloud-zorin-os`. GoreeCloud Care is maintained as the `apps/goreecloud-care/` component so its Zorin OS packaging, desktop integration, and target-device acceptance remain coupled to the GoreeCloud Zorin OS development surface while preserving a distinct application boundary.
