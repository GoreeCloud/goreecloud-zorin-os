#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import shutil
import struct
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "desktop-assets.json"
DEFAULT_OUTPUT = ROOT / "build" / "cursors"
IMAGE_TYPE = 0xFFFD0002
# Keep the nominal Xcursor frame ladder unchanged while using a slightly larger
# optical design grid. Target-device acceptance found revision 2 accurate but
# visibly larger than the surrounding Zorin cursor language; 36 vs 32 reduces
# the rendered footprint by about 11% without changing hotspot semantics.
BASE_GRID = 36.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the GoreeCloud Zorin Xcursor theme.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def argb(value: str, alpha: int = 255) -> int:
    value = value.lstrip("#")
    r, g, b = (int(value[i:i + 2], 16) for i in (0, 2, 4))
    r = (r * alpha + 127) // 255
    g = (g * alpha + 127) // 255
    b = (b * alpha + 127) // 255
    return ((alpha & 0xFF) << 24) | (r << 16) | (g << 8) | b


def with_alpha(color: int, alpha: int) -> int:
    _base_alpha, r, g, b = components(color)
    r = (r * alpha + 127) // 255
    g = (g * alpha + 127) // 255
    b = (b * alpha + 127) // 255
    return ((alpha & 0xFF) << 24) | (r << 16) | (g << 8) | b


def components(color: int) -> tuple[int, int, int, int]:
    return (
        (color >> 24) & 0xFF,
        (color >> 16) & 0xFF,
        (color >> 8) & 0xFF,
        color & 0xFF,
    )


def canvas(size: int) -> list[int]:
    return [0] * (size * size)


def put(pixels: list[int], size: int, x: int, y: int, color: int) -> None:
    if 0 <= x < size and 0 <= y < size:
        pixels[y * size + x] = color


def point_in_polygon(x: float, y: float, points: list[tuple[float, float]]) -> bool:
    inside = False
    j = len(points) - 1
    for i, (xi, yi) in enumerate(points):
        xj, yj = points[j]
        hit = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-9) + xi
        )
        if hit:
            inside = not inside
        j = i
    return inside


def fill_polygon(
    pixels: list[int],
    size: int,
    points: list[tuple[float, float]],
    color: int,
) -> None:
    min_x = max(0, math.floor(min(x for x, _ in points)))
    max_x = min(size - 1, math.ceil(max(x for x, _ in points)))
    min_y = max(0, math.floor(min(y for _, y in points)))
    max_y = min(size - 1, math.ceil(max(y for _, y in points)))
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if point_in_polygon(x + 0.5, y + 0.5, points):
                put(pixels, size, x, y, color)


def fill_disk(
    pixels: list[int],
    size: int,
    cx: float,
    cy: float,
    radius: float,
    color: int,
) -> None:
    min_x = max(0, math.floor(cx - radius))
    max_x = min(size - 1, math.ceil(cx + radius))
    min_y = max(0, math.floor(cy - radius))
    max_y = min(size - 1, math.ceil(cy + radius))
    r2 = radius * radius
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            dx = (x + 0.5) - cx
            dy = (y + 0.5) - cy
            if dx * dx + dy * dy <= r2:
                put(pixels, size, x, y, color)


def stroke_segment(
    pixels: list[int],
    size: int,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    color: int,
    width: float,
) -> None:
    radius = width / 2.0
    min_x = max(0, math.floor(min(x0, x1) - radius))
    max_x = min(size - 1, math.ceil(max(x0, x1) + radius))
    min_y = max(0, math.floor(min(y0, y1) - radius))
    max_y = min(size - 1, math.ceil(max(y0, y1) + radius))
    vx = x1 - x0
    vy = y1 - y0
    length2 = vx * vx + vy * vy
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            px = x + 0.5
            py = y + 0.5
            if length2 == 0:
                t = 0.0
            else:
                t = max(0.0, min(1.0, ((px - x0) * vx + (py - y0) * vy) / length2))
            qx = x0 + t * vx
            qy = y0 + t * vy
            if math.hypot(px - qx, py - qy) <= radius:
                put(pixels, size, x, y, color)


def ring(
    pixels: list[int],
    size: int,
    cx: float,
    cy: float,
    outer: float,
    inner: float,
    color: int,
) -> None:
    outer2 = outer * outer
    inner2 = inner * inner
    min_x = max(0, math.floor(cx - outer))
    max_x = min(size - 1, math.ceil(cx + outer))
    min_y = max(0, math.floor(cy - outer))
    max_y = min(size - 1, math.ceil(cy + outer))
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            dx = (x + 0.5) - cx
            dy = (y + 0.5) - cy
            d2 = dx * dx + dy * dy
            if inner2 <= d2 <= outer2:
                put(pixels, size, x, y, color)


