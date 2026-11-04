"""Build the home page."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import home_data as D
from blocks_ui import cta_band, picker_section, quote_section
from sitelib import (ADDR_CITY, ADDR_REGION, ADDR_STREET, ADDR_ZIP, BRAND, CTA_LABEL,
                     EMAIL, GOOGLE_URL, PHONE, PHONE_TEL, RATING, REVIEW_COUNT, REVIEW_URL,
                     STARS, esc, footer, gproof, head, header)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLE = "House & Office Cleaning in Utah, Arizona, Nevada & Texas | Salt & Slate Cleaning"
DESC = ("Licensed, insured and background-checked house and commercial cleaning across Utah, "
        "Arizona, Nevada and Texas. Flat-rate pricing, 24-hour satisfaction guarantee. "
        "Rated 5.0 on Google. Call (725) 777-1406.")


def jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "HouseCleaningService"],
        "name": BRAND,
        "description": ("Premium residential and commercial cleaning serving 100+ communities "
                        "across Utah, Arizona, Nevada and Texas."),
        "telephone": PHONE,
        "email": EMAIL,
        "url": "/",
        "image": "/images/source/00-hero-home.jpg",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": ADDR_STREET,
            "addressLocality": ADDR_CITY,
            "addressRegion": ADDR_REGION,
            "postalCode": ADDR_ZIP,
            "addressCountry": "US",
        },
        "areaServed": [{"@type": "State", "name": n} for n in
                       ("Utah", "Arizona", "Nevada", "Texas")],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": RATING,
            "reviewCount": REVIEW_COUNT,
            "bestRating": "5",
        },
        "sameAs": [GOOGLE_URL],
    }
    return '<script type="application/ld+json">%s</script>\n' % json.dumps(data)


def hero():
    return """<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">Utah &middot; Arizona &middot; Nevada &middot; Texas</span>
      <h1>Professional house &amp; office cleaning for homes and businesses that expect more</h1>
      <p class="lede">Licensed, insured, background-checked professionals serving 100+ communities
        across Utah, Arizona, Nevada and Texas &mdash; with flat-rate pricing and a 24-hour
        satisfaction guarantee on every cleaning.</p>
      <div class="cta-row">
        <a class="btn btn-primary" href="#quote">%s</a>
        <a class="btn btn-ghost" href="tel:%s">Call %s</a>
      </div>
      <div class="hero-proof">
        %s
      </div>
    </div>
    <div class="hero-media">
      <picture>
        <source type="image/webp" srcset="/images/source/01-hero-home.webp">
        <img src="/images/source/00-hero-home.jpg" width="1456" height="816"
             alt="Living room with a white sectional, wood beams and herringbone fireplace, freshly cleaned by Salt &amp; Slate"
             fetchpriority="high" decoding="async">
      </picture>
      <div class="hero-badge">
        <strong>24&#8209;hour</strong>
        <span>Satisfaction guarantee &mdash; if anything falls short we return at no charge.</span>
      </div>
    </div>
  </div>
</section>
""" % (esc(CTA_LABEL), PHONE_TEL, esc(PHONE), gproof())


def trust():
    items = "\n".join("      <li><strong>%s</strong><span>%s</span></li>" % (esc(a), esc(b))
                      for a, b in D.TRUST)
    return """<section class="trust">
  <div class="wrap">
    <ul class="trust-list">
%s
    </ul>
  </div>
</section>
""" % items


def residential():
    rows = []
    for i, (href, name, outcome, body, webp, jpg, alt, w, h) in enumerate(D.FEATURE_SERVICES):
        rows.append("""    <div class="erow">
      <div>
        <span class="erow-num">%s</span>
        <h3>%s</h3>
        <p>%s</p>
        <a class="arrow-link" href="%s">Explore %s</a>
      </div>
      <div class="erow-media">
        <picture>
          <source type="image/webp" srcset="%s">
          <img src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async">
        </picture>
      </div>
    </div>""" % (esc(outcome), esc(name), esc(body), href, esc(name.lower()),
                 webp, jpg, w, h, esc(alt)))

    extra = "\n".join(
        '      <li><a href="%s"><span class="lr-t">%s</span><span class="lr-d">%s</span>'
        '<span class="lr-go" aria-hidden="true">&rarr;</span></a></li>'
        % (href, esc(name), esc(desc)) for href, name, desc in D.LIST_SERVICES)

    return """<section class="sect sect-paper" id="services">
  <div class="wrap">
    <div class="sect-head">
      <span class="eyebrow">Residential</span>
      <h2>Cleaning services for your home</h2>
      <p class="lede">Nine distinct services designed around the way you actually live &mdash; from
        weekly maintenance to post-construction cleanup.</p>
    </div>
