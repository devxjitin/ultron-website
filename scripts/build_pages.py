"""Builds the Docs section (dist/docs/...) from data/connectors.json (extracted from the Android app), the hand-written
copy in scripts/usecases.py (connectors) and scripts/docs_content.py (getting started, features, skills).

Run from the site folder:  python scripts/build_pages.py
The output is plain HTML committed under dist/, so the site stays static and needs no build on deploy.
"""
import json
import shutil
from html import escape as e
from pathlib import Path

from docs_content import FEATURES, GETTING_STARTED, SKILLS
from usecases import ACCESS_TEXT, CONNECTORS, TOOLS

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
DOCS = DIST / "docs"
V = "20261114"
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
ICONS_SVG = (DIST / "index.html").read_text(encoding="utf-8").split("<defs>")[1].split("</defs>")[0]

for c in conns:
    c["copy"] = CONNECTORS[c["id"]]
    for t in c["tools"]:
        t["say"] = TOOLS[t["fn"]]
seq = [c for cat in ORDER for c in conns if c["cat"] == cat]


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
<a href="/">Home</a><a href="/#features">Features</a><a href="/#connectors">Connectors</a><a href="/#pricing">Plans</a><a href="/docs/" class="on">Docs</a>
</div>
<a class="btn btn-sm" href="{DOWNLOAD}" download rel="nofollow">Download APK</a>
<button class="menu-toggle" aria-label="Open navigation" aria-controls="nav-links" aria-expanded="false"><span></span><span></span></button>
</nav>
</header>
"""


def foot():
    return f"""<section class="cta" id="contact">
<div class="cta-in wrap rv"><h2>Ready to try it?</h2><p>Download the app, then pick a plan. Your activation key arrives by email.</p>
<div class="cta-row"><a class="btn" href="{DOWNLOAD}" download rel="nofollow">Download APK</a><a class="btn btn-ghost" href="/#pricing">See plans</a></div></div>
<footer class="foot wrap"><span>Built by Jitin Kumar Sengar and Sonia</span><nav><a href="/docs/">Docs</a><a href="/#pricing">Pricing</a><a href="/#install">Install</a><a href="/#faq">FAQ</a><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a></nav><button class="motion" aria-pressed="false">Pause motion</button></footer>
</section>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="/page.js?v={V}" defer></script>
</body>
</html>
"""


def icon(name):
    return f'<svg class="ic"><use href="#{name}"/></svg>'


def sidebar(current):
    def a(href, text, extra=""):
        cur = ' aria-current="page"' if href == current else ""
        return f'<a href="{href}"{cur}{extra}>{e(text)}</a>'

    out = ['<aside class="dside" aria-label="Docs"><details class="dside-m" open><summary>Docs menu</summary><div class="dside-in">']
    out.append(a("/docs/", "Overview") + a("/docs/getting-started.html", "Getting started"))
    out.append('<h4>Features</h4>' + "".join(a(f"/docs/features/{f['slug']}.html", f["name"]) for f in FEATURES))
    out.append(a("/docs/skills.html", "Skills").replace("<a", '<a class="solo"', 1))
    out.append(f'<h4>Connectors</h4>{a("/docs/connectors/", "All connectors")}')
    for cat in ORDER:
        items = [c for c in conns if c["cat"] == cat]
        is_open = " open" if any(f"/docs/connectors/{c['id']}.html" == current for c in items) or current == "/docs/connectors/" else ""
        out.append(f'<details class="dcat"{is_open}><summary>{e(cat)}</summary>' + "".join(a(f"/docs/connectors/{c['id']}.html", c["name"]) for c in items) + "</details>")
    out.append("</div></details></aside>")
    return "".join(out)


def page(title, desc, path, crumbs, inner, pn=None):
    crumb = '<p class="crumb">' + "<span>/</span>".join(f'<a href="{h}">{e(t)}</a>' if h else e(t) for t, h in crumbs) + "</p>"
    prev_next = ""
    if pn:
        p, n = pn
        prev_next = f'<nav class="pn" aria-label="Previous and next"><a href="{p[1]}"><small>Previous</small>{e(p[0])}</a><a href="{n[1]}"><small>Next</small>{e(n[0])}</a></nav>'
    return head(title, desc, path) + f"""<main id="main" class="docs wrap">
{sidebar(path)}
<article class="dmain">
{crumb}
{inner}
{prev_next}
</article>
</main>
""" + foot()


def scenes_html(scenes):
    return '<div class="ucs">' + "".join(f"""<article class="uc rv" style="--d:{i * .08}s">
