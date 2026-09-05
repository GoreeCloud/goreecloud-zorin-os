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

## Interface, accessibility, and appearance
- GoreeCloud Care opens in a light appearance by default on the target Zorin OS laptop.
- The application-local light preference must not change the desktop-wide Zorin OS appearance setting.
- System high-contrast presentation takes precedence over the application color mapping; GoreeCloud Care must retain usable hierarchy and control semantics when its Development color provider is suppressed.
- Status feedback must communicate changed state with text plus a recognizable symbol and an appropriate semantic surface/border treatment; color alone is not sufficient.
- The maintenance status surface must expose assistive-technology semantics and update its accessible name when operation state changes.
- User-initiated cancellation is an attention/changed-state condition, not an error or destructive warning. It must be immediately noticeable without exaggerating it into a critical condition.
- Keyboard focus must remain visibly perceivable on supported interactive controls.
- Interactive controls must remain reachable by keyboard and expose useful accessible names/descriptions through the GTK/ATK mapping.
- Category counts must remain associated with understandable category text for visual and assistive-technology users.
- Long status, system, description, and heading text must wrap instead of clipping.
- The desktop window must support a compact composition below the Development breakpoint: category amounts move below category content and the bottom action row becomes a vertical action stack.
- The compact transition must occur early enough that supported enlarged-text layouts can reach the compact composition before intrinsic widget sizing prevents further narrowing.
- For the GTK `GDK_DPI_SCALE` large-text acceptance path, compact selection must account for the text scale when interpreting the allocated width rather than assuming the raw allocation alone represents the effective reading/layout width.
- The compact HeaderBar may omit the Development subtitle while retaining the application title and primary Scan action when necessary to reduce horizontal pressure.
- The compact composition must preserve action availability, focus order, reading order, and vertical scrolling rather than depending on horizontal scrolling.
- The Development window has a defined minimum supported size of 480 × 420 logical pixels; narrower or shorter unsupported sizes are not claimed.
- Current Stable Glaze UI V1.1 / 1.1.0 remains the governing design target; these Development mappings do not establish conformance until rendered, accessibility, resilience, and platform-native evidence is accepted.

## Data and privacy
The app reads local filesystem metadata, `/proc/meminfo`, and disk usage. It sends nothing over the network and contains no telemetry.

## Platform and toolkit
Python 3 + GTK 3/PyGObject, selected to match the verified Zorin OS 17.3 desktop application's GTK 3 environment. ATK semantics are exposed through GTK accessibility objects. PolicyKit is used for privileged maintenance.

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
Development / nonconformant. Core maintenance execution is representative-device verified through dev5, dev6 normal-text compact/minimum-window acceptance is verified, and dev8 now closes the combined `GDK_DPI_SCALE=2` + compact adaptive-layout blocker that remained after dev7. Exact dev8 head `45b5f11a49f363ebcaf753c892245a31109bc9bb` passed all three repository workflow families; the representative laptop passed 24 local tests plus XML/source validation, built and installed `0.1.0~dev8`, and fresh enlarged-text screenshots verify wide-layout readability plus narrow compact HeaderBar behavior, category-amount reflow, wrapping, complete vertical scrolling, and the vertical full-width bottom action stack. HighContrast, full keyboard-under-resilience, assistive-technology acceptance, supported appearance decisions, official branding, rollback, final current-Stable Glaze UI V1.1 consumer acceptance, and remaining Integral Platform System evidence remain open.
