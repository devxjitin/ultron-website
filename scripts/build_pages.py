"""Builds the Docs section (dist/docs/...) from data/connectors.json (extracted from the Android app), the hand-written
copy in scripts/usecases.py (connectors) and scripts/docs_content.py (getting started, features, skills).

Run from the site folder:  python scripts/build_pages.py
The output is plain HTML committed under dist/, so the site stays static and needs no build on deploy.

Docs are written as reference pages: plain text, one list of tools per connector with an example phrase each, and one
phone demo per page that plays through that page's examples.
"""
import json
import shutil
from html import escape as e
from pathlib import Path

from docs_content import FEATURE_SCENE_TOOLS, FEATURES, GETTING_STARTED, SKILLS, SKILLS_SCENE_TOOLS
from scenes import CONNECTORS as CONN_SCREENS, FEATURES as FEAT_SCREENS, SKILLS as SKILL_SCREENS
from skills_content import FEATURES_SKILL, WA_GROUPS, WA_TASKS, WHATSAPP
from usecases import CONNECTORS, SCENE_TOOLS, TOOLS

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
DOCS = DIST / "docs"
V = "20261123"
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
ICONS_SVG = (DIST / "index.html").read_text(encoding="utf-8").split("<defs>")[1].split("</defs>")[0]

for c in conns:
    c["copy"] = CONNECTORS[c["id"]]
    for t in c["tools"]:
        t["say"] = TOOLS[t["fn"]]
seq = [c for cat in ORDER for c in conns if c["cat"] == cat]
ALL_TOOLS = {t["fn"]: t for c in conns for t in c["tools"]}


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
    return f"""<footer class="foot wrap"><span>Built by Jitin Kumar Sengar and Sonia</span><nav><a href="/">Home</a><a href="/#pricing">Pricing</a><a href="/#faq">FAQ</a><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a></nav><button class="motion" aria-pressed="false">Pause motion</button></footer>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="/page.js?v={V}" defer></script>
</body>
</html>
"""


def sidebar(current):
    def a(href, text, extra=""):
        cur = ' aria-current="page"' if href == current else ""
        return f'<a href="{href}"{cur}{extra}>{e(text)}</a>'

    out = ['<aside class="dside" aria-label="Docs" data-lenis-prevent><details class="dside-m" open><summary>Docs menu</summary><div class="dside-in" data-lenis-prevent>']
    out.append(a("/docs/", "Overview") + a("/docs/getting-started.html", "Getting started"))
    out.append('<h4>Features</h4>' + "".join(a(f"/docs/features/{f['slug']}.html", f["name"]) for f in FEATURES))
    in_skills = current.startswith("/docs/skills")
    out.append("<h4>Skills</h4>" + a("/docs/skills.html", "All skills") + a("/docs/skills/ultron-features.html", FEATURES_SKILL["name"]))
    wa_open = " open" if current.startswith("/docs/skills/whatsapp") else ""
    out.append(f'<details class="dcat"{wa_open}><summary>WhatsApp</summary>' + a("/docs/skills/whatsapp.html", "All WhatsApp tasks")
               + "".join(a(f"/docs/skills/whatsapp/{k['id']}.html", k["name"]) for k in WA_TASKS) + "</details>")
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


def demo(items):
    """One phone for the whole page, in the same frame as the landing page, showing the real voice screen. `items` is a
    list of (situation, say, result, tool function or None, screen). The page script plays them one after another; the
    first one is already in the markup so the page reads fine without scripts."""
    data = []
    for situation, say, result, fn, screen in items:
        t = ALL_TOOLS.get(fn)
        item = {"title": situation, "say": say, "tool": t["label"] if t else (fn or "Understanding"), "result": result, "reply": result}
        item.update(screen)
        data.append(item)
    first = data[0]
    dots = "".join(f'<button type="button" aria-label="Example {i + 1}"{" aria-current=true" if i == 0 else ""}></button>' for i in range(len(data)))
    return f"""<figure class="demo" data-demo='{e(json.dumps(data, ensure_ascii=False), quote=True)}'>
<div class="dphone"><div class="dscr">
<img src="/assets/app/dark-voice.webp" alt="The Ultron voice screen" width="720" height="1600">
<p class="v-sub"><span class="ty-src">{e(first["say"])}</span></p>
<p class="v-chip ok"><span>{e(first["tool"])}</span><i class="spin"></i></p>
<p class="v-reply">{e(first["reply"])}</p>
<div class="kscr"></div>
</div></div>
<figcaption><span class="dcap">{e(first["title"])}</span><span class="dots">{dots}</span></figcaption>
<p class="demo-note">Example screens. The values shown are made up.</p>
</figure>"""