<small>{e(s)}</small>
<p class="uc-say"><span>You say</span>{e(q)}</p>
<p class="uc-does"><span>Ultron</span>{e(a)}</p>
</article>""" for i, (s, q, a) in enumerate(scenes)) + "</div>"


def how_html(items):
    return '<ul class="how">' + "".join(f'<li class="rv"><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in items) + "</ul>"


def notes_html(notes):
    return "".join(f'<p class="warn rv">{e(n)}</p>' for n in notes)


def connector_page(c, p, n):
    cp = c["copy"]
    chips = (f'<span class="chip">{e(c["cat"])}</span><span class="chip">Runs on: {e(c["runs"])}</span>'
             f'<span class="chip {"on" if c["on"] else ""}">{"On for a fresh install" if c["on"] else "Off until you add it"}</span>')
    tools = "".join(f"""<li class="tool rv"><div><h3>{e(t["label"])}</h3><p>{e(t["hint"])}</p></div><p class="try"><span>Try saying</span>{e(t["say"])}</p></li>""" for t in c["tools"])
    nt = len(c["tools"])
    warn = notes_html([CAT_NOTE[c["cat"]]]) if c["cat"] in ("Phone control", "Personal data") else ""
    inner = f"""<div class="ph-row"><span class="ph-ic">{icon(ICON[c["id"]])}</span><h1>{e(c["name"])}</h1></div>
<p class="lead">{e(cp["lead"])}</p>
<div class="chips">{chips}</div>
<h2 class="dh">Why you will want it</h2>
<p class="dp">{e(cp["why"])}</p>
{scenes_html(cp["scenes"])}
<h2 class="dh" id="tools">{"Every tool" if nt > 1 else "The tool"} in this connector</h2>
<p class="dp">{e(c["about"])} Ultron picks the right tool from what you say, so you never have to name one.</p>
<ul class="tools">{tools}</ul>
<h2 class="dh">Access and privacy</h2>
<dl class="facts1 rv">
<div><dt>Needs</dt><dd>{e(c["needs"])}</dd></div>
<div><dt>Runs on</dt><dd>{e(c["runs"])}</dd></div>
<div><dt>Privacy</dt><dd>{e(c["privacy"])}</dd></div>
<div><dt>Default</dt><dd>{"On for a fresh install." if c["on"] else "Off. You turn it on from the Connectors page in the app."}</dd></div>
</dl>
{warn}"""
    return page(f'{c["name"]} connector | Ultron Docs', f'{cp["lead"]} {c["desc"]}', f'/docs/connectors/{c["id"]}.html',
                [("Docs", "/docs/"), ("Connectors", "/docs/connectors/"), (c["name"], None)], inner,
                ((p["name"], f'/docs/connectors/{p["id"]}.html'), (n["name"], f'/docs/connectors/{n["id"]}.html')))


def connectors_index():
    total = sum(len(c["tools"]) for c in conns)
    groups = ""
    for cat in ORDER:
        items = [c for c in conns if c["cat"] == cat]
        cards = "".join(f"""<a class="ccard rv" href="/docs/connectors/{c["id"]}.html" style="--d:{i % 2 * .07}s">
<span class="ph-ic">{icon(ICON[c["id"]])}</span>
<h3>{e(c["name"])}</h3>
<p>{e(c["copy"]["lead"])}</p>
<small>{len(c["tools"])} tool{"s" if len(c["tools"]) != 1 else ""} · {"on by default" if c["on"] else "off by default"}{icon("i-arrow")}</small>
</a>""" for i, c in enumerate(items))
        groups += f'<h2 class="dh">{e(cat)}</h2><p class="dp">{e(CAT_NOTE[cat])}</p><div class="cgrid2">{cards}</div>'
    inner = f"""<h1>{len(conns)} connectors, {total} tools</h1>
<p class="lead">A connector is a bundle of tools for one job, like Calendar or YouTube Downloads. Open any of them to see what it does, what to say to use it, and exactly what access it needs. Risky ones stay off until you switch them on.</p>
{groups}"""
    return page("Connectors | Ultron Docs", f"{len(conns)} connectors and {total} tools. See what each one does, what to say to use it, and what access it needs.",
                "/docs/connectors/", [("Docs", "/docs/"), ("Connectors", None)], inner)


def feature_page(f, p, n):
    links = "".join(f'<a class="btn btn-ghost btn-sm" href="{h}">{e(t)}</a>' for t, h in f["links"])
    inner = f"""<div class="ph-row"><span class="ph-ic">{icon(f["icon"])}</span><h1>{e(f["name"])}</h1></div>
