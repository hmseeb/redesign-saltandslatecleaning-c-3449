"""Render parsed blocks into the new Salt & Slate layout."""
import re

from blocks_ui import picker_html
from parse import addon_pairs
from sitelib import CTA_LABEL, PHONE, PHONE_TEL, esc, fix_claims, gproof, md_inline, resolve

PICKER_MARK = "Keep my home consistently clean"
RAW_MARK = "\x01raw:"  # marks a paragraph slot that already holds safe HTML


def is_eyebrow(text):
    """A short standalone label that the old site used as a section kicker."""
    t = (text or "").strip()
    if not t or len(t) > 60 or len(t.split()) > 8:
        return False
    if t.endswith((".", "!", ":", ";")) or "[" in t:
        return False
    if "," in t or re.search(r"\d", t):
        return False
    return True


def _p(text):
    out = md_inline(text)
    return "<p>%s</p>" % out if out else ""


def _paras(paras):
    """Render a list of paragraph strings, honouring the pre-built-HTML marker."""
    body = ""
    for p in paras:
        if p.startswith(RAW_MARK):
            body += "<p>%s</p>" % p[len(RAW_MARK):]
        else:
            body += _p(p)
    return body


def _cards(cards, variant="cards cards-3"):
    """cards: list of (title, desc, cta, url)."""
    has_desc = any(c[1] for c in cards)
    if not has_desc:
        return _pills([(c[0], c[3]) for c in cards])
    out = []
    for title, desc, cta, url in cards:
        href = resolve(url)
        label = esc(cta or "Learn more")
        inner = "<h3>%s</h3>" % esc(title)
        if desc:
            inner += "<p>%s</p>" % esc(fix_claims(desc))
        if href:
            out.append('      <a class="card is-link" href="%s">%s<span class="card-go">%s</span></a>'
                       % (href, inner, label))
        else:
            out.append('      <div class="card">%s</div>' % inner)
    return '    <div class="%s">\n%s\n    </div>' % (variant, "\n".join(out))


def _listrows(cards):
    rows = []
    for title, desc, cta, url in cards:
        href = resolve(url)
        body = ('<span class="lr-t">%s</span><span class="lr-d">%s</span>'
                % (esc(title), esc(fix_claims(desc))))
        if href:
            rows.append('      <li><a href="%s">%s<span class="lr-go" aria-hidden="true">&rarr;</span></a></li>'
                        % (href, body))
        else:
            rows.append('      <li><div style="padding:22px 0">%s</div></li>' % body)
    return '    <ul class="listrows">\n%s\n    </ul>' % "\n".join(rows)


def _pills(items):
    out = []
    for label, url in items:
        label = esc(label.rstrip(" →"))
        href = resolve(url)
        if href:
            out.append('      <li><a class="city-chip" href="%s">%s</a></li>' % (href, label))
        else:
            out.append('      <li><span class="city-chip">%s</span></li>' % label)
    return '    <ul class="cities">\n%s\n    </ul>' % "\n".join(out)


def _checklist(items, marker):
    cls = "checklist"
    if marker == "×":
        cls += " is-excluded"
    elif marker == "→":
        cls += " is-arrow"
    lis = "\n".join("      <li>%s</li>" % md_inline(t) for t in items)
    return '    <ul class="%s">\n%s\n    </ul>' % (cls, lis)


def _addons(pairs):
    lis = []
    for name, price in pairs:
        lis.append('      <li><span class="ad-n">%s</span><span class="ad-dot" aria-hidden="true"></span>'
                   '<span class="ad-p">%s</span></li>' % (esc(name), esc(price)))
    return '    <ul class="addons">\n%s\n    </ul>' % "\n".join(lis)


def _steps(steps):
    lis = []
    for num, title, paras in steps:
        body = _paras(paras)
        lis.append('      <li><span class="step-n">%s</span><h3>%s</h3>%s</li>'
                   % (esc(num), esc(title), body))
    return '    <ol class="steps">\n%s\n    </ol>' % "\n".join(lis)


def _feat(pairs):
    cells = []
    for title, paras in pairs:
        body = _paras(paras)
        cells.append("      <div><h3>%s</h3>%s</div>" % (esc(title), body))
    cls = "feat feat-3" if len(pairs) != 2 else "feat feat-2"
    return '    <div class="%s">\n%s\n    </div>' % (cls, "\n".join(cells))


def _faq(pairs):
    out = []
    for q, paras in pairs:
        body = _paras(paras)
        out.append("""      <details>
        <summary>%s</summary>
        <div class="acc-body">%s</div>
      </details>""" % (esc(q), body))
    return '    <div class="acc acc-faq">\n%s\n    </div>' % "\n".join(out)