%s
    <ul class="listrows" style="margin-top:46px">
%s
    </ul>
    <div class="cta-row" style="margin-top:40px">
      <a class="btn btn-primary" href="#quote">%s</a>
      <a class="btn btn-ghost" href="/services/">All residential services</a>
    </div>
  </div>
</section>
""" % ("\n".join(rows), extra, esc(CTA_LABEL))


def commercial():
    cards = "\n".join(
        '      <a class="card is-link" href="%s"><h3>%s</h3><p>%s</p>'
        '<span class="card-go">Learn more</span></a>' % (href, esc(name), esc(desc))
        for href, name, desc in D.COMMERCIAL_CARDS)
    more = "\n".join('        <li><span class="pill is-static">%s</span></li>' % esc(x)
                     for x in D.COMMERCIAL_MORE)
    return """<section class="sect" id="commercial">
  <div class="wrap">
    <div class="sect-head">
      <span class="eyebrow">Commercial</span>
      <h2>Cleaning for your business</h2>
      <p class="lede">Industry-specific cleaning protocols for offices, medical facilities,
        restaurants, gyms, and more. Detailed checklists, after-hours scheduling, and
        commercial-grade products tailored to how your business operates.</p>
    </div>
    <div class="cards cards-4">
%s
    </div>
    <h3 style="margin:42px 0 14px;font-size:1.05rem">Also serving these industries</h3>
    <ul class="pill-row">
%s
    </ul>
    <div class="cta-row" style="margin-top:36px">
      <a class="btn btn-primary" href="#quote">Request a commercial quote</a>
      <a class="btn btn-ghost" href="/commercial/">All 15 industries</a>
    </div>
  </div>
</section>
""" % (cards, more)


def why():
    cells = "\n".join("        <div><h3>%s</h3><p>%s</p></div>" % (esc(t), esc(b))
                      for t, b in D.WHY)
    return """<section class="sect sect-deep">
  <div class="wrap">
    <div class="erow" style="border-top:0;padding-top:0">
      <div>
        <span class="eyebrow">Why Salt &amp; Slate</span>
        <h2>What sets us apart</h2>
        <p class="lede">Background-checked teams, one documented standard, and a guarantee that
          means something.</p>
        <a class="arrow-link" href="/about/">Learn about us</a>
      </div>
      <div class="erow-media">
        <img src="/images/source/12-why-salt-and-slate.jpg" width="1500" height="1000"
             alt="Salt &amp; Slate cleaning professional at work in a luxury kitchen"
             loading="lazy" decoding="async">
      </div>
    </div>
    <div class="feat feat-2" style="margin-top:40px">
%s
    </div>
  </div>
</section>
""" % cells


def before_after():
    items = []
    for key, cap, sub, bw, bj, balt, aw, aj, aalt, w, h in D.BEFORE_AFTER:
        items.append("""      <div class="ba-item">
        <div class="ba">
          <picture>
            <source type="image/webp" srcset="%s">
            <img class="ba-after" src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async">
          </picture>
          <picture>
            <source type="image/webp" srcset="%s">
            <img class="ba-before" src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async">
          </picture>
          <span class="ba-tag is-before">Before</span>
          <span class="ba-tag is-after">After</span>
          <span class="ba-handle" aria-hidden="true"></span>
          <input type="range" min="0" max="100" value="50" step="1"
                 aria-label="Reveal the before and after of this %s">
        </div>
        <p class="ba-cap">%s<span>%s</span></p>
      </div>""" % (aw, aj, w, h, esc(aalt), bw, bj, w, h, esc(balt),
                   esc(cap.lower()), esc(cap), esc(sub)))

    show = "\n".join("""      <figure>
        <img src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async">
        <figcaption>%s</figcaption>
      </figure>""" % (src, w, h, esc(alt), esc(cap)) for src, alt, cap, w, h in D.SHOWCASE)

    return """<section class="sect sect-paper" id="work">
  <div class="wrap">
    <div class="sect-head">
      <span class="eyebrow">Before &amp; After</span>
      <h2>Real cleanings, real customers</h2>
      <p>Drag each slider to see the difference. Every photo is from a Salt &amp; Slate job.</p>
    </div>
    <div class="ba-grid">
%s
    </div>
    <div class="showcase">
%s
    </div>
  </div>