<p class="lead">{e(f["lead"])}</p>
<h2 class="dh">What it is</h2>
<p class="dp">{e(f["why"])}</p>
<h2 class="dh">How it works</h2>
{how_html(f["how"])}
<h2 class="dh">What it looks like</h2>
{scenes_html(f["scenes"])}
{notes_html(f["notes"])}
{('<div class="cta-row dlinks">' + links + '</div>') if links else ''}"""
    return page(f'{f["name"]} | Ultron Docs', f["lead"] + " " + f["why"], f'/docs/features/{f["slug"]}.html',
                [("Docs", "/docs/"), ("Features", "/docs/features/live-conversation.html"), (f["name"], None)], inner,
                ((p["name"], f'/docs/features/{p["slug"]}.html'), (n["name"], f'/docs/features/{n["slug"]}.html')))


def skills_page():
    s = SKILLS
    inner = f"""<div class="ph-row"><span class="ph-ic">{icon("i-spark")}</span><h1>{e(s["title"])}</h1></div>
<p class="lead">{e(s["lead"])}</p>
<h2 class="dh">What a skill is</h2>
<p class="dp">{e(s["why"])}</p>
<h2 class="dh">How they work</h2>
{how_html(s["how"])}
<h2 class="dh">What it looks like</h2>
{scenes_html(s["scenes"])}
{notes_html(s["notes"])}"""
    return page("Skills | Ultron Docs", s["lead"] + " " + s["why"], "/docs/skills.html", [("Docs", "/docs/"), ("Skills", None)], inner)


def getting_started_page():
    g = GETTING_STARTED
    steps = "".join(f'<li class="step rv"><b>{i}</b><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for i, (t, d) in enumerate(g["steps"], 1))
    inner = f"""<h1>{e(g["title"])}</h1>
<p class="lead">{e(g["lead"])}</p>
<div class="cta-row dlinks"><a class="btn" href="{DOWNLOAD}" download rel="nofollow">Download APK</a><a class="btn btn-ghost" href="/#pricing">See plans</a></div>
<ol class="steps dsteps">{steps}</ol>
<h2 class="dh">Good to know</h2>
{how_html(g["notes"])}"""
    return page("Getting started | Ultron Docs", g["lead"], "/docs/getting-started.html", [("Docs", "/docs/"), ("Getting started", None)], inner)


def docs_home():
    total = sum(len(c["tools"]) for c in conns)
    cards = [
        ("/docs/getting-started.html", "i-down", "Getting started", "Download, install, activate and say hello."),
        ("/docs/features/live-conversation.html", "i-mic", "Features", f"{len(FEATURES)} features explained: voice, working other apps, documents, memory, YouTube and personalities."),
        ("/docs/connectors/", "i-grid", "Connectors", f"{len(conns)} connectors and {total} tools, each with what to say and what access it needs."),
        ("/docs/skills.html", "i-spark", "Skills", "Short Markdown routines that teach Ultron your own steps."),
    ]
    grid = "".join(f"""<a class="ccard rv" href="{h}" style="--d:{i * .07}s"><span class="ph-ic">{icon(ic)}</span><h3>{e(t)}</h3><p>{e(d)}</p><small>Open{icon("i-arrow")}</small></a>""" for i, (h, ic, t, d) in enumerate(cards))
    inner = f"""<h1>Ultron docs</h1>
<p class="lead">Everything Ultron can do, explained with what to say and what happens. Start with Getting started, or jump straight to the connector you are curious about.</p>
<div class="cgrid2 dhome">{grid}</div>"""
    return page("Ultron Docs", "Everything Ultron can do, explained with what to say and what happens.", "/docs/", [("Docs", None)], inner)


def write(path, html):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8", newline="\n")


def main():
    for old in (DIST / "connectors", DOCS):
        if old.exists():
            shutil.rmtree(old)
    urls = ["/", "/docs/", "/docs/getting-started.html", "/docs/skills.html", "/docs/connectors/"]
    write(DOCS / "index.html", docs_home())
    write(DOCS / "getting-started.html", getting_started_page())
    write(DOCS / "skills.html", skills_page())
    write(DOCS / "connectors" / "index.html", connectors_index())
    for i, f in enumerate(FEATURES):
        write(DOCS / "features" / f"{f['slug']}.html", feature_page(f, FEATURES[i - 1], FEATURES[(i + 1) % len(FEATURES)]))
        urls.append(f"/docs/features/{f['slug']}.html")
    for i, c in enumerate(seq):
        write(DOCS / "connectors" / f"{c['id']}.html", connector_page(c, seq[i - 1], seq[(i + 1) % len(seq)]))
        urls.append(f"/docs/connectors/{c['id']}.html")
    urls += ["/privacy.html", "/terms.html"]
    write(DIST / "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
          + "".join(f"<url><loc>{SITE}{u}</loc></url>" for u in urls) + "</urlset>\n")
    write(DIST / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print(len(urls), "pages listed")


if __name__ == "__main__":
    main()
