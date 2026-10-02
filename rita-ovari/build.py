#!/usr/bin/env python3
"""Builds the Rita Ovari site.

  site/index.html      Hungarian (default, x-default)
  site/en/index.html   English
  site/assets/...      shared CSS/JS/favicon
  site/sitemap.xml, site/robots.txt

`python3 build.py --preview OUT.html` also writes a single-file preview with both
languages and an in-page HU/EN switch.

Before launch, edit the CONFIG block (domain, e-mail, form endpoint, socials).
"""
import html, json, os, sys, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from content import HU, EN

# ---- CONFIG: replace before going live ---------------------------------
DOMAIN = "https://ritaovari.com"          # final domain, no trailing slash
EMAIL = "hello@ritaovari.com"             # placeholder until Rita confirms
FORM_ENDPOINT = "https://formspree.io/f/YOUR_FORM_ID"
SOCIALS = [
    ("LinkedIn", "https://hu.linkedin.com/in/rita-ovari-a25335179"),
    ("Instagram", "https://www.instagram.com/ritaovari/"),
    ("Facebook", "https://www.facebook.com/rita.ovari"),
]
# ------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(ROOT, "src"), os.path.join(ROOT, "site")
FONTS = ("https://fonts.googleapis.com/css2?family=Caprasimo&family=Kalam:wght@700"
         "&family=Onest:wght@400;500;600&family=Martian+Mono:wght@500&display=swap")
e = html.escape
ARROW = '<span class="arr" aria-hidden="true">↗</span>'


def flower(cls="", petal="var(--tulip)", centre="var(--butter)"):
    import math
    petals = "".join(f'<circle cx="{50+30*math.cos(math.radians(a)):.1f}" cy="{50+30*math.sin(math.radians(a)):.1f}" r="19" style="fill:{petal}"/>' for a in range(0, 360, 60))
    return f'<svg class="{cls}" viewBox="0 0 100 100" aria-hidden="true">{petals}<circle cx="50" cy="50" r="18" style="fill:{centre}"/></svg>'


def hero_art(t):
    return f'''<svg viewBox="0 0 500 525" role="img" aria-label="{e(t['hero_label'])}">
  <defs><clipPath id="pill-{t['lang']}"><rect x="80" y="30" width="250" height="470" rx="125"/></clipPath></defs>
  <circle cx="320" cy="215" r="175" style="fill:var(--cornflower)"/>
  <circle cx="420" cy="70" r="26" style="fill:var(--peach)"/>
  <rect x="80" y="30" width="250" height="470" rx="125" style="fill:var(--cobalt-deep)"/>
  <g clip-path="url(#pill-{t['lang']})" style="fill:none;stroke:var(--white);stroke-width:2.5;opacity:.35">
    <path d="M40 300 q45 -26 90 0 t90 0 t90 0 t90 0"/><path d="M40 340 q45 -26 90 0 t90 0 t90 0 t90 0"/>
    <path d="M40 380 q45 -26 90 0 t90 0 t90 0 t90 0"/><path d="M40 420 q45 -26 90 0 t90 0 t90 0 t90 0"/>
    <path d="M40 460 q45 -26 90 0 t90 0 t90 0 t90 0"/>
  </g>
  <path d="M120 300 a85 85 0 0 1 170 0 v20 h-170z" style="fill:var(--white)"/>
  <circle cx="205" cy="165" r="56" style="fill:var(--white)"/>
  <circle cx="186" cy="160" r="11" style="fill:var(--night)"/><circle cx="224" cy="160" r="11" style="fill:var(--night)"/>
  <circle class="eye" cx="189" cy="157" r="4" style="fill:var(--white)"/><circle class="eye" cx="227" cy="157" r="4" style="fill:var(--white)"/>
  <rect class="lid" x="172" y="146" width="66" height="28" style="fill:var(--white)"/>
  <path d="M190 186 q15 14 30 0" style="fill:none;stroke:var(--night);stroke-width:4;stroke-linecap:round"/>
  <circle cx="172" cy="182" r="7" style="fill:var(--tulip)"/><circle cx="238" cy="182" r="7" style="fill:var(--tulip)"/>
  <g transform="translate(400 430)">{"".join(f'<circle cx="{c}" cy="{d}" r="24" style="fill:var(--tulip)"/>' for c, d in ((0,-36),(31,-18),(31,18),(0,36),(-31,18),(-31,-18)))}<circle r="22" style="fill:var(--butter)"/></g>
  <ellipse cx="70" cy="470" rx="30" ry="13" transform="rotate(-30 70 470)" style="fill:var(--leaf)"/>
</svg>'''


