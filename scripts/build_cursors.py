#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import shutil
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "desktop-assets.json"
DEFAULT_OUTPUT = ROOT / "build" / "cursors"
IMAGE_TYPE = 0xFFFD0002


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the GoreeCloud Zorin Xcursor theme.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def argb(value: str) -> int:
    value = value.lstrip("#")
    r, g, b = (int(value[i:i + 2], 16) for i in (0, 2, 4))
    return (255 << 24) | (r << 16) | (g << 8) | b


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


def canvas(size: int) -> list[int]:
    return [0] * (size * size)


def put(pixels: list[int], size: int, x: int, y: int, color: int) -> None:
    if 0 <= x < size and 0 <= y < size:
        pixels[y * size + x] = color


def line(pixels: list[int], size: int, x0: int, y0: int, x1: int, y1: int, color: int, width: int = 1) -> None:
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        radius = max(0, width // 2)
        for yy in range(y0 - radius, y0 + radius + 1):
            for xx in range(x0 - radius, x0 + radius + 1):
                put(pixels, size, xx, yy, color)
        if x0 == x1 and y0 == y1:
            return
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def fill_polygon(pixels: list[int], size: int, points: list[tuple[float, float]], color: int) -> None:
    min_x = max(0, math.floor(min(x for x, _ in points)))
    max_x = min(size - 1, math.ceil(max(x for x, _ in points)))
    min_y = max(0, math.floor(min(y for _, y in points)))
    max_y = min(size - 1, math.ceil(max(y for _, y in points)))
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if point_in_polygon(x + 0.5, y + 0.5, points):
                put(pixels, size, x, y, color)


def fill_rect(pixels: list[int], size: int, x0: int, y0: int, x1: int, y1: int, color: int) -> None:
    for y in range(max(0, y0), min(size, y1)):
        for x in range(max(0, x0), min(size, x1)):
            put(pixels, size, x, y, color)


def ring(pixels: list[int], size: int, cx: float, cy: float, outer: float, inner: float, color: int) -> None:
    for y in range(size):
        for x in range(size):
            d = math.hypot((x + 0.5) - cx, (y + 0.5) - cy)
            if inner <= d <= outer:
                put(pixels, size, x, y, color)


def scale_points(points: list[tuple[float, float]], scale: float) -> list[tuple[float, float]]:
    return [(x * scale, y * scale) for x, y in points]


def arrow_image(size: int, colors: dict[str, int]) -> tuple[list[int], tuple[int, int]]:
    s = size / 32.0
    p = canvas(size)
    shadow = scale_points([(3,2),(3,27),(9,21),(15,31),(20,28),(14,18),(25,18)], s)
    outer = scale_points([(2,1),(2,26),(8,20),(14,30),(19,27),(13,17),(24,17)], s)
    inner = scale_points([(4,5),(4,22),(8,18),(14,27),(16,26),(10,16),(20,16)], s)
    fill_polygon(p, size, [(x+s, y+s) for x,y in shadow], colors["graphite"])
    fill_polygon(p, size, outer, colors["blue"])
    fill_polygon(p, size, inner, colors["frost"])
    return p, (max(0, round(2*s)), max(0, round(1*s)))


def hand_image(size: int, colors: dict[str, int]) -> tuple[list[int], tuple[int, int]]:
    s = size / 32.0
    p = canvas(size)
    outer = scale_points([(11,3),(15,3),(15,13),(17,10),(20,11),(20,13),(22,11),(25,13),(25,16),(27,15),(29,18),(27,27),(22,31),(13,29),(8,22),(9,18),(12,20)], s)
    inner = scale_points([(12.5,5),(14,5),(14,17),(17,13),(19,13),(19,17),(22,14),(24,15),(24,19),(27,17.5),(27.5,19),(26,26),(21,29),(14,27),(10,22),(10.5,20),(14,23),(14,5)], s)
    fill_polygon(p, size, outer, colors["blue"])
    fill_polygon(p, size, inner, colors["frost"])
    return p, (round(13*s), round(5*s))


def text_image(size: int, colors: dict[str, int]) -> tuple[list[int], tuple[int, int]]:
    s = size / 32.0
    p = canvas(size)
    cx = round(16*s)
    top, bottom = round(4*s), round(28*s)
    w = max(1, round(2*s))
    line(p,size,cx,top,cx,bottom,colors["blue"],w+2)
    line(p,size,round(10*s),top,round(22*s),top,colors["blue"],w+2)
    line(p,size,round(10*s),bottom,round(22*s),bottom,colors["blue"],w+2)
    line(p,size,cx,top+max(1,w),cx,bottom-max(1,w),colors["frost"],w)
    return p, (cx, round(16*s))


def cross_image(size: int, colors: dict[str, int]) -> tuple[list[int], tuple[int, int]]:
    s=size/32.0; p=canvas(size); c=round(16*s)
    line(p,size,c,round(3*s),c,round(29*s),colors["blue"],max(2,round(3*s)))
    line(p,size,round(3*s),c,round(29*s),c,colors["blue"],max(2,round(3*s)))
    line(p,size,c,round(6*s),c,round(26*s),colors["frost"],max(1,round(s)))
    line(p,size,round(6*s),c,round(26*s),c,colors["frost"],max(1,round(s)))
    return p,(c,c)


def move_image(size: int, colors: dict[str, int]) -> tuple[list[int], tuple[int, int]]:
    s=size/32.0; p=canvas(size); c=round(16*s); blue=colors["blue"]; frost=colors["frost"]
    line(p,size,c,round(5*s),c,round(27*s),blue,max(2,round(3*s)))
    line(p,size,round(5*s),c,round(27*s),c,blue,max(2,round(3*s)))
    for pts in [
        [(16,2),(12,8),(20,8)],[(16,30),(12,24),(20,24)],[(2,16),(8,12),(8,20)],[(30,16),(24,12),(24,20)]
    ]:
        fill_polygon(p,size,scale_points(pts,s),blue)
    put(p,size,c,c,frost)
    return p,(c,c)


def wait_image(size: int, colors: dict[str, int]) -> tuple[list[int], tuple[int, int]]:
    s=size/32.0; p=canvas(size); c=16*s
    ring(p,size,c,c,12*s,8*s,colors["blue"])
    line(p,size,round(c),round(c),round(c),round(5*s),colors["frost"],max(1,round(2*s)))
    return p,(round(c),round(c))


def forbidden_image(size: int, colors: dict[str, int]) -> tuple[list[int], tuple[int, int]]:
    s=size/32.0; p=canvas(size); c=16*s
    ring(p,size,c,c,12*s,9*s,colors["blocked"])
    line(p,size,round(8*s),round(8*s),round(24*s),round(24*s),colors["blocked"],max(2,round(4*s)))
    return p,(round(c),round(c))


def resize_image(size: int, colors: dict[str, int], kind: str) -> tuple[list[int], tuple[int, int]]:
    s=size/32.0; p=canvas(size); blue=colors["blue"]; c=round(16*s)
    if kind == "h":
        line(p,size,round(6*s),c,round(26*s),c,blue,max(2,round(3*s)))
        fill_polygon(p,size,scale_points([(3,16),(10,11),(10,21)],s),blue)
        fill_polygon(p,size,scale_points([(29,16),(22,11),(22,21)],s),blue)
    elif kind == "v":
        line(p,size,c,round(6*s),c,round(26*s),blue,max(2,round(3*s)))
        fill_polygon(p,size,scale_points([(16,3),(11,10),(21,10)],s),blue)
        fill_polygon(p,size,scale_points([(16,29),(11,22),(21,22)],s),blue)
    elif kind == "d1":
        line(p,size,round(7*s),round(7*s),round(25*s),round(25*s),blue,max(2,round(3*s)))
        fill_polygon(p,size,scale_points([(4,4),(13,6),(6,13)],s),blue)
        fill_polygon(p,size,scale_points([(28,28),(19,26),(26,19)],s),blue)
    else:
        line(p,size,round(25*s),round(7*s),round(7*s),round(25*s),blue,max(2,round(3*s)))
        fill_polygon(p,size,scale_points([(28,4),(19,6),(26,13)],s),blue)
        fill_polygon(p,size,scale_points([(4,28),(13,26),(6,19)],s),blue)
    return p,(c,c)


def progress_image(size: int, colors: dict[str, int]) -> tuple[list[int], tuple[int, int]]:
    p, hot = arrow_image(size, colors)
    s=size/32.0
    ring(p,size,23*s,23*s,6*s,4*s,colors["blue"])
    return p,hot


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
            0,
        ) + b"".join(struct.pack("<I", int(pixel)) for pixel in pixels)
        chunks.append(chunk)
        position += len(chunk)
    path.write_bytes(header + b"".join(tocs) + b"".join(chunks))


