"""Shared constants, link resolution and page chrome for the Salt & Slate site."""
import html
import re

BRAND = "Salt & Slate Cleaning Company"
BRAND_SHORT = "Salt & Slate"
PHONE = "(725) 777-1406"
PHONE_TEL = "+17257771406"
EMAIL = "hello@saltandslatecleaning.com"
ADDR_STREET = "3930 University Center Dr #807"
ADDR_CITY = "Las Vegas"
ADDR_REGION = "NV"
ADDR_ZIP = "89119"
ADDR_ONE_LINE = "3930 University Center Dr #807, Las Vegas, NV 89119"
GOOGLE_URL = "https://maps.google.com/?cid=18264511951078511304"
REVIEW_URL = "/review"
RATING = "5.0"
REVIEW_COUNT = "39"
FORM_ACTION = "https://vision.leadrai.com/api/forms/8e89c62d8b1083f389e7b97ba98bc588"
CTA_LABEL = "Get a Free Quote"
STARS = "★★★★★"

RESIDENTIAL = [
    ("/services/recurring-cleaning/", "Standard & Recurring Cleaning"),
    ("/services/deep-cleaning/", "Deep Cleaning"),
    ("/services/move-in-cleaning/", "Move-In Cleaning"),
    ("/services/move-out-cleaning/", "Move-Out Cleaning"),
    ("/services/vacation-home-cleaning/", "Vacation Home Cleaning"),
    ("/services/airbnb-cleaning/", "Airbnb & Rental Cleaning"),
    ("/services/estate-cleaning/", "Estate Cleaning"),
    ("/services/specialty-cleaning/", "Specialty Cleaning"),
    ("/services/post-construction-cleaning/", "Post-Construction Cleaning"),
]

COMMERCIAL = [
    ("/commercial/office-cleaning/", "Office Cleaning"),
    ("/commercial/medical-office-cleaning/", "Medical Office Cleaning"),
    ("/commercial/dental-office-cleaning/", "Dental Office Cleaning"),
    ("/commercial/law-firm-cleaning/", "Law Firm Cleaning"),
    ("/commercial/gym-cleaning/", "Gym & Fitness Cleaning"),
    ("/commercial/restaurant-cleaning/", "Restaurant Cleaning"),
    ("/commercial/warehouse-cleaning/", "Warehouse Cleaning"),
    ("/commercial/retail-cleaning/", "Retail Cleaning"),
]

STATES = [
    ("/locations/utah/", "Utah"),
    ("/locations/arizona/", "Arizona"),
    ("/locations/nevada/", "Nevada"),
    ("/locations/texas/", "Texas"),
]

VALID = {"/", "/services/", "/commercial/", "/locations/", "/about/"}
VALID |= {p for p, _ in RESIDENTIAL} | {p for p, _ in COMMERCIAL} | {p for p, _ in STATES}

# Commercial verticals the old site had that are not rebuilt here (no page = no link).
UNBUILT_COMMERCIAL = {
    "church-cleaning", "event-cleaning", "property-management", "daycare-cleaning",
    "salon-spa-cleaning", "coworking-space-cleaning", "construction-site-cleanup",
}

SERVICE_SLUGS = {p.strip("/").split("/")[-1]: p for p, _ in RESIDENTIAL}
SERVICE_SLUGS.update({p.strip("/").split("/")[-1]: p for p, _ in COMMERCIAL})

STATE_SLUGS = {"utah", "arizona", "nevada", "texas"}


def resolve(url):
    """Map an old-site URL onto a path that exists here, or None to drop the link."""
    if not url:
        return None
    url = url.strip()
    if url.startswith("#"):
        return url
    if url.startswith(("sms:", "tel:", "mailto:")):
        return None
    if url.startswith(("http://", "https://")):
        if "saltandslatecleaning.com" in url:
            url = re.sub(r"^https?://(www\.)?saltandslatecleaning\.com", "", url) or "/"
        else:
            return None  # external old-site socials etc. are dropped
    if not url.startswith("/"):
        return None

    path, _, frag = url.partition("#")
    if not path.endswith("/"):
        path += "/"

    if path in VALID:
        return path
    if path in ("/book/", "/contact/", "/quote/"):
        return "#quote"
    if path == "/reviews/":
        return "/#reviews"
    if path in ("/guarantee/", "/our-process/"):
        return "/about/"
    if path.startswith("/blog/") or path.startswith("/service-areas/"):
        return None
    if path in ("/press/", "/privacy/", "/terms/", "/careers/"):
        return None

    parts = [p for p in path.strip("/").split("/") if p]
    if parts and parts[0] == "locations":
        if len(parts) >= 2 and parts[1] in STATE_SLUGS:
            # /locations/<state>/<service-or-county>/... collapses to the state page
            return "/locations/%s/" % parts[1]
        return "/locations/"
    if parts and parts[0] == "commercial":
        if len(parts) >= 2 and parts[1] in UNBUILT_COMMERCIAL:
            return None
        return "/commercial/"
    if parts and parts[0] == "services":
        return "/services/"
    return None