def portrait(t):
    return f'''<figure class="portrait">
  <svg viewBox="0 0 400 500" role="img" aria-label="{e(t['photo_cap'])}">
    <circle cx="250" cy="170" r="150" style="fill:var(--butter)"/>
    <rect x="50" y="40" width="250" height="440" rx="125" style="fill:var(--bg-raised)"/>
    <circle cx="175" cy="185" r="56" style="fill:var(--ink-muted);opacity:.45"/>
    <path d="M85 400 a90 90 0 0 1 180 0 v80 h-180z" style="fill:var(--ink-muted);opacity:.45"/>
  </svg>
  <figcaption>{e(t['photo_cap'])}</figcaption>
</figure>'''


def jsonld(t):
    url = DOMAIN + t["path"]
    person = {"@type": "Person", "@id": DOMAIN + "/#rita", "name": "Rita Ovari", "jobTitle": "Coach & Trainer",
              "knowsLanguage": ["hu", "en"], "sameAs": [u for _, u in SOCIALS], "url": DOMAIN + "/",
              "knowsAbout": ["Coaching", "Team building", "Agile", "Scrum", "Kanban", "Facilitation", "Leadership coaching"]}
    biz = {"@type": "ProfessionalService", "@id": DOMAIN + "/#business", "name": "Rita Ovari Coaching",
           "url": url, "description": t["desc"], "founder": {"@id": DOMAIN + "/#rita"}, "email": EMAIL,
           "address": {"@type": "PostalAddress", "addressLocality": "Budapest", "addressCountry": "HU"},
           "areaServed": [{"@type": "City", "name": "Budapest"}, {"@type": "Country", "name": "Hungary"}],
           "availableLanguage": ["Hungarian", "English"],
           "hasOfferCatalog": {"@type": "OfferCatalog", "name": t["srv_label"], "itemListElement": [
               {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n[1], "description": n[2]}}
               for _, notes in t["cols"] for n in notes]}}
    faq = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faqs"]]}
    site = {"@type": "WebSite", "@id": DOMAIN + "/#site", "url": DOMAIN + "/", "name": "Rita Ovari", "inLanguage": ["hu", "en"]}
    data = {"@context": "https://schema.org", "@graph": [site, person, biz, faq]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def head(t, css_href):
    url = DOMAIN + t["path"]
    other_locale = "en_US" if t["lang"] == "hu" else "hu_HU"
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(t['title'])}</title>
<meta name="description" content="{e(t['desc'])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="hu" href="{DOMAIN}/">
<link rel="alternate" hreflang="en" href="{DOMAIN}/en/">
<link rel="alternate" hreflang="x-default" href="{DOMAIN}/">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#f7f5ff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#110d2c" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Rita Ovari">
<meta property="og:title" content="{e(t['title'])}">
<meta property="og:description" content="{e(t['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:locale:alternate" content="{other_locale}">
<meta property="og:image" content="{DOMAIN}/assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{css_href.rsplit('/',1)[0]}/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{css_href}">
{jsonld(t)}'''


def hop(word, start):
    return "".join(f'<span class="ch" style="--i:{start+i}">{e(c)}</span>' for i, c in enumerate(word))


def headline(t):
    a, b = t["hero_h1"]
    return (f'<span class="sr-only">{e(a)} {e(b)}</span><span aria-hidden="true"><span class="w">{hop(a,0)}</span> '
            f'<em class="ac w">{hop(b,len(a))}</em></span>')


def body(t, preview=False):
    L = t["lang"]
    sid = (lambda x: f"{x}-{L}") if preview else (lambda x: x)
    ids = [a for a, _ in t["nav"]]  # services, approach, about, faq, contact
    if preview:
        hu_href, en_href = "#", "#"
        sw = lambda code: f'data-lang-switch="{code}"'
    else:
        hu_href, en_href = ("./" if L == "hu" else "../"), ("en/" if L == "hu" else "./")
        sw = lambda code: ""
    cur = lambda code: 'aria-current="true"' if code == L else ""
    nav = "".join(f'<a href="#{a}">{e(b)}</a>' for a, b in t["nav"])
    facts = "".join(f"<li>{e(f)}</li>" for f in t["facts"])
    floats = "".join(f'<div class="float f{i+1}">{e(a)}<small>{e(b)}</small></div>' for i, (a, b) in enumerate(t["floats"]))
    aud = "".join(f'''<article class="rv" style="--d:{i}"><span class="dot" style="background:var(--{c})"></span><h3>{e(h)}</h3><p>{e(p)}</p><span class="tagline">{e(tg)}</span></article>'''
                  for i, (c, h, p, tg) in enumerate(t["aud"]))
    cols = "".join(f'''<div class="col"><div class="col-h"><span class="label">{e(name)}</span><span class="count">{len(notes)}</span></div>'''
                   + "".join(f'<article class="note {c}"><h3>{e(h)}</h3><p>{e(p)}</p><button class="pick" type="button" aria-pressed="false" data-title="{e(h)}" data-on="{e(t["picked"])}" data-off="{e(t["pick"])}">{e(t["pick"])}</button></article>' for c, h, p in notes) + "</div>"
                   for name, notes in t["cols"])
    formats = "".join(f'<span class="chip">{e(f)}</span>' for f in t["formats"])
    steps = "".join(f'<li class="rv" style="--d:{i}"><h3>{e(h)}</h3><p>{e(p)}</p></li>' for i, (h, p) in enumerate(t["steps"]))
    about_p = "".join(f"<p>{e(p)}</p>" for p in t["about_p"])
    creds = "".join(f"<li>{e(c)}</li>" for c in t["creds"])
    off = "".join(f"<span>{e(o)}</span>" for o in t["off"])
    outs = "".join(f'<div class="rv" style="--d:{i}"><b>{n}</b><p>{e(p)}</p></div>' for i, (n, p) in enumerate(t["outs"]))
    faqs = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in t["faqs"])
    who = "".join(f'<input type="radio" name="who" id="{sid("who"+str(i))}" value="{e(o)}"{" checked" if i==0 else ""}><label for="{sid("who"+str(i))}">{e(o)}</label>' for i, o in enumerate(t["f_who_opts"]))
    topics = "".join(f"<option>{e(o)}</option>" for o in t["f_topics"])
    langs = "".join(f"<option>{e(o)}</option>" for o in t["f_langs"])
    socials = "".join(f'<a class="btn btn-ghost btn-sm" href="{u}" rel="me noopener" target="_blank">{n} {ARROW}</a>' for n, u in SOCIALS)
    err = "Hiba történt, kérlek írj e-mailt." if L == "hu" else "Something went wrong, please email me instead."
    return f'''<a class="skip" href="#{sid('main')}">{e(t['skip'])}</a>
