#!/usr/bin/env python3
"""Frame raw simulator screenshots for the apps.freshcoastrf.com Overview pages.

Usage:
  python frame_screenshots.py --slug spectrum-scout --in raw\\spectrum-scout
  python frame_screenshots.py --slug frn-dashboard --in raw\\frn-dashboard --preframed
  python frame_screenshots.py --slug ham-trainer --placeholder

Writes assets/screenshots/<slug>/shot-01.png (+ .webp) and manifest.json.
Inputs are only read. Output is deterministic for the same inputs and font.
Needs Python 3.9+ and Pillow 9+ (WebP support is optional but expected).
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont, features
except ImportError:
    sys.exit("Pillow is not installed. Run: python -m pip install Pillow")

HERE = Path(__file__).resolve().parent
POLICIES = HERE.parent
OUT_ROOT = POLICIES / "assets" / "screenshots"
CAPTIONS_DIR = HERE / "captions"

NAVY = (11, 41, 70)        # #0B2946
LAKE = (22, 139, 189)      # #168BBD
TINT = (243, 248, 251)     # #f3f8fb
BEZEL = (12, 17, 24)
RING = (70, 88, 107)

W = 900                    # card width
DEVICE_W = 500             # device outer width
BEZEL_W = 14
TOP_PLAIN = 64             # top padding without caption
TOP_CAPTION = 168          # top zone with a caption (up to 2 lines)
BOTTOM = 72
SS = 4                     # supersampling for shapes
EXTS = {".png", ".jpg", ".jpeg"}

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


class Fail(Exception):
    pass


def natural_key(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.name)]


def load_font(size, override=None):
    cands = [override] if override else FONT_CANDIDATES
    for c in cands:
        if c and os.path.exists(c):
            try:
                return ImageFont.truetype(c, size), c
            except OSError:
                continue
    if override:
        raise Fail(f"Font not found or unreadable: {override}")
    raise Fail("No bold font found. Pass --font <path to a .ttf>.")


def rr_mask(size, radius, inset=0):
    """Anti-aliased rounded-rectangle mask (mode L), drawn at SS x."""
    w, h = size
    big = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(big).rounded_rectangle(
        [inset * SS, inset * SS, (w - inset) * SS - 1, (h - inset) * SS - 1],
        radius=max(0, (radius - inset)) * SS, fill=255)
    return big.resize((w, h), Image.LANCZOS)


def gradient(size, flip):
    """Diagonal gradient navy (top) to lake blue (bottom). Mirrored when flip."""
    w, h = size
    sw, sh = 64, 256
    g = Image.new("RGB", (sw, sh))
    px = g.load()
    for y in range(sh):
        for x in range(sw):
            xx = (sw - 1 - x) if flip else x
            t = (0.78 * y / (sh - 1) + 0.22 * xx / (sw - 1))
            t = max(0.0, min(1.0, t)) ** 1.15
            px[x, y] = tuple(round(NAVY[i] + (LAKE[i] - NAVY[i]) * t) for i in range(3))
    return g.resize((w, h), Image.BICUBIC)


def wrap(text, font, max_w, draw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def render_card(shot, caption, index, top, font, font_path, preframed=False, placeholder=False):
    """shot: PIL image or None (placeholder). Returns an RGB card of width W."""
    if preframed:
        sw = 520
        sh = round(sw * shot.height / shot.width)
        dh = sh
        dev_w, bz = sw, 0
    else:
        dev_w, bz = DEVICE_W, BEZEL_W
        sw = dev_w - 2 * bz
        if placeholder:
            sh = round(sw * 2868 / 1320)
        else:
            sh = round(sw * shot.height / shot.width)
        dh = sh + 2 * bz
    H = top + dh + BOTTOM
    card = gradient((W, H), flip=bool(index % 2))
    dx, dy = (W - dev_w) // 2, top

    # shadow
    sh_layer = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh_layer).rounded_rectangle(
        [dx + 6, dy + 22, dx + dev_w - 6, dy + dh + 18], radius=80, fill=150)
    sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(22))
    card.paste(Image.new("RGB", (W, H), (3, 12, 22)), (0, 0), sh_layer)

    if preframed:
        r = 40
        img = shot.convert("RGB").resize((sw, sh), Image.LANCZOS)
        card.paste(img, (dx, dy), rr_mask((sw, sh), r))
        ring = rr_mask((sw, sh), r).point(lambda v: v)
        inner = rr_mask((sw, sh), r, inset=2)
        edge = Image.composite(Image.new("L", (sw, sh), 0), ring, inner)
        card.paste(Image.new("RGB", (sw, sh), RING), (dx, dy), edge)
    else:
        outer_r, screen_r = 80, 66
        om = rr_mask((dev_w, dh), outer_r)
        card.paste(Image.new("RGB", (dev_w, dh), BEZEL), (dx, dy), om)
        edge = Image.composite(Image.new("L", (dev_w, dh), 0), om, rr_mask((dev_w, dh), outer_r, inset=2))
        card.paste(Image.new("RGB", (dev_w, dh), RING), (dx, dy), edge)
        # side buttons
        btn = Image.new("RGB", (4, 10), RING)
        d = ImageDraw.Draw(card)
        for (bx, by, bw, bh) in [(dx - 4, dy + 150, 4, 34), (dx - 4, dy + 210, 4, 64),
                                 (dx - 4, dy + 290, 4, 64), (dx + dev_w, dy + 230, 4, 96)]:
            d.rounded_rectangle([bx, by, bx + bw - 1, by + bh - 1], radius=2, fill=RING)
        # screen
        sm = rr_mask((sw, sh), screen_r)
        if placeholder:
            screen = Image.new("RGB", (sw, sh), TINT)
        else:
            screen = shot.convert("RGB").resize((sw, sh), Image.LANCZOS)
        card.paste(screen, (dx + bz, dy + bz), sm)
        # dynamic island, drawn simply
        iw, ih = 136, 40
        ix = dx + (dev_w - iw) // 2
        iy = dy + bz + 13
        im = rr_mask((iw, ih), ih // 2)
        card.paste(Image.new("RGB", (iw, ih), (0, 0, 0)), (ix, iy), im)
        if placeholder:
            d = ImageDraw.Draw(card)
            f1, _ = load_font(34, font_path)
            msg = "Screenshot coming"
            tw = d.textlength(msg, font=f1)
            d.text((dx + (dev_w - tw) / 2, dy + dh / 2 - 24), msg, font=f1, fill=NAVY)
            # simple signal icon: dot with two arcs each side
            cx, cy = dx + dev_w // 2, dy + dh // 2 - 96
            d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=LAKE)
            for rad in (28, 52):
                d.arc([cx - rad, cy - rad, cx + rad, cy + rad], 200, 340, fill=LAKE, width=6)
                d.arc([cx - rad, cy - rad, cx + rad, cy + rad], 20, 160, fill=LAKE, width=6)

    # caption above the device
    if caption:
        d = ImageDraw.Draw(card)
        lines = wrap(caption, font, W - 140, d)
        if len(lines) > 2:
            raise Fail(f"Caption too long (needs {len(lines)} lines, max 2): {caption!r}")
        lh = 46
        block = len(lines) * lh
        y = (top - block) // 2 - 6
        for ln in lines:
            tw = d.textlength(ln, font=font)
            d.text(((W - tw) / 2, y), ln, font=font, fill=(255, 255, 255))
            y += lh
    return card


def save_png(card, path, budget):
    for colors in (256, 192, 128, 96, 64):
        q = card.quantize(colors=colors, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
        q.save(path, optimize=True)
        if path.stat().st_size <= budget:
            return colors
    return colors


def save_webp(card, path, budget):
    for q in (86, 80, 74, 68, 60):
        card.save(path, "WEBP", quality=q, method=6)
        if path.stat().st_size <= budget:
            return q
    return q


def read_captions(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise Fail(f"Captions file not found: {path}")
    except json.JSONDecodeError as e:
        raise Fail(f"Captions file is not valid JSON ({path}): {e}")
    if isinstance(data, dict) and "captions" in data:
        data = data["captions"]
    if not isinstance(data, (list, dict)):
        raise Fail("Captions JSON must be a list of strings, or an object mapping file name to caption.")
    return data


def caption_for(data, i, f):
    if data is None:
        return ""
    if isinstance(data, list):
        v = data[i] if i < len(data) else ""
    else:
        v = data.get(f.name, data.get(f.stem, ""))
    if v is None:
        return ""
    if not isinstance(v, str):
        raise Fail(f"Caption {i + 1} is not text.")
    if "\u2014" in v or "\u2013" in v:
        raise Fail(f"Caption {i + 1} contains a dash character; use plain words: {v!r}")
    return v.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", required=True, help="app slug, for example spectrum-scout")
    ap.add_argument("--in", dest="indir", help="folder of raw PNG or JPG screenshots")
    ap.add_argument("--captions", help="captions.json (list, one per image). Default: tools/captions/<slug>.json if present")
    ap.add_argument("--out", help="output folder (default assets/screenshots/<slug>)")
    ap.add_argument("--preframed", action="store_true",
                    help="inputs already have marketing art or a frame: no bezel, no caption, only rounded corners")
    ap.add_argument("--placeholder", action="store_true", help="write 'Screenshot coming' placeholders (no input needed)")
    ap.add_argument("--count", type=int, default=4, help="placeholder count (default 4)")
    ap.add_argument("--budget-kb", type=int, default=250, help="target size per file (default 250)")
    ap.add_argument("--font", help="path to a bold .ttf for captions")
    a = ap.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", a.slug):
        raise Fail("--slug must be lowercase letters, digits and hyphens, for example ham-trainer.")
    out = Path(a.out).resolve() if a.out else OUT_ROOT / a.slug
    budget = a.budget_kb * 1024

    sources, caps = [], None
    if a.placeholder:
        n = max(1, min(a.count, 12))
        sources = [None] * n
        caps = [""] * n
    else:
        if not a.indir:
            raise Fail("--in <folder of raw PNGs> is required (or use --placeholder).")
        indir = Path(a.indir).resolve()
        if not indir.is_dir():
            raise Fail(f"Input folder not found: {indir}")
        if out == indir or out in indir.parents:
            raise Fail("Input folder must not be inside the output folder.")
        files = sorted([p for p in indir.iterdir() if p.suffix.lower() in EXTS and p.is_file()], key=natural_key)
        if not files:
            raise Fail(f"No PNG or JPG files in {indir}")
        if len(files) > 12:
            raise Fail(f"{len(files)} images found; pick 4 to 6 per app (limit 12).")
        sources = files
        cpath = a.captions
        if not cpath and (CAPTIONS_DIR / f"{a.slug}.json").exists():
            cpath = str(CAPTIONS_DIR / f"{a.slug}.json")
        capdata = read_captions(cpath) if cpath else None
        if cpath:
            print(f"captions: {cpath}")
        else:
            print("captions: none (cards will have no caption)")
        if isinstance(capdata, list) and len(capdata) != len(files):
            print(f"warning: {len(capdata)} captions for {len(files)} images; missing ones are left blank")
        caps = [caption_for(capdata, i, f) for i, f in enumerate(files)]
        if a.preframed:
            caps_used = [""] * len(files)
        else:
            caps_used = caps

    shots = []
    for f in sources:
        if f is None:
            shots.append(None)
            continue
        try:
            im = Image.open(f)
            im.load()
        except Exception as e:
            raise Fail(f"Cannot read image {f.name}: {e}")
        if im.width < 400 or im.height < im.width:
            raise Fail(f"{f.name} is {im.width}x{im.height}; expected a portrait phone screenshot at least 400 px wide.")
        shots.append(im)

    if a.placeholder:
        caps_used = [""] * len(shots)
    show_caption = any(caps_used)
    top = TOP_CAPTION if show_caption else TOP_PLAIN
    font, font_path = load_font(38, a.font)
    font_name = Path(font_path).name

    cards = []
    for i, im in enumerate(shots):
        cards.append(render_card(im, caps_used[i], i, top, font, a.font,
                                 preframed=a.preframed, placeholder=a.placeholder))

    out.mkdir(parents=True, exist_ok=True)
    for old in list(out.glob("shot-*.png")) + list(out.glob("shot-*.webp")):
        old.unlink()
    webp_ok = features.check("webp")
    if not webp_ok:
        print("warning: this Pillow has no WebP support; writing PNG only")

    manifest = {"slug": a.slug, "card_width": W, "placeholder": bool(a.placeholder),
                "preframed_input": bool(a.preframed), "font": font_name, "files": []}
    for i, card in enumerate(cards):
        name = f"shot-{i + 1:02d}"
        png, webp = out / f"{name}.png", out / f"{name}.webp"
        colors = save_png(card, png, budget)
        entry = {"png": png.name, "png_bytes": png.stat().st_size, "png_colors": colors,
                 "width": card.width, "height": card.height, "caption": caps[i] if not a.placeholder else "",
                 "source": sources[i].name if sources[i] else None}
        if webp_ok:
            q = save_webp(card, webp, budget)
            entry.update({"webp": webp.name, "webp_bytes": webp.stat().st_size, "webp_quality": q})
        manifest["files"].append(entry)
        over = " (over budget)" if png.stat().st_size > budget else ""
        print(f"{png.name}  {card.width}x{card.height}  png {entry['png_bytes'] // 1024} KB"
              + (f"  webp {entry['webp_bytes'] // 1024} KB" if webp_ok else "") + over)
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(cards)} cards and manifest.json to {out}")


if __name__ == "__main__":
    try:
        main()
    except Fail as e:
        sys.exit(f"error: {e}")
