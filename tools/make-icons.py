#!/usr/bin/env python3
"""Makes the site's icon files from its one drawing, static/favicon.svg (spec N4).

    python3 tools/make-icons.py

Writes, in static/: favicon.ico (16, 32 and 48 pixels, for browsers that ask for it by name), apple-touch-icon.png
(180, a phone's home screen), and icon-192.png and icon-512.png (the sizes site.webmanifest names). In a tab the
disc stands alone, on nothing. On a home screen a phone wants a solid square, so there the disc sits on white with
room around it, at 32 parts of 42, as the owner picked on 27 November 2026.

Run it after any change to the drawing, and commit what it writes: the check compares each made file with the
drawing. Needs Chrome (CHROME env var, as the checks use) with Playwright, and Pillow.
"""
import io
import os
import re
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC = os.path.join(ROOT, "static")
TAB = (16, 32, 48)                       # favicon.ico's sizes: the disc alone, on nothing
HOME = {"apple-touch-icon.png": 180, "icon-192.png": 192, "icon-512.png": 512}   # the disc on white
ROOM = 5                                 # units of white on each side of the 32-unit drawing, on a home screen


def page(svg, size, home):
    """An HTML page that shows the drawing at one size, alone or on its white square."""
    inner = re.sub(r"<\?xml[^>]*\?>", "", svg)
    inner = re.search(r"<svg[^>]*>(.*)</svg>", inner, re.S).group(1)
    box = f"{-ROOM} {-ROOM} {32 + 2 * ROOM} {32 + 2 * ROOM}" if home else "0 0 32 32"
    ground = f'<rect x="{-ROOM}" y="{-ROOM}" width="{32 + 2 * ROOM}" height="{32 + 2 * ROOM}" fill="#ffffff"/>' if home else ""
    return (f'<!doctype html><html><body style="margin:0;background:transparent">'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" width="{size}" height="{size}" '
            f'style="display:block">{ground}{inner}</svg></body></html>')


def render(svg, sizes_home):
    """Each (size, home) as a Pillow image, drawn by the browser that draws the site."""
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROME") or None, args=["--no-sandbox"])
        for size, home in sizes_home:
            pg = b.new_page(viewport={"width": size, "height": size}, device_scale_factor=1)
            pg.set_content(page(svg, size, home))
            png = pg.screenshot(omit_background=not home, clip={"x": 0, "y": 0, "width": size, "height": size})
            out[(size, home)] = Image.open(io.BytesIO(png)).convert("RGB" if home else "RGBA")
            pg.close()
        b.close()
    return out


def main():
    svg = open(os.path.join(STATIC, "favicon.svg"), encoding="utf-8").read()
    made = render(svg, [(s, False) for s in TAB] + [(s, True) for s in HOME.values()])
    tab = [made[(s, False)] for s in TAB]
    tab[-1].save(os.path.join(STATIC, "favicon.ico"), format="ICO", sizes=[(s, s) for s in TAB], append_images=tab[:-1])
    for name, size in HOME.items():
        made[(size, True)].save(os.path.join(STATIC, name), format="PNG", optimize=True)
    for name in ["favicon.ico"] + list(HOME):
        print(f"wrote static/{name} ({os.path.getsize(os.path.join(STATIC, name))} bytes)")


if __name__ == "__main__":
    sys.exit(main())
