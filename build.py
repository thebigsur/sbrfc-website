#!/usr/bin/env python3
"""Builds the static sbrfc.com site.

Every page is written as plain HTML with the shared header and footer baked
in, so the site works with scripting disabled. This file is the source of
truth: edit the content here and re-run `python3 build.py`, never the
generated .html files. It also writes sitemap.xml.

Quick edits:
  * Youth "Upcoming" box ............ YOUTH_UPCOMING
  * Google Analytics / Google Ads ... GA4_ID, ADS_ID, ADS_CLUB_CLICK
  * Club contacts and links ......... the CLUB CONTACTS block
"""
import os, re

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://sbrfc.com"

LEGAL_NAME = "Santa Barbara Rugby Football Club"
EIN = "93-4659131"
ADDRESS = "2516 Mesa School Lane, Santa&nbsp;Barbara, CA&nbsp;93109"
GENERAL_EMAIL = "vicepresident@sbrfc.com"
TREASURER = "treasurer@sbrfc.com"
DONATE_URL = "https://www.zeffy.com/en-US/donation-form/sbrfc"
MISSION_SENTENCE = ("The mission of the Santa&nbsp;Barbara Rugby Football Club is to promote the sport of rugby "
                    "in our community by fostering athletic excellence, inclusivity, and personal development "
                    "through teamwork, discipline, and sportsmanship.")

# ---------------------------------------------------------------------------
# TRACKING. One Google tag (gtag.js) is written into the <head> of every page.
# GA4_ID is the sbrfc.com Google Analytics property (admin@sbrfc.com).
# Set it to "" to remove Google Analytics from every page.
GA4_ID = "G-9RX9PHGCST"
# Google Ads (Ad Grants) tag, and the conversion fired when someone clicks
# through to a club website (the conversion /landing used to fire).
ADS_ID = "AW-18473978317"
ADS_CLUB_CLICK = "AW-18473978317/GDv2CLv6sI4dEM2TiulE"
# ---------------------------------------------------------------------------

# Bump when styles.css or site.js change, so browsers fetch the new copy.
ASSET_V = "20261003"
# Sitemap lastmod and the privacy policy's "last updated" date.
RELEASE_DATE = "2026-10-03"
PRIVACY_UPDATED = "3 October 2026"

# ---------------------------------------------------------------------------
# CLUB CONTACTS
GRUNION_URL = "https://grunionrugby.com/"
MERMAIDS_URL = "https://www.sbwomensrugby.com/"
STINGRAYS_URL = "https://stingraysrfc.com/"
STINGRAYS_REGISTER = "https://rugby-register.vercel.app/stingrays"
GRUNION_COACH_JOB = "https://grunionrugby.com/coach"
CLUB78_URL = "https://grunionrugby.com/the-78-club"
GRUNION_EMAIL = "grunionrugby@gmail.com"
MERMAIDS_EMAIL = "santabarbararugby@gmail.com"
STINGRAYS_EMAIL = "club@stingraysrfc.com"
JORDAN = "(805)&nbsp;618-6510"
JORDAN_SMS = "sms:+18056186510"
JORDAN_TEL = "tel:+18056186510"
REFERRAL = "?utm_source=sbrfc&amp;utm_medium=referral&amp;utm_campaign=play-rugby"
ELINGS_MAP = "https://www.google.com/maps/search/?api=1&amp;query=Elings+Park%2C+1298+Las+Positas+Rd%2C+Santa+Barbara%2C+CA+93105"
CHASE_MAP = "https://www.google.com/maps/search/?api=1&amp;query=Chase+Palm+Park%2C+323+E+Cabrillo+Blvd%2C+Santa+Barbara%2C+CA"

# ---------------------------------------------------------------------------
# YOUTH "UPCOMING" BOX, shown on /youth and /thanks-youth.
# One line per item: (hide after this date, what, when and where).
# An item disappears on its own the day after its date. Delete a line to
# remove it, add a line to add one, then run: python3 build.py
YOUTH_UPCOMING = [
    ("2026-10-30", "Halloween Kick-Off", "Fri Oct 30, 4–7 PM, Elings Park"),
    ("2026-12-03", "Pre-season", "Nov 3–Dec 3, Tue/Thu 4–5:15 PM, Chase Palm Park"),
    ("2027-03-04", "Elings Park training from Dec 8", "U8–U10 4–5 PM, U12–U14 4:30–6 PM, U16 TBC"),
    ("2027-03-06", "Season", "About Jan 16–Mar 6, 2027"),
]

NAV = [
    ("/play",    "Play Rugby"),
    ("/mens",    "Men's"),
    ("/womens",  "Women's"),
    ("/youth",   "Youth"),
    ("/sponsor", "Sponsor"),
    ("/coach",   "Coach"),
    ("/about",   "About"),
]

# Photos in images/photos/: name -> (width/height ratio, widths available)
PHOTOS = {
    "mens":        (5 / 4, [640, 1100]),
    "womens":      (5 / 4, [640, 1100]),
    "youth":       (5 / 4, [640, 1100]),
    "coach":       (5 / 4, [640, 800]),
    "sponsor":     (5 / 4, [640, 800]),
    "card-mens":   (16 / 10, [400, 670]),
    "card-womens": (16 / 10, [400, 800]),
    "card-youth":  (16 / 10, [400, 800]),
}

SITEMAP = []   # filled by page()

# ===========================================================================
# TEMPLATE
# ===========================================================================

def header(active):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    links.append(f'<a class="nav-donate" href="{DONATE_URL}" target="_blank" rel="noopener noreferrer">Donate</a>')
    nav = "\n        ".join(links)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="/">
      <picture>
        <source srcset="/images/sbrfc-mark.webp" type="image/webp">
        <img src="/images/sbrfc-mark.png" alt="" width="96" height="110">
      </picture>
      <span class="brand-text">
        <span class="brand-name">SBRFC</span>
        <span class="brand-sub">Santa Barbara Rugby</span>
      </span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="site-nav" id="site-nav" aria-label="Main">
        {nav}
    </nav>
  </div>
</header>'''


def footer():
    return f'''<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <h2>Santa Barbara Rugby Football Club</h2>
      <p class="footer-mission">{MISSION_SENTENCE}</p>
      <p class="footer-status">501(c)(3) nonprofit &middot; EIN {EIN}</p>
      <p>{ADDRESS}<br>
      <a href="mailto:{GENERAL_EMAIL}">{GENERAL_EMAIL}</a></p>
    </div>
    <div>
      <h2>Play</h2>
      <ul>
        <li><a href="/play">Play rugby</a></li>
        <li><a href="/mens">Men's rugby</a></li>
        <li><a href="/womens">Women's rugby</a></li>
        <li><a href="/youth">Youth rugby</a></li>
        <li><a href="/coach">Coach or volunteer</a></li>
      </ul>
    </div>
    <div>
      <h2>The Club</h2>
      <ul>
        <li><a href="/about">About SBRFC</a></li>
        <li><a href="/news">News &amp; events</a></li>
        <li><a href="/support">Get involved</a></li>
        <li><a href="/sponsor">Sponsor</a></li>
        <li><a href="/contact">Contact</a></li>
        <li><a href="{DONATE_URL}" target="_blank" rel="noopener noreferrer">Donate</a></li>
        <li><a href="/privacy">Privacy policy</a></li>
      </ul>
    </div>
    <div>
      <h2>Clubs We Support</h2>
      <ul>
        <li><a href="{GRUNION_URL}" rel="noopener">Grunion RFC</a>, men's</li>
        <li><a href="{MERMAIDS_URL}" rel="noopener">Santa Barbara Mermaids</a>, women's</li>
        <li><a href="{STINGRAYS_URL}" rel="noopener">Santa Barbara Stingrays</a>, youth</li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-legal">
    &copy; 2026 {LEGAL_NAME} &middot; 501(c)(3) nonprofit &middot; EIN {EIN} &middot; Donations are tax-deductible to the extent allowed by law. &middot; <a href="/privacy">Privacy policy</a>
  </div>
</footer>'''


def analytics():
    """The Google tag, once per page. Empty if both IDs are blank."""
    first = GA4_ID or ADS_ID
    if not first:
        return ""
    cfg = ""
    if GA4_ID:
        cfg += f"gtag('config','{GA4_ID}');"
    if ADS_ID:
        cfg += f"gtag('config','{ADS_ID}');"
        if ADS_CLUB_CLICK:
            cfg += f"window.sbrfcClubConversion='{ADS_CLUB_CLICK}';"
    return f'''<script async src="https://www.googletagmanager.com/gtag/js?id={first}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('js',new Date());{cfg}</script>'''


def page(slug, title, description, body, active=None, noindex=False, og=None,
         body_attrs="", head_extra="", sitemap_priority=None):
    path = "/" if slug == "index" else "/" + slug
    canonical = SITE + path
    robots = '\n<meta name="robots" content="noindex">' if noindex else ""
    if og:
        og_tags = (f'<meta property="og:image" content="{SITE}/images/og/{og}">\n'
                   '<meta property="og:image:width" content="1200">\n'
                   '<meta property="og:image:height" content="630">\n'
                   '<meta name="twitter:card" content="summary_large_image">')
    else:
        og_tags = f'<meta property="og:image" content="{SITE}/images/sbrfc-logo.png">'
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">{robots}
<meta name="theme-color" content="#1C2B4B">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="/favicon.ico" sizes="48x48 32x32 16x16">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/vollkorn-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/styles.css?v={ASSET_V}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Santa Barbara Rugby Football Club">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
{og_tags}
{head_extra}{analytics()}
<script src="/site.js?v={ASSET_V}" defer></script>
</head>
<body{body_attrs}>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''
    # Keep times together on one line: "4&nbsp;PM", never "4" at the end of a line.
    doc = re.sub(r"(\d) (AM|PM)\b", "\\1&nbsp;\\2", doc)
    out = os.path.join(OUT, slug + ".html")
    with open(out, "w") as f:
        f.write(doc)
    if not noindex and sitemap_priority:
        SITEMAP.append((path, sitemap_priority))
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    print(f"{slug + '.html':24s} {words:5d} words{'  (noindex)' if noindex else ''}")


def photo(name, alt, sizes, eager=False, cls="lp-photo"):
    ratio, widths = PHOTOS[name]
    big = widths[-1]
    h = round(big / ratio)
    webp = ", ".join(f"/images/photos/{name}-{w}.webp {w}w" for w in widths)
    jpg = ", ".join(f"/images/photos/{name}-{w}.jpg {w}w" for w in widths)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'''<figure class="{cls}">
  <picture>
    <source type="image/webp" srcset="{webp}" sizes="{sizes}">
    <img src="/images/photos/{name}-{widths[0]}.jpg" srcset="{jpg}" sizes="{sizes}" width="{big}" height="{h}" alt="{alt}" {load}>
  </picture>
</figure>'''


HERO_SIZES = "(min-width: 1060px) 470px, (min-width: 901px) 44vw, calc(100vw - 48px)"
CARD_SIZES = "(min-width: 1060px) 337px, (min-width: 861px) 31vw, calc(100vw - 48px)"


def ext(url, label, cls="btn btn-secondary"):
    """A button to another website, opened in a new tab."""
    return f'<a class="{cls}" href="{url}" target="_blank" rel="noopener">{label}</a>'


# ---------------------------------------------------------------------------
# FORMS (Netlify Forms). Each form posts to its own thank-you page, which is
# the conversion signal for Google Ads and Analytics. The four player forms
# share identical field names so /play can route a sign-up to any of them.
# ---------------------------------------------------------------------------

def hidden_tracking():
    return '''<input type="hidden" name="utm_source" value="">
  <input type="hidden" name="utm_medium" value="">
  <input type="hidden" name="utm_campaign" value="">
  <input type="hidden" name="gclid" value="">
  <input type="hidden" name="landing_page" value="">'''


def honeypot():
    return ('<p class="hp" aria-hidden="true"><label>Leave this empty: '
            '<input name="bot-field" tabindex="-1" autocomplete="off"></label></p>')


def form_open(name, action, extra=""):
    return f'''<form class="lp-form" name="{name}" method="POST" action="{action}" data-netlify="true" netlify-honeypot="bot-field"{extra}>
  <input type="hidden" name="form-name" value="{name}">
  {honeypot()}
  {hidden_tracking()}'''