def _accordion(groups):
    """groups: list of (label, [(sub_heading, marker, items), ...])"""
    out = []
    for label, cols in groups:
        panes = []
        for heading, marker, items in cols:
            muted = " is-muted" if marker == "×" else ""
            panes.append('        <div><p class="check-h%s">%s</p>%s</div>'
                         % (muted, esc(heading), _checklist(items, marker)))
        out.append("""      <details>
        <summary>%s</summary>
        <div class="acc-body checkgrid">
%s
        </div>
      </details>""" % (esc(label), "\n".join(panes)))
    return '    <div class="acc">\n%s\n    </div>' % "\n".join(out)


# --------------------------------------------------------------- section walk

def render_section(eyebrow, heading, blocks, index, faq_hint=False):
    """Render one h2 section's worth of blocks."""
    is_faq = faq_hint or bool(re.search(r"(FAQ|Frequently Asked|Common Questions)", heading, re.I))
    parts = []
    i, n = 0, len(blocks)

    while i < n:
        kind = blocks[i][0]

        # ---- the fixed six-way service picker
        if kind == "picker" or (kind == "cards"
                                and any(PICKER_MARK in (c[0] or "") for c in blocks[i][2])):
            parts.append(picker_html())
            i += 1
            if i < n and blocks[i][0] == "p" and "Moving in?" in blocks[i][1]:
                i += 1
            continue

        # ---- room-by-room checklist accordions
        if kind == "acc":
            groups = []
            while i < n and blocks[i][0] == "acc":
                label = blocks[i][1]
                i += 1
                cols = []
                while i < n and blocks[i][0] == "h3":
                    sub = blocks[i][1]
                    i += 1
                    items, marker = [], "✓"
                    while i < n and blocks[i][0] == "li":
                        marker = blocks[i][1] or marker
                        items.append(blocks[i][2])
                        i += 1
                    cols.append((sub, marker, items))
                groups.append((label, cols))
            parts.append(_accordion(groups))
            continue

        # ---- step sequences
        if kind == "stepnum":
            steps = []
            while i < n and blocks[i][0] == "stepnum":
                num = blocks[i][1]
                i += 1
                title = ""
                if i < n and blocks[i][0] == "h3":
                    title = blocks[i][1]
                    i += 1
                paras = []
                while i < n and blocks[i][0] == "p":
                    paras.append(blocks[i][1])
                    i += 1
                steps.append((num, title, paras))
            parts.append(_steps(steps))
            continue

        # ---- h3 + paragraph pairs -> FAQ accordion or feature grid
        if kind == "h3" and i + 1 < n and blocks[i + 1][0] == "p":
            pairs = []
            while i < n and blocks[i][0] == "h3":
                title = blocks[i][1]
                i += 1
                paras = []
                while i < n and blocks[i][0] == "p":
                    paras.append(blocks[i][1])
                    i += 1
                extra = []
                while i < n and blocks[i][0] == "btn":
                    href = resolve(blocks[i][2])
                    if href:
                        extra.append('<a class="arrow-link" href="%s">%s</a>'
                                     % (href, esc(blocks[i][1].rstrip(" →"))))
                    i += 1
                if extra:
                    paras.append(RAW_MARK + "".join(extra))
                pairs.append((title, paras))
            if is_faq:
                parts.append(_faq(pairs))
            else:
                cleaned = []
                for t, ps in pairs:
                    body = []
                    for p in ps:
                        body.append(p)
                    cleaned.append((t, body))
                parts.append(_feat_with_links(cleaned))
            continue

        # ---- county / sub-area blocks on location pages
        if kind == "hlink" or (kind == "h3" and i + 1 < n and blocks[i + 1][0] in ("pills", "cards")):
            if kind == "hlink":
                label, url = blocks[i][2], blocks[i][3]
                href = resolve(url)
                i += 1
                head = ('<h3><a href="%s">%s</a></h3>' % (href, esc(label))) if href \
                    else "<h3>%s</h3>" % esc(label)
            else:
                head = "<h3>%s</h3>" % esc(blocks[i][1])
                i += 1
            inner = [head]
            while i < n and blocks[i][0] in ("p", "pills", "h4", "hlink"):
                b = blocks[i]
                if b[0] == "p":
                    inner.append(_p(b[1]))
                elif b[0] == "pills":
                    inner.append(_pills(b[1]))
                elif b[0] == "h4":
                    inner.append('<p class="county-label">%s</p>' % esc(b[1]))
                else:  # nested hlink = county inside a state
                    href = resolve(b[3])
                    txt = esc(b[2])
                    inner.append('<p class="county-label">%s</p>'
                                 % (('<a href="%s">%s</a>' % (href, txt)) if href else txt))
                i += 1
            parts.append('    <div class="citybox">%s</div>' % "".join(inner))
            continue

        if kind == "h3":
            parts.append("    <h3>%s</h3>" % esc(blocks[i][1]))
            i += 1
            continue

        if kind == "h4":
            parts.append('    <p class="county-label">%s</p>' % esc(blocks[i][1]))
            i += 1
            continue

        if kind == "addonraw":
            parts.append(_addons(addon_pairs(blocks[i][1])))
            i += 1
            continue

        if kind == "check":
            items, marker = [], blocks[i][1]
            while i < n and blocks[i][0] == "check":
                items.append(blocks[i][2])
                i += 1
            parts.append('    <div class="checklist-2col-wrap">%s</div>'
                         % _checklist(items, marker).replace('class="checklist',
                                                             'class="checklist checklist-2col'))
            continue

        if kind == "li":
            items, marker = [], blocks[i][1]
            while i < n and blocks[i][0] == "li":
                items.append(blocks[i][2])
                i += 1
            parts.append(_checklist(items, marker))
            continue

        if kind == "cards":
            cards = blocks[i][2]
            i += 1
            if len(cards) >= 7:
                parts.append(_listrows(cards))
            else:
                variant = "cards cards-2" if len(cards) == 2 else (
                    "cards cards-4" if len(cards) == 4 else "cards cards-3")
                parts.append(_cards(cards, variant))
            continue

        if kind == "pills":
            parts.append(_pills(blocks[i][1]))
            i += 1
            continue

        if kind == "btn":
            href = resolve(blocks[i][2])
            if href:
                parts.append('    <p><a class="arrow-link" href="%s">%s</a></p>'
                             % (href, esc(blocks[i][1].rstrip(" →"))))
            i += 1
            continue

        if kind == "footnote":
            notes = []
            while i < n and blocks[i][0] == "footnote":
                notes.append("<p><strong>%s</strong> %s</p>"
                             % (esc(blocks[i][1]), md_inline(blocks[i][2])))
                i += 1
            parts.append('    <div class="footnotes">%s</div>' % "".join(notes))
            continue

        if kind == "img":
            i += 1
            continue

        if kind == "p":
            paras = []
            while i < n and blocks[i][0] == "p":
                paras.append(blocks[i][1])
                i += 1
            body = "".join(_p(t) for t in paras)
            parts.append('    <div class="prose">%s</div>' % body)
            continue

        i += 1

    shade = ["", " sect-paper", " sect-deep", " sect-paper"][index % 4]
    if is_faq:
        shade = " sect-deep"
    head_html = ""
    if heading:
        eb = '<span class="eyebrow">%s</span>' % esc(eyebrow) if eyebrow else ""
        head_html = '    <div class="sect-head">%s<h2>%s</h2></div>\n' % (eb, esc(heading))
    return '<section class="sect%s">\n  <div class="wrap">\n%s%s\n  </div>\n</section>\n' % (
        shade, head_html, "\n".join(p for p in parts if p))


