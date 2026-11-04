# Salt & Slate Cleaning Company — website

Static website for Salt & Slate Cleaning Company. Vanilla HTML, CSS and JavaScript;
no build step is required to serve it — every page is a plain `index.html`.

## Structure

```
index.html                      Home
about/                          About
services/                       Residential index + 9 service pages
commercial/                     Commercial index + 8 industry pages
locations/                      Service areas index + Utah / Arizona / Nevada / Texas
assets/css/site.css             Design system (one stylesheet)
assets/js/site.js               Nav, before/after sliders, form handling
images/source/                  Photography from the business
favicon.svg
tools/                          Python generators used to produce the HTML
```

## Design

Palette is "salt and slate": warm paper (`#F7F4EF`), deep slate ink (`#1B2026` / `#2C3540`)
and a single clay accent (`#9C4F27`) reserved for calls to action. Display type is a
serif stack, body type a system sans — no webfont requests. Section layouts are varied
deliberately (editorial rows, dense list rows, accordions, chip lists) rather than one
repeated card grid.

Accessibility: one `<h1>` per page, semantic landmarks, visible focus states, all
standalone tap targets at least 44px, and every text/background pair meets WCAG AA
contrast. `prefers-reduced-motion` is honoured.

## Forms

There is one conversion form, repeated at `#quote` on every page. It posts to LeadrVision:

- `method="POST"` to `https://vision.leadrai.com/api/forms/8e89c62d8b1083f389e7b97ba98bc588`
- hidden `_form`, `_page` (set to `window.location.href` on load) and `_gotcha` honeypot
- JavaScript submits the same URL via `fetch` and shows an inline confirmation on `{"ok": true}`
- with JavaScript disabled the plain POST still works; the visitor returns with
  `?submitted=1` and sees the same confirmation

## Regenerating the HTML

`tools/` contains the generators that produced these pages from the archived source
content. They are kept for reference; the committed HTML is the deliverable and the
site serves without running them.

```
python3 tools/build_pages.py   # the 25 inner pages
python3 tools/build_home.py    # index.html
```