def field(fid, name, label, kind="text", required=False, optional=False, auto="", extra=""):
    opt = ' <span class="opt">(optional)</span>' if optional else ""
    req = " required" if required else ""
    ac = f' autocomplete="{auto}"' if auto else ""
    if kind == "textarea":
        ctl = f'<textarea id="{fid}" name="{name}" rows="3"{req}{extra}></textarea>'
    else:
        ctl = f'<input id="{fid}" name="{name}" type="{kind}"{ac}{req}{extra}>'
    return f'<div class="field"><label for="{fid}">{label}{opt}</label>{ctl}</div>'


def select(fid, name, label, options, required=False, placeholder="Pick one", label_attr="", wrap_attr=""):
    req = " required" if required else ""
    opts = f'<option value="">{placeholder}</option>' + "".join(
        f'<option value="{v}">{t}</option>' if v != t else f'<option>{t}</option>' for v, t in options)
    return (f'<div class="field"{wrap_attr}><label for="{fid}"{label_attr}>{label}</label>'
            f'<select id="{fid}" name="{name}"{req}>{opts}</select></div>')


EXPERIENCE = [("Never played", "Never played"), ("A little", "A little"), ("Played before", "Played before")]
AGES = [(str(a), str(a)) for a in range(5, 19)]
PRIVACY_NOTE = ('<p class="form-note">Your details are shared only with the club organizers who need them. '
                '<a href="/privacy">Privacy policy</a></p>')


def player_form(prefix, form_name, action, team, title, intro, button="Sign up"):
    """mens-interest, womens-interest, youth-interest: identical field names."""
    youth = team == "youth"
    name_label = "Parent/guardian name" if youth else "Your name"
    exp_label = "Has your child played before?" if youth else "Have you played rugby?"
    age = (select(f"{prefix}-age", "child_age", "Child's age", AGES, required=True, placeholder="Pick an age")
           if youth else '<input type="hidden" name="child_age" value="">')
    return f'''<div class="form-card" id="signup">
<h2>{title}</h2>
<p class="form-intro">{intro}</p>
{form_open(form_name, action)}
  <input type="hidden" name="team" value="{team}">
  {field(prefix + "-name", "name", name_label, required=True, auto="name")}
  {field(prefix + "-email", "email", "Email", kind="email", required=True, auto="email")}
  {field(prefix + "-phone", "phone", "Phone", kind="tel", optional=True, auto="tel")}
  {age}
  {select(prefix + "-experience", "experience", exp_label, EXPERIENCE)}
  {field(prefix + "-message", "message", "Message", kind="textarea", optional=True)}
  <button class="btn btn-primary" type="submit">{button}</button>
  {PRIVACY_NOTE}
</form>
</div>'''


def play_form():
    """general-interest. site.js swaps form-name and action from the team choice."""
    teams = [("mens", "Men's (Grunion)"), ("womens", "Women's (Mermaids)"),
             ("youth", "Youth (I'm a parent)"), ("general", "Not sure")]
    return f'''<div class="form-card" id="signup">
<h2>Sign up to play</h2>
<p class="form-intro">Pick a team and your details go straight to that club's organizers. Not sure which fits? Choose &ldquo;Not sure&rdquo; and SBRFC's volunteers will get your message.</p>
{form_open("general-interest", "/thanks-play", ' data-route')}
  {select("play-team", "team", "Which team?", teams, required=True, placeholder="Choose a team")}
  <div class="field"><label for="play-name" data-label-name>Your name</label><input id="play-name" name="name" type="text" autocomplete="name" required></div>
  {field("play-email", "email", "Email", kind="email", required=True, auto="email")}
  {field("play-phone", "phone", "Phone", kind="tel", optional=True, auto="tel")}
  {select("play-age", "child_age", "Child's age (parents only)", AGES, placeholder="Pick an age", wrap_attr=' data-youth-only')}
  {select("play-experience", "experience", "Have you played rugby?", EXPERIENCE, label_attr=' data-label-experience')}
  {field("play-message", "message", "Message", kind="textarea", optional=True)}
  <button class="btn btn-primary" type="submit">Sign up</button>
  {PRIVACY_NOTE}
</form>
</div>'''


def sponsor_form():
    interests = [(t, t) for t in ("Front of shirt", "Kit partner", "Beer &amp; social",
                                  "Youth program", "Mermaids (women's team)", "Not sure")]
    return f'''<div class="form-card" id="signup">
<h2>Ask about sponsoring</h2>
<p class="form-intro">Tell us about your business and what you have in mind. Your inquiry goes to the SBRFC treasurer.</p>
{form_open("sponsor-inquiry", "/thanks-sponsor")}
  {field("sp-name", "name", "Your name", required=True, auto="name")}
  {field("sp-business", "business", "Business", required=True, auto="organization")}
  {field("sp-email", "email", "Email", kind="email", required=True, auto="email")}
  {field("sp-phone", "phone", "Phone", kind="tel", optional=True, auto="tel")}
  {select("sp-interest", "interest", "Interested in", interests)}
  {field("sp-message", "message", "Message", kind="textarea", optional=True)}
  <button class="btn btn-primary" type="submit">Send inquiry</button>
  {PRIVACY_NOTE}
</form>
</div>'''


def coach_form():
    roles = ["Head coach (Grunion, paid)", "Referee", "Team manager", "Volunteer"]
    checks = "\n    ".join(f'<label><input type="checkbox" name="role[]" value="{r}"> {r}</label>' for r in roles)
    programs = [(t, t) for t in ("Men's", "Women's", "Youth", "Any")]
    return f'''<div class="form-card" id="signup">
<h2>Apply or offer to help</h2>
<p class="form-intro">Applying for the head coach job, or offering to referee, manage a team or volunteer? Tell us here. Your details go to SBRFC's officers.</p>
{form_open("coach-signup", "/thanks-coach")}
  {field("co-name", "name", "Your name", required=True, auto="name")}
  {field("co-email", "email", "Email", kind="email", required=True, auto="email")}
  {field("co-phone", "phone", "Phone", kind="tel", optional=True, auto="tel")}
  <fieldset class="checks">
    <legend>Role(s) you're interested in</legend>
    {checks}
  </fieldset>
  {select("co-program", "program", "Program", programs)}
  {field("co-background", "background", "Your rugby background", kind="textarea")}
  {field("co-message", "message", "Message", kind="textarea", optional=True)}
  <button class="btn btn-primary" type="submit">Send</button>
  {PRIVACY_NOTE}
</form>
</div>'''


def upcoming_box(heading="Upcoming"):
    items = "\n    ".join(
        f'<li data-until="{until}"><span class="what">{what}</span><span class="when">{when}</span></li>'
        for until, what, when in YOUTH_UPCOMING)
    return f'''<div class="upcoming" data-upcoming>
  <h2>{heading}</h2>
  <ol>
    {items}
  </ol>
  <p class="note">Season dates are provisional, and match fixtures are set by the club as the schedule is confirmed.</p>
  <p class="note" data-upcoming-empty hidden>New dates are on their way. Email <a href="mailto:{STINGRAYS_EMAIL}">{STINGRAYS_EMAIL}</a> for the latest.</p>
</div>'''


def lp_hero(eyebrow, h1, lede, chips, buttons, right):
    chip_html = "".join(f"<li>{c}</li>" for c in chips)
    return f'''<section class="lp-hero">
  <div class="wrap lp-hero-grid">
    <div>
      <span class="eyebrow">{eyebrow}</span>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
      <ul class="chips">{chip_html}</ul>
      <div class="btn-row">{buttons}</div>
    </div>
    {right}
  </div>
</section>'''


def lp_body(aside, main, top=""):
    top_html = f'<div class="lp-top">{top}</div>' if top else ""
    return f'''<section class="lp-body">
  <div class="wrap lp-grid">
    {top_html}
    <aside class="lp-aside" aria-label="Sign-up form">{aside}</aside>
    <div class="lp-main">
{main}
    </div>
  </div>
</section>'''


SIGNUP_BTN = '<a class="btn btn-primary" href="#signup">Sign up</a>'

# ===========================================================================
# /play
# ===========================================================================

page("play",
"Play Rugby in Santa Barbara — No Experience Needed | SBRFC",
"Men's, women's and youth rugby in Santa Barbara, and every club welcomes beginners. See when and where each team trains, then sign up in a minute.",
active="/play", og="og-play.jpg", sitemap_priority="0.9",
body=f'''
<section class="lp-hero">
  <div class="wrap lp-hero-grid form-right">
    <div>
      <span class="eyebrow">Men's &middot; Women's &middot; Youth</span>
      <h1>Play Rugby in Santa Barbara: No Experience Needed</h1>
      <p class="lede">Santa Barbara has a rugby club for men, one for women and one for kids and teens. All three teach the game from scratch, train twice a week at local parks, and are a lot of fun.</p>
      <ul class="chips"><li>Beginners welcome</li><li>Tuesday &amp; Thursday training</li><li>Elings Park &middot; Chase Palm Park</li><li>U8 to adult</li></ul>
      <div class="btn-row">{SIGNUP_BTN}<a class="btn btn-secondary" href="#teams">Find your team</a></div>
      <p class="give-line">Most people who join a Santa Barbara club had never played before. Nobody expects you to know the rules on day one, and nobody expects you to be fit yet either. That part comes from showing up.</p>
    </div>
    <div>{play_form()}</div>
  </div>
</section>

<section id="teams">
  <div class="wrap">
    <span class="eyebrow">Find your team</span>
    <h2>Three clubs, all welcoming beginners</h2>
    <p>Each club runs its own training, matches and social life. Here is when and where each one meets.</p>
    <div class="cards team-cards">

      <article class="card" id="mens">
        {photo("card-mens", "Grunion forwards packed down in a scrum", CARD_SIZES, cls="card-photo")}
        <span class="kind">Men's &middot; 18 and over</span>
        <h3>Grunion RFC</h3>
        <dl class="card-facts">
          <div><dt>Training</dt><dd>Tuesday and Thursday, 7–9 PM</dd></div>
          <div><dt>Where</dt><dd>Elings Park, upper fields</dd></div>
          <div><dt>Season</dt><dd>Pre-season from Tuesday, November 3. Matches January to April, on Saturdays.</dd></div>
          <div><dt>Ages</dt><dd>18 and over, no tryout</dd></div>
        </dl>
        <a class="go" href="/mens">Men's rugby <span class="arrow">&#8594;</span></a>
      </article>

      <article class="card" id="womens">
        {photo("card-womens", "The Santa Barbara Mermaids squad together under the posts", CARD_SIZES, cls="card-photo")}
        <span class="kind">Women's &middot; 18 and over</span>
        <h3>Santa Barbara Mermaids</h3>
        <dl class="card-facts">
          <div><dt>Training</dt><dd>Tuesday and Thursday, 7–9 PM</dd></div>
          <div><dt>Where</dt><dd>Elings Park, Soccer Field 2</dd></div>
          <div><dt>Season</dt><dd>Practice October to March, games about January to May. Co-ed touch at Chase Palm Park in summer.</dd></div>
          <div><dt>Ages</dt><dd>All women and nonconforming players, 18 and over</dd></div>
        </dl>
        <a class="go" href="/womens">Women's rugby <span class="arrow">&#8594;</span></a>
      </article>

      <article class="card" id="youth">
        {photo("card-youth", "Young Stingrays players and their coaches cheering on the field", CARD_SIZES, cls="card-photo")}
        <span class="kind">Youth &middot; U8 to U18</span>
        <h3>Santa Barbara Stingrays</h3>
        <dl class="card-facts">
          <div><dt>Training</dt><dd>Tuesday and Thursday afternoons from 4 PM, times by age group</dd></div>
          <div><dt>Where</dt><dd>Chase Palm Park from November 3, Elings Park from December 8</dd></div>
          <div><dt>Season</dt><dd>About January 16 to March 6, 2027</dd></div>
          <div><dt>Ages</dt><dd>U8 to U18. U8 plays non-contact flag rugby.</dd></div>
        </dl>
        <a class="go" href="/youth">Youth rugby <span class="arrow">&#8594;</span></a>
      </article>

    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">Why play</span>
    <h2>Why people stick with rugby</h2>
    <p><strong>It's fun.</strong> Rugby is a running, passing game where everyone handles the ball, from the biggest forward to the quickest winger. Training is outdoors, twice a week, at parks between the mountains and the ocean.</p>
    <p><strong>You'll make friends fast.</strong> Teams train together, travel to matches together and spend time together off the field. After Thursday training the Grunion head to Baja Sharkeez, and the Mermaids run socials and fundraisers through the year.</p>
    <p><strong>There's a place for every body.</strong> Rugby needs big players, small players, fast players and strong ones. New players arrive at every level of fitness and get fitter by playing.</p>
  </div>
</section>

<section id="new">
  <div class="wrap">
    <span class="eyebrow">New to rugby?</span>
    <h2>Questions beginners ask</h2>
    <dl class="faq">
      <div><dt>Do I need experience?</dt><dd>No. Coaches teach the basics from the first session: passing, catching, tackling safely and what is going on in a scrum. You don't need to be fit to start, either.</dd></div>
      <div><dt>What should I bring?</dt><dd>Boots if you have them, trainers if you don't, plus water and clothes you can run in. A mouthguard is worth having before you play contact. No mouthguard yet? Ask at your first session.</dd></div>
      <div><dt>Is it safe?</dt><dd>Rugby is a contact sport, and the clubs coach it that way. Coaches teach new players how to tackle, and how to be tackled, safely. Kids' rugby is matched to age: U8 plays non-contact flag rugby, contact comes in step by step as players get older, and the Stingrays' coaches are USA Rugby certified. If you have an injury or a worry, tell a coach before you start.</dd></div>
      <div><dt>How old do I need to be?</dt><dd>Adults 18 and over play for the Grunion (men) or the Mermaids (women and nonconforming players). Kids and teens from U8 to U18 play for the Stingrays.</dd></div>
      <div><dt>How do I start?</dt><dd>Fill in the form on this page and your details go to the club you pick. Or just turn up: get to training ten minutes early and tell someone it's your first time. Men can text Jordan at <a href="{JORDAN_SMS}">{JORDAN}</a>, women can email the Mermaids at <a href="mailto:{MERMAIDS_EMAIL}">{MERMAIDS_EMAIL}</a>, and parents can <a href="{STINGRAYS_REGISTER}" target="_blank" rel="noopener">register with the Stingrays online</a>.</dd></div>
    </dl>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">Where</span>
    <h2>Where the clubs train</h2>
    <p>Both grounds are public parks, and anyone is welcome to come and watch a session before joining in.</p>
    <div class="cards cards-2 place-cards">
      <div class="card card-light">
        <span class="kind">Grunion &middot; Mermaids &middot; Stingrays from Dec 8</span>
        <h3>Elings Park</h3>
        <p>1298 Las Positas Road, Santa Barbara, CA 93105. The Grunion use the upper fields and the Mermaids use Soccer Field 2. Free parking.</p>
        <a class="go" href="{ELINGS_MAP}" target="_blank" rel="noopener">Open in maps <span class="arrow">&#8594;</span></a>
      </div>
      <div class="card card-light">
        <span class="kind">Stingrays pre-season &middot; summer touch</span>
        <h3>Chase Palm Park</h3>
        <p>323 East Cabrillo Boulevard, Santa Barbara, CA 93101. Stingrays pre-season training from November 3, and co-ed touch rugby on summer evenings.</p>
        <a class="go" href="{CHASE_MAP}" target="_blank" rel="noopener">Open in maps <span class="arrow">&#8594;</span></a>
      </div>
    </div>
  </div>
</section>
''')