def scale_points(
    points: list[tuple[float, float]],
    scale: float,
) -> list[tuple[float, float]]:
    return [(x * scale, y * scale) for x, y in points]


def downsample(pixels: list[int], source_size: int, factor: int) -> list[int]:
    if factor == 1:
        return pixels
    target_size = source_size // factor
    output = canvas(target_size)
    sample_count = factor * factor
    for ty in range(target_size):
        for tx in range(target_size):
            alpha_sum = 0
            red_sum = 0
            green_sum = 0
            blue_sum = 0
            for sy in range(ty * factor, (ty + 1) * factor):
                row = sy * source_size
                for sx in range(tx * factor, (tx + 1) * factor):
                    a, r, g, b = components(pixels[row + sx])
                    alpha_sum += a
                    red_sum += r
                    green_sum += g
                    blue_sum += b
            alpha = round(alpha_sum / sample_count)
            if alpha_sum == 0:
                output[ty * target_size + tx] = 0
                continue
            red = round(red_sum / sample_count)
            green = round(green_sum / sample_count)
            blue = round(blue_sum / sample_count)
            output[ty * target_size + tx] = (
                ((alpha & 0xFF) << 24)
                | ((red & 0xFF) << 16)
                | ((green & 0xFF) << 8)
                | (blue & 0xFF)
            )
    return output


Renderer = Callable[[int, dict[str, int], int], tuple[list[int], tuple[int, int]]]


def render_supersampled(
    size: int,
    renderer: Renderer,
    colors: dict[str, int],
    phase: int,
    factor: int,
) -> tuple[list[int], tuple[int, int]]:
    source_size = size * factor
    pixels, hot = renderer(source_size, colors, phase)
    return downsample(pixels, source_size, factor), (
        round(hot[0] / factor),
        round(hot[1] / factor),
    )


def arrow_image(
    size: int,
    colors: dict[str, int],
    _phase: int = 0,
) -> tuple[list[int], tuple[int, int]]:
    s = size / BASE_GRID
    p = canvas(size)
    outer = scale_points(
        [(3.0, 2.0), (3.0, 26.4), (9.2, 20.5), (15.3, 30.0),
         (19.8, 27.2), (13.8, 17.8), (24.8, 17.8)],
        s,
    )
    inner = scale_points(
        [(5.4, 6.2), (5.4, 21.0), (9.6, 17.1), (15.6, 26.8),
         (16.6, 26.1), (10.4, 16.1), (20.6, 16.1)],
        s,
    )
    fill_polygon(p, size, outer, colors["graphite"])
    fill_polygon(p, size, inner, colors["frost"])
    return p, (round(3.2 * s), round(2.2 * s))


def hand_image(
    size: int,
    colors: dict[str, int],
    _phase: int = 0,
) -> tuple[list[int], tuple[int, int]]:
    s = size / BASE_GRID
    p = canvas(size)
    outer = scale_points(
        [(11.1, 3.0), (15.2, 3.0), (15.2, 13.2), (17.2, 10.5),
         (20.2, 10.7), (20.7, 13.0), (22.3, 11.6), (25.0, 12.6),
         (25.4, 15.3), (27.2, 15.1), (29.3, 17.8), (27.7, 26.9),
         (22.3, 30.2), (13.2, 28.7), (8.2, 22.0), (8.8, 18.0),
         (11.7, 19.8)],
        s,
    )
    inner = scale_points(
        [(12.8, 5.0), (14.0, 5.0), (14.0, 17.2), (17.3, 13.0),
         (19.0, 13.1), (19.1, 17.1), (22.1, 14.0), (23.8, 14.7),
         (23.9, 18.5), (26.7, 17.3), (27.3, 18.6), (25.9, 25.5),
         (21.5, 28.1), (14.3, 26.8), (10.3, 21.7), (10.6, 20.2),
         (13.9, 22.8), (13.9, 5.0)],
        s,
    )
    fill_polygon(p, size, outer, colors["graphite"])
    fill_polygon(p, size, inner, colors["frost"])
    return p, (round(13.6 * s), round(5.0 * s))


