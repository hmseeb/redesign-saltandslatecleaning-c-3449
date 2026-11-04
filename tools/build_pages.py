"""Build every inner page at its exact old-site path."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from blocks_ui import cta_band, quote_section
from parse import parse
from render import crumbs_html, is_eyebrow, page_hero, render_section
from sitelib import CTA_LABEL, esc, fix_claims, footer, head, header, md_inline

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, ".git", "gsb-source-pages")

IMG = {
    "/services/": ("/images/source/02-carousel-kitchen.jpg",
                   "Freshly cleaned kitchen with marble waterfall island and brass pendants, cleaned by Salt & Slate",
                   1024, 1024),
    "/services/recurring-cleaning/": ("/images/source/04-carousel-primary-bedroom.jpg",
                                      "Primary bedroom with made bed and linen bedding kept clean by Salt & Slate recurring house cleaning",
                                      1024, 1024),
    "/services/deep-cleaning/": ("/images/source/12-why-salt-and-slate.jpg",
                                 "Salt & Slate cleaning professional deep cleaning a luxury kitchen",
                                 1500, 1000),
    "/services/move-in-cleaning/": ("/images/source/08-carousel-foyer.jpg",
                                    "Grand foyer with sweeping oak staircase cleaned before move-in by Salt & Slate",
                                    1024, 1024),
    "/services/move-out-cleaning/": ("/images/source/37-img-4784-1764259564769.jpg",
                                     "Kitchen sink scrubbed and restored during a Salt & Slate move-out cleaning",
                                     1280, 960),
    "/services/vacation-home-cleaning/": ("/images/source/14-luxuryhome3-1764622946784.webp",
                                          "Luxury vacation home living room with mountain views cleaned by Salt & Slate",
                                          683, 1024),
    "/services/airbnb-cleaning/": ("/images/source/05-carousel-primary-bedroom.webp",
                                   "Guest-ready bedroom with fresh linens after a Salt & Slate Airbnb turnover clean",
                                   1024, 1024),
    "/services/estate-cleaning/": ("/images/source/13-luxuryhom2-1764622932087.webp",
                                   "Estate marble floors and grand entryway maintained by Salt & Slate estate cleaning",
                                   683, 1024),
    "/services/specialty-cleaning/": ("/images/source/06-carousel-primary-bathroom.jpg",
                                      "Marble primary bathroom with freestanding tub given specialty surface care by Salt & Slate",
                                      1024, 1024),
    "/services/post-construction-cleaning/": ("/images/source/33-img-4757-1764112803330.jpg",
                                              "Newly tiled shower left spotless after a Salt & Slate post-construction cleaning",
                                              1125, 1500),
    "/commercial/": ("/images/source/10-carousel-office.jpg",
                     "Professional office interior reset and cleaned by Salt & Slate commercial cleaning teams",
                     1024, 1024),
    "/locations/": ("/images/source/00-hero-home.jpg",
                    "Living room with white sectional and herringbone fireplace, freshly cleaned by Salt & Slate",
                    1456, 816),
    "/locations/utah/": ("/images/source/14-luxuryhome3-1764622946784.webp",
                         "Luxury home living room with mountain views in Utah, cleaned by Salt & Slate",
                         683, 1024),
    "/locations/arizona/": ("/images/source/03-carousel-kitchen.webp",
                            "Kitchen with marble waterfall island cleaned by Salt & Slate in Arizona",
                            1024, 1024),
    "/locations/nevada/": ("/images/source/09-carousel-foyer.webp",
                           "Entry foyer with oak staircase cleaned by Salt & Slate in Nevada",
                           1024, 1024),
    "/locations/texas/": ("/images/source/07-carousel-primary-bathroom.webp",
                          "Marble primary bathroom cleaned by Salt & Slate in Texas",
                          1024, 1024),
    "/about/": ("/images/source/12-why-salt-and-slate.jpg",
                "Salt & Slate cleaning professional at work in a luxury home kitchen",
                1536, 1024),
}
COMMERCIAL_IMG = ("/images/source/11-carousel-office.webp",
                  "Professional office interior reset and cleaned by Salt & Slate commercial cleaning teams",
                  1024, 1024)

PAGES = [
    ("01", "/services/"),
    ("02", "/services/recurring-cleaning/"),
    ("03", "/services/deep-cleaning/"),
    ("04", "/services/move-in-cleaning/"),
    ("05", "/services/move-out-cleaning/"),
    ("06", "/services/vacation-home-cleaning/"),
    ("07", "/services/airbnb-cleaning/"),
    ("08", "/services/estate-cleaning/"),
    ("09", "/services/specialty-cleaning/"),
    ("10", "/services/post-construction-cleaning/"),
    ("11", "/commercial/"),
    ("12", "/commercial/office-cleaning/"),
    ("13", "/commercial/medical-office-cleaning/"),
    ("14", "/commercial/dental-office-cleaning/"),
    ("15", "/commercial/law-firm-cleaning/"),
    ("16", "/commercial/gym-cleaning/"),
    ("17", "/commercial/restaurant-cleaning/"),
    ("18", "/commercial/warehouse-cleaning/"),
    ("19", "/commercial/retail-cleaning/"),
    ("20", "/locations/"),
    ("21", "/locations/utah/"),
    ("22", "/locations/arizona/"),
    ("23", "/locations/nevada/"),
    ("24", "/locations/texas/"),
    ("25", "/about/"),
]

DROP_SECTION = re.compile(r"(Guides for your next clean|Guides for)", re.I)
CLOSING_CTA = re.compile(r"^\s*(Ready\b|Get a |Get Your |Let.s |Elevate )", re.I)
CARD_RUN_HEADING = "Cleaning services for your home"


def split_sections(blocks):
    """Return (crumbs, hero_parts, [(eyebrow, heading, blocks)])."""
    crumbs = []
    if blocks and blocks[0][0] == "crumbs":
        crumbs = blocks[0][1]
        blocks = blocks[1:]

    hero = {"img": None, "eyebrow": "", "h1": "", "lede": "", "rest": []}

    # the h1 anchors the hero; whatever precedes it is the image + kicker label
    h1i = next((k for k, b in enumerate(blocks) if b[0] == "h1"), None)
    for b in blocks[:h1i if h1i is not None else 0]:
        if b[0] == "img" and not hero["img"]:
            hero["img"] = b
        elif b[0] == "p" and not hero["eyebrow"] and len(b[1]) <= 90 and "[" not in b[1]:
            hero["eyebrow"] = b[1]
    if h1i is not None:
        hero["h1"] = blocks[h1i][1]
        i = h1i + 1
    else:
        i = 0
    if i < len(blocks) and blocks[i][0] == "p":
        hero["lede"] = blocks[i][1]
        i += 1
    while i < len(blocks) and blocks[i][0] == "btn":
        i += 1

    rest = blocks[i:]

    # everything before the first h2 is intro prose
    sections = []
    pre = []
    j = 0
    while j < len(rest) and rest[j][0] != "h2":
        pre.append(rest[j])
        j += 1
    # an eyebrow immediately preceding the first h2 belongs to that h2
    pending_eyebrow = ""
    if pre and pre[-1][0] == "p" and is_eyebrow(pre[-1][1]):
        pending_eyebrow = pre[-1][1]
        pre = pre[:-1]
    hero["rest"] = pre

    cur = None
    while j < len(rest):
        b = rest[j]
        if b[0] == "h2":
            if cur:
                sections.append(cur)
            cur = [pending_eyebrow, b[1], []]
            pending_eyebrow = ""
            j += 1
            continue
        if b[0] == "cards" and b[1] == 2:
            # an unheaded h2-level card run is its own section
            if cur:
                sections.append(cur)
            cur = [pending_eyebrow or "Residential", CARD_RUN_HEADING, [b]]
            pending_eyebrow = ""
            j += 1
            continue
        if cur is None:
            j += 1
            continue
        # a short label right before the next h2 is that section's eyebrow
        if b[0] == "p" and is_eyebrow(b[1]) and j + 1 < len(rest) and rest[j + 1][0] == "h2":
            pending_eyebrow = b[1]
            j += 1
            continue
        cur[2].append(b)
        j += 1
    if cur:
        sections.append(cur)
    return crumbs, hero, sections


def meta_desc(lede, title):
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", fix_claims(lede or title))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:185].rsplit(" ", 1)[0] + ("…" if len(text) > 185 else "")


def build_page(num, path):
    title, blocks = parse(os.path.join(SRC, "%s.md" % num))
    crumbs, hero, sections = split_sections(blocks)

    img = IMG.get(path) or (COMMERCIAL_IMG if path.startswith("/commercial/") else None)
    hero_img = (img[0], img[1], img[2], img[3]) if img else None

    out = [head(title, meta_desc(hero["lede"], title), path,
                hero_preload=hero_img[0] if hero_img else None),
           header(),
           '<main id="main">\n']

    if crumbs:
        out.append(crumbs_html(crumbs))
    out.append(page_hero(hero["eyebrow"], hero["h1"], hero["lede"], hero_img))

    if hero["rest"]:
        intro = render_section("", "", hero["rest"], 1)
        out.append(intro.replace('class="sect sect-paper"', 'class="sect-tight sect-paper"'))

    # the old site's closing "Ready to ..." block becomes our CTA band
    cta_head = "Ready for a space that holds its standard?"
    cta_text = ("Licensed, background-checked and fully insured professionals, flat-rate pricing "
                "and a 24-hour satisfaction guarantee on every cleaning.")
    if sections:
        e, h, sb = sections[-1]
        if CLOSING_CTA.match(h) and all(b[0] == "p" for b in sb):
            cta_head = h
            body = " ".join(b[1] for b in sb).strip()
            if len(body) > 30:
                cta_text = body
            sections = sections[:-1]

    idx = 2
    for eyebrow, heading, sblocks in sections:
        if DROP_SECTION.search(heading):
            continue
        if not sblocks:
            continue
        out.append(render_section(eyebrow, heading, sblocks, idx))
        idx += 1

    out.append(cta_band(fix_claims(cta_head), fix_claims(cta_text)))
    form_name = "Commercial quote request" if path.startswith("/commercial/") else "Quote request"
    out.append(quote_section(form_name=form_name))
    out.append("</main>\n")
    out.append(footer())

    dest = os.path.join(ROOT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write("".join(out))
    return dest


if __name__ == "__main__":
    for num, path in PAGES:
        dest = build_page(num, path)
        print("built", path, "->", os.path.relpath(dest, ROOT))