<header class="top"><div class="wrap">
  <a class="mark" href="#{sid('main')}">Rita Ovari<i>.</i></a>
  <nav class="nav" aria-label="Main">{nav}</nav>
  <nav class="lt" aria-label="{e(t['switch_label'])}"><a href="{hu_href}" hreflang="hu" lang="hu" {sw('hu')} {cur('hu')}>HU</a><a href="{en_href}" hreflang="en" lang="en" {sw('en')} {cur('en')}>EN</a></nav>
  <a class="btn btn-primary btn-sm" href="#{ids[4]}">{e(t['cta_short'])} {ARROW}</a>
</div></header>
<main id="{sid('main')}">
<section class="hero"><span class="blob b1"></span>{flower("flower f-a")}<span class="blob b3"></span><span class="blob b4"></span><div class="wrap">
  <div>
    <p class="label">{e(t['hero_label'])}</p>
    <h1>{headline(t)}</h1>
    <p class="lead">{e(t['hero_lead'])}</p>
    <div class="ctas"><a class="btn btn-primary" href="#{ids[4]}">{e(t['cta_primary'])} {ARROW}</a><a class="btn btn-ghost" href="#{ids[0]}">{e(t['cta_secondary'])} {ARROW}</a></div>
  </div>
  <div class="hero-art" data-art>{hero_art(t)}{floats}<span class="drag-hint" aria-hidden="true">{e(t['drag_hint'])}</span></div>