def meta_rows(rows):
    return '<dl class="meta">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in rows) + "</dl>"


def connector_page(c, p, n):
    cp = c["copy"]
    nt = len(c["tools"])
    by_fn = {}
    for fn, sc in zip(SCENE_TOOLS[c["id"]], cp["scenes"]):
        by_fn.setdefault(fn, sc)
    rows = []
    for t in c["tools"]:
        sc = by_fn.get(t["fn"])
        say = sc[1] if sc else t["say"]
        rows.append(f"""<li class="trow"><div class="tn"><h3>{e(t["label"])}</h3><code>{e(t["fn"])}</code></div><p>{e(t["hint"])}</p><p class="ex">Say: <q>{e(say)}</q></p></li>""")
    scenes = [(s, q, a, fn, sc) for (s, q, a), fn, sc in zip(cp["scenes"], SCENE_TOOLS[c["id"]], CONN_SCREENS[c["id"]])]
    note = f'<p class="note">{e(CAT_NOTE[c["cat"]])}</p>' if c["cat"] in ("Phone control", "Personal data") else ""
    inner = f"""<h1>{e(c["name"])}</h1>
<div class="top">
<div class="top-text">
<p class="sum">{e(c["about"])}</p>
{meta_rows([("Group", c["cat"]), ("Needs", c["needs"]), ("Runs on", c["runs"]), ("Privacy", c["privacy"]), ("Default", "On for a fresh install" if c["on"] else "Off until you add it in the app")])}
{note}
</div>
{demo(scenes)}
</div>
<h2 class="dh" id="tools">{"Tools" if nt > 1 else "Tool"}</h2>
<p class="dp">Ultron picks the right tool from what you say, so you never have to name one. The phrases are only examples.</p>
<ul class="trows">{"".join(rows)}</ul>"""
    return page(f'{c["name"]} connector | Ultron Docs', f'{c["about"]} {c["desc"]}', f'/docs/connectors/{c["id"]}.html',
                [("Docs", "/docs/"), ("Connectors", "/docs/connectors/"), (c["name"], None)], inner,
                ((p["name"], f'/docs/connectors/{p["id"]}.html'), (n["name"], f'/docs/connectors/{n["id"]}.html')))


def connectors_index():
    total = sum(len(c["tools"]) for c in conns)
    groups = ""
    for cat in ORDER:
        items = [c for c in conns if c["cat"] == cat]
        rows = "".join(f"""<li><a href="/docs/connectors/{c["id"]}.html"><b>{e(c["name"])}</b><span>{e(c["desc"])}</span><em>{len(c["tools"])} tool{"s" if len(c["tools"]) != 1 else ""}</em></a></li>""" for c in items)
        groups += f'<h2 class="dh">{e(cat)}</h2><p class="dp">{e(CAT_NOTE[cat])}</p><ul class="idx">{rows}</ul>'
    inner = f"""<h1>Connectors</h1>
<p class="sum">A connector is a bundle of tools for one job, like Calendar or YouTube Downloads. There are {len(conns)} connectors with {total} tools in all. A fresh install switches on the everyday ones and leaves the rest off until you add them.</p>
{groups}"""
    return page("Connectors | Ultron Docs", f"{len(conns)} connectors and {total} tools, with what each does and what access it needs.",
                "/docs/connectors/", [("Docs", "/docs/"), ("Connectors", None)], inner)


def dlist(items):
    return '<dl class="dl">' + "".join(f"<div><dt>{e(t)}</dt><dd>{e(d)}</dd></div>" for t, d in items) + "</dl>"


def feature_page(f, p, n):
    scenes = [(s, q, a, fn, sc) for (s, q, a), fn, sc in zip(f["scenes"], FEATURE_SCENE_TOOLS[f["slug"]], FEAT_SCREENS[f["slug"]])]
    links = "".join(f'<li><a class="inline" href="{h}">{e(t)}</a></li>' for t, h in f["links"])
    notes = "".join(f'<p class="note">{e(x)}</p>' for x in f["notes"])
    inner = f"""<h1>{e(f["name"])}</h1>
<div class="top">
<div class="top-text">
<p class="sum">{e(f["why"])}</p>
{notes}
</div>
{demo(scenes)}
</div>
<h2 class="dh">How it works</h2>
{dlist(f["how"])}
{('<h2 class="dh">Related</h2><ul class="rel">' + links + '</ul>') if links else ''}"""
    return page(f'{f["name"]} | Ultron Docs', f["lead"] + " " + f["why"], f'/docs/features/{f["slug"]}.html',
                [("Docs", "/docs/"), ("Features", "/docs/features/live-conversation.html"), (f["name"], None)], inner,
                ((p["name"], f'/docs/features/{p["slug"]}.html'), (n["name"], f'/docs/features/{n["slug"]}.html')))