def text_image(
    size: int,
    colors: dict[str, int],
    _phase: int = 0,
) -> tuple[list[int], tuple[int, int]]:
    s = size / BASE_GRID
    p = canvas(size)
    cx = 16.0 * s
    top = 4.0 * s
    bottom = 28.0 * s
    left = 10.0 * s
    right = 22.0 * s
    outer = max(2.0 * s, 2.0)
    inner = max(0.9 * s, 1.0)
    for x0, y0, x1, y1 in (
        (cx, top, cx, bottom),
        (left, top, right, top),
        (left, bottom, right, bottom),
    ):
        stroke_segment(p, size, x0, y0, x1, y1, colors["graphite"], outer)
        stroke_segment(p, size, x0, y0, x1, y1, colors["frost"], inner)
    return p, (round(cx), round(16.0 * s))


def cross_image(
    size: int,
    colors: dict[str, int],
    _phase: int = 0,
) -> tuple[list[int], tuple[int, int]]:
    s = size / BASE_GRID
    p = canvas(size)
    c = 16.0 * s
    outer = max(2.2 * s, 2.0)
    inner = max(0.9 * s, 1.0)
    for x0, y0, x1, y1 in (
        (c, 4.5 * s, c, 27.5 * s),
        (4.5 * s, c, 27.5 * s, c),
    ):
        stroke_segment(p, size, x0, y0, x1, y1, colors["graphite"], outer)
        stroke_segment(p, size, x0, y0, x1, y1, colors["frost"], inner)
    return p, (round(c), round(c))


def move_image(
    size: int,
    colors: dict[str, int],
    _phase: int = 0,
) -> tuple[list[int], tuple[int, int]]:
    s = size / BASE_GRID
    p = canvas(size)
    c = 16.0 * s
    outer = max(2.4 * s, 2.0)
    inner = max(1.0 * s, 1.0)
    for x0, y0, x1, y1 in (
        (c, 6.0 * s, c, 26.0 * s),
        (6.0 * s, c, 26.0 * s, c),
    ):
        stroke_segment(p, size, x0, y0, x1, y1, colors["graphite"], outer)
        stroke_segment(p, size, x0, y0, x1, y1, colors["frost"], inner)
    outer_heads = [
        [(16, 2.5), (11.7, 8.8), (20.3, 8.8)],
        [(16, 29.5), (11.7, 23.2), (20.3, 23.2)],
        [(2.5, 16), (8.8, 11.7), (8.8, 20.3)],
        [(29.5, 16), (23.2, 11.7), (23.2, 20.3)],
    ]
    inner_heads = [
        [(16, 4.5), (13.7, 7.8), (18.3, 7.8)],
        [(16, 27.5), (13.7, 24.2), (18.3, 24.2)],
        [(4.5, 16), (7.8, 13.7), (7.8, 18.3)],
        [(27.5, 16), (24.2, 13.7), (24.2, 18.3)],
    ]
    for pts in outer_heads:
        fill_polygon(p, size, scale_points(pts, s), colors["graphite"])
    for pts in inner_heads:
        fill_polygon(p, size, scale_points(pts, s), colors["frost"])
    return p, (round(c), round(c))


def spinner(
    pixels: list[int],
    size: int,
    colors: dict[str, int],
    cx: float,
    cy: float,
    radius: float,
    dot_radius: float,
    phase: int,
) -> None:
    alpha_steps = (255, 210, 165, 125, 95, 70, 48, 32)
    for index in range(8):
        angle = (index / 8.0) * math.tau - math.pi / 2.0
        x = cx + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius
        alpha = alpha_steps[(index - phase) % 8]
        fill_disk(
            pixels,
            size,
            x,
            y,
            dot_radius,
            with_alpha(colors["blue"], alpha),
        )


def wait_image(
    size: int,
    colors: dict[str, int],
    phase: int = 0,
) -> tuple[list[int], tuple[int, int]]:
    s = size / BASE_GRID
    p = canvas(size)
    c = 16.0 * s
    spinner(p, size, colors, c, c, 9.0 * s, max(1.5 * s, 1.3), phase)
    return p, (round(c), round(c))


def progress_image(
    size: int,
    colors: dict[str, int],
    phase: int = 0,
) -> tuple[list[int], tuple[int, int]]:
    p, hot = arrow_image(size, colors)
    s = size / BASE_GRID
    spinner(
        p,
        size,
        colors,
        23.2 * s,
        23.0 * s,
        4.0 * s,
        max(1.0 * s, 1.0),
        phase,
    )
    return p, hot


