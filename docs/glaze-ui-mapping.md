# Glaze UI V1.1 Mapping for Zorin OS

## Status

This document records the intended mapping from Glaze UI V1.1 / 1.1.0 to the GoreeCloud Zorin OS theme source.

This is a **platform adaptation**, not evidence by itself that the desktop theme has passed Glaze UI conformance or target-environment acceptance.

## Mapping principles

Glaze UI's surface model is adapted to desktop-theme primitives as follows:

| Glaze UI concept | Zorin / GTK / GNOME Shell mapping |
| --- | --- |
| Canvas | desktop application background and lowest-level window background |
| Surface | header bars, sidebars, popovers, menus, shell panel surfaces |
| Soft Glaze | hover and lightweight selection surfaces |
| Glaze | menus, search, quick settings, dialogs, overview controls |
| Deep Glaze | tooltips, OSD surfaces, deep-dark elevated containers |
| Live Glaze | intentionally not emulated; desktop CSS cannot safely reproduce the web design system's full live/backdrop optical model |

The desktop implementation keeps reading surfaces substantially solid. Translucency is limited primarily to GNOME Shell surfaces where the shell compositor already supports it.

## Color mapping

The Stable Glaze UI atmospheric anchors are represented directly where appropriate:

- Canvas Black `#081016`
- Deep Graphite `#101A20`
- Slate Graphite `#18252B`
- Deep Teal `#0F6B6F`
- Mineral Teal `#1C8A8D`
- Soft Aqua `#8FD6D2`
- Soft Amber `#D9A35F`
- Champagne Gold `#E7C78A`

Light-mode neutrals are desktop-specific derivatives chosen to preserve readability with the same teal family.

Deep Teal / Mineral Teal are used for interaction emphasis, focus, selected controls, progress, and other ordinary accent roles. Amber remains an atmospheric identity token rather than a warning/success/error semantic color; the theme source therefore does not force Amber into semantic widget states.

## Geometry mapping

Glaze UI geometry is carried into the desktop theme approximately as:

- 8 px: compact menu items and tooltips;
- 16 px: controls, fields, toggles, search, notifications;
- 24 px: major dialogs, dash surfaces, quick settings;
- 999 px: switches, scroll thumbs, progress tracks, and other pill/capsule geometry.

These values are adapted where GTK or GNOME Shell widget constraints require a smaller radius.

## Modes

The theme family exposes three Glaze-aligned modes:

- `GoreeCloud-Zorin-Light`
- `GoreeCloud-Zorin-Dark`
- `GoreeCloud-Zorin-DeepDark`

Deep Dark is intentionally distinct from Dark: it uses Canvas Black as the base with Deep Graphite and Slate Graphite layered above it.

## GTK 4 / libadwaita mapping

Target-device Dark-mode screenshots showed that selecting the GTK 3 + Shell theme did not bring the Files application onto the expected GoreeCloud canvas/surface hierarchy. The Development source therefore now includes a GTK 4 stylesheet and Zorin's explicit `.libadwaita` opt-in marker so native libadwaita applications can be tested instead of being treated as out of scope.

The GTK 4 mapping intentionally focuses on stable libadwaita named color roles and common widget states rather than copying another theme's complete stylesheet. It maps:

- `window_bg_color` and `view_bg_color` to the GoreeCloud canvas;
- headerbar, sidebar, dialog, popover, and card roles to GoreeCloud surface/elevated layers;
- accent/destructive roles to the existing GoreeCloud semantic tokens;
- selected navigation rows, checked controls, focus, progress, scrollbars, and common geometry to the same interaction hierarchy used by GTK 3.

Zorin OS 17+ requires an empty `gtk-4.0/.libadwaita` marker for this opt-in path. The marker is generated only as part of this Development acceptance candidate and does not constitute compatibility evidence by itself.

## Platform limitations

GTK, libadwaita, and GNOME Shell CSS do not reproduce the exact optical and backdrop-blur behavior of Glaze UI's web implementation. The mapping prioritizes hierarchy, contrast, geometry, color, and interaction-state consistency instead of simulating unsupported effects.

GTK 2 remains a discovery compatibility shim rather than a full visual implementation. Browser chrome, Flatpak/Snap packaging, and application-provided CSS can also retain their own visual styling.

## Accessibility intent

The theme deliberately avoids decorative animation and therefore does not introduce a new motion dependency. Interaction states retain visible boundaries, selected states use strong contrast, and focus states use a teal border/inner ring where supported.

Actual contrast, keyboard focus visibility, legibility, state clarity, GTK 4/libadwaita compatibility, and Shell behavior must still be accepted on the target Zorin OS 17.3 laptop before release qualification.
