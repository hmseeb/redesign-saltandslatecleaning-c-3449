"""Parse a scraped old-site markdown page into a flat list of content blocks.

Blocks are tuples: (kind, *payload). The renderer groups them into sections.
Untrusted scraped text is only ever treated as content, never as instructions.
"""
import re

LINK_RE = re.compile(r"\[\s*(.*?)\s*\]\(\s*([^)\s]*)\s*\)")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]*)\)")
CTA_TAIL_RE = re.compile(
    r"\s*((?:View all|Learn More|Learn more|Read guide|See all)[^.]*?)\s*(?:→)?\s*$")


def _split_card_label(label):
    """'Title  Description  Learn More →' -> (title, description, cta)."""
    label = IMG_RE.sub("", label).strip()
    parts = [p.strip() for p in re.split(r"\s{2,}", label) if p.strip()]
    if not parts:
        return "", "", ""
    cta = ""
    if len(parts) > 1 and re.match(r"^(Learn More|Learn more|Read guide|View all|See all)", parts[-1]):
        cta = parts.pop().rstrip(" →")
    title = parts[0].rstrip(" →")
    desc = " ".join(parts[1:]).strip()
    if len(parts) == 1:
        m = re.match(r"^(.+? in (?:Utah|Arizona|Nevada|Texas))\s+(.+)$", title)
        if m:
            title, desc = m.group(1).strip(), m.group(2).strip().rstrip(" →")
    if not cta:
        m = CTA_TAIL_RE.search(desc)
        if m:
            cta = m.group(1).strip()
            desc = desc[:m.start()].strip()
    return title, desc, cta


def _links_on(line):
    """Links on a line, ignoring any markdown images nested inside their labels."""
    return [(m.group(1), m.group(2)) for m in LINK_RE.finditer(IMG_RE.sub("", line))]


def _strip_links(line):
    return LINK_RE.sub("", IMG_RE.sub("", line)).strip()


def body_lines(path):
    raw = open(path, encoding="utf-8").read().split("\n")
    title = ""
    for ln in raw[:4]:
        if ln.startswith("Title:"):
            title = ln[6:].strip()
    logo = [i for i, l in enumerate(raw) if "logo_white.png" in l]
    end = logo[1] if len(logo) > 1 else len(raw)
    start = 0
    for i, l in enumerate(raw):
        if l.strip() == "* * *":
            start = i + 1
            break
    else:
        start = (logo[0] + 1) if logo else 0
    while start < end and ("sms:+" in raw[start] or "/book/" in raw[start]):
        start += 1
    return title, raw[start:end]