</div></section>
<div class="facts" aria-label="{e(t['facts'][0])}"><ul>{facts}{facts.replace('<li>', '<li aria-hidden="true">')}</ul></div>

<section class="sec" aria-labelledby="{sid('aud-h')}"><div class="wrap">
  <div class="sec-head rv"><span class="label">{e(t['aud_label'])}</span><h2 id="{sid('aud-h')}">{t['aud_h2']}</h2><p class="lead muted">{e(t['aud_lead'])}</p></div>
  <div class="aud">{aud}</div>
</div></section>

<section class="sec" id="{ids[0]}" aria-labelledby="{sid('srv-h')}" style="padding-top:0"><div class="wrap">
  <div class="sec-head rv"><span class="label">{e(t['srv_label'])}</span><h2 id="{sid('srv-h')}">{t['srv_h2']}</h2><p class="lead muted">{e(t['srv_lead'])}</p></div>
  <div class="board rv" data-board>{cols}</div>
  <div class="formats">{formats}</div>
</div></section>

<section class="sec" id="{ids[1]}" aria-labelledby="{sid('proc-h')}" style="padding-top:0"><div class="wrap">
  <div class="sec-head rv"><span class="label">{e(t['proc_label'])}</span><h2 id="{sid('proc-h')}">{t['proc_h2']}</h2></div>
  <ol class="steps" data-steps>{steps}</ol>
</div></section>

<section class="sec band-dark about" id="{ids[2]}" aria-labelledby="{sid('about-h')}"><div class="wrap">
  {portrait(t)}
  <div>
    <div class="sec-head" style="margin-bottom:28px"><span class="label">{e(t['about_label'])}</span><h2 id="{sid('about-h')}">{t['about_h2']}</h2></div>
    {about_p}
    <ul class="creds">{creds}</ul>
    <p class="label" style="margin:0 0 14px">{e(t['off_label'])}</p>
    <div class="offclock">{off}</div>
    <p class="muted" style="margin-top:18px">{e(t['off_note'])}</p>
  </div>
</div></section>

<div class="divider" aria-hidden="true">{flower("", "var(--cobalt)", "var(--butter)")}{flower("", "var(--tulip)", "var(--white)")}{flower("", "var(--leaf)", "var(--butter)")}</div>
<section class="sec" aria-labelledby="{sid('out-h')}"><div class="wrap">
  <div class="sec-head rv"><span class="label">{e(t['out_label'])}</span><h2 id="{sid('out-h')}">{t['out_h2']}</h2></div>
  <div class="outs">{outs}</div>
</div></section>

<section class="sec faq" id="{ids[3]}" aria-labelledby="{sid('faq-h')}" style="padding-top:0"><div class="wrap">
  <div class="sec-head rv"><span class="label">{e(t['faq_label'])}</span><h2 id="{sid('faq-h')}">{t['faq_h2']}</h2><p class="muted">{e(t['faq_lead'])}</p></div>
  <div>{faqs}</div>
</div></section>