# ===========================================================================
# /mens
# ===========================================================================

page("mens",
"Men's Rugby in Santa Barbara — Grunion RFC | SBRFC",
"Play men's rugby in Santa Barbara with Grunion RFC. Beginners and veterans both welcome. Training Tuesday and Thursday, 7–9 PM, at Elings Park. Season January to April.",
active="/mens", og="og-mens.jpg", sitemap_priority="0.9",
body=lp_hero(
    "Men's rugby &middot; 18 and over",
    "Men's Rugby in Santa Barbara with the Grunion",
    "Beginners and veterans both welcome. The Grunion have played rugby in Santa Barbara since 1978, train twice a week at Elings Park, and teach new players from their first session.",
    ["Tue &amp; Thu &middot; 7–9 PM", "Elings Park", "Season Jan–Apr", "18 and over"],
    SIGNUP_BTN + f'<a class="btn btn-secondary" href="{JORDAN_SMS}">Text Jordan</a>',
    photo("mens", "A Grunion player in the club's blue and green kit runs at a defender with the ball", HERO_SIZES, eager=True),
) + lp_body(
    player_form("mens", "mens-interest", "/thanks-mens", "mens", "Sign up",
                "Leave your details and they go straight to the Grunion."),
    f'''
<h2>When and where</h2>
<p>Training is every Tuesday and Thursday, 7–9 PM, on the upper fields at Elings Park, 1298 Las Positas Road. Pre-season starts Tuesday, November 3. After a break for the holidays, training is back on Tuesday, January 5, and the season runs January to April with matches on Saturdays, at home at Elings or away across Southern California.</p>
<dl class="facts">
  <div><dt>Training</dt><dd>Tuesday and Thursday, 7–9 PM</dd></div>
  <div><dt>Where</dt><dd>Elings Park upper fields, 1298 Las Positas Rd, Santa Barbara. Free parking. <a href="{ELINGS_MAP}" target="_blank" rel="noopener">Get directions</a></dd></div>
  <div><dt>Pre-season</dt><dd>Starts Tuesday, November 3</dd></div>
  <div><dt>Holiday break</dt><dd>Back Tuesday, January 5</dd></div>
  <div><dt>Season</dt><dd>January to April, matches on Saturdays</dd></div>
  <div><dt>Who</dt><dd>Men 18 and over. No tryout.</dd></div>
</dl>

<h2>Your first session</h2>
<p>Get there ten minutes early, find Jordan and join the group. Nobody makes you give a speech. Sessions mix fitness, skills and game play, and coaches show new players how to pass, catch and tackle safely.</p>
<p>Bring boots if you have them, trainers if you don't, plus water and a mouthguard. No mouthguard yet? The club will sort you out.</p>

<h2>Who plays</h2>
<p>Anyone 18 or over. The squad mixes men in their first season with players who have been at it for years, and every fitness level in between. There's no tryout and nobody gets cut. Ask new players whether they had played before and most say never, which is how most of the club started.</p>
<p>When you're ready for matches, you register with USA Rugby under the club's name, and someone at the club will walk you through it.</p>

<h2>After practice</h2>
<p>After Thursday training and home matches, the club heads to Baja Sharkeez at 416 State St, a Grunion sponsor and the home of the third half. New players are welcome to come along.</p>

<h2>Questions?</h2>
<p>Text or call Jordan at <a href="{JORDAN_SMS}">{JORDAN}</a>, or email <a href="mailto:{GRUNION_EMAIL}">{GRUNION_EMAIL}</a>. Fixtures, results and club news are on the Grunion's own website.</p>
<div class="btn-row">
  <a class="btn btn-primary" href="{JORDAN_SMS}">Text Jordan</a>
  <a class="btn btn-secondary" href="{JORDAN_TEL}">Call Jordan</a>
  {ext(GRUNION_URL + REFERRAL, "Visit the Grunion site")}
</div>
'''))

# ===========================================================================
# /womens
# ===========================================================================

page("womens",
"Women's Rugby in Santa Barbara — Santa Barbara Mermaids | SBRFC",
"Play women's rugby in Santa Barbara with the Mermaids. No experience necessary, open to all women and nonconforming players 18+. Practice Tuesday and Thursday, 7–9 PM, at Elings Park.",
active="/womens", og="og-womens.jpg", sitemap_priority="0.9",
body=lp_hero(
    "Women's rugby &middot; 18 and over",
    "Women's Rugby in Santa Barbara with the Mermaids",
    "No experience necessary. The Mermaids play competitive rugby, teach the game from scratch, and welcome all women and nonconforming players 18 and over.",
    ["Tue &amp; Thu &middot; 7–9 PM", "Elings Park, Soccer Field 2", "Practice Oct–Mar", "18 and over"],
    SIGNUP_BTN + f'<a class="btn btn-secondary" href="mailto:{MERMAIDS_EMAIL}">Email the Mermaids</a>',
    photo("womens", "The Santa Barbara Mermaids squad in blue kit, together under the posts after a match", HERO_SIZES, eager=True),
) + lp_body(
    player_form("womens", "womens-interest", "/thanks-womens", "womens", "Sign up",
                "Leave your details and they go straight to the Mermaids."),
    f'''
<h2>Practice and games</h2>
<p>15s practices run every Tuesday and Thursday, 7–9 PM, on Soccer Field 2 at Elings Park, from October to March. Games run roughly January to May, with the Mermaids playing women's teams from across California in tournaments about once or twice a month.</p>
<p>The Mermaids have played competitive rugby in Santa Barbara since 2015 and compete in the Southern California Senior Women's Division II.</p>
<dl class="facts">
  <div><dt>15s practice</dt><dd>Tuesday and Thursday, 7–9 PM, October to March</dd></div>
  <div><dt>Where</dt><dd>Elings Park, Soccer Field 2, 1298 Las Positas Rd, Santa Barbara. <a href="{ELINGS_MAP}" target="_blank" rel="noopener">Get directions</a></dd></div>
  <div><dt>Games</dt><dd>Roughly January to May</dd></div>
  <div><dt>Summer</dt><dd>Co-ed touch rugby at Chase Palm Park, April to September</dd></div>
  <div><dt>Who</dt><dd>All women and nonconforming players, 18 and over</dd></div>
</dl>

<h2>Summer touch rugby</h2>
<p>From April to September the club plays co-ed touch rugby with the Grunion at Chase Palm Park, Tuesday and Thursday from 5:30 PM until sunset. Touch is light contact and relaxed, which makes it an easy first taste of the game.</p>

<h2>Who plays</h2>
<p>The squad is a mix of young professionals, college students, moms, first-time players and rugby veterans from Goleta, Santa Barbara and the neighboring cities. Rugby needs every kind of player: small, tall, strong, fast and scrappy. You don't need any experience, and you'll get fitter by playing.</p>
<p>The Mermaids play full-contact rugby, and coaches keep practice safe and fun. Tell a coach ahead of time about any injury or concern.</p>

<h2>What to bring</h2>
<p>Clothes you can run in, boots if you have them (trainers are fine to start), water and a mouthguard if you have one. Take off jewelry, including piercings, before contact.</p>

<h2>Stay in the loop</h2>
<p>The Mermaids share practice updates, events and workouts on Discord. Email <a href="mailto:{MERMAIDS_EMAIL}">{MERMAIDS_EMAIL}</a> and they'll send you the invite link.</p>
<div class="btn-row">
  <a class="btn btn-primary" href="mailto:{MERMAIDS_EMAIL}">Email the Mermaids</a>
  {ext(MERMAIDS_URL + REFERRAL, "Visit the Mermaids site")}
</div>
'''))

# ===========================================================================
# /youth
# ===========================================================================

