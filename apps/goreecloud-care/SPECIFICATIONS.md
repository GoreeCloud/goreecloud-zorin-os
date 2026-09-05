# GoreeCloud Care — Development Specification

## Purpose
Provide a native GoreeCloud maintenance interface for the user's Zorin OS laptop without turning ordinary cleanup into a privileged or opaque operation.

## Users
Primary user: a person maintaining their own GoreeCloud/Zorin OS workstation.

## Safety model
- Preview first; cleanup never starts merely because a scan ran.
- User cache, thumbnail cache, and stale temporary files run as the logged-in user.
- Trash is a dedicated destructive action with an explicit, last-moment confirmation.
- Privilege is limited to two allowlisted helper actions: `apt-clean` and `reclaim-memory`.
- Privileged helper accepts no paths, commands, shell fragments, or arbitrary arguments.
- Symlinks are never followed during user-file scanning or deletion.
- Stale generic cache and temporary files use a 7-day threshold.
- Cleanup candidates are individual leaf nodes; broad recursive deletion of cache/temp directories is not used.
- Errors are surfaced and failed items are not counted as successful deletion.

## Interface and appearance
- GoreeCloud Care opens in a light appearance by default on the target Zorin OS laptop.
- The application-local light preference must not change the desktop-wide Zorin OS appearance setting.
- Status feedback must communicate changed state with text plus a recognizable symbol and an appropriate semantic surface/border treatment; color alone is not sufficient.
- User-initiated cancellation is an attention/changed-state condition, not an error or destructive warning. It must be immediately noticeable without exaggerating it into a critical condition.
- Keyboard focus must remain visibly perceivable on supported interactive controls.
- Current Stable Glaze UI remains the governing design target; these Development mappings do not establish conformance until rendered, accessibility, and platform-native evidence is accepted.

## Data and privacy
The app reads local filesystem metadata, `/proc/meminfo`, and disk usage. It sends nothing over the network and contains no telemetry.

## Platform and toolkit
Python 3 + GTK 3/PyGObject, selected to match the verified Zorin OS 17.3 desktop application's GTK 3 environment. PolicyKit is used for privileged maintenance.

## Exclusions in this Development slice
- No automatic scheduled deletion.
- No browser-history or credential deletion.
- No process killer or “one-click optimizer.”
- No swap manipulation.
- No package removal/autoremove.
- No registry-style tuning, CPU overclocking, or kernel parameter tuning.
- No claim that dropping file caches permanently boosts RAM or performance.
- No GoreeCloud cloud account requirement or remote management.

## Release status
Development / nonconformant. Target-device acceptance and Integral Platform System evidence remain open.
