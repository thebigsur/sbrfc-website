#!/usr/bin/env python3
"""Builds the static sbrfc.com site. Header and footer are rendered into every
page as plain HTML so the site works with scripting disabled."""
import os, re

OUT = os.path.dirname(os.path.abspath(__file__))

LEGAL_NAME = "Santa Barbara Rugby Football Club"
EIN = "93-4659131"
ADDRESS = "2516 Mesa School Lane, Santa&nbsp;Barbara, CA&nbsp;93109"
GENERAL_EMAIL = "vicepresident@sbrfc.com"
TREASURER = "treasurer@sbrfc.com"
DONATE_URL = "https://www.zeffy.com/en-US/donation-form/sbrfc"
GA4_ID = "G-9RX9PHGCST"   # sbrfc.com property, GA account "Santa Barbara Rugby Football Club" under admin@sbrfc.com

NAV = [
    ("index.html",  "Home"),
    ("about.html",  "About"),
    ("programs.html", "Programs"),
    ("support.html", "Get Involved"),
    ("news.html",   "News"),
    ("contact.html", "Contact"),
]

def todo(text):
    return f'<span class="todo">[PLACEHOLDER: {text}]</span>'

def header(active, p):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links.append(f'<a href="{p}{href}"{cur}>{label}</a>')
    links.append(f'<a class="nav-donate" href="{DONATE_URL}" target="_blank" rel="noopener noreferrer">Donate</a>')
    nav = "\n        ".join(links)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{p}index.html">
      <picture>
        <source srcset="{p}images/sbrfc-mark.webp" type="image/webp">
        <img src="{p}images/sbrfc-mark.png" alt="" width="96" height="110">
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

def footer(p):
    return f'''<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <h2>Santa Barbara Rugby Football Club</h2>
      <p class="footer-status">A 501(c)(3) non-profit organization<br>
      EIN {EIN}</p>
      <p>{ADDRESS}<br>
      <a href="mailto:{GENERAL_EMAIL}">{GENERAL_EMAIL}</a></p>
    </div>
    <div>
      <h2>The Club</h2>
      <ul>
        <li><a href="{p}about.html">About SBRFC</a></li>
        <li><a href="{p}programs.html">Programs</a></li>
        <li><a href="{p}support.html">Get Involved</a></li>
        <li><a href="{p}news.html">News &amp; Events</a></li>
        <li><a href="{p}contact.html">Contact</a></li>
        <li><a href="{DONATE_URL}" target="_blank" rel="noopener noreferrer">Donate</a></li>
        <li><a href="{p}privacy.html">Privacy policy</a></li>
      </ul>
    </div>
    <div>
      <h2>Clubs We Support</h2>
      <ul>
        <li><a href="{p}programs/grunion.html">Grunion RFC, men's</a> &middot; <a href="https://grunionrugby.com/" rel="noopener">grunionrugby.com</a></li>
        <li><a href="{p}programs/mermaids.html">SB Mermaids, women's</a> &middot; <a href="https://www.sbwomensrugby.com/" rel="noopener">sbwomensrugby.com</a></li>
        <li><a href="{p}programs/stingrays.html">SB Stingrays, youth</a> &middot; <a href="https://stingraysrfc.com/" rel="noopener">stingraysrfc.com</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-legal">
    &copy; 2026 {LEGAL_NAME}. A 501(c)(3) non-profit organization, EIN {EIN}. Donations are tax-deductible to the extent allowed by law.
  </div>
</footer>'''

TOGGLE_JS = '''<script>
(function(){var b=document.querySelector('.nav-toggle'),n=document.getElementById('site-nav');
if(!b||!n)return;b.addEventListener('click',function(){var o=n.classList.toggle('open');
b.setAttribute('aria-expanded',o?'true':'false');b.textContent=o?'Close':'Menu';});})();
</script>'''