page("youth",
"Youth Rugby in Santa Barbara, U8 to U18 — Santa Barbara Stingrays | SBRFC",
"Youth rugby for kids and teens in Santa Barbara, U8 to U18, with the Stingrays. USA Rugby certified coaches, safety first, and U8 plays non-contact flag rugby. New families welcome.",
active="/youth", og="og-youth.jpg", sitemap_priority="0.9",
body=lp_hero(
    "Youth rugby &middot; U8 to U18",
    "Youth Rugby for Kids and Teens in Santa Barbara",
    "The Santa Barbara Stingrays coach kids and teens from U8 to U18. No experience needed, safety comes first, and the youngest players start with non-contact flag rugby.",
    ["U8 to U18", "USA Rugby certified coaches", "Tue &amp; Thu afternoons", "New families welcome"],
    SIGNUP_BTN + ext(STINGRAYS_REGISTER, "Register with the Stingrays"),
    photo("youth", "Young Stingrays players chase a ball carrier during a game of flag rugby", HERO_SIZES, eager=True),
) + lp_body(
    player_form("youth", "youth-interest", "/thanks-youth", "youth", "Interested? Tell us",
                "For parents and guardians. Your details go straight to the Stingrays, and we don't ask for your child's name.",
                button="Send"),
    f'''
<h2>Safety first</h2>
<p>Stingrays coaches are USA Rugby certified, and they teach individual skills and team play with player safety at the heart of every session and match. Contact comes in step by step as players get older. U8 plays non-contact flag rugby, where a tackle means pulling a flag from the ball carrier's belt.</p>
<p>Players and coaches are registered with USA Rugby, which carries the club's insurance, and the club follows a concussion protocol.</p>

<h2>New to rugby? Most families are</h2>
<p>New players are welcome at any point in the year, and nobody is expected to know the rules on day one. Pre-season training runs for all age groups together at Chase Palm Park. From December 8 the club moves to Elings Park, where U8 to U10 and U12 to U14 train at different times, so kids learn alongside players their own size.</p>

<div data-until="2026-10-30">
<h2>Halloween Kick-Off, Friday, October 30</h2>
<p>From 4 to 7 PM at Elings Park. Players, families, friends and newcomers are welcome for rugby games, a candy scavenger hunt, food for sale, drinks and a fundraiser raffle. Costumes encouraged. It's the easiest way to meet the club before you sign up.</p>
</div>

<h2>What to bring</h2>
<p>Boots if your child has them, trainers if not, plus water, a mouthguard and clothes they can run around in.</p>

<h2>How to sign up</h2>
<p>Register online with the Stingrays whenever you're ready, or leave your details in the form on this page and they'll go straight to the club. For questions about age groups, training or anything else, email <a href="mailto:{STINGRAYS_EMAIL}">{STINGRAYS_EMAIL}</a>.</p>
<p>Scholarships and financial aid available. Ask the club.</p>
<div class="btn-row">
  {ext(STINGRAYS_REGISTER, "Register with the Stingrays", "btn btn-primary")}
  {ext(STINGRAYS_URL + REFERRAL, "Visit the Stingrays site")}
</div>
''',
    top=upcoming_box()))

# ===========================================================================
# /sponsor
# ===========================================================================

page("sponsor",
"Sponsor Rugby in Santa Barbara — Packages for Local Businesses | SBRFC",
"Sponsor rugby in Santa Barbara: Grunion front-of-shirt and kit partner packages, beer and social sponsors, and Stingrays and Mermaids partnerships. SBRFC is a 501(c)(3) nonprofit.",
active="/sponsor", og="og-sponsor.jpg", sitemap_priority="0.8",
body=lp_hero(
    "For local businesses",
    "Sponsor Rugby in Santa Barbara",
    "Local businesses keep rugby going in this town. A sponsorship puts your name on the kit, at Elings Park and in front of a loyal community of players, families and supporters.",
    ["Front of shirt $5,000", "Kit partner $1,000", "Beer &amp; social", "Youth &amp; women's teams"],
    '<a class="btn btn-primary" href="#signup">Ask about sponsoring</a>',
    photo("sponsor", "A Grunion player in the club's blue and green kit makes a tackle", HERO_SIZES, eager=True),
) + lp_body(
    sponsor_form(),
    f'''
<h2>Packages</h2>
<div class="pkgs">
  <div class="pkg">
    <h3>Grunion Front of Shirt</h3>
    <p class="price">$5,000 &middot; 2 years</p>
    <ul>
      <li>Your logo on the front of the Grunion's match-day and training kits for two years</li>
      <li>Headline sponsor placement on the Grunion website</li>
      <li>Headline placement in match-day and social posts, club emails and press releases</li>
      <li>A solo social media highlight</li>
      <li>Clubhouse banner and fence banner at Elings Park</li>
    </ul>
  </div>
  <div class="pkg">
    <h3>Grunion Kit Partner</h3>
    <p class="price">$1,000 &middot; 2 years</p>
    <ul>
      <li>A small logo on the sleeves or back of the match-day shirt for two years</li>
      <li>Sponsor placement on the Grunion website</li>
      <li>Placement in match-day and social posts, club emails and press releases</li>
      <li>A group sponsor highlight on social media</li>
    </ul>
  </div>
  <div class="pkg">
    <h3>Beer and Social Sponsors</h3>
    <p class="price">Let's talk</p>
    <ul>
      <li>Beer sponsor: your logo on display at the clubhouse as the official beer on tap</li>
      <li>Social sponsor: 30+ players come through your doors every Thursday, and 60+ on Saturdays</li>
    </ul>
  </div>
  <div class="pkg">
    <h3>Stingrays and Mermaids</h3>
    <p class="price">Let's talk</p>
    <ul>
      <li>Stingrays: club partner, kit partner, community partner and scholarship support for the 2026/27 season</li>
      <li>Mermaids: your logo on their website, social media and jerseys</li>
    </ul>
  </div>
</div>

<h2>What sponsorship pays for</h2>
<p>Sponsorship money stays in Santa Barbara rugby. It pays for kits, field fees, referees, travel to away matches, and scholarships.</p>

<h2>Who sees your name</h2>
<p>The Grunion play at Elings Park, which sees more than 250,000 visitors a year, and post match days, results and sponsor shout-outs on Facebook and Instagram. Sponsors are named on the kit, on the sideline, at socials and on the clubs' websites.</p>

<h2>Current sponsors</h2>
<ul class="logos">
  <li><a href="https://www.sharkeez.net/" target="_blank" rel="noopener"><img src="/images/sponsors/baja-sharkeez.png" alt="Baja Sharkeez" width="240" height="64" loading="lazy" decoding="async"></a></li>
  <li><a href="https://www.rinconbrewery.com/" target="_blank" rel="noopener"><img src="/images/sponsors/rincon-brewery.png" alt="Rincon Brewery" width="64" height="64" loading="lazy" decoding="async"></a></li>
  <li><a href="https://www.goldenroostersb.com/" target="_blank" rel="noopener"><img src="/images/sponsors/golden-rooster.png" alt="Golden Rooster Transportation" width="54" height="64" loading="lazy" decoding="async"></a></li>
</ul>

<h2>A registered nonprofit</h2>
<p>The Santa Barbara Rugby Football Club is a 501(c)(3) nonprofit, EIN {EIN}, that supports the Grunion, the Mermaids and the Stingrays. Sponsorship inquiries sent from this page go to the SBRFC treasurer.</p>
<p class="give-line">Prefer to give personally? <a href="{CLUB78_URL}" target="_blank" rel="noopener">Join the '78 Club</a>.</p>
'''))

# ===========================================================================
# /coach
# ===========================================================================

page("coach",
"Paid Rugby Head Coach Job in Santa Barbara — Grunion RFC | SBRFC",
"The Grunion, Santa Barbara's men's rugby club, are hiring a paid head coach: $200–$400 per match, mileage on away fixtures, playoff bonuses. Referees, team managers and volunteers welcome too.",
active="/coach", og="og-coach.jpg", sitemap_priority="0.8",
body=lp_hero(
    "Coaches, referees and volunteers",
    "Coach the Grunion: Paid Head Coach in Santa Barbara",
    "The Grunion, Santa Barbara's men's rugby club, are hiring a paid head coach. Former players especially welcome. Referees, team managers and volunteers are welcome too.",
    ["Paid per match", "Tue &amp; Thu &middot; 7–9 PM", "Saturdays Jan–Apr", "Elings Park"],
    '<a class="btn btn-primary" href="#signup">Apply</a>' + ext(GRUNION_COACH_JOB, "Full job details"),
    photo("coach", "Two Grunion players in blue and green kit make a tackle", HERO_SIZES, eager=True),
) + lp_body(
    coach_form(),
    f'''
<h2>The head coach job</h2>
<p>The Grunion play Division 2 men's rugby. Pre-season runs November to December and the season January to April, with 13 or more matches. Training is Tuesday and Thursday nights at Elings Park, and match day is Saturday, at home or on the road across Southern California.</p>
<dl class="facts">
  <div><dt>Pay</dt><dd>$200–$400 per match</dd></div>
  <div><dt>Away fixtures</dt><dd>Mileage paid</dd></div>
  <div><dt>Postseason</dt><dd>Playoff and Nationals bonuses</dd></div>
  <div><dt>Training</dt><dd>Tuesday and Thursday, 7–9 PM, Elings Park</dd></div>
  <div><dt>Season</dt><dd>Pre-season November to December, matches January to April, 13 or more a season</dd></div>
  <div><dt>Commitment</dt><dd>Multi-season. The club is hiring for the long term.</dd></div>
</dl>
<p>You own the season plan, training, selection and the standard the club holds itself to. Fundraising, registration, kit orders and fixtures admin stay with the board.</p>

<h2>Who we're looking for</h2>
<ul>
  <li>Free Tuesday and Thursday evenings from November to April, plus Saturdays from January to April</li>
  <li>Based in Santa Barbara, or able to get there</li>
  <li>A playing or coaching background at club, collegiate or representative level</li>
  <li>USA Rugby coaching certification, or willingness to get it. The club pays for the course.</li>
  <li>Experience turning walk-ons into starters, since that is most of the club's intake</li>
</ul>
<p>Former players especially welcome. The full job description, and the Grunion's own application form with room for a résumé, are at <a href="{GRUNION_COACH_JOB}" target="_blank" rel="noopener">grunionrugby.com/coach</a>. Or apply with the form on this page.</p>
<p>SBRFC is an equal opportunity organization. All qualified applicants will be considered without regard to race, color, religion, sex, sexual orientation, gender identity, national origin, age, disability or veteran status.</p>

<h2>Referees, team managers and volunteers</h2>
<p>Rugby in Santa Barbara also runs on referees, team managers and volunteers. Every match needs a referee, and former players already know the game. A team manager keeps rosters, match-day logistics and travel organized. Volunteers help on match days and at club events. If one of those fits, use the same form and pick your role.</p>
<div class="btn-row">
  <a class="btn btn-primary" href="#signup">Apply or offer to help</a>
  {ext(GRUNION_URL + REFERRAL, "Visit the Grunion site")}
</div>
'''))

# ===========================================================================
# THANK-YOU PAGES (noindex, not in the sitemap). Each load fires a Google
# Analytics event from site.js via data-track on <body>.
# Renaming any /thanks-* URL breaks conversion counting in Google Ads.
# ===========================================================================

def thanks_head(eyebrow, h1, lede):
    return f'''<section class="page-head">
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>'''


page("thanks-mens",
"Thanks for Signing Up — Grunion RFC | SBRFC",
"Thanks for signing up to play men's rugby with Grunion RFC. Here's when and where to come to training.",
noindex=True, og="og-mens.jpg", body_attrs=' data-track="player_signup" data-team="mens"',
body=thanks_head("Men's rugby", "Thanks, see you at training",
                 "Your details have gone to the Grunion. The next step is the fun part: come to a session.") + f'''
<section>
  <div class="wrap">
    <div class="status-box next-box">
      <h2>Next practice</h2>
      <dl class="facts">
        <div><dt>When</dt><dd>Tuesday and Thursday, 7–9 PM. Pre-season starts Tuesday, November 3. After the holiday break, training is back Tuesday, January 5.</dd></div>
        <div><dt>Where</dt><dd>Elings Park upper fields, 1298 Las Positas Rd, Santa Barbara. Free parking.</dd></div>
        <div><dt>Bring</dt><dd>Boots or trainers, water, and a mouthguard if you have one</dd></div>
      </dl>
      <div class="btn-row">
        <a class="btn btn-primary" href="{JORDAN_SMS}">Text Jordan</a>
        <a class="btn btn-ghost" href="{JORDAN_TEL}">Call Jordan</a>
        <a class="btn btn-ghost" href="{ELINGS_MAP}" target="_blank" rel="noopener">Get directions</a>
      </div>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <h2>Before you come</h2>
    <p>Get there ten minutes early, find Jordan and join the group. Nobody will make you introduce yourself to the squad. If something comes up, or you want to check the plan, text Jordan at <a href="{JORDAN_SMS}">{JORDAN}</a>.</p>
    <p>The first session is about learning the basics: how to pass, catch and tackle safely. Go at your own pace and ask questions.</p>
    <p>After Thursday training and home matches the club heads to Baja Sharkeez, 416 State St. You're welcome to come along.</p>
    <h2 class="thanks-more">Getting to match day</h2>
    <p>Pre-season comes before the first match, which makes it the easiest time to start: you learn the basics before anyone plays a fixture. Matches are on Saturdays from January to April, at Elings Park or away across Southern California. When you're ready to play in one, you register with USA Rugby under the club's name, and someone at the club will walk you through it.</p>
    <div class="btn-row">{ext(GRUNION_URL + REFERRAL, "Visit the Grunion site")}</div>
  </div>
</section>
''')