def forbidden_image(
    size: int,
    colors: dict[str, int],
    _phase: int = 0,
) -> tuple[list[int], tuple[int, int]]:
    s = size / BASE_GRID
    p = canvas(size)
    c = 16.0 * s
    ring(p, size, c, c, 12.3 * s, 8.4 * s, colors["graphite"])
    ring(p, size, c, c, 10.9 * s, 8.9 * s, colors["blocked"])
    stroke_segment(
        p, size,
        8.1 * s, 8.1 * s,
        23.9 * s, 23.9 * s,
        colors["graphite"],
        max(4.4 * s, 3.0),
    )
    stroke_segment(
        p, size,
        8.5 * s, 8.5 * s,
        23.5 * s, 23.5 * s,
        colors["blocked"],
        max(2.2 * s, 1.5),
    )
    return p, (round(c), round(c))


def resize_image(
    size: int,
    colors: dict[str, int],
    kind: str,
    _phase: int = 0,
) -> tuple[list[int], tuple[int, int]]:
    s = size / BASE_GRID
    p = canvas(size)
    c = 16.0 * s
    graphite = colors["graphite"]
    frost = colors["frost"]
    outer_w = max(2.4 * s, 2.0)
    inner_w = max(1.0 * s, 1.0)

    if kind == "h":
        start, end = (6.0, 16.0), (26.0, 16.0)
        outer_heads = [[(2.7, 16), (9.2, 11.6), (9.2, 20.4)],
                       [(29.3, 16), (22.8, 11.6), (22.8, 20.4)]]
        inner_heads = [[(4.7, 16), (8.2, 13.6), (8.2, 18.4)],
                       [(27.3, 16), (23.8, 13.6), (23.8, 18.4)]]
    elif kind == "v":
        start, end = (16.0, 6.0), (16.0, 26.0)
        outer_heads = [[(16, 2.7), (11.6, 9.2), (20.4, 9.2)],
                       [(16, 29.3), (11.6, 22.8), (20.4, 22.8)]]
        inner_heads = [[(16, 4.7), (13.6, 8.2), (18.4, 8.2)],
                       [(16, 27.3), (13.6, 23.8), (18.4, 23.8)]]
    elif kind == "d1":
        start, end = (7.0, 7.0), (25.0, 25.0)
        outer_heads = [[(3.4, 3.4), (12.5, 5.6), (5.6, 12.5)],
                       [(28.6, 28.6), (19.5, 26.4), (26.4, 19.5)]]
        inner_heads = [[(5.2, 5.2), (10.2, 6.4), (6.4, 10.2)],
                       [(26.8, 26.8), (21.8, 25.6), (25.6, 21.8)]]
    else:
        start, end = (25.0, 7.0), (7.0, 25.0)
        outer_heads = [[(28.6, 3.4), (19.5, 5.6), (26.4, 12.5)],
                       [(3.4, 28.6), (12.5, 26.4), (5.6, 19.5)]]
        inner_heads = [[(26.8, 5.2), (21.8, 6.4), (25.6, 10.2)],
                       [(5.2, 26.8), (10.2, 25.6), (6.4, 21.8)]]

    stroke_segment(
        p, size,
        start[0] * s, start[1] * s,
        end[0] * s, end[1] * s,
        graphite, outer_w,
    )
    stroke_segment(
        p, size,
        start[0] * s, start[1] * s,
        end[0] * s, end[1] * s,
        frost, inner_w,
    )
    for pts in outer_heads:
        fill_polygon(p, size, scale_points(pts, s), graphite)
    for pts in inner_heads:
        fill_polygon(p, size, scale_points(pts, s), frost)
    return p, (round(c), round(c))


def copy_image(
    size: int,
    colors: dict[str, int],
    _phase: int = 0,
) -> tuple[list[int], tuple[int, int]]:
    p, hot = arrow_image(size, colors)
    s = size / BASE_GRID
    cx = 23.5 * s
    cy = 23.5 * s
    fill_disk(p, size, cx, cy, 5.0 * s, colors["frost"])
    ring(p, size, cx, cy, 5.0 * s, 3.8 * s, colors["graphite"])
    stroke_segment(
        p, size,
        cx - 2.4 * s, cy,
        cx + 2.4 * s, cy,
        colors["blue"],
        max(1.4 * s, 1.0),
    )
    stroke_segment(
        p, size,
        cx, cy - 2.4 * s,
        cx, cy + 2.4 * s,
        colors["blue"],
        max(1.4 * s, 1.0),
    )
    return p, hot


