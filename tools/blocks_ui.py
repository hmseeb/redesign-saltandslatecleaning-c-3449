"""Reusable UI sections: the quote form, contact facts and the picker."""
from sitelib import (ADDR_CITY, ADDR_ONE_LINE, BRAND_SHORT, CTA_LABEL, EMAIL,
                     FORM_ACTION, GOOGLE_URL, PHONE, PHONE_TEL, RATING,
                     REVIEW_COUNT, REVIEW_URL, STARS, esc)

SERVICE_OPTIONS = [
    "Standard & Recurring Cleaning",
    "Deep Cleaning",
    "Move-In Cleaning",
    "Move-Out Cleaning",
    "Vacation Home Cleaning",
    "Airbnb & Rental Cleaning",
    "Estate Cleaning",
    "Specialty Cleaning",
    "Post-Construction Cleaning",
    "Commercial / Office Cleaning",
    "Not sure yet",
]


def quote_section(form_name="Quote request", heading=None, lede=None, preselect=None):
    """The site's one conversion form. Works without JavaScript."""
    heading = heading or "Your property. Our standard."
    lede = lede or ("Background-checked teams, flat-rate pricing and a 24-hour satisfaction "
                    "guarantee. Tell us about your space and we'll send you a quote.")
    opts = ['            <option value="">Select a service</option>']
    for s in SERVICE_OPTIONS:
        sel = " selected" if preselect and preselect == s else ""
        opts.append('            <option value="%s"%s>%s</option>' % (esc(s), sel, esc(s)))
    options = "\n".join(opts)

    return """<section class="sect sect-dark quote" id="quote">
  <div class="wrap quote-grid">
    <div>
      <span class="eyebrow">Request a quote</span>
      <h2>%s</h2>
      <p class="lede">%s</p>
      <ul class="quote-facts">
        <li><span class="qf-k">Call</span><span class="qf-v"><a href="tel:%s">%s</a></span></li>
        <li><span class="qf-k">Email</span><span class="qf-v"><a href="mailto:%s">%s</a></span></li>
        <li><span class="qf-k">Office</span><span class="qf-v">%s</span></li>
        <li><span class="qf-k">Areas</span><span class="qf-v">Utah, Arizona, Nevada &amp; Texas &mdash; 100+ communities</span></li>
        <li><span class="qf-k">Google</span><span class="qf-v"><a href="%s" target="_blank" rel="noopener"><span aria-hidden="true">%s</span> %s from %s reviews &mdash; read our reviews on Google</a></span></li>
        <li><span class="qf-k">Reviews</span><span class="qf-v"><a href="%s">Leave us a review</a></span></li>
      </ul>
    </div>

    <div class="form-card">
      <div class="form-ok" role="status" data-show="false">
        <span aria-hidden="true">✓</span>
        <div>
          <strong>Thanks, your message was sent</strong>
          <p>A %s team member will be in touch shortly. Need us sooner? Call <a href="tel:%s">%s</a>.</p>
        </div>
      </div>

      <div class="form-head">
        <h3>%s</h3>
        <p>No obligation. Flat-rate pricing so you know the full cost upfront.</p>
      </div>

      <form method="POST" action="%s" data-leadr>
        <input type="hidden" name="_form" value="%s">
        <input type="hidden" name="_page" value="">
        <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" style="display:none">

        <div class="form-grid cols-2">
          <div class="field">
            <label for="f-name">Your name <span class="req" aria-hidden="true">*</span></label>
            <input id="f-name" name="name" type="text" autocomplete="name" required>
          </div>
          <div class="field">
            <label for="f-phone">Phone <span class="req" aria-hidden="true">*</span></label>
            <input id="f-phone" name="phone" type="tel" autocomplete="tel" required>
          </div>
          <div class="field">
            <label for="f-email">Email <span class="req" aria-hidden="true">*</span></label>
            <input id="f-email" name="email" type="email" autocomplete="email" required>
          </div>
          <div class="field">
            <label for="f-city">City</label>
            <input id="f-city" name="City" type="text" autocomplete="address-level2" placeholder="%s">
          </div>
        </div>

        <div class="form-grid" style="margin-top:18px">
          <div class="field">
            <label for="f-service">Service needed</label>
            <select id="f-service" name="Service needed">
%s
            </select>
          </div>
          <div class="field">
            <label for="f-date">Preferred date</label>
            <input id="f-date" name="Preferred date" type="date">
          </div>
          <div class="field">
            <label for="f-details">What do you need cleaned?</label>
            <textarea id="f-details" name="Details" rows="4" placeholder="Square footage, bedrooms and bathrooms, pets, anything needing extra attention."></textarea>
            <span class="hint">The more detail you give us, the more accurate your flat rate.</span>
          </div>
        </div>

        <div class="form-foot">
          <button class="btn btn-primary" type="submit">%s</button>
          <p class="form-note">Prefer to talk it through? Call <a href="tel:%s">%s</a>.</p>
        </div>
      </form>
    </div>
  </div>
</section>
""" % (
        esc(heading), esc(lede),
        PHONE_TEL, esc(PHONE), EMAIL, EMAIL, esc(ADDR_ONE_LINE),
        GOOGLE_URL, STARS, RATING, REVIEW_COUNT, REVIEW_URL,
        esc(BRAND_SHORT), PHONE_TEL, esc(PHONE),
        esc("Request your free quote"),
        FORM_ACTION, esc(form_name), esc(ADDR_CITY), options,
        esc(CTA_LABEL), PHONE_TEL, esc(PHONE),
    )