page("thanks-womens",
"Thanks for Signing Up — Santa Barbara Mermaids | SBRFC",
"Thanks for signing up to play women's rugby with the Santa Barbara Mermaids. Here's when and where to come to practice.",
noindex=True, og="og-womens.jpg", body_attrs=' data-track="player_signup" data-team="womens"',
body=thanks_head("Women's rugby", "Thanks, the Mermaids have your details",
                 "No experience necessary, so the next step is simple: come to practice.") + f'''
<section>
  <div class="wrap">
    <div class="status-box next-box">
      <h2>Next practice</h2>
      <dl class="facts">
        <div><dt>When</dt><dd>Tuesday and Thursday, 7–9 PM, October to March</dd></div>
        <div><dt>Where</dt><dd>Elings Park, Soccer Field 2, 1298 Las Positas Rd, Santa Barbara</dd></div>
        <div><dt>Bring</dt><dd>Clothes you can run in, boots or trainers, water, and a mouthguard if you have one</dd></div>
      </dl>
      <div class="btn-row">
        <a class="btn btn-primary" href="mailto:{MERMAIDS_EMAIL}">Email the Mermaids</a>
        <a class="btn btn-ghost" href="{ELINGS_MAP}" target="_blank" rel="noopener">Get directions</a>
      </div>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <h2>Get on the team Discord</h2>
    <p>The Mermaids share practice updates, events and workouts on Discord. Email <a href="mailto:{MERMAIDS_EMAIL}">{MERMAIDS_EMAIL}</a> and ask for the invite link.</p>
    <h2 class="thanks-more">Your first practice</h2>
    <p>The squad includes plenty of first-time players, so you won't be the only new face. Want to see a game before you play one? The Mermaids play tournaments about once or twice a month from January to May, and fans are welcome on the sideline.</p>
    <h2 class="thanks-more">Good to know</h2>
    <p>Take off jewelry, including piercings, before contact, and tell a coach ahead of time about any injury or concern. Games run roughly January to May, and from April to September there's co-ed touch rugby at Chase Palm Park on Tuesday and Thursday evenings.</p>
    <div class="btn-row">{ext(MERMAIDS_URL + REFERRAL, "Visit the Mermaids site")}</div>
  </div>
</section>
''')

page("thanks-youth",
"Thanks for Getting in Touch — Santa Barbara Stingrays | SBRFC",
"Thanks for your interest in youth rugby with the Santa Barbara Stingrays. Here's what's coming up and how to register.",
noindex=True, og="og-youth.jpg", body_attrs=' data-track="player_signup" data-team="youth"',
body=thanks_head("Youth rugby", "Thanks, the Stingrays have your details",
                 "Here's what's coming up. New families are welcome at all of it.") + f'''
<section>
  <div class="wrap">
    {upcoming_box("Next up")}
    <div class="btn-row">
      {ext(STINGRAYS_REGISTER, "Register with the Stingrays", "btn btn-primary")}
      <a class="btn btn-secondary" href="mailto:{STINGRAYS_EMAIL}">Email the club</a>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <h2>Next steps</h2>
    <p>When you're ready, register your child online with the Stingrays. Questions about age groups, training times or anything else go to <a href="mailto:{STINGRAYS_EMAIL}">{STINGRAYS_EMAIL}</a>. Scholarships and financial aid available.</p>
    <p>The online registration asks for parent and player details, a photo and proof of age, and emergency and medical information, so it helps to have those handy before you start.</p>
    <p>For training, bring boots or trainers, water and a mouthguard. The youngest group, U8, plays non-contact flag rugby, and every Stingrays coach is USA Rugby certified.</p>
    <div data-until="2026-10-30">
    <h2 class="thanks-more">See you at the Halloween Kick-Off?</h2>
    <p>Friday, October 30, 4–7 PM at Elings Park: rugby games, a candy scavenger hunt, food for sale, drinks and a raffle. Costumes encouraged, and newcomers are welcome.</p>
    </div>
    <div class="btn-row">{ext(STINGRAYS_URL + REFERRAL, "Visit the Stingrays site")}</div>
  </div>
</section>
''')

page("thanks-play",
"Thanks for Signing Up — Play Rugby in Santa Barbara | SBRFC",
"Thanks for your interest in playing rugby in Santa Barbara. Here's when and where each club trains.",
noindex=True, og="og-play.jpg", body_attrs=' data-track="player_signup" data-team="general"',
body=thanks_head("Play rugby", "Thanks, we've got your details",
                 "Your message has reached SBRFC's volunteers. In the meantime, here's when and where each club trains, so you can pick one and come along.") + f'''
<section>
  <div class="wrap">
    <div class="cards">
      <div class="card">
        <span class="kind">Men's &middot; 18+</span>
        <h3>Grunion RFC</h3>
        <p>Tuesday and Thursday, 7–9 PM, Elings Park upper fields. Pre-season from Tuesday, November 3.</p>
        <a class="go" href="{JORDAN_SMS}">Text Jordan <span class="arrow">&#8594;</span></a>
      </div>
      <div class="card">
        <span class="kind">Women's &middot; 18+</span>
        <h3>Santa Barbara Mermaids</h3>
        <p>Tuesday and Thursday, 7–9 PM, Elings Park Soccer Field 2, October to March.</p>
        <a class="go" href="mailto:{MERMAIDS_EMAIL}">Email the Mermaids <span class="arrow">&#8594;</span></a>
      </div>
      <div class="card">
        <span class="kind">Youth &middot; U8 to U18</span>
        <h3>Santa Barbara Stingrays</h3>
        <p>Tuesday and Thursday afternoons. Chase Palm Park from November 3, Elings Park from December 8.</p>
        <a class="go" href="{STINGRAYS_REGISTER}" target="_blank" rel="noopener">Register with the Stingrays <span class="arrow">&#8594;</span></a>
      </div>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <h2>Not sure which team?</h2>
    <p>Adults 18 and over play for the Grunion (men) or the Mermaids (women and nonconforming players). Kids and teens from U8 to U18 play for the Stingrays. All three take beginners.</p>
    <p>Whichever you choose, get there ten minutes early, bring boots or trainers, water and a mouthguard if you have one, and tell someone it's your first time.</p>
    <p>Rather watch a session first? Both grounds are public parks, and you're welcome on the sideline. Elings Park is at 1298 Las Positas Road and Chase Palm Park is at 323 East Cabrillo Boulevard.</p>
    <div class="btn-row">
      <a class="btn btn-secondary" href="/mens">Men's rugby</a>
      <a class="btn btn-secondary" href="/womens">Women's rugby</a>
      <a class="btn btn-secondary" href="/youth">Youth rugby</a>
    </div>
  </div>
</section>
''')

page("thanks-sponsor",
"Thanks for Your Sponsorship Inquiry | SBRFC",
"Thanks for your interest in sponsoring rugby in Santa Barbara. Your inquiry has gone to the SBRFC treasurer.",
noindex=True, og="og-sponsor.jpg", body_attrs=' data-track="sponsor_inquiry"',
body=thanks_head("Sponsorship", "Thanks for your interest in sponsoring",
                 "Your inquiry has gone to the SBRFC treasurer at treasurer@sbrfc.com.") + f'''
<section>
  <div class="wrap">
    <div class="status-box next-box">
      <h2>Want to add something?</h2>
      <p>To add details to your inquiry, send a logo, or talk sooner, email the treasurer directly at <a href="mailto:{TREASURER}">{TREASURER}</a>.</p>
      <div class="btn-row"><a class="btn btn-primary" href="mailto:{TREASURER}">Email the treasurer</a></div>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <h2>Packages at a glance</h2>
    <dl class="facts">
      <div><dt>Grunion front of shirt</dt><dd>$5,000 for two years, with headline placement on the kit, the website, social posts and banners at Elings Park</dd></div>
      <div><dt>Grunion kit partner</dt><dd>$1,000 for two years, with a small logo on the match-day shirt and sponsor placement online</dd></div>
      <div><dt>Beer and social</dt><dd>Let's talk</dd></div>
      <div><dt>Stingrays and Mermaids</dt><dd>Let's talk</dd></div>
    </dl>
    <h2 class="thanks-more">See the clubs play</h2>
    <p>The best way to see what a sponsorship puts your name in front of is to come to a match. The Grunion play on Saturdays from January to April, at home at Elings Park or away across Southern California. The Mermaids play tournaments about once or twice a month from January to May, and the Stingrays' youth season runs about January 16 to March 6, 2027.</p>
    <div class="btn-row">
      {ext(GRUNION_URL + REFERRAL, "Visit the Grunion site")}
      {ext(MERMAIDS_URL + REFERRAL, "Visit the Mermaids site")}
      {ext(STINGRAYS_URL + REFERRAL, "Visit the Stingrays site")}
    </div>
  </div>
</section>
''')

page("thanks-coach",
"Thanks for Getting in Touch — Coaches and Volunteers | SBRFC",
"Thanks for applying to coach the Grunion, or offering to referee, manage a team or volunteer with rugby in Santa Barbara.",
noindex=True, og="og-coach.jpg", body_attrs=' data-track="coach_signup"',
body=thanks_head("Coaches, referees and volunteers", "Thanks, we've got your details",
                 "Your details have reached SBRFC's officers. The best next step is to come and watch a session.") + f'''
<section>
  <div class="wrap">
    <div class="status-box next-box">
      <h2>Come and watch</h2>
      <dl class="facts">
        <div><dt>Grunion training</dt><dd>Tuesday and Thursday, 7–9 PM, Elings Park upper fields. Pre-season starts Tuesday, November 3, and training is back Tuesday, January 5 after the holiday break.</dd></div>
        <div><dt>Match days</dt><dd>Saturdays, January to April, at Elings Park or away across Southern California</dd></div>
        <div><dt>Where</dt><dd>1298 Las Positas Rd, Santa Barbara. Free parking.</dd></div>
      </dl>
      <div class="btn-row"><a class="btn btn-ghost" href="{ELINGS_MAP}" target="_blank" rel="noopener">Get directions</a></div>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <h2>Good to know</h2>
    <p>The head coach job is paid per match, from $200 to $400, with mileage on away fixtures and bonuses for the playoffs and Nationals. The full description is at <a href="{GRUNION_COACH_JOB}" target="_blank" rel="noopener">grunionrugby.com/coach</a>, along with the Grunion's own application form if you would like to send a résumé.</p>
    <p>Offering to referee, manage a team or volunteer for the Mermaids or the Stingrays? Their training times and places are on the <a href="/womens">women's</a> and <a href="/youth">youth</a> pages.</p>
    <div class="btn-row">
      {ext(GRUNION_COACH_JOB, "Full job details")}
      {ext(GRUNION_URL + REFERRAL, "Visit the Grunion site")}
    </div>
  </div>
</section>
''')

# ===========================================================================
# HOME
# ===========================================================================