def write_xcursor(path: Path, frames: list[dict[str, object]]) -> None:
    header = struct.pack("<4sIII", b"Xcur", 16, 0x00010000, len(frames))
    position = 16 + 12 * len(frames)
    tocs: list[bytes] = []
    chunks: list[bytes] = []
    for frame in frames:
        nominal = int(frame["size"])
        pixels = frame["pixels"]
        width = height = nominal
        xhot, yhot = frame["hot"]
        delay = int(frame.get("delay", 0))
        tocs.append(struct.pack("<III", IMAGE_TYPE, nominal, position))
        chunk = struct.pack(
            "<IIIIIIIII",
            36,
            IMAGE_TYPE,
            nominal,
            1,
            width,
            height,
            int(xhot),
            int(yhot),
            delay,
        ) + b"".join(struct.pack("<I", int(pixel)) for pixel in pixels)
        chunks.append(chunk)
        position += len(chunk)
    path.write_bytes(header + b"".join(tocs) + b"".join(chunks))


def build_cursor(
    path: Path,
    sizes: list[int],
    renderer: Renderer,
    colors: dict[str, int],
    supersample: int,
    phases: int = 1,
    delay: int = 0,
) -> None:
    frames: list[dict[str, object]] = []
    for size in sizes:
        for phase in range(phases):
            pixels, hot = render_supersampled(
                size,
                renderer,
                colors,
                phase,
                supersample,
            )
            frames.append(
                {
                    "size": size,
                    "pixels": pixels,
                    "hot": hot,
                    "delay": delay if phases > 1 else 0,
                }
            )
    write_xcursor(path, frames)


def main() -> int:
    args = parse_args()
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))["cursor_theme"]
    theme = args.output.expanduser().resolve() / cfg["id"]
    cursors = theme / "cursors"
    if theme.exists():
        shutil.rmtree(theme)
    cursors.mkdir(parents=True, exist_ok=True)

    (theme / "index.theme").write_text(
        "[Icon Theme]\n"
        f"Name={cfg['name']}\n"
        f"Comment={cfg['comment']}\n"
        f"Inherits={','.join(cfg['inherits'])}\n",
        encoding="utf-8",
    )

    palette = cfg["palette"]
    colors = {
        "frost": argb(palette["frost"]),
        "blue": argb(palette["primary_blue"]),
        "graphite": argb(palette["graphite"]),
        "blocked": argb(palette["blocked"]),
    }
    sizes = [int(size) for size in cfg["sizes"]]
    supersample = int(cfg.get("supersample", 4))
    animation_frames = int(cfg.get("animation_frames", 8))
    animation_delay = int(cfg.get("animation_delay_ms", 55))

    renderers: dict[str, Renderer] = {
        "arrow": arrow_image,
        "hand": hand_image,
        "text": text_image,
        "cross": cross_image,
        "move": move_image,
        "wait": wait_image,
        "progress": progress_image,
        "blocked": forbidden_image,
        "hresize": lambda size, c, phase=0: resize_image(size, c, "h", phase),
        "vresize": lambda size, c, phase=0: resize_image(size, c, "v", phase),
        "d1resize": lambda size, c, phase=0: resize_image(size, c, "d1", phase),
        "d2resize": lambda size, c, phase=0: resize_image(size, c, "d2", phase),
        "copy": copy_image,
    }
    aliases = {
        "arrow": ["left_ptr", "default", "arrow", "top_left_arrow"],
        "hand": ["hand2", "hand1", "pointer", "link", "dnd-link"],
        "text": ["xterm", "text", "ibeam"],
        "cross": ["crosshair", "cross"],
        "move": ["fleur", "move", "all-scroll", "size_all", "dnd-move"],
        "wait": ["watch", "wait"],
        "progress": ["left_ptr_watch", "progress"],
        "blocked": ["not-allowed", "forbidden", "no-drop"],
        "hresize": [
            "sb_h_double_arrow", "size_hor", "ew-resize", "e-resize",
            "w-resize", "left_side", "right_side",
        ],
        "vresize": [
            "sb_v_double_arrow", "size_ver", "ns-resize", "n-resize",
            "s-resize", "top_side", "bottom_side",
        ],
        "d1resize": [
            "size_bdiag", "nwse-resize", "nw-resize", "se-resize",
            "top_left_corner", "bottom_right_corner",
        ],
        "d2resize": [
            "size_fdiag", "nesw-resize", "ne-resize", "sw-resize",
            "top_right_corner", "bottom_left_corner",
        ],
        "copy": ["dnd-copy", "copy"],
    }

    for family, renderer in renderers.items():
        canonical = cursors / f".goreecloud-{family}"
        animated = family in {"wait", "progress"}
        build_cursor(
            canonical,
            sizes,
            renderer,
            colors,
            supersample,
            phases=animation_frames if animated else 1,
            delay=animation_delay if animated else 0,
        )
        payload = canonical.read_bytes()
        for name in aliases[family]:
            (cursors / name).write_bytes(payload)
        canonical.unlink()

    print(f"Built GoreeCloud cursor theme: {theme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
