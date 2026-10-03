# SBRFC — Santa Barbara Rugby Football Club

Static site for sbrfc.com. No build step on Netlify: it publishes the
repository root and republishes automatically on every push to `main`.

## Structure

| File | Page |
| --- | --- |
| `index.html` | Home |
| `play.html` | /play: hub for "play rugby" ads, three team cards, FAQ, sign-up form |
| `mens.html` | /mens: Grunion RFC, men's rugby |
| `womens.html` | /womens: Santa Barbara Mermaids, women's rugby |
| `youth.html` | /youth: Santa Barbara Stingrays, written for parents |
| `sponsor.html` | /sponsor: packages and inquiry form for local businesses |
| `coach.html` | /coach: coaches, referees, youth volunteers, team managers |
| `thanks-*.html` | Thank-you pages for each form (noindex, not in the sitemap) |
| `about.html` | About, mission, 501(c)(3) status, history, board |
| `support.html` | Get Involved: donate, '78 Club, volunteering, sponsorship |
| `news.html` | News and events |
| `contact.html` | Contact |
| `privacy.html` | Privacy policy |
| `404.html` | Not found |
| `styles.css` | Shared stylesheet for every page |
| `site.js` | Shared script: mobile menu, form helpers, Google Analytics events |
| `build.py` | Generates every HTML page and `sitemap.xml` |
| `_redirects` | 301s from the retired /landing and /programs URLs |

The header and footer are written into every page as plain HTML so the site
works with scripting disabled. `build.py` is the source of truth: edit the page
content there and re-run `python3 build.py` rather than editing the generated
HTML by hand. If you change `styles.css` or `site.js`, bump `ASSET_V` in
`build.py` so browsers fetch the new copy.

## Common edits

- **Youth "Upcoming" box** (on /youth and /thanks-youth): the `YOUTH_UPCOMING`
  list near the top of `build.py`. Each line has a date after which it hides
  itself, so past events drop off on their own.
- **Google Analytics / Google Ads IDs**: `GA4_ID`, `ADS_ID` and `ADS_CLUB_CLICK`
  in `build.py`. The Google tag is written once into every page's `<head>`.
- **Club contacts and links**: the CLUB CONTACTS block in `build.py`.

## Forms (Netlify Forms)

Six forms, each posting to its own thank-you page:

| Form name | Page | Thank-you page |
| --- | --- | --- |
| `mens-interest` | /mens (and /play, Men's) | /thanks-mens |
| `womens-interest` | /womens (and /play, Women's) | /thanks-womens |
| `youth-interest` | /youth (and /play, Youth) | /thanks-youth |
| `general-interest` | /play (Not sure, or scripting off) | /thanks-play |
| `sponsor-inquiry` | /sponsor | /thanks-sponsor |
| `coach-signup` | /coach | /thanks-coach |

- The four player forms share identical field names (`name`, `email`, `phone`,
  `experience`, `child_age`, `message`, `team`), which is what lets /play send
  a sign-up to any of them: `site.js` switches the hidden `form-name` and the
  form `action` to match the "Which team?" choice. With scripting off, /play
  submits as `general-interest`.
- Every form carries hidden `utm_source`, `utm_medium`, `utm_campaign`,
  `gclid` and `landing_page` fields, filled by `site.js` from the ad visit.
- Every form has a honeypot field (`bot-field`).
- **Do not rename the /thanks-* pages or turn the forms into AJAX
  submissions.** The thank-you page load is the conversion that Google Ads and
  Google Analytics count.
- Netlify files test-looking submissions ("Test", "asdf") as spam and sends no
  notification for them. Check a form's Spam filter before assuming it is broken.

## Analytics events (GA4)

Fired from `site.js`, and silent if the Google tag is missing or blocked:

- `player_signup` (param `team`: mens, womens, youth, general) on each player thank-you page
- `sponsor_inquiry` on /thanks-sponsor, `coach_signup` on /thanks-coach
- `contact_click` (params `method`, `page`) on any tel:, sms: or mailto: click
- `youth_register_click` on clicks to rugby-register.vercel.app
- `club_site_click` (param `club`) on clicks to grunionrugby.com,
  sbwomensrugby.com or stingraysrfc.com, which also fires the Google Ads
  conversion that the old /landing page used

## Images

`images/` holds WebP with PNG or JPG fallbacks, sized for how they are displayed:

- `sbrfc-logo` 860px, home hero; `sbrfc-badge` 380px; `sbrfc-mark` 96px, header
- `photos/` team photos from the Grunion, Mermaids and Stingrays sites, at two widths each
- `og/` 1200x630 share images for the new pages
- `sponsors/` current sponsor logos for /sponsor

Re-export at the displayed size rather than shipping full-resolution files.

## Ad Grants notes

Google Ad Grants requires the whole site over HTTPS, no broken links, a clear
mission and visible non-profit status, and substantial original content on the
site itself. Keep `netlify.toml`, `sitemap.xml` and `robots.txt` in place, and
do not add third-party ads. Point ads at https://sbrfc.com/play, /mens,
/womens, /youth, /sponsor and /coach (no www; www redirects to the bare domain).