page("index",
"SBRFC — Santa Barbara Rugby Football Club",
"The Santa Barbara Rugby Football Club is a 501(c)(3) non-profit, EIN 93-4659131. We fund coaching, player recruitment and season dues so that anyone in Santa Barbara County can play rugby.",
head_extra='<link rel="preload" as="image" href="/images/sbrfc-logo.webp" type="image/webp" fetchpriority="high">\n',
sitemap_priority="1.0",
body=f'''
<section class="hero">
  <div class="wrap">
    <picture>
      <source srcset="/images/sbrfc-logo.webp" type="image/webp">
      <img class="logo" src="/images/sbrfc-logo.png" alt="SBRFC logo, a grunion, a mermaid, and stingrays around the letters SBRFC" width="860" height="860" fetchpriority="high">
    </picture>
    <div class="rule rule-center" role="presentation"></div>
    <h1 class="statement">Welcome to <strong>SBRFC</strong> <span class="full-name">(Santa&nbsp;Barbara Rugby Football Club)</span>, the 501(c)(3) non-profit for the promotion, encouragement, and extension of Rugby&nbsp;Union football in Santa&nbsp;Barbara County.</h1>
  </div>
</section>

<section class="mission-band">
  <div class="wrap">
    <picture>
      <source srcset="/images/sbrfc-badge.webp" type="image/webp">
      <img class="badge" src="/images/sbrfc-badge.png" alt="SBRFC shield badge, a rugby ball in front of the Santa Barbara mountains, palm trees, and ocean" width="380" height="438" loading="lazy" decoding="async">
    </picture>
    <div class="rule rule-center" role="presentation"></div>
    <h2>Our mission</h2>
    <p>The mission of the Santa&nbsp;Barbara Rugby Football Club is to promote the sport of rugby in our community by fostering athletic excellence, inclusivity, and personal development through teamwork, discipline, and sportsmanship. As a 501(c)(3) non-profit organization, we are committed to providing opportunities for youth and adults of all backgrounds to participate in and learn the game of rugby, supporting physical health, leadership, and lifelong community engagement.</p>
    <p class="status-line">Santa Barbara Rugby Football Club is a 501(c)(3) non-profit organization, EIN {EIN}, incorporated in California in 2023. Donations are tax-deductible to the extent allowed by law.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">What we do</span>
    <h2>We pay for the parts of rugby that people cannot</h2>
    <p class="lede">Rugby has been played in Santa Barbara since 1978. SBRFC is the registered non-profit behind the sport in this county. We raise money for rugby here and put it back into coaching, into the clubs, and into individual players who would otherwise have to stop.</p>

    <h3>Where the money goes</h3>
    <ul>
      <li><strong>Season dues for players who cannot pay them.</strong> Dues run $250 at the men's club and $150 at the women's club. When a player cannot cover that, SBRFC does, and the conversation stays between that player and the treasurer.</li>
      <li><strong>Scholarship places in youth rugby.</strong> No child in Santa Barbara should miss a season because of the registration fee, so the club backs scholarship support in the youth program.</li>
      <li><strong>Coaching.</strong> Qualified, certified coaching across all three clubs, funded properly rather than leaned on until a volunteer burns out.</li>
      <li><strong>Local player recruitment and retention.</strong> Finding people in this county who have never played, getting them to a first session, and keeping them in the sport season after season.</li>
      <li><strong>Club infrastructure.</strong> The standing costs a season carries before a ball is kicked.</li>
    </ul>

    <h3>How we are run</h3>
    <p>SBRFC is run by a volunteer board and has no paid staff and no office. Money comes from players and their families, from local businesses, and from a group of long-standing donors through the '78 Club. The club files with the IRS and the State of California every year and publishes those filings, and the treasurer will send a financial summary to anyone who asks.</p>
    <div class="btn-row">
      <a class="btn btn-secondary" href="/about">How the club is run</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">The rugby we support</span>
    <h2>Three clubs, every age, no experience needed</h2>
    <p>Between them, the three clubs SBRFC supports put rugby on a field in Santa Barbara most weeks of the year, for players from U8 upwards. None of them ask for experience. Most of the adults on a Santa Barbara roster had never touched a rugby ball before they walked on, and the youth club is built for children who are new to the game.</p>
    <p>They train at Elings Park, 1298 Las Positas Road, and Chase Palm Park, 323 East Cabrillo Boulevard. Both are public parks, and anyone is welcome to come and watch.</p>
    <div class="cards">

      <div class="card">
        <span class="kind">Men's Rugby</span>
        <h3>The Grunion</h3>
        <p>Santa Barbara's men's club, playing since 1978 and open to anyone 18 or over. Division 2 rugby, training twice a week at Elings Park through a pre-season that starts in November, then a Saturday fixture list from January to April.</p>
        <p>No tryout and no experience needed. Season dues are $250, and SBRFC covers them for players who cannot.</p>
        <a class="go" href="/mens">Grunion program details <span class="arrow">&#8594;</span></a>
      </div>

      <div class="card">
        <span class="kind">Women's Rugby</span>
        <h3>The Mermaids</h3>
        <p>Competitive women's rugby for players 18 and over, open to women and nonconforming players from Goleta, Santa Barbara and the neighboring cities. The Mermaids compete in the Southern California Senior Women's Division II.</p>
        <p>The club trains through the October to March season and keeps a lighter touch rugby program running over the summer. Dues are $150, with help available.</p>
        <a class="go" href="/womens">Mermaids program details <span class="arrow">&#8594;</span></a>
      </div>

      <div class="card">
        <span class="kind">Youth Rugby</span>
        <h3>The Stingrays</h3>
        <p>Youth rugby from U8 to U18, coached by a USA Rugby certified staff who put player safety at the center of every session. New players and new families are welcome at any point in the year.</p>
        <p>Pre-season training starts at Chase Palm Park in November and moves to Elings Park in December, with matches expected from mid-January.</p>
        <a class="go" href="/youth">Stingrays program details <span class="arrow">&#8594;</span></a>
      </div>

    </div>
    <div class="btn-row">
      <a class="btn btn-secondary" href="/play">Compare all three programs</a>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <h2>Every dollar stays in Santa Barbara County</h2>
    <p class="lede">SBRFC has no paid staff. What comes in goes back out to coaching, recruitment, club costs and dues assistance for players in this county. Volunteer hours do the same work, and the club needs both.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="{DONATE_URL}" target="_blank" rel="noopener noreferrer">Donate</a>
      <a class="btn btn-ghost" href="/support">Get involved</a>
    </div>
  </div>
</section>
''')

# ===========================================================================
# ABOUT
# ===========================================================================

page("about",
"About SBRFC — Our Mission, History and Non-Profit Status",
"The Santa Barbara Rugby Football Club is a 501(c)(3) non-profit, EIN 93-4659131, incorporated in California in 2023. Read our mission, our history since 1978, the clubs we support, and who leads the organization.",
active="/about", sitemap_priority="0.8",
body=f'''
<section class="page-head">
  <div class="wrap">
    <span class="eyebrow">About the club</span>
    <h1>The non-profit behind rugby in Santa Barbara</h1>
    <p class="lede">SBRFC exists so that rugby in this county has something permanent behind it: an organization that can receive tax-deductible gifts, support the clubs that play here, and outlast any one committee or generation of players.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">Our mission</span>
    <h2>Why the club exists</h2>
    <p>The mission of the Santa&nbsp;Barbara Rugby Football Club is to promote the sport of rugby in our community by fostering athletic excellence, inclusivity, and personal development through teamwork, discipline, and sportsmanship. As a 501(c)(3) non-profit organization, we are committed to providing opportunities for youth and adults of all backgrounds to participate in and learn the game of rugby, supporting physical health, leadership, and lifelong community engagement.</p>
    <p>In practice that mission is tested by a single question, asked of every decision: does this keep more people playing rugby in Santa Barbara? Paying a coach properly keeps more people playing. Covering the dues of a player who has just lost a job keeps that player on the field. Helping a family who cannot afford a youth season keeps a child in the sport. That is where the money and the volunteer hours go.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">Non-profit status</span>
    <h2>Our 501(c)(3) registration</h2>
    <p>The Santa Barbara Rugby Football Club is a non-profit organization recognized as tax-exempt under section 501(c)(3) of the Internal Revenue Code. Contributions to the club are tax-deductible to the extent allowed by law.</p>
    <div class="status-box">
      <h3>Organization details</h3>
      <dl class="facts">
        <div><dt>Legal name</dt><dd>{LEGAL_NAME}</dd></div>
        <div><dt>Tax status</dt><dd>501(c)(3) non-profit organization</dd></div>
        <div><dt>EIN / Tax ID</dt><dd>{EIN}</dd></div>
        <div><dt>Incorporated</dt><dd>California, 2023</dd></div>
        <div><dt>IRS determination</dt><dd>Tax exemption issued July 2025</dd></div>
        <div><dt>Mailing address</dt><dd>{ADDRESS}</dd></div>
        <div><dt>Contact</dt><dd><a href="mailto:{GENERAL_EMAIL}">{GENERAL_EMAIL}</a></dd></div>
      </dl>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">History</span>
    <h2>Rugby in Santa Barbara since 1978</h2>
    <p>The Grunion have played rugby in Santa Barbara since 1978, and the club was formally founded in 1980. The name is local: the California grunion is a small silver fish that comes ashore at night to spawn on Santa Barbara beaches, and the club took it as its own.</p>
    <p>The Grunion's best-known run came in the mid-2000s. The club reached the Division II Sweet 16 in Newport, Rhode Island in both 2004 and 2005. In 2006 it came through the Sweet 16 in Columbia, South Carolina and reached the Division II Final Four in San Diego, beating Montauk 35 to 3 in the semifinal before losing the national final to Pearl City, 32 to 5. The following season, playing Division I, the Grunion beat the Denver Barbarians and lost to the Cincinnati Wolfhounds. Photographs from those seasons are kept in the club's MERchives archive.</p>
    <p>Rugby in this county is broader now than it was then. The Stingrays, the youth club, were founded in 2010 and run age groups from U8 to U18. The Mermaids, the women's club, were founded in 2015 and play in the Southern California Senior Women's Division II. Between the three clubs there is rugby being played in Santa Barbara most weeks of the year.</p>
    <p>The Santa Barbara Rugby Football Club came last. It was set up in 2023 to support rugby in Santa Barbara, and the IRS issued its 501(c)(3) tax exemption in July 2025.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">What we do</span>
    <h2>How SBRFC supports rugby in this county</h2>
    <p>SBRFC is the registered non-profit behind rugby in Santa Barbara County. It receives tax-deductible donations and sponsorship on behalf of the sport here, and puts that money into coaching, into recruiting and keeping local players, and into individuals who would otherwise have to stop playing. Giving to SBRFC is giving to rugby in Santa Barbara rather than to one team.</p>
    <p>Three clubs play here, and SBRFC supports all three. Each of them is separately organized, with its own coaches, its own committee and its own competition, and each runs its own training, fixtures and registration. SBRFC's job is the funding and the paperwork that sit underneath all of it.</p>
    <h3>Where the money goes</h3>
    <ul>
      <li><strong>Player recruitment and retention.</strong> Bringing local players into the sport and keeping them in it season after season.</li>
      <li><strong>Coaching.</strong> Supporting qualified coaching at all three clubs rather than relying on a volunteer until they burn out.</li>
      <li><strong>Club infrastructure.</strong> The unglamorous costs a club carries before a ball is kicked.</li>
      <li><strong>Dues assistance.</strong> Season dues are $250 at the Grunion and $150 at the Mermaids. SBRFC covers them for players who cannot, and supports scholarship places in the youth club.</li>
    </ul>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">Leadership</span>
    <h2>Board and officers</h2>
    <p>SBRFC is run by a volunteer board of officers drawn from the rugby community in Santa Barbara.</p>
    <div class="status-box">
      <h3>SBRFC board</h3>
      <dl class="facts">
        <div><dt>President</dt><dd>Joseph King</dd></div>
        <div><dt>Vice President</dt><dd>James Buchanon</dd></div>
        <div><dt>Treasurer</dt><dd>Josh Timpe</dd></div>
        <div><dt>Secretary</dt><dd>Connor Worden</dd></div>
        <div><dt>Community Director</dt><dd>Jordan Killebrew</dd></div>
      </dl>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">Transparency</span>
    <h2>Where the money goes</h2>
    <p>SBRFC is small, volunteer-run, and funded by players, their families, local businesses and a group of long-standing donors. The club has no paid staff and no office.</p>
    <p>The club files with both the IRS and the State of California every year, and publishes those filings here. For the 2025 tax year SBRFC filed <strong>IRS Form 990-N</strong>, the e-Postcard for tax-exempt organizations whose gross receipts are normally under $50,000, which the IRS accepted on 17 February 2026. The club also filed California Form <strong>199N</strong> with the Franchise Tax Board for the same year.</p>
    <dl class="facts">
      <div><dt>2025 federal filing</dt><dd><a href="/documents/sbrfc-form-990n-2025.pdf">Form 990-N for tax year 2025 (PDF)</a>, accepted by the IRS 17 February 2026</dd></div>
      <div><dt>Public record</dt><dd><a href="https://projects.propublica.org/nonprofits/organizations/934659131" rel="noopener">SBRFC on ProPublica's Nonprofit Explorer</a></dd></div>
      <div><dt>IRS verification</dt><dd>Search EIN 93-4659131 in the IRS Tax Exempt Organization Search</dd></div>
      <div><dt>Anything else</dt><dd>Email the treasurer at <a href="mailto:{TREASURER}">{TREASURER}</a></dd></div>
    </dl>
    <div class="btn-row">
      <a class="btn btn-primary" href="/support#donate">Support the club</a>
      <a class="btn btn-secondary" href="/contact">Contact us</a>
    </div>
  </div>
</section>
''')

