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

## If an action fails
GoreeCloud Care reports failure instead of treating it as success. Re-scan to see current state. No automatic retry performs a destructive action without another user invocation.