def analytics():
    if not GA4_ID:
        return ""
    return f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('js',new Date());gtag('config','{GA4_ID}');</script>'''

def page(filename, title, description, body, depth=0, noindex=False, head_extra=""):
    p = "../" * depth
    canonical = "https://sbrfc.com/" + ("" if filename == "index.html" else filename)
    robots = '\n<meta name="robots" content="noindex">' if noindex else ""
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">{robots}
<meta name="theme-color" content="#1C2B4B">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="{p}favicon.ico" sizes="48x48 32x32 16x16">
<link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
<link rel="preload" href="{p}fonts/vollkorn-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}styles.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Santa Barbara Rugby Football Club">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://sbrfc.com/images/sbrfc-logo.png">
{head_extra}{analytics()}
</head>
<body>
{header(filename if depth == 0 else "programs.html", p)}
<main id="main">
{body}
</main>
{footer(p)}
{TOGGLE_JS}
</body>
</html>
'''
    path = os.path.join(OUT, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(doc)
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    print(f"{filename:28s} {words:5d} words")

# ===========================================================================
# HOME
# ===========================================================================

page("index.html",
"SBRFC — Santa Barbara Rugby Football Club",
"The Santa Barbara Rugby Football Club is a 501(c)(3) non-profit that supports rugby in Santa Barbara County: the Grunion men's club, the Mermaids women's club, and the Stingrays youth club.",
head_extra='<link rel="preload" as="image" href="images/sbrfc-logo.webp" type="image/webp" fetchpriority="high">\n',
body=f'''
<section class="hero">
  <div class="wrap">
    <picture>
      <source srcset="images/sbrfc-logo.webp" type="image/webp">
      <img class="logo" src="images/sbrfc-logo.png" alt="SBRFC logo, a grunion, a mermaid, and stingrays around the letters SBRFC" width="860" height="860" fetchpriority="high">
    </picture>
    <div class="rule rule-center" role="presentation"></div>
    <p class="statement">Welcome to <strong>SBRFC</strong> <span class="full-name">(Santa&nbsp;Barbara Rugby Football Club)</span>, the 501(c)(3) non-profit for the promotion, encouragement, and extension of Rugby&nbsp;Union football in Santa&nbsp;Barbara County.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">What we do</span>
    <h2>The non-profit behind rugby in Santa Barbara</h2>
    <p class="lede">Rugby has been played in this town since 1978. SBRFC was incorporated in California in 2023 and granted 501(c)(3) status in 2026, for one purpose: to support the sport in Santa Barbara County and keep people playing it.</p>
    <p>SBRFC is not itself a team. Three independent clubs play here, and SBRFC supports all three. The Grunion play men's rugby, the Mermaids play women's rugby, and the Stingrays run youth rugby from U8 to U18. Each club runs its own coaching, training and fixtures.</p>
    <p>What SBRFC does is the part that costs money and carries no glamour. Support goes to what decides whether a club stays competitive rather than merely surviving: recruiting and keeping local players, coaching, and club infrastructure. It also goes to individual players. Season dues are $250 at the men's club and $150 at the women's club, and SBRFC covers them for anyone who cannot.</p>
    <p>None of the three clubs ask for experience. Most of the adults on a Santa Barbara roster had never touched a rugby ball before they walked onto the field, and the youth club is built for children who are new to the game. Turning up is the entire entry requirement.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">The clubs we support</span>
    <h2>Find the team that fits</h2>
    <div class="cards">

      <div class="card">
        <span class="kind">Men's Rugby</span>
        <h3>The Grunion</h3>
        <p>Santa Barbara's men's club, playing since 1978 and open to anyone 18 or over. The Grunion play Division 2 men's rugby, training twice a week at Elings Park through a pre-season from October to December, then a Saturday fixture list from January to April.</p>
        <p>No tryout and no experience needed. Season dues are $250, and SBRFC helps players who cannot cover them.</p>
        <a class="go" href="programs/grunion.html">Grunion program details <span class="arrow">&#8594;</span></a>
      </div>

      <div class="card">
        <span class="kind">Women's Rugby</span>
        <h3>The Mermaids</h3>
        <p>Competitive women's rugby for players 18 and over, open to women and nonconforming players from Goleta, Santa Barbara and the neighboring cities. The Mermaids compete in the Southern California Senior Women's Division II.</p>
        <p>The club trains through the October to March season and keeps a lighter touch rugby program running over the summer. Season dues are $150, with help available.</p>
        <a class="go" href="programs/mermaids.html">Mermaids program details <span class="arrow">&#8594;</span></a>
      </div>

      <div class="card">
        <span class="kind">Youth Rugby</span>
        <h3>The Stingrays</h3>
        <p>Youth rugby from U8 to U18, coached by a USA Rugby certified staff who put player safety at the center of every session. New players and new families are welcome at any point in the year.</p>
        <p>Pre-season training starts at Chase Palm Park in November and moves to Elings Park in December, with matches expected from mid-January.</p>
        <a class="go" href="programs/stingrays.html">Stingrays program details <span class="arrow">&#8594;</span></a>
      </div>

    </div>
  </div>
</section>

<section class="mission-band">
  <div class="wrap">
    <picture>
      <source srcset="images/sbrfc-badge.webp" type="image/webp">
      <img class="badge" src="images/sbrfc-badge.png" alt="SBRFC shield badge, a rugby ball in front of the Santa Barbara mountains, palm trees, and ocean" width="380" height="438" loading="lazy">
    </picture>
    <div class="rule rule-center" role="presentation"></div>
    <h2>Our mission</h2>
    <p>The mission of the Santa&nbsp;Barbara Rugby Football Club is to promote the sport of rugby in our community by fostering athletic excellence, inclusivity, and personal development through teamwork, discipline, and sportsmanship. As a 501(c)(3) non-profit organization, we are committed to providing opportunities for youth and adults of all backgrounds to participate in and learn the game of rugby, supporting physical health, leadership, and lifelong community engagement.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn-secondary" href="about.html">More about SBRFC</a>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <h2>Rugby in this town runs on people who chip in</h2>
    <p class="lede">Every dollar given to SBRFC goes back into coaching, recruitment and dues assistance for players in Santa Barbara County. Every volunteer hour does the same. There is room for both.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="{DONATE_URL}" target="_blank" rel="noopener noreferrer">Donate</a>
      <a class="btn btn-ghost" href="support.html">Get involved</a>
    </div>
  </div>
</section>
''')

# ===========================================================================
# ABOUT
# ===========================================================================

page("about.html",
"About SBRFC — Our Mission, History and Non-Profit Status",
"The Santa Barbara Rugby Football Club is a 501(c)(3) non-profit, EIN 93-4659131, incorporated in California in 2023. Read our mission, our history since 1978, the clubs we support, and who leads the organization.",
f'''
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
    <span class="eyebrow">Structure</span>
    <h2>How SBRFC and the clubs fit together</h2>
    <p>The Grunion, the Mermaids and the Stingrays are independent clubs. Each has its own coaches, its own committee, its own competition and its own culture, and each runs its own training, fixtures and registration. SBRFC does not run any of them.</p>
    <p>What SBRFC does is support them. It is the registered non-profit that can receive tax-deductible donations and sponsorship on behalf of rugby in this county and direct that money to the three clubs and to the players in them. When you give to SBRFC, you are giving to rugby in Santa Barbara rather than to one team.</p>
    <h3>Where that support goes</h3>
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
      <div><dt>2025 federal filing</dt><dd><a href="documents/sbrfc-form-990n-2025.pdf">Form 990-N for tax year 2025 (PDF)</a>, accepted by the IRS 17 February 2026</dd></div>
      <div><dt>Public record</dt><dd><a href="https://projects.propublica.org/nonprofits/organizations/934659131" rel="noopener">SBRFC on ProPublica's Nonprofit Explorer</a></dd></div>
      <div><dt>IRS verification</dt><dd>Search EIN 93-4659131 in the IRS Tax Exempt Organization Search</dd></div>
      <div><dt>Anything else</dt><dd>Email the treasurer at <a href="mailto:{TREASURER}">{TREASURER}</a></dd></div>
    </dl>
    <div class="btn-row">
      <a class="btn btn-primary" href="support.html#donate">Support the club</a>
      <a class="btn btn-secondary" href="contact.html">Contact us</a>
    </div>
  </div>
</section>
''')

# ===========================================================================
# PROGRAMS HUB
# ===========================================================================

page("programs.html",
"Programs — Men's, Women's and Youth Rugby in Santa Barbara",
"The three rugby clubs SBRFC supports: the Grunion men's club, the Mermaids women's club, and the Stingrays youth club for players U8 to U18. Training times, seasons, dues and how to join.",
f'''
<section class="page-head">
  <div class="wrap">
    <span class="eyebrow">Programs</span>
    <h1>Three ways to play rugby in Santa Barbara</h1>
    <p class="lede">Men's, women's and youth rugby, three independent clubs training on the same fields, all open to players who have never held a ball. Pick the one that fits and come to a session.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>What a rugby season looks like here</h2>
    <p>Rugby in Southern California is a winter and spring sport. The adult clubs use the autumn for pre-season conditioning and skills, then play competitive fixtures through the first months of the year, with matches on Saturdays and training on two weeknights. Youth rugby follows a similar shape, built around shorter sessions and age-appropriate contact.</p>
    <p>All three are club sides rather than school or college teams, which means you join as an individual, not through an institution. There are no tryouts for the adult clubs. Players arrive at wildly different levels of fitness and experience, and the coaching is built to absorb that.</p>
    <p>The clubs train at Elings Park, 1298 Las Positas Road, and Chase Palm Park, 323 East Cabrillo Boulevard. Both are public parks with parking and lighting.</p>
    <p>Season dues are $250 at the Grunion and $150 at the Mermaids. SBRFC covers dues for players who cannot, and supports scholarship places in the youth club. Nobody is kept out of rugby in this town over money.</p>

    <div class="cards" style="margin-top:2.4em">

      <div class="card">
        <span class="kind">Men's &middot; 18+</span>
        <h3>The Grunion</h3>
        <p>Santa Barbara's men's club since 1978, playing Division 2 men's rugby. Pre-season from October to December, competitive fixtures from January to April, training twice a week at Elings Park.</p>
        <p>Open to anyone 18 or over. No tryout and no experience required, which is how most of the current roster started. Dues $250.</p>
        <a class="go" href="programs/grunion.html">Full program details <span class="arrow">&#8594;</span></a>
      </div>

      <div class="card">
        <span class="kind">Women's &middot; 18+</span>
        <h3>The Mermaids</h3>
        <p>Competitive women's rugby in the Southern California Senior Women's Division II, with a season from October to March and a summer touch rugby program that keeps players on the field year round.</p>
        <p>Open to all women and nonconforming people aged 18 and over across Santa Barbara, Goleta and the neighboring cities. Dues $150.</p>
        <a class="go" href="programs/mermaids.html">Full program details <span class="arrow">&#8594;</span></a>
      </div>

      <div class="card">
        <span class="kind">Youth &middot; U8 to U18</span>
        <h3>The Stingrays</h3>
        <p>Youth rugby for boys and girls from U8 through U18, taught by USA Rugby certified coaches with player safety at the front of every session.</p>
        <p>Pre-season starts at Chase Palm Park in November and moves to Elings Park in December. New families are welcome at any point in the year.</p>
        <a class="go" href="programs/stingrays.html">Full program details <span class="arrow">&#8594;</span></a>
      </div>

    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>What you need to start</h2>
    <p>Less than people expect. For an adult session: boots, or trainers if you do not own boots yet, water, and a mouthguard. The clubs keep spare mouthguards for anyone who turns up without one. Everything else, including a jersey on match day, comes from the club.</p>
    <p>You do not need to be fit before you start, and you do not need to know the laws of the game. Both are learned at training, which is what training is for.</p>
    <div class="callout">
      <h3>Never played rugby?</h3>
      <p class="callout-note">That is the most common answer the clubs get, and it is not a disqualifier. Turn up to a session, say it is your first time, and someone will walk you through it.</p>
    </div>
    <div class="btn-row">
      <a class="btn btn-primary" href="contact.html">Ask a question</a>
      <a class="btn btn-secondary" href="news.html">See what is coming up</a>
    </div>
  </div>
</section>
''')

# ===========================================================================
# PROGRAM: GRUNION
# ===========================================================================

page("programs/grunion.html",
"Grunion RFC — Men's Rugby in Santa Barbara | SBRFC",
"The Grunion are Santa Barbara's men's rugby club, playing Division 2 since 1978. Training Tuesday and Thursday at Elings Park, pre-season October to December, fixtures January to April. Open to anyone 18 and over, no experience needed.",
f'''
<section class="page-head">
  <div class="wrap">
    <span class="eyebrow">Men's rugby &middot; 18 and over</span>
    <h1>The Grunion</h1>
    <p class="lede">Santa Barbara's men's rugby club, playing on this coast since 1978. No tryout, no experience required, and a place on the roster for anyone willing to turn up twice a week.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Who it is for</h2>
    <p>Anyone 18 or over. The roster runs from players in their first season to men who have been playing for years, and fitness levels vary just as widely. There is no tryout and nobody is cut for arriving out of shape.</p>
    <p>The most common answer new players give when asked how much rugby they have played is none at all. That is not a disqualifier. It is the origin story of most of the club, and the coaching group is set up to teach the game from the beginning: how to pass, how to tackle safely, and what is actually happening in a scrum or a lineout.</p>

    <h3>Season and competition</h3>
    <p>The Grunion play Division 2 men's rugby. Pre-season runs from October to December and is used for conditioning, skills and new-player onboarding. The competitive season runs from January to April, with Saturdays as match day and a fixture list of 13 or more matches against clubs across Southern California.</p>

    <h3>Training</h3>
    <p>The Grunion train Tuesday and Thursday evenings, 7 to 9PM, on the upper fields at Elings Park, every week of the season. Sessions run through pre-season and the season alike. Turn up a few minutes early for your first one and find a coach before the warm-up starts.</p>

    <h3>Dues</h3>
    <p>Season dues are $250. If that is the thing standing between you and a season, SBRFC provides assistance for players who cannot cover it. Email <a href="mailto:{TREASURER}">{TREASURER}</a>, and the conversation stays between you and the treasurer.</p>

    <dl class="facts">
      <div><dt>Who</dt><dd>Men, 18 and over. No experience required and no tryout.</dd></div>
      <div><dt>Competition</dt><dd>Division 2 men's rugby</dd></div>
      <div><dt>Training</dt><dd>Tuesday and Thursday, 7 to 9PM</dd></div>
      <div><dt>Where</dt><dd>Elings Park upper fields, 1298 Las Positas Road, Santa Barbara, CA 93105</dd></div>
      <div><dt>Pre-season</dt><dd>October to December</dd></div>
      <div><dt>Season</dt><dd>January to April, matches on Saturdays</dd></div>
      <div><dt>Fixtures</dt><dd>13 or more matches per season</dd></div>
      <div><dt>Dues</dt><dd>$250 per season, with assistance available from SBRFC</dd></div>
      <div><dt>Bring</dt><dd>Boots or trainers, water, mouthguard. The club has spare mouthguards.</dd></div>
      <div><dt>Contact</dt><dd><a href="mailto:grunionrugby@gmail.com">grunionrugby@gmail.com</a></dd></div>
    </dl>

    <h3>How to join</h3>
    <p>Come to a training session. There is no form to fill in before your first one and nothing to pay on the night. If you would rather say hello first, email <a href="mailto:grunionrugby@gmail.com">grunionrugby@gmail.com</a> and someone will tell you where to park and who to look for.</p>
    <p>To play in matches you register through USA Rugby, listing the club by name. The club will walk you through it when you are ready.</p>

    <div class="callout">
      <h3>More from the Grunion</h3>
      <p class="callout-note">The Grunion run their own site with fixtures, results, the club archive and a dedicated page for new players: <a href="https://grunionrugby.com/" rel="noopener">grunionrugby.com</a>. Prospective players can go straight to <a href="https://grunionrugby.com/play" rel="noopener">grunionrugby.com/play</a>.</p>
    </div>

    <div class="btn-row">
      <a class="btn btn-primary" href="../support.html#donate">Support the club</a>
      <a class="btn btn-secondary" href="../programs.html">All programs</a>
    </div>
  </div>
</section>
''', depth=1)

# ===========================================================================
# PROGRAM: MERMAIDS
# ===========================================================================

page("programs/mermaids.html",
"Santa Barbara Mermaids — Women's Rugby | SBRFC",
"The Santa Barbara Mermaids are the area's women's rugby club, competing in Southern California Senior Women's Division II. Season October to March, training at Elings Park, open to all women and nonconforming players 18 and over.",
f'''
<section class="page-head">
  <div class="wrap">
    <span class="eyebrow">Women's rugby &middot; 18 and over</span>
    <h1>The Santa Barbara Mermaids</h1>
    <p class="lede">Competitive women's rugby on the South Coast, open to all women and nonconforming people aged 18 and over, with no experience required.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Who it is for</h2>
    <p>The Mermaids are open to all women and nonconforming people aged 18 and over in Goleta, Santa Barbara and the neighboring cities. New players are welcome and no prior rugby is expected. The club keeps dedicated guidance for new players and an introduction to the basics of the game on its own site, so a first-timer is not asked to learn the laws from the sideline.</p>
    <p>The club was founded in 2015.</p>

    <h3>Season and competition</h3>
    <p>The Mermaids compete in the Southern California Senior Women's Division II. The competitive fifteens season runs from October through March, with training on two weeknights and fixtures against clubs across the region.</p>
    <p>Over the summer, from April to September, the club shifts to touch rugby and lighter sessions. Touch is non-contact, forgiving on the body and the single easiest way for someone curious about the sport to try it without committing to a full contact season.</p>

    <h3>Training</h3>
    <p>In season, from October to March, the Mermaids train Tuesday and Thursday evenings from 7 to 8:30PM on Soccer Field 2 at Elings Park.</p>
    <p>Over the summer, from April to September, touch rugby runs Tuesday and Thursday evenings from 5:30PM until sunset at Chase Palm Park, with a practice session on Wednesday evenings at 6PM. The club also runs Monday track workouts at SBCC and UCSB, with current details posted to the club's Discord.</p>

    <h3>Dues</h3>
    <p>Season dues are $150. SBRFC provides assistance for players who cannot cover them. Email <a href="mailto:{TREASURER}">{TREASURER}</a> and it stays between you and the treasurer.</p>

    <dl class="facts">
      <div><dt>Who</dt><dd>All women and nonconforming people, 18 and over. No experience required.</dd></div>
      <div><dt>Founded</dt><dd>2015</dd></div>
      <div><dt>Competition</dt><dd>Southern California Senior Women's Division II</dd></div>
      <div><dt>Season</dt><dd>October to March</dd></div>
      <div><dt>In-season training</dt><dd>Tuesday and Thursday, 7 to 8:30PM, Elings Park Soccer Field 2</dd></div>
      <div><dt>Summer touch</dt><dd>April to September. Tuesday and Thursday from 5:30PM, plus Wednesday 6PM, at Chase Palm Park</dd></div>
      <div><dt>Track sessions</dt><dd>Mondays at SBCC and UCSB, details on the club Discord</dd></div>
      <div><dt>Dues</dt><dd>$150 per season, with assistance available from SBRFC</dd></div>
      <div><dt>Bring</dt><dd>Boots or trainers, water, mouthguard</dd></div>
      <div><dt>Contact</dt><dd><a href="mailto:santabarbararugby@gmail.com">santabarbararugby@gmail.com</a></dd></div>
    </dl>

    <h3>How to join</h3>
    <p>Email <a href="mailto:santabarbararugby@gmail.com">santabarbararugby@gmail.com</a>, or use the Become a Mermaid form on the club's own site. Summer touch is the lowest-commitment way in: turn up at Chase Palm Park on a summer evening, play, and decide about the contact season later.</p>

    <div class="callout">
      <h3>More from the Mermaids</h3>
      <p class="callout-note">The Mermaids run their own site with New Players and Rugby Basics sections, the fixture list and the current training schedule: <a href="https://www.sbwomensrugby.com/" rel="noopener">sbwomensrugby.com</a>. The joining form is at <a href="https://www.sbwomensrugby.com/join-us" rel="noopener">sbwomensrugby.com/join-us</a>.</p>
    </div>

    <div class="btn-row">
      <a class="btn btn-primary" href="../support.html#donate">Support the club</a>
      <a class="btn btn-secondary" href="../programs.html">All programs</a>
    </div>
  </div>
</section>
''', depth=1)

# ===========================================================================
# PROGRAM: STINGRAYS
# ===========================================================================

page("programs/stingrays.html",
"Santa Barbara Stingrays — Youth Rugby, U8 to U18 | SBRFC",
"The Santa Barbara Stingrays are the area's youth rugby club for players U8 to U18, coached by USA Rugby certified staff. Pre-season from November at Chase Palm Park, winter training at Elings Park, new families welcome.",
f'''
<section class="page-head">
  <div class="wrap">
    <span class="eyebrow">Youth rugby &middot; U8 to U18</span>
    <h1>The Santa Barbara Stingrays</h1>
    <p class="lede">Santa Barbara's youth rugby home since 2010. Certified coaching, a place for every player, and a welcoming club for new families.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Who it is for</h2>
    <p>Children and teenagers from U8 through U18. The Stingrays are a club side rather than a school team, so players join as individuals rather than through a school. New players are always welcome, and the club is built around the assumption that most families arrive knowing nothing about rugby.</p>
    <p>Rugby at youth level is taught in stages. The youngest age groups play non-contact or limited-contact forms of the game, and contact is introduced gradually as players get older.</p>

    <h3>Coaching and safety</h3>
    <p>The Stingrays coaching staff are USA Rugby certified and teach individual skills and team tactics with player safety at the heart of every session and every match. For a contact sport being learned by children, that is the part of the program that matters most, and it is the part the club leads with.</p>
    <p>Coaches and players are registered with USA Rugby, which carries the club's insurance, and the club follows a concussion protocol.</p>

    <h3>Season and training</h3>
    <p>The 2026/27 season opens with a Halloween kick-off party at Elings Park on Friday 30 October, from 4 to 7PM, which is open to newcomers as well as current families.</p>
    <p>Pre-season training runs from 3 November to 3 December, Tuesday and Thursday, 4 to 5:15PM for all age grades, at Chase Palm Park.</p>
    <p>From 8 December the club moves to Soccer Field 1 at Elings Park, booked through 4 March 2027. Tuesday and Thursday training there runs 4 to 5PM for U8 to U10 and 4:30 to 6PM for U12 to U14. U16 participation is still to be confirmed by the club.</p>
    <p>The season itself is estimated to run from 16 January to 6 March 2027. Both dates are provisional and the season may start later in January. Match fixtures, opponents and kickoff times are confirmed by the club as the schedule is set.</p>

    <dl class="facts">
      <div><dt>Who</dt><dd>Boys and girls, U8 through U18</dd></div>
      <div><dt>Founded</dt><dd>2010</dd></div>
      <div><dt>Coaching</dt><dd>USA Rugby certified staff</dd></div>
      <div><dt>Kick-off party</dt><dd>Friday 30 October 2026, 4 to 7PM, Elings Park</dd></div>
      <div><dt>Pre-season</dt><dd>3 November to 3 December, Tuesday and Thursday, 4 to 5:15PM, Chase Palm Park</dd></div>
      <div><dt>Winter training</dt><dd>From 8 December, Elings Park Soccer Field 1. U8 to U10 4 to 5PM, U12 to U14 4:30 to 6PM</dd></div>
      <div><dt>Season</dt><dd>Estimated 16 January to 6 March 2027, provisional</dd></div>
      <div><dt>Registration</dt><dd>Through the Stingrays' own site. Email the club for the current season fee and for scholarship support.</dd></div>
      <div><dt>Bring</dt><dd>Boots or trainers, water, mouthguard</dd></div>
      <div><dt>Contact</dt><dd><a href="mailto:club@stingraysrfc.com">club@stingraysrfc.com</a></dd></div>
    </dl>

    <h3>How to join</h3>
    <p>Registration for the 2026/27 season is open on the Stingrays' own site. Email <a href="mailto:club@stingraysrfc.com">club@stingraysrfc.com</a> for current age-group and training details, or for anything a form cannot answer.</p>
    <p>Families who would rather meet the club before committing are welcome at the Halloween kick-off party, which is built around rugby games rather than assessment.</p>
    <p>The Stingrays run scholarship support for families who need help with the cost of a season, and SBRFC backs it. Ask the club about current needs, or email <a href="mailto:{TREASURER}">{TREASURER}</a>.</p>

    <div class="callout">
      <h3>More from the Stingrays</h3>
      <p class="callout-note">The Stingrays run their own site with fixtures, the gallery, coaching staff and registration: <a href="https://stingraysrfc.com/" rel="noopener">stingraysrfc.com</a>.</p>
    </div>

    <div class="btn-row">
      <a class="btn btn-primary" href="../support.html#donate">Support youth rugby</a>
      <a class="btn btn-secondary" href="../programs.html">All programs</a>
    </div>
  </div>
</section>
''', depth=1)

# ===========================================================================
# GET INVOLVED / DONATE
# ===========================================================================

page("support.html",
"Get Involved — Donate, Volunteer or Sponsor | SBRFC",
"Support rugby in Santa Barbara. Donate to the Santa Barbara Rugby Football Club, a 501(c)(3) non-profit, volunteer with a club, sponsor a team, or join the '78 Club legacy donor program.",
f'''
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
    <p style="margin-top:1.4em">To pledge, ask questions, or arrange a giving conversation, email <a href="mailto:{TREASURER}">{TREASURER}</a>. Full details of the program, including the patron wall, are on the Grunion site at <a href="https://grunionrugby.com/the-78-club" rel="noopener">grunionrugby.com/the-78-club</a>.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">Volunteer</span>
    <h2>Give time instead</h2>
    <p>Amateur rugby is held together by people doing unpaid jobs badly needed and rarely noticed. If you have a few hours, the clubs can use them.</p>
    <ul>
      <li><strong>Match day.</strong> Setting up and breaking down pitches, running the sideline, keeping time and score, working the gate at home fixtures.</li>
      <li><strong>Youth support.</strong> Assistant coaching, team management and touchline supervision for the Stingrays age groups. Coaching and volunteer requirements are handled through the youth club.</li>
      <li><strong>Events.</strong> The autumn kick-off, fundraisers, socials and the third half after home matches.</li>
      <li><strong>Behind the scenes.</strong> Photography, social media, newsletter, grant writing, bookkeeping and anything else a small non-profit needs and cannot afford to buy.</li>
    </ul>
    <p>You do not need to have played rugby to be useful here.</p>
    <div class="btn-row">
      <a class="btn btn-secondary" href="contact.html">Offer to help</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">Sponsorship</span>
    <h2>Put your business behind a local team</h2>
    <p>Local sponsorship is what lets the clubs hold player costs down. Sponsors are named on kit, on the sideline, at socials and on the clubs' sites, and they are genuinely part of the season rather than a logo in a footer.</p>
    <p>The Grunion currently run front-of-shirt, kit partner, beer sponsor and social sponsor packages, and the Stingrays run club partner, kit partner and community partner packages alongside scholarship support for youth players. The right fit depends on the business, so the club would rather have the conversation than publish a rate card.</p>
    <p>Current club sponsors include Baja Sharkeez, Rincon Brewery and Golden Rooster Transportation.</p>
    <p>To talk about sponsorship, email <a href="mailto:{TREASURER}">{TREASURER}</a>.</p>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <h2>Every gift stays in Santa Barbara</h2>
    <p class="lede">SBRFC is a volunteer-run club. What comes in goes back out to coaching, recruitment, club costs and dues assistance for players in this county.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="{DONATE_URL}" target="_blank" rel="noopener noreferrer">Donate</a>
      <a class="btn btn-ghost" href="about.html">How the club is run</a>
    </div>
  </div>
</section>
''')

# ===========================================================================
# NEWS & EVENTS
# ===========================================================================

page("news.html",
"News &amp; Events — Santa Barbara Rugby Football Club",
"What is happening in Santa Barbara rugby: recent club news, the 2026/27 season calendar for the Grunion, Mermaids and Stingrays, and where to find fixtures and results.",
f'''
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
        <p>A batch of 431 photographs from a former player went into the Grunion's MERchives archive, covering the Division II Sweet 16 seasons of 2004 and 2005 in Newport, Rhode Island, and the 2006 run through Columbia, South Carolina to the Final Four in San Diego. They are live at <a href="https://grunionrugby.com/MERchives" rel="noopener">grunionrugby.com/MERchives</a>.</p>
      </div>

      <div class="entry">
        <span class="when">22 August 2026 &middot; Elings Park</span>
        <h3>SB Sevens tournament</h3>
        <p>The Mermaids hosted the 2026 SB Sevens tournament at Elings Park, closing out a summer of touch rugby at Chase Palm Park before the fifteens season opened in October.</p>
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
        <p>The women's season runs October through March in the Southern California Senior Women's Division II, with training Tuesday and Thursday evenings, 7 to 8:30PM, on Soccer Field 2 at Elings Park.</p>
      </div>

      <div class="entry">
        <span class="when">October to December 2026</span>
        <h3>Grunion pre-season</h3>
        <p>Pre-season conditioning and skills for the men's club, training Tuesday and Thursday evenings from 7 to 9PM on the upper fields at Elings Park. This is the easiest point in the year for a new player to start, with three months of training before the first competitive fixture.</p>
      </div>

      <div class="entry">
        <span class="when">Friday 30 October 2026 &middot; Elings Park</span>
        <h3>Stingrays Halloween pre-season kick-off</h3>
        <p>From 4 to 7PM at Elings Park. Players, families, friends and newcomers are welcome for rugby games, a candy scavenger hunt, food for sale, drinks and a club fundraiser raffle. Costumes encouraged. This is the open event for any family thinking about youth rugby.</p>
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
      <div><dt>Men's</dt><dd><a href="https://grunionrugby.com/" rel="noopener">grunionrugby.com</a></dd></div>
      <div><dt>Women's</dt><dd><a href="https://www.sbwomensrugby.com/" rel="noopener">sbwomensrugby.com</a></dd></div>
      <div><dt>Youth</dt><dd><a href="https://stingraysrfc.com/" rel="noopener">stingraysrfc.com</a></dd></div>
    </dl>
    <div class="btn-row">
      <a class="btn btn-primary" href="programs.html">Program details</a>
      <a class="btn btn-secondary" href="contact.html">Contact the club</a>
    </div>
  </div>
</section>
''')

# ===========================================================================
# CONTACT
# ===========================================================================

page("contact.html",
"Contact SBRFC — Santa Barbara Rugby Football Club",
"Contact the Santa Barbara Rugby Football Club: email, mailing address, where our clubs train at Elings Park and Chase Palm Park, and who to reach for the men's, women's and youth programs.",
f'''
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
      <div><dt>Men's rugby</dt><dd><a href="mailto:grunionrugby@gmail.com">grunionrugby@gmail.com</a> &middot; <a href="programs/grunion.html">Grunion program page</a></dd></div>
      <div><dt>Women's rugby</dt><dd><a href="mailto:santabarbararugby@gmail.com">santabarbararugby@gmail.com</a> &middot; <a href="programs/mermaids.html">Mermaids program page</a></dd></div>
      <div><dt>Youth rugby</dt><dd><a href="mailto:club@stingraysrfc.com">club@stingraysrfc.com</a> &middot; <a href="programs/stingrays.html">Stingrays program page</a></dd></div>
      <div><dt>Donations and '78 Club</dt><dd><a href="mailto:{TREASURER}">{TREASURER}</a> &middot; <a href="support.html#donate">Get Involved</a></dd></div>
      <div><dt>Sponsorship</dt><dd><a href="mailto:{TREASURER}">{TREASURER}</a></dd></div>
      <div><dt>Volunteering</dt><dd><a href="mailto:{GENERAL_EMAIL}">{GENERAL_EMAIL}</a></dd></div>
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
        <a class="go" href="https://www.google.com/maps/search/?api=1&amp;query=Elings+Park%2C+1298+Las+Positas+Rd%2C+Santa+Barbara%2C+CA+93105" rel="noopener">Open in maps <span class="arrow">&#8594;</span></a>
      </div>
      <div class="card card-light">
        <span class="kind">Training</span>
        <h3>Chase Palm Park</h3>
        <p>323 East Cabrillo Boulevard<br>Santa Barbara, CA 93101</p>
        <p>Stingrays pre-season training in November, and Mermaids summer touch rugby from April to September.</p>
        <a class="go" href="https://www.google.com/maps/search/?api=1&amp;query=Chase+Palm+Park%2C+323+E+Cabrillo+Blvd%2C+Santa+Barbara%2C+CA" rel="noopener">Open in maps <span class="arrow">&#8594;</span></a>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Follow the clubs</h2>
    <p>SBRFC does not run social accounts of its own. Fixture changes, results and photographs are posted by each club to its own channels.</p>
    <dl class="facts">
      <div><dt>Grunion</dt><dd><a href="https://www.facebook.com/GrunionRugby" rel="noopener">Facebook</a> &middot; <a href="https://www.instagram.com/santabarbaragrunionrugby" rel="noopener">Instagram</a> &middot; <a href="https://grunionrugby.com/" rel="noopener">grunionrugby.com</a></dd></div>
      <div><dt>Mermaids</dt><dd><a href="https://www.facebook.com/santabarbaramermaidrugby/" rel="noopener">Facebook</a> &middot; <a href="https://www.instagram.com/sbmermaidrugby/" rel="noopener">Instagram</a> &middot; <a href="https://www.tiktok.com/@sb.rugby" rel="noopener">TikTok</a> &middot; <a href="https://www.sbwomensrugby.com/" rel="noopener">sbwomensrugby.com</a></dd></div>
      <div><dt>Stingrays</dt><dd><a href="https://www.facebook.com/SantaBarbaraYouthRugby" rel="noopener">Facebook</a> &middot; <a href="https://www.instagram.com/sbyouthrugby/" rel="noopener">Instagram</a> &middot; <a href="https://stingraysrfc.com/" rel="noopener">stingraysrfc.com</a></dd></div>
    </dl>
  </div>
</section>
''')

# ===========================================================================
# PRIVACY POLICY
# ===========================================================================

page("privacy.html",
"Privacy Policy — Santa Barbara Rugby Football Club",
"How the Santa Barbara Rugby Football Club handles information on sbrfc.com: what we collect, what we do not, how analytics and cookies work, and how to contact us about your data.",
f'''
<section class="page-head">
  <div class="wrap">
    <span class="eyebrow">Privacy</span>
    <h1>Privacy policy</h1>
    <p class="lede">This policy covers sbrfc.com, the website of the Santa Barbara Rugby Football Club. Last updated 23 September 2026.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>The short version</h2>
    <p>SBRFC is a small volunteer-run non-profit. This site has no accounts, no login, no shop and no advertising. We do not sell, rent or trade anyone's information, ever, and we do not buy it either.</p>

    <h3>What this site collects</h3>
    <p>sbrfc.com uses Google Analytics to understand how many people visit and which pages they read. Google Analytics sets cookies in your browser and records information such as the pages you view, roughly how long you spend on them, the type of device and browser you are using, and an approximate location derived from your IP address. We see this as aggregate statistics. We do not use it to identify individual visitors, and we have not enabled advertising or remarketing features.</p>
    <p>If you would rather not be counted, Google publishes a browser opt-out add-on at <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener">tools.google.com/dlpage/gaoptout</a>, and most browsers offer their own cookie and tracking controls.</p>
    <p>Our host, Netlify, keeps standard server logs, which include IP addresses, for security and reliability purposes.</p>

    <h3>What this site does not collect</h3>
    <p>There are no forms on sbrfc.com. We do not ask for your name, address, phone number or payment details anywhere on this site. Donations are handled by Zeffy on its own secure pages, under Zeffy's privacy policy, and card details never reach us or this website.</p>

    <h3>If you email us</h3>
    <p>When you write to an SBRFC address we keep your message and reply to it. We use what you tell us to answer your question, and for nothing else. We do not add you to a mailing list because you emailed us, and we do not pass your message to anyone outside the club unless you ask us to.</p>

    <h3>Donors</h3>
    <p>If you give to the club, we keep the records a non-profit is required to keep: who gave, how much, when, and how to send an acknowledgement and a receipt. Donor information is seen by the treasurer and by the officers who need it. It is not published, sold or shared, except where the law requires it. Donors recognized on the patron wall are listed by name only, and only if they have agreed to it.</p>

    <h3>Children</h3>
    <p>SBRFC supports a youth rugby club, so this deserves saying plainly. This website is not directed at children, has no forms, and does not knowingly collect information from anyone under 13. Youth registration happens on the Stingrays' own site and through USA Rugby, each under its own policy, not here. If you believe a child's information has somehow reached us through this site, write to us and we will delete it.</p>

    <h3>Links to other sites</h3>
    <p>This site links to the three clubs' own websites, to Zeffy, to map and social media services, and to public non-profit records. Once you follow one of those links you are on someone else's site, under their privacy policy, not this one.</p>

    <h3>Changes</h3>
    <p>If this policy changes we will update the date at the top of the page. Material changes will be described here rather than made quietly.</p>

    <h3>Contact</h3>
    <p>Questions about this policy, or a request to see or delete anything we hold about you: <a href="mailto:{GENERAL_EMAIL}">{GENERAL_EMAIL}</a>, or write to {LEGAL_NAME}, {ADDRESS}.</p>
  </div>
</section>
''')

# ===========================================================================
# 404
# ===========================================================================

page("404.html",
"Page not found — SBRFC",
"That page could not be found on sbrfc.com. Use the links here to reach our programs, our About page, or the club contact details.",
f'''
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
      <li><a href="index.html">Home</a></li>
      <li><a href="about.html">About SBRFC, our mission and non-profit status</a></li>
      <li><a href="programs.html">Programs</a>, including <a href="programs/grunion.html">the Grunion</a>, <a href="programs/mermaids.html">the Mermaids</a> and <a href="programs/stingrays.html">the Stingrays</a></li>
      <li><a href="support.html">Get Involved and donate</a></li>
      <li><a href="news.html">News and events</a></li>
      <li><a href="contact.html">Contact</a></li>
      <li><a href="privacy.html">Privacy policy</a></li>
    </ul>
  </div>
</section>
''')