# ===========================================================================
# GET INVOLVED / DONATE
# ===========================================================================

page("support",
"Get Involved — Donate, Volunteer or Sponsor | SBRFC",
"Support rugby in Santa Barbara. Donate to the Santa Barbara Rugby Football Club, a 501(c)(3) non-profit, volunteer with a club, sponsor a team, or join the '78 Club legacy donor program.",
sitemap_priority="0.7",
body=f'''
<section class="page-head">
  <div class="wrap">
    <span class="eyebrow">Get involved</span>
    <h1>Rugby here runs on people who chip in</h1>
    <p class="lede">Money, time, or a business willing to put its name on a jersey. All three keep players on the field in Santa Barbara County, and the club needs all three.</p>
  </div>
</section>

<section id="donate">
  <div class="wrap">
    <span class="eyebrow">Donate</span>
    <h2>Give to SBRFC</h2>
    <p>The Santa Barbara Rugby Football Club is a 501(c)(3) non-profit organization, EIN {EIN}. Contributions are tax-deductible to the extent allowed by law.</p>
    <p>A gift to SBRFC is a gift to rugby in this county rather than to one team. It goes to what decides whether a club stays competitive rather than merely surviving: recruiting and keeping local players, coaching, and club infrastructure. It also goes straight to individual players, because SBRFC covers season dues for anyone who cannot, and backs scholarship places in the youth club.</p>

    <div class="btn-row">
      <a class="btn btn-primary" href="{DONATE_URL}" target="_blank" rel="noopener noreferrer">Donate to SBRFC</a>
    </div>
    <p class="callout-note" style="margin-top:1.2em"><strong>NOTE:</strong> <em>Our giving page runs on Zeffy, a fundraising service that is free to the club. At checkout Zeffy pre-fills an optional tip, 15% by default, about $15 on a $100 gift and $75 on a $500 one. That tip goes to <strong>Zeffy, not SBRFC</strong>, and it is not required. To skip it, click the tip box, choose <strong>Other</strong>, and enter <strong>$0</strong>.</em></p>

    <h3>Other ways to give</h3>
    <dl class="facts">
      <div><dt>By check</dt><dd>Payable to {LEGAL_NAME}, mailed to {ADDRESS}</dd></div>
      <div><dt>By conversation</dt><dd>Pledges, donor-advised funds, stock gifts and multi-year giving: email <a href="mailto:{TREASURER}">{TREASURER}</a></dd></div>
    </dl>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">Legacy giving</span>
    <h2>The '78 Club</h2>
    <p>The '78 Club is the legacy donor program, named for the year rugby started in this town. It is built for former players, families and supporters who want to give at a level that underwrites a season rather than a match, and it is where the most committed giving sits.</p>
    <p>Members are recognized on the club's patron wall, and gifts at every tier fund the same things: player recruitment and retention, coaching, and the infrastructure that keeps a club competitive.</p>
    <dl class="facts">
      <div><dt>Supporters' Union</dt><dd>$350 and above per year</dd></div>
      <div><dt>Second XV</dt><dd>$750 and above per year</dd></div>
      <div><dt>Founders' XV</dt><dd>$2,500 and above per year</dd></div>
    </dl>
    <p style="margin-top:1.4em">To pledge, ask questions, or arrange a giving conversation, email <a href="mailto:{TREASURER}">{TREASURER}</a>. Full details of the program, including the patron wall, are on the Grunion site at <a href="{CLUB78_URL}" rel="noopener">grunionrugby.com/the-78-club</a>.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">Volunteer</span>
    <h2>Give time instead</h2>
    <p>Amateur rugby is held together by people doing unpaid jobs badly needed and rarely noticed. If you have a few hours, the clubs can use them.</p>
    <ul>
      <li><strong>Match day.</strong> Setting up and breaking down pitches, running the sideline, keeping time and score, working the gate at home fixtures.</li>
      <li><strong>Youth support.</strong> Team management and touchline supervision for the Stingrays age groups. Volunteer requirements are handled through the youth club.</li>
      <li><strong>Events.</strong> The autumn kick-off, fundraisers, socials and the third half after home matches.</li>
      <li><strong>Behind the scenes.</strong> Photography, social media, newsletter, grant writing, bookkeeping and anything else a small non-profit needs and cannot afford to buy.</li>
    </ul>
    <p>You do not need to have played rugby to be useful here. Referees, team managers and volunteers can sign up on the <a href="/coach">coach and volunteer page</a>, which also has the Grunion's paid head coach job.</p>
    <div class="btn-row">
      <a class="btn btn-secondary" href="/coach">Offer to help</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">Sponsorship</span>
    <h2>Put your business behind a local team</h2>
    <p>Local sponsorship is what lets the clubs hold player costs down. Sponsors are named on kit, on the sideline, at socials and on the clubs' sites, and they are genuinely part of the season rather than a logo in a footer.</p>
    <p>The Grunion currently run front-of-shirt, kit partner, beer sponsor and social sponsor packages, and the Stingrays run club partner, kit partner and community partner packages alongside scholarship support for youth players. Packages, prices and an inquiry form are on the <a href="/sponsor">sponsorship page</a>.</p>
    <p>Current club sponsors include Baja Sharkeez, Rincon Brewery and Golden Rooster Transportation.</p>
    <p>To talk about sponsorship, email <a href="mailto:{TREASURER}">{TREASURER}</a>.</p>
    <div class="btn-row">
      <a class="btn btn-secondary" href="/sponsor">Sponsorship packages</a>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <h2>Every gift stays in Santa Barbara</h2>
    <p class="lede">SBRFC is a volunteer-run club. What comes in goes back out to coaching, recruitment, club costs and dues assistance for players in this county.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="{DONATE_URL}" target="_blank" rel="noopener noreferrer">Donate</a>
      <a class="btn btn-ghost" href="/about">How the club is run</a>
    </div>
  </div>
</section>
''')

# ===========================================================================
# NEWS & EVENTS
# ===========================================================================

page("news",
"News &amp; Events — Santa Barbara Rugby Football Club",
"What is happening in Santa Barbara rugby: recent club news, the 2026/27 season calendar for the Grunion, Mermaids and Stingrays, and where to find fixtures and results.",
sitemap_priority="0.6",
body=f'''
<section class="page-head">
  <div class="wrap">
    <span class="eyebrow">News and events</span>
    <h1>What is coming up</h1>
    <p class="lede">Three clubs, three overlapping seasons, and something on a field in Santa Barbara most weeks of the year. Fixture-by-fixture results live on each club's own site; this page is the calendar across all three.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Recent news</h2>
    <div class="timeline">

      <div class="entry">
        <span class="when">14 September 2026</span>
        <h3>431 photographs from the 2004 to 2006 playoff runs added to the archive</h3>
        <p>A batch of 431 photographs from a former player went into the Grunion's MERchives archive, covering the Division II Sweet 16 seasons of 2004 and 2005 in Newport, Rhode Island, and the 2006 run through Columbia, South Carolina to the Final Four in San Diego. They are live at <a href="https://grunionrugby.com/merchives" rel="noopener">grunionrugby.com/MERchives</a>.</p>
      </div>

      <div class="entry">
        <span class="when">22 August 2026 &middot; Elings Park</span>
        <h3>SB Sevens tournament</h3>
        <p>SBRFC hosted the 2026 SB Sevens tournament at Elings Park, closing out a summer of touch rugby at Chase Palm Park before the fifteens season opened in October.</p>
      </div>

      <div class="entry">
        <span class="when">12 August 2026 &middot; Funk Zone</span>
        <h3>Mermaids annual silent auction</h3>
        <p>The women's club held its annual silent auction at Validation Ale in the Funk Zone, one of the fundraisers that keeps season dues at $150 rather than something higher.</p>
      </div>

    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>The 2026/27 season</h2>
    <div class="timeline">

      <div class="entry">
        <span class="when">October 2026 to March 2027</span>
        <h3>Mermaids fifteens season</h3>
        <p>The women's season runs October through March in the Southern California Senior Women's Division II, with training Tuesday and Thursday evenings, 7 to 9PM, on Soccer Field 2 at Elings Park.</p>
      </div>

      <div class="entry">
        <span class="when">Friday 30 October 2026 &middot; Elings Park</span>
        <h3>Stingrays Halloween pre-season kick-off</h3>
        <p>From 4 to 7PM at Elings Park. Players, families, friends and newcomers are welcome for rugby games, a candy scavenger hunt, food for sale, drinks and a club fundraiser raffle. Costumes encouraged. This is the open event for any family thinking about youth rugby.</p>
      </div>

      <div class="entry">
        <span class="when">From Tuesday 3 November 2026 &middot; Elings Park</span>
        <h3>Grunion pre-season</h3>
        <p>Pre-season conditioning and skills for the men's club, training Tuesday and Thursday evenings from 7 to 9PM on the upper fields at Elings Park. After the holiday break, training is back on Tuesday 5 January. This is the easiest point in the year for a new player to start, before the first competitive fixture.</p>
      </div>

      <div class="entry">
        <span class="when">3 November to 3 December 2026 &middot; Chase Palm Park</span>
        <h3>Stingrays pre-season begins</h3>
        <p>Youth pre-season training runs Tuesday and Thursday, 4 to 5:15PM, for all age grades at Chase Palm Park.</p>
      </div>

      <div class="entry">
        <span class="when">8 December 2026 to 4 March 2027 &middot; Elings Park</span>
        <h3>Stingrays winter training block</h3>
        <p>Training moves to Soccer Field 1 at Elings Park, Tuesday and Thursday. U8 to U10 train 4 to 5PM and U12 to U14 train 4:30 to 6PM. U16 participation is still to be confirmed by the club.</p>
      </div>

      <div class="entry">
        <span class="when">16 January to 6 March 2027 &middot; provisional</span>
        <h3>Stingrays season</h3>
        <p>Estimated season dates for the youth club. Both are provisional and the season may start later in January. Match fixtures, opponents and kickoff times are confirmed by the club as the schedule is set.</p>
      </div>

      <div class="entry">
        <span class="when">January to April 2027</span>
        <h3>Grunion season</h3>
        <p>The men's Division 2 season, with Saturdays as match day and a fixture list of 13 or more matches against clubs across Southern California. Training continues Tuesday and Thursday evenings throughout.</p>
      </div>

      <div class="entry">
        <span class="when">April to September 2027 &middot; Chase Palm Park</span>
        <h3>Mermaids summer touch</h3>
        <p>Non-contact touch rugby on Tuesday and Thursday evenings from 5:30PM, plus a Wednesday evening session at 6PM. Open to anyone curious about the sport who is not ready to commit to a contact season.</p>
      </div>

    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Fixtures and results</h2>
    <p>Each club keeps its own fixture list and results, updated through the season.</p>
    <dl class="facts">
      <div><dt>Men's</dt><dd><a href="{GRUNION_URL}" rel="noopener">grunionrugby.com</a></dd></div>
      <div><dt>Women's</dt><dd><a href="{MERMAIDS_URL}" rel="noopener">sbwomensrugby.com</a></dd></div>
      <div><dt>Youth</dt><dd><a href="{STINGRAYS_URL}" rel="noopener">stingraysrfc.com</a></dd></div>
    </dl>
    <div class="btn-row">
      <a class="btn btn-primary" href="/play">Play rugby</a>
      <a class="btn btn-secondary" href="/contact">Contact the club</a>
    </div>
  </div>
</section>
''')

# ===========================================================================
# CONTACT
# ===========================================================================

