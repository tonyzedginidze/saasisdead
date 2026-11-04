# Compose the README's SVG art from the vectorized illustrations in lfs/art/svg.
# Run: uv run --with fonttools python scripts/compose-art.py
# Text is converted to outlines (Archivo + Geist, the website's fonts), so the
# SVGs render the same everywhere GitHub shows them.
import json, re
from html import escape
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "lfs/art/svg"
OUT = ROOT / "assets"
SITE_LOGOS = Path.home() / "repos/ghtop-to-sites/sites/saasisdead/public/logos"

INK, MUTED, ACCENT, SOFT, PANEL, LINE = "#0b0b0f", "#46424f", "#5f2ee0", "#efebfd", "#f7f5fb", "#e6e2ec"

GROUPS = json.loads((ROOT / "scripts/groups.json").read_text())

FONTS = {}
def font(name):
    if name not in FONTS:
        FONTS[name] = TTFont(ROOT / f"lfs/fonts/{name}.ttf")
    return FONTS[name]

def text(s, fname, size, x, y, anchor="start", fill=INK):
    """Return (svg path element, width) for s with baseline at y."""
    f = font(fname)
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    upm = f["head"].unitsPerEm
    k = size / upm
    width = sum(hmtx[cmap[ord(c)]][0] for c in s) * k
    x0 = {"start": x, "middle": x - width / 2, "end": x - width}[anchor]
    pen = SVGPathPen(gs)
    cx = 0
    for c in s:
        g = cmap[ord(c)]
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x0 + cx * k, y)))
        cx += hmtx[g][0]
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>', width

def inner(svg_text):
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg_text).group(1).split()]
    body = re.sub(r"^.*?<svg[^>]*>", "", svg_text, flags=re.S)
    body = re.sub(r"</svg>\s*$", "", body.strip())
    return vb, body

def place(svg_text, x, y, w=None, h=None):
    """Nest an SVG scaled to fit a box (aspect kept, centred)."""
    vb, body = inner(svg_text)
    s = min(w / vb[2] if w else 1e9, h / vb[3] if h else 1e9)
    dx = x + ((w or vb[2] * s) - vb[2] * s) / 2
    dy = y + ((h or vb[3] * s) - vb[3] * s) / 2
    return f'<g transform="translate({dx:.1f} {dy:.1f}) scale({s:.5f}) translate({-vb[0]} {-vb[1]})">{body}</g>', vb[2] * s, vb[3] * s

def wrap(w, h, content, title, panel=True):
    bg = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>' if panel else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img"><title>{escape(title)}</title>{bg}{content}</svg>\n'

def save(rel, data):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(data)
    print(rel, f"{len(data)//1024} KB")

def art(name):
    return (ART / f"{name}.svg").read_text()

def banner(name, title, pad=28, W=1600):
    vb, _ = inner(art(name))
    aw = W - 2 * pad
    ah = aw * vb[3] / vb[2]
    g, _, _ = place(art(name), pad, pad, aw, ah)
    save(f"art/{name}.svg", wrap(W, int(ah + 2 * pad), g, title))

# --- hero: wordmark, tagline, graveyard with real logos on the stones -------
def hero():
    W, pad, top = 1600, 40, 214
    aw = W - 2 * pad
    vb, _ = inner(art("hero"))
    s = aw / vb[2]
    g, _, ah = place(art("hero"), pad, top, aw)
    mark, mw, _ = place((Path.home() / "repos/ghtop-to-sites/sites/saasisdead/public/brand/mark.svg").read_text(), 0, 0, 96, 96)
    word, ww = text("SaaS is dead", "Archivo-wght-900", 112, 0, 0)
    gap = 18
    total = 96 + gap + ww
    x0 = (W - total) / 2
    head = (f'<g transform="translate({x0:.1f} 44)">{mark}</g>'
            f'<g transform="translate({x0 + 96 + gap:.1f} 124)">{word}</g>')
    tag, _ = text("Open-source alternatives to the apps you pay for.", "Geist-wght-500", 34, W / 2, 186, "middle", MUTED)
    # stone faces in the hero raster (connected-components on the white areas)
    stones = [  # x, y, w, h in art px, logo
        (148, 426, 162, 215, "slack"), (411, 489, 128, 155, "figma"),
        (913, 337, 216, 288, "notion"), (1229, 464, 124, 157, "zoom"),
        (1448, 400, 169, 230, "salesforce"), (1702, 500, 98, 137, "jira"),
        (1881, 448, 151, 192, "google-analytics"),
    ]
    logos = ""
    for x, y, w, h, slug in stones:
        size = min(w * 0.52, h * 0.42) * s
        cx, cy = pad + (x + w / 2) * s, top + (y + h * 0.5) * s
        lg, _, _ = place((SITE_LOGOS / f"{slug}.svg").read_text(), cx - size / 2, cy - size / 2, size, size)
        logos += lg
    H = int(top + ah + pad)
    save("art/hero.svg", wrap(W, H, head + tag + g + logos, "SaaS is dead"))

# --- buttons ---------------------------------------------------------------
def icon(name, x, y, size, color):
    svg = (ROOT / f"lfs/icons/{name}.svg").read_text().replace("currentColor", color)
    g, _, _ = place(svg, x, y, size, size)
    return g

def button(name, label, ic, primary):
    h, padx, isz, gap = 64, 28, 28, 12
    t, tw = text(label, "Geist-wght-600", 26, 0, 0)
    w = int(padx * 2 + isz + gap + tw)
    fg = "#ffffff" if primary else INK
    bg = ACCENT if primary else "#ffffff"
    stroke = ACCENT if primary else "#d2ccdc"
    t, _ = text(label, "Geist-wght-600", 26, padx + isz + gap, 41, fill=fg)
    body = (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{bg}" stroke="{stroke}" stroke-width="2"/>'
            + icon(ic, padx, (h - isz) / 2, isz, fg) + t)
    save(f"buttons/{name}.svg", wrap(w, h, body, label, panel=False))

# --- category tiles --------------------------------------------------------
def tile(slug, name, ic, primary=False):
    W, H, box = 520, 112, 68
    bg, fg = (ACCENT, "#ffffff") if primary else ("#ffffff", INK)
    body = f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{bg}" stroke="{ACCENT if primary else LINE}" stroke-width="2"/>'
    body += f'<rect x="22" y="{(H-box)/2}" width="{box}" height="{box}" rx="12" fill="{"#7b52ea" if primary else SOFT}"/>'
    body += icon(ic, 22 + 14, (H - box) / 2 + 14, box - 28, "#ffffff" if primary else ACCENT)
    size = 30
    t, tw = text(name, "Archivo-wght-800", size, 0, 0)
    while tw > W - 130 and size > 22:
        size -= 1
        t, tw = text(name, "Archivo-wght-800", size, 0, 0)
    t, _ = text(name, "Archivo-wght-800", size, 112, H / 2 + size * 0.36, fill=fg)
    save(f"tiles/{slug}.svg", wrap(W, H, body + t, name, panel=False))

hero()
banner("contribute", "Add a project with a pull request")
banner("footer", "The reaper waves goodbye")
for g in GROUPS:
    banner(g["slug"], g["name"])
    tile(g["slug"], g["name"], g["icon"])
tile("add-a-project", "Add a project", "git-pull-request", primary=True)
button("website", "Visit saasisdead.si", "globe-bold", False)
button("add", "Add a project", "git-pull-request-bold", True)
button("contributing", "Contributing guide", "book-open-text-bold", False)
