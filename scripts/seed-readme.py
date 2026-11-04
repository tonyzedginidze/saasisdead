# One-time seed of the saasisdead README from the website catalog.
# After this, README.md is edited by hand through pull requests.
import json, re, shutil, subprocess
from pathlib import Path

SITE = Path.home() / "repos/ghtop-to-sites/sites/saasisdead"
REPO = Path.home() / "repos/saasisdead"
GH = "https://github.com/tonyzedginidze/saasisdead"
c = json.loads((SITE / "data/catalog.json").read_text())
logos = json.loads((SITE / "data/logos.json").read_text())

groups = [x for x in c["categories"] if x["kind"] == "group"]
products = {x["slug"]: x for x in c["categories"] if x["kind"] == "saas"}
by_product = {}
for it in c["items"]:
    by_product.setdefault(it["category"], []).append(it)

def anchor(h):
    h = h.strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")

def clean(s):
    s = re.sub(r"\s+", " ", (s or "").strip())
    s = re.sub(r"[\U0001F000-\U0001FFFF☀-➿️]", "", s).strip()
    s = re.sub(r"(\.\.\.|…)$", "", s).rstrip(" ,;:")
    if s and s[-1] not in ".!?":
        s += "."
    return s[:1].upper() + s[1:]

def logo(slug):
    f = logos.get(slug)
    if not f:
        return ""
    f, _, variant = f.partition("#")
    dst = REPO / "assets/logos" / f
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(SITE / "public/logos" / f, dst)
    img = f'<img src="assets/logos/{f}" width="22" height="22" alt="">'
    if variant == "invert":
        # a black logo: give dark mode a light copy
        stem, ext = f.rsplit(".", 1)
        if ext == "svg":
            src = re.sub(r"<\?xml[^>]*>", "", dst.read_text())
            m = re.search(r'viewBox="([^"]+)"', src, re.I)
            if m:
                vb = m.group(1)
            else:
                wh = [float(re.search(rf'<svg[^>]*\b{a}="([\d.]+)', src).group(1)) for a in ("width", "height")]
                vb = f"0 0 {wh[0]} {wh[1]}"
            (REPO / "assets/logos" / f"{stem}-dark.svg").write_text(
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"><defs><filter id="i">'
                '<feColorMatrix type="matrix" values="-1 0 0 0 1 0 -1 0 0 1 0 0 -1 0 1 0 0 0 1 0"/></filter></defs>'
                f'<g filter="url(#i)">{src}</g></svg>')
            dark = f"{stem}-dark.svg"
        else:
            subprocess.run(["magick", str(dst), "-channel", "RGB", "-negate", "+channel",
                            str(REPO / "assets/logos" / f"{stem}-dark.png")], check=True)
            dark = f"{stem}-dark.png"
        img = (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/logos/{dark}">'
               f'{img}</picture>')
    return img + "&nbsp; "

out = []
w = out.append
w('<p align="center"><a href="https://saasisdead.si"><img src="assets/art/hero.svg" width="100%" alt="SaaS is dead: open-source alternatives to the apps you pay for"></a></p>\n')
w('<p align="center">')
w('  <a href="https://saasisdead.si"><img src="assets/buttons/website.svg" height="44" alt="Visit saasisdead.si"></a>&nbsp;')
w(f'  <a href="{GH}/edit/main/README.md"><img src="assets/buttons/add.svg" height="44" alt="Add a project"></a>&nbsp;')
w('  <a href="CONTRIBUTING.md"><img src="assets/buttons/contributing.svg" height="44" alt="Contributing guide"></a>')
w('</p>\n')
w('A hand-picked catalog of open-source projects that replace paid SaaS, grouped by the product they replace. '
  'Every entry is reviewed by hand. The same catalog, with live GitHub stars, growth and launch dates, lives at **[saasisdead.si](https://saasisdead.si)**.\n')

w('## How to add a project\n')
w('<img src="assets/art/contribute.svg" width="100%" alt="The reaper hands over a pull request">\n')
w('1. Find the category and the paid product your project replaces. If the product is missing, add a `### Product` heading in the right category.')
w('2. Add one bullet in alphabetical order: `- [Name](https://github.com/owner/repo) - What it does in one sentence.`')
w('3. Open a pull request. Accepted projects are added to [saasisdead.si](https://saasisdead.si) too.\n')
w(f'Read the [contributing guide](CONTRIBUTING.md) for what gets in. No time for a pull request? [Suggest a project]({GH}/issues/new?template=suggest-project.yml) instead.\n')

w('## Contents\n')
tiles = []
for g in groups:
    tiles.append(f'<a href="#{anchor(g["name"])}"><img src="assets/tiles/{g["slug"]}.svg" width="32%" alt="{g["name"]}"></a>')
tiles.append(f'<a href="{GH}/edit/main/README.md"><img src="assets/tiles/add-a-project.svg" width="32%" alt="Add a project"></a>')
w('<p align="center">')
for i in range(0, len(tiles), 3):
    w("  " + "\n  ".join(tiles[i:i + 3]) + "<br>")
w('</p>\n')

total = 0
for g in groups:
    prods = sorted((p for p in products.values() if p["parent"] == g["slug"] and by_product.get(p["slug"])), key=lambda p: p["name"].lower())
    if not prods:
        continue
    w(f'## {g["name"]}\n')
    w(f'<img src="assets/art/{g["slug"]}.svg" width="100%" alt="">\n')
    for p in prods:
        w(f'### {logo(p["slug"])}{p["name"]}\n')
        for it in sorted(by_product[p["slug"]], key=lambda i: i["name"].lower()):
            url = it.get("githubUrl") or it.get("url")
            desc = clean(it.get("description") or (it.get("github") or {}).get("description"))
            also = [products[a]["name"] for a in it.get("alsoIn", []) if a in products]
            line = f'- [{it["name"]}]({url}) - {desc}'
            if also:
                line += f' Also replaces {", ".join(also)}.'
            w(line)
            total += 1
        w("")
    w(f'<sub>[Back to contents](#contents)</sub>\n')

w('---\n')
w('<p align="center"><img src="assets/art/footer.svg" width="100%" alt="The reaper waves goodbye"></p>\n')
w('<p align="center">Made by <a href="https://www.linkedin.com/in/tokozedg">Tony Zedginidze</a>. Product logos are trademarks of their owners. The list is released under <a href="LICENSE">CC0</a>.</p>')

(REPO / "README.md").write_text("\n".join(out) + "\n")
print("entries", total, "bytes", len("\n".join(out)))