</section>
""" % ("\n".join(items), show)


def recognized():
    cells = "\n".join("      <div><h3>%s</h3><p>%s</p></div>" % (esc(t), esc(b))
                      for t, b in D.RECOGNIZED)
    return """<section class="sect">
  <div class="wrap">
    <div class="sect-head">
      <span class="eyebrow">Recognized By</span>
      <h2>Trusted with the events and estates that demand discretion</h2>
    </div>
    <div class="recog">
%s
    </div>
    <p class="recog-note">%s</p>
  </div>
</section>
""" % (cells, esc(D.RECOGNIZED_NOTE))


def reviews():
    def card(quote, who, meta, featured):
        return """      <figure class="review%s">
        <span class="stars" aria-hidden="true">%s</span>
        <blockquote>&ldquo;%s&rdquo;</blockquote>
        <figcaption><b>%s</b>%s</figcaption>
      </figure>""" % (" is-featured" if featured else "", STARS, esc(quote), esc(who), esc(meta))

    cards = [card(q, w, m, True) for q, w, m in D.FEATURED_REVIEWS]
    cards += [card(q, w, m, False) for q, w, m in D.MORE_REVIEWS]

    return """<section class="sect sect-deep" id="reviews">
  <div class="wrap">
    <div class="sect-head">
      <span class="eyebrow">Verified Google Reviews</span>
      <h2>What our clients are saying</h2>
      <p class="lede">Rated <strong>%s out of 5</strong> from <strong>%s Google reviews</strong>.
        Every review below was left on Google by a Salt &amp; Slate customer.</p>
    </div>
    <div class="reviews">
%s
    </div>
    <div class="review-foot">
      <a class="review-link" href="%s">Leave us a review</a>
      <a class="gproof" href="%s" target="_blank" rel="noopener">
        <span class="stars" aria-hidden="true">%s</span>
        <span><b>%s</b> from %s reviews</span>
        <span class="gproof-cta">Read our reviews on Google</span>
      </a>
    </div>
  </div>
</section>
""" % (RATING, REVIEW_COUNT, "\n".join(cards), REVIEW_URL, GOOGLE_URL, STARS, RATING, REVIEW_COUNT)


def areas():
    cards = []
    for href, name, cities, more in D.AREAS:
        cards.append("""      <a class="loc" href="%s">
        <h3>%s</h3>
        <p>%s</p>
        <span class="loc-go">%s</span>
      </a>""" % (href, esc(name), esc(cities), esc(more or "View service area")))
    return """<section class="sect sect-paper" id="areas">
  <div class="wrap">
    <div class="sect-head">
      <span class="eyebrow">Where We Serve</span>
      <h2>Service areas across four states</h2>
      <p>Residential and commercial cleaning across 106 cities. Our Las Vegas office is at
        3930 University Center Dr #807, Las Vegas, NV 89119.</p>
    </div>
    <div class="locgrid">
%s
    </div>
    <p style="margin-top:28px"><a class="arrow-link" href="/locations/">View all service areas</a></p>
  </div>
</section>
""" % "\n".join(cards)


def how():
    lis = "\n".join('      <li><span class="step-n">%s</span><h3>%s</h3><p>%s</p></li>'
                    % (esc(n), esc(t), esc(b)) for n, t, b in D.STEPS)
    return """<section class="sect">
  <div class="wrap">
    <div class="sect-head">
      <span class="eyebrow">How It Works</span>
      <h2>Three steps to a cleaner space</h2>
    </div>
    <ol class="steps">
%s
    </ol>
  </div>
</section>
""" % lis


def build():
    parts = [
        head(TITLE, DESC, "/", hero_preload="/images/source/00-hero-home.jpg"),
        header(),
        '<main id="main">\n',
        hero(), trust(), picker_section(), residential(), commercial(), why(),
        before_after(), recognized(), reviews(), areas(), how(),
        cta_band("Your property. Our standard.",
                 "Background-checked teams, flat-rate pricing and a 24-hour satisfaction "
                 "guarantee. Serving homes and businesses across Utah, Arizona, Nevada and Texas."),
        quote_section(form_name="Quote request",
                      heading="Request your free quote",
                      lede="Tell us about your home or facility and we'll send flat-rate pricing "
                           "so you know the full cost upfront."),
        "</main>\n",
        footer().replace("</body>", jsonld() + "</body>"),
    ]
    dest = os.path.join(ROOT, "index.html")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write("".join(parts))
    print("built / ->", dest)


if __name__ == "__main__":
    build()
