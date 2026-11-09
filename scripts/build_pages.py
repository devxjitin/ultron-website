"""Builds the connector pages (dist/connectors/index.html and one page per connector) from data/connectors.json
(extracted from the Android app) and the hand-written copy in scripts/usecases.py.

Run from the site folder:  python scripts/build_pages.py
The output is plain HTML committed under dist/, so the site stays static and needs no build on deploy.
"""
import json
from html import escape as e
from pathlib import Path

from usecases import ACCESS_TEXT, CONNECTORS, TOOLS

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
V = "20261113"
SITE = "https://ultron.devxjitin.dev"
DOWNLOAD = "https://api.devxjitin.dev/v1/releases/download"

conns = json.loads((ROOT / "data" / "connectors.json").read_text(encoding="utf-8"))
ORDER = ["Essentials", "Search and media", "Personal data", "Phone control"]
CAT_NOTE = {
    "Essentials": "Everyday phone info and controls. Nothing here reads your personal data.",
    "Search and media": "Web search, web pages, YouTube and pictures.",
    "Personal data": "Reads private data from your phone, such as contacts, calendar, location, files and notifications. What you ask about is sent to Gemini.",
    "Phone control": "Lets Ultron operate other apps through Android accessibility. It can tap, type and read the screen, so turn it on only if you understand that.",
}
ICON = {
    "device_info": "i-chart", "device_controls": "i-flash", "alarms": "i-clock", "reminders": "i-bell", "apps_settings": "i-grid",
    "weather": "i-sun", "duckduckgo": "i-search", "web_reader": "i-globe", "youtube": "i-play", "youtube_downloads": "i-down",
    "calendar": "i-cal", "contacts": "i-user", "calls": "i-phone", "location": "i-pin", "files": "i-files", "images": "i-img",
    "app_usage": "i-chart", "notifications": "i-msg", "navigation": "i-compass", "screen": "i-touch",
}
ICONS_SVG = Path(DIST / "index.html").read_text(encoding="utf-8").split("<defs>")[1].split("</defs>")[0]

for c in conns:
    c["copy"] = CONNECTORS[c["id"]]
    for t in c["tools"]:
        t["say"] = TOOLS[t["fn"]]
missing = [t["fn"] for c in conns for t in c["tools"] if t["fn"] not in TOOLS]
assert not missing, missing

NAV = [("Features", "/#features"), ("Connectors", "/connectors/"), ("Skills", "/#skills"), ("Plans", "/#pricing"), ("FAQ", "/#faq")]


def head(title, desc, path):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0d0c0c">
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<title>{e(title)}</title>
<link rel="icon" href="/assets/mark.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;600&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/styles.css?v={V}">
<link rel="stylesheet" href="/pages.css?v={V}">
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{ICONS_SVG}</defs></svg>
<div id="progress" aria-hidden="true"></div>
<a class="skip" href="#main">Skip to content</a>
<header class="nav-wrap">
<nav class="nav" aria-label="Main">
<a class="brand" href="/"><img src="/assets/mark.svg" alt="" width="28" height="28">Ultron</a>
<div class="nav-links" id="nav-links">
{''.join(f'<a href="{h}"{" class=on" if h == "/connectors/" else ""}>{n}</a>' for n, h in NAV)}
</div>
<a class="btn btn-sm" href="{DOWNLOAD}" download rel="nofollow">Download APK</a>
<button class="menu-toggle" aria-label="Open navigation" aria-controls="nav-links" aria-expanded="false"><span></span><span></span></button>
</nav>
</header>
<main id="main">
"""


def foot():
    return f"""</main>
<section class="cta" id="contact">
<div class="cta-in wrap rv"><h2>Ready to try it?</h2><p>Download the app, then pick a plan. Your activation key arrives by email.</p>
<div class="cta-row"><a class="btn" href="{DOWNLOAD}" download rel="nofollow">Download APK</a><a class="btn btn-ghost" href="/#pricing">See plans</a></div></div>
<footer class="foot wrap"><span>Built by Jitin Kumar Sengar and Sonia</span><nav><a href="/connectors/">Connectors</a><a href="/#pricing">Pricing</a><a href="/#install">Install</a><a href="/#faq">FAQ</a><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a></nav><button class="motion" aria-pressed="false">Pause motion</button></footer>
</section>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="/page.js?v={V}" defer></script>
</body>
</html>
"""


def icon(cid):
    return f'<svg class="ic"><use href="#{ICON[cid]}"/></svg>'


def chips(c):
    out = [f'<span class="chip">{e(c["cat"])}</span>',
           f'<span class="chip">Runs on: {e(c["runs"])}</span>',
           f'<span class="chip {"on" if c["on"] else ""}">{"On for a fresh install" if c["on"] else "Off until you add it"}</span>']
    return "".join(out)


def connector_page(c, prev, nxt):
    cp = c["copy"]
    scenes = "".join(f"""<article class="uc rv" style="--d:{i * .08}s">
<small>{e(s)}</small>
<p class="uc-say"><span>You say</span>{e(q)}</p>
<p class="uc-does"><span>Ultron</span>{e(a)}</p>
</article>""" for i, (s, q, a) in enumerate(cp["scenes"]))
    tools = "".join(f"""<li class="tool rv"><div><h3>{e(t["label"])}</h3><p>{e(t["hint"])}</p></div><p class="try"><span>Try saying</span>{e(t["say"])}</p></li>""" for t in c["tools"])
    access = ACCESS_TEXT[c["access"]]
    needs = c["needs"]
    body = head(f'{c["name"]} connector | Ultron', f'{cp["lead"]} {c["desc"]}', f'/connectors/{c["id"]}.html') + f"""