def skills_page():
    s = SKILLS
    scenes = [(a, b, c_, fn, sc) for (a, b, c_), fn, sc in zip(s["scenes"], SKILLS_SCENE_TOOLS, SKILL_SCREENS)]
    notes = "".join(f'<p class="note">{e(x)}</p>' for x in s["notes"])
    cards = [
        ("/docs/skills/whatsapp.html", WHATSAPP["name"], WHATSAPP["summary"], f'{WHATSAPP["category"]}, {len(WA_TASKS)} tasks'),
        ("/docs/skills/ultron-features.html", FEATURES_SKILL["name"], FEATURES_SKILL["summary"], FEATURES_SKILL["category"]),
    ]
    lst = "".join(f'<li><a href="{h}"><b>{e(n)}</b><span>{e(d)}</span><em>{e(m)}</em></a></li>' for h, n, d, m in cards)
    inner = f"""<h1>{e(s["title"])}</h1>
<div class="top">
<div class="top-text">
<p class="sum">{e(s["why"])}</p>
{notes}
</div>
{demo(scenes)}
</div>
<h2 class="dh">Built-in skills</h2>
<p class="dp">These come with the app. Open one to see what it does, what it needs and a showcase of every task.</p>
<ul class="idx">{lst}</ul>
<h2 class="dh">How they work</h2>
{dlist(s["how"])}"""
    return page("Skills | Ultron Docs", s["why"], "/docs/skills.html", [("Docs", "/docs/"), ("Skills", None)], inner)


def wa_task_card(k):
    return (f'<li class="trow"><div class="tn"><h3><a class="inline" href="/docs/skills/whatsapp/{k["id"]}.html">{e(k["name"])}</a></h3>'
            f'<code>{e(k["id"])}</code></div><p>{e(k["about"])}</p><p class="ex">Say: <q>{e(k["say"][0])}</q></p></li>')


def whatsapp_page():
    w = WHATSAPP
    scenes = [(a, b, c_, fn, sc) for (a, b, c_, fn, sc) in (k["scene"] for k in WA_TASKS)]
    notes = "".join(f'<p class="note">{e(x)}</p>' for x in w["notes"])
    groups = ""
    for g, note in WA_GROUPS:
        items = [k for k in WA_TASKS if k["group"] == g]
        groups += f'<h2 class="dh" id="{e(g.lower().replace(" ", "-"))}">{e(g)}</h2><p class="dp">{e(note)}</p><ul class="trows">{"".join(wa_task_card(k) for k in items)}</ul>'
    inner = f"""<h1>WhatsApp skill</h1>
<div class="top">
<div class="top-text">
<p class="sum">{e(w["why"])}</p>
{meta_rows([("Group", w["category"]), ("Tasks", str(len(WA_TASKS))), ("Needs", NEEDS_SCREEN_TEXT), ("Runs on", "The WhatsApp app on your phone")])}
{notes}
</div>
{demo(scenes)}
</div>
<h2 class="dh">How it works</h2>
{dlist(w["how"])}
{groups}"""
    return page("WhatsApp skill | Ultron Docs", f'{w["summary"]} {len(WA_TASKS)} tasks, each with an example.', "/docs/skills/whatsapp.html",
                [("Docs", "/docs/"), ("Skills", "/docs/skills.html"), ("WhatsApp", None)], inner)


NEEDS_SCREEN_TEXT = "Screen control and Phone navigation connectors, plus Files for sending files"