def _feat_with_links(pairs):
    cells = []
    for title, paras in pairs:
        body = _paras(paras)
        cells.append("      <div><h3>%s</h3>%s</div>" % (esc(title), body))
    cls = "feat feat-2" if len(pairs) == 2 else "feat feat-3"
    return '    <div class="%s">\n%s\n    </div>' % (cls, "\n".join(cells))


def crumbs_html(items):
    out = []
    for idx, (label, url) in enumerate(items):
        href = resolve(url) if url else None
        last = idx == len(items) - 1
        if href and not last:
            out.append('      <li><a href="%s">%s</a></li>' % (href, esc(label)))
        else:
            out.append('      <li><span aria-current="page">%s</span></li>' % esc(label))
    return """<nav class="crumbs wrap" aria-label="Breadcrumb">
  <ol>
%s
  </ol>
</nav>
""" % "\n".join(out)


def page_hero(eyebrow, h1, lede, img, cta_label=None):
    cta_label = cta_label or CTA_LABEL
    media = ""
    if img:
        src, alt, w, h = img
        media = """    <div class="phero-media">
      <img src="%s" alt="%s" width="%d" height="%d" fetchpriority="high" decoding="async">
    </div>""" % (src, esc(alt), w, h)
    eb = '<span class="eyebrow">%s</span>' % esc(eyebrow) if eyebrow else ""
    return """<section class="phero">
  <div class="wrap phero-grid">
    <div>
      %s
      <h1>%s</h1>
      <p class="lede">%s</p>
      <div class="cta-row">
        <a class="btn btn-primary" href="#quote">%s</a>
        <a class="btn btn-ghost" href="tel:%s">Call %s</a>
      </div>
      %s
    </div>
%s
  </div>
</section>
""" % (eb, esc(h1), md_inline(lede), esc(cta_label), PHONE_TEL, esc(PHONE), gproof(), media)
