"""One-off: turn the client's brand files into web-sized assets in src/img/.
Run: python3 src/prep_images.py <logo.png> <mascot.webp>"""
import os, sys
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(OUT, exist_ok=True)


def trim(im):
    """Crop away transparent or near-white margins."""
    rgba = im.convert("RGBA")
    bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
    flat = Image.alpha_composite(bg, rgba).convert("L")
    mask = flat.point(lambda v: 255 if v < 245 else 0)
    box = mask.getbbox()
    return rgba.crop(box) if box else rgba


def white_to_alpha(im):
    """Make near-white pixels transparent (for files delivered on a white background)."""
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            m = min(r, g, b)
            if m > 244:
                px[x, y] = (r, g, b, 0)
            elif m > 225:
                px[x, y] = (r, g, b, int(a * (244 - m) / 19))
    return im


logo_src, mascot_src = sys.argv[1], sys.argv[2]

logo = trim(Image.open(logo_src))
print("logo src mode/size", Image.open(logo_src).mode, logo.size)
for h in (60, 120):
    w = round(logo.width * h / logo.height)
    logo.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, f"logo-{h}.png"), optimize=True)
    print("logo", h, w)

m_in = Image.open(mascot_src)
print("mascot src mode/size", m_in.mode, m_in.size)
mascot = m_in.convert("RGBA")
if m_in.mode != "RGBA":
    mascot = white_to_alpha(mascot)
mascot = trim(mascot)
h = 900
w = round(mascot.width * h / mascot.height)
mascot.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, "mascot.webp"), quality=86, method=6)
print("mascot", w, h)