page("contact",
"Contact SBRFC — Santa Barbara Rugby Football Club",
"Contact the Santa Barbara Rugby Football Club: email, mailing address, where our clubs train at Elings Park and Chase Palm Park, and who to reach for the men's, women's and youth programs.",
sitemap_priority="0.6",
body=f'''
<section class="page-head">
  <div class="wrap">
    <span class="eyebrow">Contact</span>
    <h1>Get in touch</h1>
    <p class="lede">Questions about playing, giving, sponsoring or volunteering all reach a real person. This is a volunteer club, so give it a day or two.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>The club</h2>
    <div class="status-box">
      <dl class="facts">
        <div><dt>Organization</dt><dd>{LEGAL_NAME}<br>A 501(c)(3) non-profit organization, EIN {EIN}</dd></div>
        <div><dt>General enquiries</dt><dd><a href="mailto:{GENERAL_EMAIL}">{GENERAL_EMAIL}</a><br>Playing, volunteering, press and anything else</dd></div>
        <div><dt>Giving and sponsorship</dt><dd><a href="mailto:{TREASURER}">{TREASURER}</a><br>Donations, the '78 Club, sponsorship and gifts</dd></div>
        <div><dt>Mailing address</dt><dd>{ADDRESS}</dd></div>
      </dl>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Who to contact about what</h2>
    <p>Each club handles its own players, training and registration, so the fastest answer usually comes from the club rather than from SBRFC.</p>
    <dl class="facts">
      <div><dt>Men's rugby</dt><dd><a href="mailto:{GRUNION_EMAIL}">{GRUNION_EMAIL}</a> &middot; <a href="/mens">Men's rugby page</a></dd></div>
      <div><dt>Women's rugby</dt><dd><a href="mailto:{MERMAIDS_EMAIL}">{MERMAIDS_EMAIL}</a> &middot; <a href="/womens">Women's rugby page</a></dd></div>
      <div><dt>Youth rugby</dt><dd><a href="mailto:{STINGRAYS_EMAIL}">{STINGRAYS_EMAIL}</a> &middot; <a href="/youth">Youth rugby page</a></dd></div>
      <div><dt>Donations and '78 Club</dt><dd><a href="mailto:{TREASURER}">{TREASURER}</a> &middot; <a href="/support#donate">Get Involved</a></dd></div>
      <div><dt>Sponsorship</dt><dd><a href="mailto:{TREASURER}">{TREASURER}</a> &middot; <a href="/sponsor">Sponsorship page</a></dd></div>
      <div><dt>Volunteering</dt><dd><a href="mailto:{GENERAL_EMAIL}">{GENERAL_EMAIL}</a> &middot; <a href="/coach">Coach or volunteer</a></dd></div>
      <div><dt>Dues assistance</dt><dd><a href="mailto:{TREASURER}">{TREASURER}</a></dd></div>
    </dl>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Where we play</h2>
    <p>Both training grounds are public parks with parking. Visitors are welcome on the touchline at training and at home matches, and there is nothing to pay to watch.</p>
    <div class="cards cards-2">
      <div class="card card-light">
        <span class="kind">Training and matches</span>
        <h3>Elings Park</h3>
        <p>1298 Las Positas Road<br>Santa Barbara, CA 93105</p>
        <p>The Grunion train on the upper fields. The Mermaids train on Soccer Field 2 in season, and the Stingrays have Soccer Field 1 through the winter block.</p>
        <a class="go" href="{ELINGS_MAP}" rel="noopener">Open in maps <span class="arrow">&#8594;</span></a>
      </div>
      <div class="card card-light">
        <span class="kind">Training</span>
        <h3>Chase Palm Park</h3>
        <p>323 East Cabrillo Boulevard<br>Santa Barbara, CA 93101</p>
        <p>Stingrays pre-season training in November, and Mermaids summer touch rugby from April to September.</p>
        <a class="go" href="{CHASE_MAP}" rel="noopener">Open in maps <span class="arrow">&#8594;</span></a>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Follow the clubs</h2>
    <p>SBRFC does not run social accounts of its own. Fixture changes, results and photographs are posted by each club to its own channels.</p>
    <dl class="facts">
      <div><dt>Grunion</dt><dd><a href="https://www.facebook.com/GrunionRugby" rel="noopener">Facebook</a> &middot; <a href="https://www.instagram.com/santabarbaragrunionrugby" rel="noopener">Instagram</a> &middot; <a href="{GRUNION_URL}" rel="noopener">grunionrugby.com</a></dd></div>
      <div><dt>Mermaids</dt><dd><a href="https://www.facebook.com/santabarbaramermaidrugby/" rel="noopener">Facebook</a> &middot; <a href="https://www.instagram.com/sbmermaidrugby/" rel="noopener">Instagram</a> &middot; <a href="https://www.tiktok.com/@sb.rugby" rel="noopener">TikTok</a> &middot; <a href="{MERMAIDS_URL}" rel="noopener">sbwomensrugby.com</a></dd></div>
      <div><dt>Stingrays</dt><dd><a href="https://www.facebook.com/SantaBarbaraYouthRugby" rel="noopener">Facebook</a> &middot; <a href="https://www.instagram.com/sbyouthrugby/" rel="noopener">Instagram</a> &middot; <a href="{STINGRAYS_URL}" rel="noopener">stingraysrfc.com</a></dd></div>
    </dl>
  </div>
</section>
''')

# ===========================================================================
# PRIVACY POLICY
# ===========================================================================

page("privacy",
"Privacy Policy — Santa Barbara Rugby Football Club",
"How the Santa Barbara Rugby Football Club handles information on sbrfc.com: what our sign-up forms collect and who sees it, how analytics and advertising cookies work, and how to ask us to delete your data.",
sitemap_priority="0.3",
body=f'''
<section class="page-head">
  <div class="wrap">
    <span class="eyebrow">Privacy</span>
    <h1>Privacy policy</h1>
    <p class="lede">This policy covers sbrfc.com, the website of the Santa Barbara Rugby Football Club. Last updated {PRIVACY_UPDATED}.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>The short version</h2>
    <p>SBRFC is a small volunteer-run non-profit. This site has no accounts, no login, no shop and no advertising on its pages. When you fill in one of our forms, what you send goes only to the club organizers who need it. We do not sell, rent or trade anyone's information, ever, and we do not buy it either. To have anything deleted, email <a href="mailto:{TREASURER}">{TREASURER}</a>.</p>

    <h3>What our forms collect</h3>
    <p>Some pages have short forms: to sign up to play (men's, women's, youth, or not sure yet), to ask about sponsorship, or to offer to coach, referee or volunteer. They ask for your name and email address, a phone number if you choose to give one, and a few details that depend on the form: your rugby experience, your child's age on the youth form (we do not ask for a child's name), your business on the sponsorship form, the roles and club you are interested in on the volunteer form, and any message you add.</p>
    <p>Each form also records how you found us when that information is available: the ad campaign or link that brought you to the site, Google's ad click identifier, and the page you arrived on. We use it to see which ads and pages bring people to rugby.</p>

    <h3>Who sees it</h3>
    <p>Form submissions are received and stored by Netlify, the company that hosts this website. We share each submission only with the organizers of the relevant club: men's sign-ups go to the Grunion, women's sign-ups to the Mermaids, youth sign-ups to the Stingrays, and sponsorship, volunteer and not-sure messages to SBRFC's volunteer officers, who pass them to a club only to help you get started. We use what you send to answer you and help you start playing or helping, and for nothing else.</p>

    <h3>Analytics and advertising cookies</h3>
    <p>sbrfc.com uses Google Analytics and the Google Ads tag on every page. Google Analytics sets cookies in your browser and records information such as the pages you view, roughly how long you spend on them, the type of device and browser you are using, and an approximate location derived from your IP address. We see this as aggregate statistics.</p>
    <p>The Google Ads tag sets cookies so Google can tell us when someone who clicked one of our ads goes on to send a form or visit a club's website. We use these cookies only to count which pages and ads work. We do not use them to identify individual visitors, and we do not run remarketing ads.</p>
    <p>If you would rather not be counted, Google publishes a browser opt-out add-on at <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener">tools.google.com/dlpage/gaoptout</a>, and most browsers offer their own cookie and tracking controls. Google explains how its advertising cookies work at <a href="https://policies.google.com/technologies/ads" rel="noopener">policies.google.com/technologies/ads</a>.</p>
    <p>Netlify also keeps standard server logs, which include IP addresses, for security and reliability purposes.</p>

    <h3>Seeing or deleting your information</h3>
    <p>To see, correct or delete anything you have sent us through a form or by email, write to <a href="mailto:{TREASURER}">{TREASURER}</a>. We will delete it from our records and from Netlify, and ask the club it went to to delete their copy.</p>

    <h3>Payments</h3>
    <p>We never ask for payment details on this site. Donations are handled by Zeffy on its own secure pages, under Zeffy's privacy policy, and card details never reach us or this website.</p>

    <h3>If you email us</h3>
    <p>When you write to an SBRFC address we keep your message and reply to it. We use what you tell us to answer your question, and for nothing else. We do not add you to a mailing list because you emailed us, and we do not pass your message to anyone outside the club unless you ask us to.</p>

    <h3>Donors</h3>
    <p>If you give to the club, we keep the records a non-profit is required to keep: who gave, how much, when, and how to send an acknowledgement and a receipt. Donor information is seen by the treasurer and by the officers who need it. It is not published, sold or shared, except where the law requires it. Donors recognized on the patron wall are listed by name only, and only if they have agreed to it.</p>

    <h3>Children</h3>
    <p>SBRFC supports a youth rugby club, so this deserves saying plainly. This website is not directed at children and does not knowingly collect information from anyone under 13. The youth sign-up form is for parents and guardians: it asks for a child's age, but not their name. Youth registration happens on the Stingrays' own registration site and through USA Rugby, each under its own policy, not here. If you believe a child's information has reached us through this site, write to us and we will delete it.</p>

    <h3>Links to other sites</h3>
    <p>This site links to the three clubs' own websites, to the Stingrays' registration site, to Zeffy, to map and social media services, and to public non-profit records. Once you follow one of those links you are on someone else's site, under their privacy policy, not this one.</p>

    <h3>Changes</h3>
    <p>If this policy changes we will update the date at the top of the page. Material changes will be described here rather than made quietly.</p>
    <p>{PRIVACY_UPDATED}: added the sign-up forms (described under What our forms collect and Who sees it), and the Google Ads tag now runs on every page rather than only the old landing page.</p>
    <p>2 October 2026: added the Google Ads tag on the rugby landing page.</p>

    <h3>Contact</h3>
    <p>Questions about this policy, or a request to see or delete anything we hold about you: <a href="mailto:{TREASURER}">{TREASURER}</a>, or write to {LEGAL_NAME}, {ADDRESS}.</p>
  </div>
</section>
''')

# ===========================================================================
# 404
# ===========================================================================

page("404",
"Page not found — SBRFC",
"That page could not be found on sbrfc.com. Use the links here to reach our programs, our About page, or the club contact details.",
noindex=True,
body='''
<section class="page-head">
  <div class="wrap">
    <span class="eyebrow">404</span>
    <h1>That page has gone into touch</h1>
    <p class="lede">The page you were looking for is not here. Everything on the site is one click away below.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Try one of these</h2>
    <ul>
      <li><a href="/play">Play rugby</a>: <a href="/mens">men's</a>, <a href="/womens">women's</a> and <a href="/youth">youth</a></li>
      <li><a href="/coach">Coach, referee or volunteer</a></li>
      <li><a href="/sponsor">Sponsor a team</a></li>
      <li><a href="/about">About SBRFC, our mission and non-profit status</a></li>
      <li><a href="/support">Get involved and donate</a></li>
      <li><a href="/news">News and events</a></li>
      <li><a href="/contact">Contact</a></li>
      <li><a href="/">Home</a></li>
    </ul>
  </div>
</section>
''')

# ===========================================================================
# SITEMAP (indexable pages only; thank-you pages and 404 are left out)
# ===========================================================================

urls = "\n".join(
    f"  <url>\n    <loc>{SITE}{path}</loc>\n    <lastmod>{RELEASE_DATE}</lastmod>\n    <priority>{prio}</priority>\n  </url>"
    for path, prio in sorted(SITEMAP, key=lambda x: -float(x[1])))
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
print(f"sitemap.xml              {len(SITEMAP)} urls")