<section class="sec contact" id="{ids[4]}" aria-labelledby="{sid('ct-h')}" style="padding-top:0"><div class="wrap">
  <div>
    <div class="sec-head" style="margin-bottom:0"><span class="label">{e(t['ct_label'])}</span><h2 id="{sid('ct-h')}">{t['ct_h2']}</h2><p class="lead">{e(t['ct_lead'])}</p></div>
    <div class="cinfo"><span class="label">E-mail</span><span style="user-select:all">{EMAIL}</span><span class="muted">{e(t['ct_loc'])}</span></div>
    <div class="socials">{socials}</div>
  </div>
  <form class="card" data-contact data-endpoint="{'' if preview else FORM_ENDPOINT}" data-ok="{e(t['f_ok'])}" data-preview="{e(t['f_preview'])}" data-error="{e(err)}" novalidate>
    <fieldset class="field" style="border:0;padding:0;margin:0"><legend class="label" style="margin-bottom:9px">{e(t['f_who'])}</legend><div class="seg">{who}</div></fieldset>
    <div class="row2">
      <div class="field"><label for="{sid('f-name')}">{e(t['f_name'])}</label><input id="{sid('f-name')}" name="name" autocomplete="name" required></div>
      <div class="field"><label for="{sid('f-email')}">{e(t['f_email'])}</label><input id="{sid('f-email')}" name="email" type="email" autocomplete="email" required></div>
    </div>
    <div class="field"><label for="{sid('f-company')}">{e(t['f_company'])}</label><input id="{sid('f-company')}" name="company" autocomplete="organization"></div>
    <div class="row2">
      <div class="field"><label for="{sid('f-topic')}">{e(t['f_topic'])}</label><select id="{sid('f-topic')}" name="topic">{topics}</select></div>
      <div class="field"><label for="{sid('f-lang')}">{e(t['f_lang'])}</label><select id="{sid('f-lang')}" name="language">{langs}</select></div>
    </div>
    <div class="field"><label for="{sid('f-msg')}">{e(t['f_msg'])}</label><textarea id="{sid('f-msg')}" name="message" rows="4" placeholder="{e(t['f_msg_ph'])}" required></textarea></div>
    <div><button class="btn btn-primary" type="submit">{e(t['f_send'])} {ARROW}</button></div>
    <p class="form-note">{e(t['f_note'])}</p>
    <p class="ok" data-msg role="status" hidden></p>
  </form>
</div></section>
</main>
<div class="tray" data-tray role="status" aria-live="polite"><span><b data-count>0</b>{e(t['tray_txt'])}</span><a class="btn btn-sm" href="#{ids[4]}" data-tray-go data-prefill="{e(t['tray_prefill'])}">{e(t['tray_btn'])} {ARROW}</a></div>
<footer><div class="wrap">
  <a class="mark" href="#{sid('main')}">Rita Ovari<i>.</i></a>
  <nav aria-label="Footer">{nav}<a href="#">{e(t['privacy'])}</a></nav>
  <small>© {datetime.date.today().year} Rita Ovari · {e(t['foot'])}</small>
</div></footer>'''


def page(t, asset_prefix):
    return (f'<!doctype html>\n<html lang="{t["lang"]}">\n<head>\n{head(t, asset_prefix + "assets/styles.css")}\n</head>\n'
            f'<body>\n{body(t)}\n<script src="{asset_prefix}assets/main.js" defer></script>\n</body>\n</html>\n')


FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#3d3dff"/>'
           '<text x="11" y="46" font-family="Georgia,serif" font-weight="700" font-size="38" fill="#ffffff">R</text>'
           '<circle cx="48" cy="42" r="6" fill="#ff4f8b"/></svg>\n')


def build():
    css, js = open(os.path.join(SRC, "styles.css")).read(), open(os.path.join(SRC, "main.js")).read()
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "en"), exist_ok=True)
    w = lambda p, s: open(os.path.join(OUT, p), "w").write(s)
    w("index.html", page(HU, ""))
    w("en/index.html", page(EN, "../"))
    w("assets/styles.css", css)
    w("assets/main.js", js)
    w("assets/favicon.svg", FAVICON)
    w("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    today = datetime.date.today().isoformat()
    urls = ""
    for p in ("/", "/en/"):
        urls += (f"  <url><loc>{DOMAIN}{p}</loc><lastmod>{today}</lastmod>"
                 f'<xhtml:link rel="alternate" hreflang="hu" href="{DOMAIN}/"/>'
                 f'<xhtml:link rel="alternate" hreflang="en" href="{DOMAIN}/en/"/>'
                 f'<xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}/"/></url>\n')
    w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
      'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + "</urlset>\n")
    return css, js


def preview(path, css, js):
    blocks = "".join(f'<div data-lang-block="{t["lang"]}" lang="{t["lang"]}"{" hidden" if t is EN else ""}>{body(t, preview=True)}</div>' for t in (HU, EN))
    open(path, "w").write(f'<title>Rita Ovari Website</title>\n<link rel="stylesheet" href="{FONTS}">\n'
                          f'<style>\n{css}\n</style>\n{blocks}\n<script>\n{js}\n</script>\n')


if __name__ == "__main__":
    css, js = build()
    if "--preview" in sys.argv:
        preview(sys.argv[sys.argv.index("--preview") + 1], css, js)
    print("built", OUT)