def whatsapp_task_page(k, p, n):
    sit, say, result, fn, screen = k["scene"]
    say_rows = "".join(f"<li><q>{e(x)}</q></li>" for x in k["say"])
    notes = "".join(f'<p class="note">{e(x)}</p>' for x in k["notes"])
    inner = f"""<h1>{e(k["name"])}</h1>
<div class="top">
<div class="top-text">
<p class="sum">{e(k["about"])}</p>
{meta_rows([("Skill", "WhatsApp"), ("Group", k["group"]), ("Task id", k["id"]), ("Needs", k["needs"])])}
{notes}
</div>
{demo([k["scene"]])}
</div>
<h2 class="dh">Ways to say it</h2>
<p class="dp">Ultron works from what you mean, so these are only examples. English, Hindi and Hinglish all work.</p>
<ul class="rel">{say_rows}</ul>
<h2 class="dh">Related</h2>
<ul class="rel"><li><a class="inline" href="/docs/skills/whatsapp.html">All WhatsApp tasks</a></li><li><a class="inline" href="/docs/skills.html">How skills work</a></li></ul>"""
    return page(f'{k["name"]} on WhatsApp | Ultron Docs', f'{k["about"]}', f'/docs/skills/whatsapp/{k["id"]}.html',
                [("Docs", "/docs/"), ("Skills", "/docs/skills.html"), ("WhatsApp", "/docs/skills/whatsapp.html"), (k["name"], None)], inner,
                ((p["name"], f'/docs/skills/whatsapp/{p["id"]}.html'), (n["name"], f'/docs/skills/whatsapp/{n["id"]}.html')))


def features_skill_page():
    f = FEATURES_SKILL
    notes = "".join(f'<p class="note">{e(x)}</p>' for x in f["notes"])
    inner = f"""<h1>{e(f["name"])}</h1>
<div class="top">
<div class="top-text">
<p class="sum">{e(f["why"])}</p>
{meta_rows([("Skill", "ultron-features"), ("Group", f["category"]), ("Needs", "Nothing"), ("Runs on", "Inside the app")])}
{notes}
</div>
{demo([f["scene"]])}
</div>
<h2 class="dh">How it works</h2>
{dlist(f["how"])}"""
    return page(f'{f["name"]} skill | Ultron Docs', f["summary"] + " " + f["why"], "/docs/skills/ultron-features.html",
                [("Docs", "/docs/"), ("Skills", "/docs/skills.html"), (f["name"], None)], inner)


def getting_started_page():
    g = GETTING_STARTED
    steps = "".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in g["steps"])
    inner = f"""<h1>{e(g["title"])}</h1>
<p class="sum">Download, install, activate and talk. Ultron is not on the Play Store, so the APK comes straight from this site.</p>
<p class="dp"><a class="btn" href="{DOWNLOAD}" download rel="nofollow">Download APK</a></p>
<ol class="osteps">{steps}</ol>
<h2 class="dh">Good to know</h2>
{dlist(g["notes"])}"""
    return page("Getting started | Ultron Docs", "How to download, install and activate Ultron.", "/docs/getting-started.html", [("Docs", "/docs/"), ("Getting started", None)], inner)


def docs_home():
    total = sum(len(c["tools"]) for c in conns)
    rows = [
        ("/docs/getting-started.html", "Getting started", "Download, install, activate and say hello."),
        ("/docs/features/live-conversation.html", "Features", f"{len(FEATURES)} pages: voice, working other apps, documents, memory, YouTube and personalities."),
        ("/docs/connectors/", "Connectors", f"{len(conns)} connectors and {total} tools, with what each does and what access it needs."),
        ("/docs/skills.html", "Skills", f"Short routines that teach Ultron a job. The WhatsApp skill alone has {len(WA_TASKS)} tasks."),
    ]
    lst = "".join(f'<li><a href="{h}"><b>{e(t)}</b><span>{e(d)}</span></a></li>' for h, t, d in rows)
    inner = f"""<h1>Docs</h1>
<p class="sum">What Ultron does and how each part works. If you are new, start with Getting started.</p>
<ul class="idx">{lst}</ul>"""
    return page("Ultron Docs", "What Ultron does and how each part works.", "/docs/", [("Docs", None)], inner)


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
    write(DOCS / "skills" / "whatsapp.html", whatsapp_page())
    write(DOCS / "skills" / "ultron-features.html", features_skill_page())
    urls += ["/docs/skills/whatsapp.html", "/docs/skills/ultron-features.html"]
    for i, k in enumerate(WA_TASKS):
        write(DOCS / "skills" / "whatsapp" / f"{k['id']}.html", whatsapp_task_page(k, WA_TASKS[i - 1], WA_TASKS[(i + 1) % len(WA_TASKS)]))
        urls.append(f"/docs/skills/whatsapp/{k['id']}.html")
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