def esc(text):
    return html.escape(text or "", quote=True)


RATING_FIXES = [
    ("273 reviews across 6 locations", "%s Google reviews" % REVIEW_COUNT),
    ("273 reviews", "%s reviews" % REVIEW_COUNT),
]


def fix_claims(text):
    """The real Google Business Profile is 5.0 from 39 reviews - correct stale counts."""
    for old, new in RATING_FIXES:
        text = text.replace(old, new)
    return text


def md_inline(raw):
    """Escape text and turn markdown links into resolved anchors (dropping dead ones)."""
    raw = fix_claims(raw or "")
    out, pos = [], 0
    for m in re.finditer(r"\[([^\]]*)\]\(([^)]*)\)", raw):
        out.append(esc(raw[pos:m.start()]))
        label = m.group(1).strip()
        target = resolve(m.group(2))
        if m.group(2).strip().startswith(("sms:", "tel:")):
            label = ""  # drop stale office phone numbers entirely
        if target and label:
            out.append('<a href="%s">%s</a>' % (target, esc(label)))
        else:
            out.append(esc(label))
        pos = m.end()
    out.append(esc(raw[pos:]))
    return re.sub(r"\s{2,}", " ", "".join(out)).strip()


# --------------------------------------------------------------------- chrome

def head(title, description, path, hero_preload=None):
    canon = path if path.endswith("/") else path + "/"
    pre = ""
    if hero_preload:
        pre = '\n  <link rel="preload" as="image" href="%s" fetchpriority="high">' % hero_preload
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>%s</title>
  <meta name="description" content="%s">
  <meta name="theme-color" content="#2C3540">
  <link rel="canonical" href="%s">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="%s">
  <meta property="og:title" content="%s">
  <meta property="og:description" content="%s">
  <meta property="og:image" content="/images/source/00-hero-home.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/favicon.svg">
  <link rel="stylesheet" href="/assets/css/site.css">%s
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
""" % (esc(title), esc(description), esc(canon), esc(BRAND), esc(title), esc(description), pre)


def _brand(extra_class=""):
    return """<a class="brand%s" href="/">
      <span class="brand-mark" aria-hidden="true">S&amp;S</span>
      <span>
        <span class="brand-name">Salt &amp; Slate</span>
        <span class="brand-sub">Cleaning Company</span>
      </span>
    </a>""" % ((" " + extra_class) if extra_class else "")


def _submenu(items, all_label, all_href):
    rows = "\n".join(
        '        <li><a href="%s">%s</a></li>' % (href, esc(label)) for href, label in items
    )
    return """      <ul class="submenu submenu-wide">
%s
        <li class="submenu-all"><a href="%s">%s</a></li>
      </ul>""" % (rows, all_href, esc(all_label))


def header():
    return """<header class="site-header">
  <div class="wrap header-bar">
    %s
    <nav class="nav" aria-label="Main navigation">
      <ul class="nav-list">
        <li class="has-sub">
          <button class="nav-toggle" type="button" aria-expanded="false">Residential <span class="chev" aria-hidden="true"></span></button>
%s
        </li>
        <li class="has-sub">
          <button class="nav-toggle" type="button" aria-expanded="false">Commercial <span class="chev" aria-hidden="true"></span></button>
%s
        </li>
        <li class="has-sub">
          <button class="nav-toggle" type="button" aria-expanded="false">Locations <span class="chev" aria-hidden="true"></span></button>
%s
        </li>
        <li><a class="nav-link" href="/about/">About</a></li>
        <li><a class="nav-link" href="/#reviews">Reviews</a></li>
      </ul>
    </nav>
    <div class="header-actions">
      <a class="header-tel" href="tel:%s"><span><small>Call us</small>%s</span></a>
      <a class="btn btn-primary btn-sm" href="#quote">%s</a>
    </div>
    <button class="burger" type="button" aria-expanded="false" aria-controls="drawer">
      <span class="burger-bars" aria-hidden="true"><span></span><span></span><span></span></span>
      Menu
    </button>
  </div>
</header>

<div class="drawer" id="drawer" data-open="false">
  <div class="drawer-top">
    %s
    <button class="drawer-close" type="button">Close</button>
  </div>
  <div class="drawer-body">
    <div class="drawer-group">
      <button type="button" aria-expanded="false">Residential <span class="chev" aria-hidden="true"></span></button>
      <ul class="drawer-sub">
        <li><a href="/services/">All Residential Services</a></li>
%s
      </ul>
    </div>
    <div class="drawer-group">
      <button type="button" aria-expanded="false">Commercial <span class="chev" aria-hidden="true"></span></button>
      <ul class="drawer-sub">
        <li><a href="/commercial/">All Commercial Services</a></li>
