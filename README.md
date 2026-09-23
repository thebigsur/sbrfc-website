# SBRFC — Santa Barbara Rugby Football Club

Static site for sbrfc.com. No build step: Netlify publishes the repository root
and republishes automatically on every push to `main`.

## Structure

| File | Page |
| --- | --- |
| `index.html` | Home |
| `about.html` | About, mission, 501(c)(3) status, history, board |
| `programs.html` | Programs hub |
| `programs/grunion.html` | Men's rugby |
| `programs/mermaids.html` | Women's rugby |
| `programs/stingrays.html` | Youth rugby |
| `support.html` | Get Involved, donate, '78 Club, volunteer, sponsorship |
| `news.html` | News and events |
| `contact.html` | Contact |
| `404.html` | Not found |
| `styles.css` | Shared stylesheet for every page |
| `build.py` | Generates the HTML pages from shared header/footer templates |

The header and footer are written into every page as plain HTML so the site
works with scripting disabled. `build.py` is the source of truth for them: edit
the template or page content there and re-run `python3 build.py` rather than
editing the generated HTML by hand.

## Images

`images/` holds WebP with PNG fallbacks, sized for how they are displayed:

- `sbrfc-logo` 860px, hero
- `sbrfc-badge` 380px, mission band
- `sbrfc-mark` 96px, header

Originals are in the repository history. Re-export at the displayed size rather
than shipping full-resolution source files; the original 1254px logo was 1.3MB.

## Ad Grants notes

Google Ad Grants requires the whole site over HTTPS, no broken links, a clear
mission and visible non-profit status, and substantial original content on the
site itself. Keep `netlify.toml`, `sitemap.xml` and `robots.txt` in place, and
do not add third-party ads.
