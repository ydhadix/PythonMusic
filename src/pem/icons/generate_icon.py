#!/usr/bin/env python3
"""Generate rounded, drop-shadowed app icons from a source image.

Produces a squircle-masked icon with a soft drop shadow and a subtle top
highlight for depth, then exports cross-platform formats:
  - icon_rounded.png  (1024, with transparency + shadow; X11 + macOS Dock)
  - icon_128.png      (128, for the in-app About dialog)
  - icon.ico          (Windows, multi-size)
  - icon.icns         (macOS)

Re-run any time the source art changes:  python3 generate_icon.py
"""
from __future__ import annotations
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageChops

HERE = Path(__file__).parent
SRC = HERE / "icon.png"

# --- tunables -------------------------------------------------------------
SIZE = 1024            # working resolution
MARGIN = 90            # transparent padding around the tile (room for shadow)
CORNER = 0.2237        # corner-radius as fraction of tile size (~Apple squircle)
SHADOW_BLUR = 28       # softness of the drop shadow
SHADOW_OFFSET = 22     # how far the shadow drops (px)
SHADOW_OPACITY = 110   # 0-255
HIGHLIGHT = 28         # strength of the top sheen (0 = off)
# -------------------------------------------------------------------------


def rounded_mask(size: int, radius: int) -> Image.Image:
    """An anti-aliased rounded-rectangle alpha mask (4x supersampled)."""
    s = size * 4
    m = Image.new("L", (s, s), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, s - 1, s - 1), radius * 4, fill=255)
    return m.resize((size, size), Image.LANCZOS)


def square(im: Image.Image, size: int) -> Image.Image:
    """Center-crop to square, then resize to `size`."""
    im = im.convert("RGBA")
    w, h = im.size
    side = min(w, h)
    im = im.crop(((w - side) // 2, (h - side) // 2,
                  (w - side) // 2 + side, (h - side) // 2 + side))
    return im.resize((size, size), Image.LANCZOS)


def add_highlight(tile: Image.Image, strength: int) -> Image.Image:
    """Lighten the top edge / darken the bottom for a faint 3D sheen."""
    if strength <= 0:
        return tile
    h = tile.size[1]
    grad = Image.new("L", (1, h))
    for y in range(h):
        t = y / (h - 1)               # 0 top -> 1 bottom
        grad.putpixel((0, y), int(128 + strength * (1 - 2 * t)))
    grad = grad.resize(tile.size)
    overlay = Image.merge("RGB", (grad, grad, grad))
    rgb = ImageChops.overlay(tile.convert("RGB"), overlay)
    rgb.putalpha(tile.getchannel("A"))
    return rgb


def build() -> Image.Image:
    tile_size = SIZE - 2 * MARGIN
    radius = int(tile_size * CORNER)

    tile = square(Image.open(SRC), tile_size)
    tile.putalpha(rounded_mask(tile_size, radius))
    tile = add_highlight(tile, HIGHLIGHT)

    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))

    # drop shadow: blurred silhouette of the tile, offset down
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    sil = Image.new("RGBA", tile.size, (0, 0, 0, SHADOW_OPACITY))
    sil.putalpha(ImageChops.multiply(sil.getchannel("A"), tile.getchannel("A")))
    shadow.paste(sil, (MARGIN, MARGIN + SHADOW_OFFSET), sil)
    shadow = shadow.filter(ImageFilter.GaussianBlur(SHADOW_BLUR))

    canvas = Image.alpha_composite(canvas, shadow)
    canvas.paste(tile, (MARGIN, MARGIN), tile)
    return canvas


def write_icns(icon: Image.Image, out: Path) -> None:
    """Build a proper .iconset (incl. Retina @2x) and run `iconutil`.

    Falls back to Pillow's ICNS writer if `iconutil` is unavailable
    (i.e. not on macOS).
    """
    iconutil = shutil.which("iconutil")
    if not iconutil:
        icon.save(out)
        print("  (iconutil not found; used Pillow's ICNS writer)")
        return

    iconset = HERE / "icon.iconset"
    if iconset.exists():
        shutil.rmtree(iconset)
    iconset.mkdir()
    # (base point size, is @2x)
    specs = [(16, False), (16, True), (32, False), (32, True),
             (128, False), (128, True), (256, False), (256, True),
             (512, False), (512, True)]
    for base, retina in specs:
        px = base * 2 if retina else base
        name = f"icon_{base}x{base}{'@2x' if retina else ''}.png"
        icon.resize((px, px), Image.LANCZOS).save(iconset / name)
    subprocess.run([iconutil, "-c", "icns", str(iconset), "-o", str(out)],
                   check=True)
    shutil.rmtree(iconset)


def main() -> None:
    icon = build()
    icon.save(HERE / "icon_rounded.png")
    icon.resize((128, 128), Image.LANCZOS).save(HERE / "icon_128.png")

    sizes = [16, 32, 48, 64, 128, 256, 512]
    icon.save(HERE / "icon.ico", sizes=[(s, s) for s in sizes])
    write_icns(icon, HERE / "icon.icns")
    print("Wrote icon_rounded.png, icon_128.png, icon.ico, icon.icns to", HERE)


if __name__ == "__main__":
    main()