def build_cursor(path: Path, sizes: list[int], renderer, colors: dict[str, int]) -> None:
    frames = []
    for size in sizes:
        pixels, hot = renderer(size, colors)
        frames.append({"size": size, "pixels": pixels, "hot": hot})
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
        "deep_blue": argb(palette["deep_blue"]),
        "graphite": argb(palette["graphite"]),
        "blocked": argb(palette["blocked"]),
    }
    sizes = [int(size) for size in cfg["sizes"]]
    renderers = {
        "arrow": arrow_image,
        "hand": hand_image,
        "text": text_image,
        "cross": cross_image,
        "move": move_image,
        "wait": wait_image,
        "progress": progress_image,
        "blocked": forbidden_image,
        "hresize": lambda size, c: resize_image(size, c, "h"),
        "vresize": lambda size, c: resize_image(size, c, "v"),
        "d1resize": lambda size, c: resize_image(size, c, "d1"),
        "d2resize": lambda size, c: resize_image(size, c, "d2"),
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
        "hresize": ["sb_h_double_arrow", "size_hor", "ew-resize", "e-resize", "w-resize", "left_side", "right_side"],
        "vresize": ["sb_v_double_arrow", "size_ver", "ns-resize", "n-resize", "s-resize", "top_side", "bottom_side"],
        "d1resize": ["size_bdiag", "nwse-resize", "nw-resize", "se-resize", "top_left_corner", "bottom_right_corner"],
        "d2resize": ["size_fdiag", "nesw-resize", "ne-resize", "sw-resize", "top_right_corner", "bottom_left_corner"],
    }

    for family, renderer in renderers.items():
        canonical = cursors / f".goreecloud-{family}"
        build_cursor(canonical, sizes, renderer, colors)
        payload = canonical.read_bytes()
        for name in aliases[family]:
            (cursors / name).write_bytes(payload)
        canonical.unlink()

    # DnD copy uses the pointer hand rather than falling back to an unrelated theme.
    (cursors / "dnd-copy").write_bytes((cursors / "hand2").read_bytes())
    (cursors / "copy").write_bytes((cursors / "hand2").read_bytes())

    print(f"Built GoreeCloud cursor theme: {theme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