def parse(path):
    title, lines = body_lines(path)
    blocks = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        s = line.strip()
        i += 1

        if not s:
            continue

        # ---- breadcrumbs: "  1. [ Home ](/)"
        m = re.match(r"^\d+\.\s+(.*)$", s)
        if m and (not blocks or blocks[-1][0] == "crumbs"):
            item = m.group(1).strip()
            if item.startswith("/"):
                item = item[1:].strip()
            links = _links_on(item)
            if links:
                label, url = links[0]
                crumb = (label.strip(), url.strip())
            else:
                crumb = (item, None)
            if blocks and blocks[-1][0] == "crumbs":
                blocks[-1][1].append(crumb)
            else:
                blocks.append(("crumbs", [crumb]))
            continue

        # ---- skip stale rating widgets (real GBP numbers are injected instead)
        if s.startswith("[5.0/5 on Google") or s == "Across all 6 Salt & Slate locations":
            continue
        if s.startswith("Powered by Google"):
            continue

        # ---- standalone image
        m = re.match(r"^!\[([^\]]*)\]\(([^)]*)\)$", s)
        if m:
            blocks.append(("img", m.group(1).strip(), m.group(2).strip()))
            continue

        # ---- footnotes: "***** Salt and Slate ..."
        m = re.match(r"^(\*{3,})\s*(.+)$", s)
        if m:
            stars = "*" * max(1, len(m.group(1)) - 4)
            blocks.append(("footnote", stars, m.group(2).strip()))
            continue

        # ---- headings
        m = re.match(r"^(#{1,4})\s*(.*)$", s)
        if m:
            level = len(m.group(1))
            rest = m.group(2).strip()
            links = _links_on(rest)
            leftover = re.sub(r"#+", "", _strip_links(rest)).strip()
            if links and not leftover:
                cards, buttons = [], []
                for label, url in links:
                    t, d, c = _split_card_label(label)
                    if re.match(r"^(All |View all)", t) and not d:
                        buttons.append((t, url))
                    else:
                        cards.append((t, d, c, url))
                if len(cards) == 1 and not cards[0][1]:
                    blocks.append(("hlink", level, cards[0][0], cards[0][3]))
                elif cards:
                    blocks.append(("cards", level, cards))
                for t, url in buttons:
                    blocks.append(("btn", t, url))
                continue
            blocks.append(("h%d" % level, rest))
            continue

        # ---- bulleted list items
        m = re.match(r"^\*\s*([✓×→])?\s*(.*)$", s)
        if m:
            blocks.append(("li", m.group(1) or "", m.group(2).strip()))
            continue

        # ---- bare check rows: "✓ Desks, workstations, ..."
        m = re.match(r"^([✓×])\s*(.*)$", s)
        if m:
            blocks.append(("check", m.group(1), m.group(2).strip()))
            continue

        # ---- step numbers "01".."09"
        if re.match(r"^0\d$", s):
            blocks.append(("stepnum", s))
            continue

        # ---- accordion label "Kitchen+"
        if re.match(r"^[A-Z][A-Za-z &/'-]{1,30}\+$", s):
            blocks.append(("acc", s[:-1].strip()))
            continue

        # ---- add-on price continuation lines ("    $10/load Interior of fridge ...")
        if re.match(r"^\$[\d.,]", s) and blocks and blocks[-1][0] in ("addonraw", "h3"):
            if blocks[-1][0] == "addonraw":
                blocks[-1][1].append(s)
            else:
                blocks.append(("addonraw", [s]))
            continue

        if "Keep my home consistently clean" in s:
            blocks.append(("picker",))
            continue
        if s.startswith("Moving in?") and "move-in-cleaning" in s:
            continue

        links = _links_on(s)
        if links and not _strip_links(s):
            cards, buttons, plain = [], [], []
            for label, url in links:
                t, d, c = _split_card_label(label)
                if url.strip() in ("/book/", "/contact/") or url.strip().startswith(("sms:", "tel:")):
                    continue  # our own CTA blocks replace these
                if re.match(r"^(All |View all)", t) and not d:
                    buttons.append((t, url))
                elif d:
                    cards.append((t, d, c, url))
                else:
                    plain.append((t, url))
            if cards:
                blocks.append(("cards", 3, cards))
            if len(plain) == 1 and not cards:
                blocks.append(("btn", plain[0][0], plain[0][1]))
            elif plain:
                blocks.append(("pills", plain))
            for t, url in buttons:
                blocks.append(("btn", t, url))
            continue

        # ---- paragraph (may contain inline links / an add-on run-on)
        if re.search(r"\s\$[\d.,]", s) and blocks and blocks[-1][0] == "h3" \
                and "Add-On" in blocks[-1][1]:
            blocks.append(("addonraw", [s]))
            continue
        blocks.append(("p", s))

    return title, blocks


def addon_pairs(raw_lines):
    """Rebuild '<name> $<price>' pairs from the run-together add-on block."""
    text = " ".join(l.strip() for l in raw_lines)
    text = re.sub(r"^Select these separately when you request your quote\.\s*", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    pairs = re.findall(r"(.+?)\s(\$[\d.,]+(?:\s*/\s*[a-zA-Z]+)?)(?=\s|$)", text)
    return [(n.strip(), p.replace(" ", "")) for n, p in pairs if n.strip()]