PICKER = [
    ("Keep my home consistently clean",
     "Regular visits once your home is at maintenance condition.",
     "Recurring cleaning", "/services/recurring-cleaning/"),
    ("Catch up on buildup",
     "More detail on baseboards, cabinet fronts, doors and shower tile grout.",
     "Deep cleaning", "/services/deep-cleaning/"),
    ("Get ready to move",
     "Empty cabinets, refrigerator and oven interiors, kitchens, bathrooms and floors.",
     "Move-out cleaning", "/services/move-out-cleaning/"),
    ("Prepare for the next guest",
     "Cleaning between bookings, with linen and access needs agreed in advance.",
     "Airbnb turnover cleaning", "/services/airbnb-cleaning/"),
    ("Clean my workplace",
     "A scope and schedule built around your workspace and business hours.",
     "Office cleaning", "/commercial/office-cleaning/"),
    ("Finish a build or remodel",
     "A final clean for construction dust after the trades have finished.",
     "Post-construction cleaning", "/services/post-construction-cleaning/"),
]


def picker_html():
    items = []
    for q, d, a, href in PICKER:
        items.append("""      <a class="picker-item" href="%s">
        <span class="pk-q">%s</span>
        <span class="pk-d">%s</span>
        <span class="pk-a">%s</span>
      </a>""" % (href, esc(q), esc(d), esc(a)))
    return """    <div class="picker">
%s
    </div>
    <p class="inline-note">Moving in? <a href="/services/move-in-cleaning/">See move-in cleaning</a>. Maintaining a second home? <a href="/services/vacation-home-cleaning/">Explore vacation-home care</a>.</p>
""" % "\n".join(items)


def picker_section():
    return """<section class="sect sect-paper">
  <div class="wrap">
    <div class="sect-head">
      <span class="eyebrow">Find your clean</span>
      <h2>What would you like help with?</h2>
      <p>Choose what fits your space. See the checklist, compare the options and request a quote.</p>
    </div>
%s  </div>
</section>
""" % picker_html()


def cta_band(heading, lede, eyebrow="Ready when you are"):
    return """<section class="sect-tight sect-dark finalcta">
  <div class="wrap">
    <span class="eyebrow">%s</span>
    <h2>%s</h2>
    <p class="lede">%s</p>
    <div class="cta-row">
      <a class="btn btn-primary" href="#quote">%s</a>
      <a class="btn btn-ghost" href="tel:%s">Call %s</a>
    </div>
  </div>
</section>
""" % (esc(eyebrow), esc(heading), esc(lede), esc(CTA_LABEL), PHONE_TEL, esc(PHONE))