<section class="page-hero wrap">
<p class="crumb"><a href="/connectors/">Connectors</a><span>/</span>{e(c["cat"])}</p>
<div class="ph-row"><span class="ph-ic">{icon(c["id"])}</span><h1>{e(c["name"])}</h1></div>
<p class="lead">{e(cp["lead"])}</p>
<div class="chips">{chips(c)}</div>
<div class="cta-row"><a class="btn" href="{DOWNLOAD}" download rel="nofollow">Download APK</a><a class="btn btn-ghost" href="#tools">See all {len(c["tools"])} tool{"s" if len(c["tools"]) != 1 else ""}</a></div>
</section>

<section class="section wrap">
<div class="head rv"><h2>Why you will want it</h2><p>{e(cp["why"])}</p></div>
<div class="ucs">{scenes}</div>
</section>

<section class="section wrap" id="tools">
<div class="head rv"><h2>{"Every tool" if len(c["tools"]) > 1 else "The tool"} in this connector</h2><p>{e(c["about"])} Ultron picks the right tool from what you say, so you never have to name one.</p></div>
<ul class="tools">{tools}</ul>
</section>

<section class="section wrap narrow">
<div class="head rv"><h2>Access and privacy</h2></div>
<dl class="facts rv">
<div><dt>Needs</dt><dd>{e(needs)}</dd></div>
<div><dt>Runs on</dt><dd>{e(c["runs"])}</dd></div>
<div><dt>Privacy</dt><dd>{e(c["privacy"])}</dd></div>
<div><dt>Default</dt><dd>{"On for a fresh install." if c["on"] else "Off. You turn it on from the Connectors page in the app."}</dd></div>
</dl>
{('<p class="warn rv">' + e(CAT_NOTE[c["cat"]]) + '</p>') if c["cat"] in ("Phone control", "Personal data") else ''}
</section>

<nav class="pn wrap" aria-label="More connectors">
<a href="/connectors/{prev["id"]}.html"><small>Previous</small>{e(prev["name"])}</a>
<a href="/connectors/" class="all">All connectors</a>
<a href="/connectors/{nxt["id"]}.html"><small>Next</small>{e(nxt["name"])}</a>
</nav>
""" + foot()
    return body


def hub_page():
    total_tools = sum(len(c["tools"]) for c in conns)
    groups = ""
    for cat in ORDER:
        items = [c for c in conns if c["cat"] == cat]
        cards = "".join(f"""<a class="ccard rv" href="/connectors/{c["id"]}.html" style="--d:{i % 3 * .07}s">
<span class="ph-ic">{icon(c["id"])}</span>
<h3>{e(c["name"])}</h3>
<p>{e(c["copy"]["lead"])}</p>
<small>{len(c["tools"])} tool{"s" if len(c["tools"]) != 1 else ""} · {"on by default" if c["on"] else "off by default"}<svg class="ic"><use href="#i-arrow"/></svg></small>
</a>""" for i, c in enumerate(items))
        groups += f"""<section class="section wrap cgroup">
<div class="head rv"><h2>{e(cat)}</h2><p>{e(CAT_NOTE[cat])}</p></div>
<div class="cgrid2">{cards}</div>
</section>"""
    return head("Ultron connectors and tools", f"{len(conns)} connectors and {total_tools} tools. See what each one does, what to say to use it, and what access it needs.", "/connectors/") + f"""
<section class="page-hero wrap">
<p class="crumb"><a href="/">Ultron</a><span>/</span>Connectors</p>
<h1>{len(conns)} connectors, {total_tools} tools. Every one explained.</h1>
<p class="lead">A connector is a bundle of tools for one job, like Calendar or YouTube Downloads. Open any of them to see what it does, what to say to use it, and exactly what access it needs. Risky ones stay off until you switch them on.</p>
<div class="cta-row"><a class="btn" href="{DOWNLOAD}" download rel="nofollow">Download APK</a><a class="btn btn-ghost" href="/#pricing">See plans</a></div>
</section>
{groups}
""" + foot()


def main():
    out = DIST / "connectors"
    out.mkdir(exist_ok=True)
    # keep a stable, readable order inside the previous/next links: the same order as the hub
    seq = [c for cat in ORDER for c in conns if c["cat"] == cat]
    (out / "index.html").write_text(hub_page(), encoding="utf-8", newline="\n")
    for i, c in enumerate(seq):
        (out / f'{c["id"]}.html').write_text(connector_page(c, seq[i - 1], seq[(i + 1) % len(seq)]), encoding="utf-8", newline="\n")
    sm = ["/", "/connectors/"] + [f'/connectors/{c["id"]}.html' for c in seq]
    urls = "".join(f"<url><loc>{SITE}{p}</loc></url>" for p in sm + ["/privacy.html", "/terms.html"])
    (DIST / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n',
        encoding="utf-8", newline="\n")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8", newline="\n")
    print(len(seq), "connector pages written")
    return sm


if __name__ == "__main__":
    main()
