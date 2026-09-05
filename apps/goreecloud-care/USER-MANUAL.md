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

## Keyboard and accessibility
Use **Tab** and **Shift+Tab** to move through interactive controls. GoreeCloud Care requires keyboard focus to be visibly perceivable as it moves; an interface where focus changes cannot be seen is not considered accepted keyboard behavior.

The ordinary Care presentation uses its established application focus styling. When a system HighContrast presentation suppresses Care's normal palette provider, dev10 installs a separate focus-only fallback beneath the ordinary Care CSS. The fallback uses the active GTK theme foreground color and does not define Care backgrounds, surfaces, or palette colors, so HighContrast remains authoritative while keyboard focus retains a visible outline.

Representative-device dev10 evidence now verifies visible HighContrast focus on **Scan**, the **Thumbnail cache** selector, and **Reclaim file cache…** while the system HighContrast presentation remains active. This confirms the dev10 focus fallback for those sampled controls. Complete forward/reverse traversal, the remaining bottom action controls, constrained-width HighContrast, and assistive-technology acceptance are still Development validation work.

GoreeCloud Care is designed to remain vertically scrollable when text is enlarged or the window becomes shorter. In compact windows, category amounts move below their category description and the bottom action buttons stack vertically so the primary workflow does not depend on horizontal scrolling. For the Development 200%-text acceptance path, the compact decision accounts for the GTK `GDK_DPI_SCALE` text scale rather than relying only on the raw allocated width. The compact HeaderBar may omit the Development subtitle when space is constrained; the GoreeCloud Care title and **Scan** action remain available.

The application opens in a light appearance by default. Effective HighContrast detection honors both the desktop GTK theme state and an explicit process-local `GTK_THEME` override.

## If an action fails
GoreeCloud Care reports failure instead of treating it as success. Re-scan to see current state. No automatic retry performs a destructive action without another user invocation.
