# GoreeCloud Care User Manual

## Scan
Open GoreeCloud Care and choose **Scan**. Scanning is read-only and shows the estimated size and item count for Application cache, Thumbnail cache, Temporary files, Trash, and the APT package cache.

## Clean selected
Check any of Application cache, Thumbnail cache, and Temporary files, then choose **Clean selected**. A confirmation summarizes the estimated amount before deletion. Application cache and temporary files are limited to files older than seven days; temporary files must be owned by your current user.

## Empty Trash
Choose **Empty Trash…**. GoreeCloud Care shows a separate warning because Trash deletion is permanent. Nothing is deleted if you cancel.

## Clean APT cache
Choose **Clean APT cache…** and confirm. PolicyKit asks for administrator authentication. The privileged helper can run only the fixed `apt-get clean` action; it does not accept arbitrary commands or paths.

## Memory Refresh
Choose **Reclaim file cache…** only when you deliberately want Linux to release page/dentry/inode caches. Linux normally manages these caches automatically. Available memory may rise temporarily, but this is not a lasting performance boost and later file/app loads may be slower while caches rebuild.

## Read-only maintenance reports — dev13

From a terminal, GoreeCloud Care can generate local diagnostic summaries without opening the maintenance window or performing cleanup:

```sh
goreecloud-care --report
```

This prints a human-readable report containing disk headroom, memory/file-cache information, visible maintenance totals, per-category byte/item counts, and scan-error counts.

For machine-readable output:

```sh
goreecloud-care --report-json
```

The JSON report is intended for local scripts and future governed GoreeCloud integrations. It is schema-versioned and includes an explicit privacy/mode section.

To check the installed Development version:

```sh
goreecloud-care --version
```

Report modes are read-only. They do not delete files, request administrator authentication, invoke PolicyKit, run the privileged helper, or access the network. Candidate file paths, filenames, and raw scan-error strings are omitted by default.

Disk-headroom labels such as `comfortable`, `watch`, `low`, and `critical` are informational capacity signals. They are not filesystem-health certification and do not trigger cleanup automatically.

## Keyboard and accessibility
Use **Tab** and **Shift+Tab** to move through interactive controls. GoreeCloud Care requires keyboard focus to be visibly perceivable as it moves; an interface where focus changes cannot be seen is not considered accepted keyboard behavior.

The ordinary Care presentation uses its established application focus styling. When a system HighContrast presentation suppresses Care's normal palette provider, a separate focus-only fallback remains underneath the ordinary Care CSS. The fallback uses the active GTK theme foreground color and does not define Care backgrounds, surfaces, or palette colors, so HighContrast remains authoritative while keyboard focus retains a visible outline.

Representative-device dev10 evidence verifies HighContrast palette authority, visible focus, constrained-width rendering, and the complete requested forward/reverse keyboard path. Representative-device dev12 evidence verifies that AT-SPI discovers the application as **GoreeCloud Care** and exposes the current static status/control roles, names, descriptions, checked state, and focused state. Dynamic status-event delivery and Orca announcement quality remain Development validation work.

GoreeCloud Care remains vertically scrollable when text is enlarged or the window becomes shorter. In compact windows, category amounts move below their category description and the bottom action buttons stack vertically so the primary workflow does not depend on horizontal scrolling. For the Development 200%-text acceptance path, the compact decision accounts for GTK `GDK_DPI_SCALE`. The compact HeaderBar may omit the Development subtitle when space is constrained; the GoreeCloud Care title and **Scan** action remain available.

The application opens in a light appearance by default. Effective HighContrast detection honors both the desktop GTK theme state and an explicit process-local `GTK_THEME` override.

## If an action fails
GoreeCloud Care reports failure instead of treating it as success. Re-scan to see current state. No automatic retry performs a destructive action without another user invocation.
