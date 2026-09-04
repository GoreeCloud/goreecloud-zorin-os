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

Deep Teal / Mineral Teal are used for interaction emphasis, focus, selected controls, progress, and other ordinary accent roles. Amber remains an atmospheric identity token rather than a warning/success/error semantic color; the first theme source therefore does not force Amber into semantic widget states.

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

## Platform limitations

GTK 3 and GNOME Shell CSS do not reproduce the exact optical and backdrop-blur behavior of Glaze UI's web implementation. The mapping prioritizes hierarchy, contrast, geometry, color, and interaction-state consistency instead of simulating unsupported effects.

The initial implementation does not generate a GTK 4 stylesheet or the Zorin-specific `.libadwaita` opt-in marker. Native libadwaita theming remains a separate acceptance item because Zorin requires theme developers to opt in and extensively test compatibility.

## Accessibility intent

The theme deliberately avoids decorative animation and therefore does not introduce a new motion dependency. Interaction states retain visible boundaries, selected states use strong contrast, and focus states use a teal border/inner ring.

Actual contrast, keyboard focus visibility, legibility, and state clarity must still be accepted on the target Zorin OS 17.3 laptop before release qualification.