%s
      </ul>
    </div>
    <div class="drawer-group">
      <button type="button" aria-expanded="false">Locations <span class="chev" aria-hidden="true"></span></button>
      <ul class="drawer-sub">
        <li><a href="/locations/">All Service Areas</a></li>
%s
      </ul>
    </div>
    <div class="drawer-group"><a href="/about/">About</a></div>
    <div class="drawer-group"><a href="/#reviews">Reviews</a></div>
  </div>
  <div class="drawer-foot">
    <a class="btn btn-primary" href="#quote">%s</a>
    <a class="btn btn-ghost" href="tel:%s">Call %s</a>
  </div>
</div>

<div class="mobile-bar">
  <a class="btn btn-ghost" href="tel:%s">Call now</a>
  <a class="btn btn-primary" href="#quote">Free quote</a>
</div>
""" % (
        _brand(),
        _submenu(RESIDENTIAL, "All Services →", "/services/"),
        _submenu(COMMERCIAL, "All Commercial Services →", "/commercial/"),
        _submenu(STATES, "All Service Areas →", "/locations/"),
        PHONE_TEL, esc(PHONE), esc(CTA_LABEL),
        _brand(),
        "\n".join('        <li><a href="%s">%s</a></li>' % (h, esc(l)) for h, l in RESIDENTIAL),
        "\n".join('        <li><a href="%s">%s</a></li>' % (h, esc(l)) for h, l in COMMERCIAL),
        "\n".join('        <li><a href="%s">%s</a></li>' % (h, esc(l)) for h, l in STATES),
        esc(CTA_LABEL), PHONE_TEL, esc(PHONE), PHONE_TEL,
    )


def gproof(dark=False):
    return """<a class="gproof" href="%s" target="_blank" rel="noopener">
        <span class="stars" aria-hidden="true">%s</span>
        <span><b>%s</b> from %s reviews</span>
        <span class="gproof-cta">Read our reviews on Google</span>
      </a>""" % (GOOGLE_URL, STARS, RATING, REVIEW_COUNT)


def footer():
    res = "\n".join('          <li><a href="%s">%s</a></li>' % (h, esc(l)) for h, l in RESIDENTIAL)
    com = "\n".join('          <li><a href="%s">%s</a></li>' % (h, esc(l)) for h, l in COMMERCIAL)
    states = "\n".join('          <li><a href="%s">%s cleaning services</a></li>' % (h, esc(l))
                       for h, l in STATES)
    return """<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        %s
        <p>Premium home and office cleaning serving 100+ communities across Utah, Arizona, Nevada, and Texas. Background-checked teams, consistent quality, every visit.</p>
        <a class="footer-google" href="%s" target="_blank" rel="noopener">
          <span class="stars" aria-hidden="true">%s</span> %s out of 5 on Google &middot; %s reviews
        </a>
        <ul class="footer-contact">
          <li><span class="fc-k">Phone</span><a href="tel:%s">%s</a></li>
          <li><span class="fc-k">Email</span><a href="mailto:%s">%s</a></li>
          <li><span class="fc-k">Office</span><address>%s<br>%s, %s %s</address></li>
        </ul>
        <a class="footer-review" href="%s">Leave us a review</a>
      </div>
      <div class="footer-col">
        <h3>Home Cleaning</h3>
        <ul>
%s
        </ul>
      </div>
      <div class="footer-col">
        <h3>Commercial Cleaning</h3>
        <ul>
%s
          <li><a href="/commercial/">All Commercial Services</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>Company</h3>
        <ul>
%s
          <li><a href="/locations/">All Service Areas</a></li>
          <li><a href="/about/">About Salt &amp; Slate</a></li>
          <li><a href="/#reviews">Customer Reviews</a></li>
          <li><a href="%s">Leave us a review</a></li>
          <li><a href="#quote">%s</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-areas">
      <h3>Offices</h3>
      <p>Salt Lake City, UT &middot; Park City, UT &middot; Draper, UT &middot; Scottsdale, AZ &middot; Las Vegas, NV &middot; Frisco, TX</p>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 %s</span>
      <nav aria-label="Footer links">
        <a href="%s">Leave us a review</a>
        <a href="%s" target="_blank" rel="noopener">Reviews on Google</a>
        <a href="#quote">%s</a>
      </nav>
    </div>
  </div>
</footer>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
""" % (
        _brand(), GOOGLE_URL, STARS, RATING, REVIEW_COUNT,
        PHONE_TEL, esc(PHONE), EMAIL, EMAIL,
        esc(ADDR_STREET), esc(ADDR_CITY), ADDR_REGION, ADDR_ZIP,
        REVIEW_URL, res, com, states, REVIEW_URL, esc(CTA_LABEL),
        esc(BRAND), REVIEW_URL, GOOGLE_URL, esc(CTA_LABEL),
    )
