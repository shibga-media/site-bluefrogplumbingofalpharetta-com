#!/usr/bin/env python3
"""
Builds the site into docs/ (GitHub Pages serves main:/docs).   python3 build.py

THE Shibga Media standard site template: the static build first made for CJ's Roofing
(github.com/shibga-media/site-roofingsanramonca). Same layout, sections, CSS and components for every
client site; only content.py (words, business details, palette, service/area pages) and the colour
variables at the top of src/site.css differ. Sites with no client photos use the template's icon panels
in place of photos. Heading font: Teko (SIL OFL, self-hosted in src/fonts/).

Words + facts: content.py (+ copy.json)    Look: src/site.css    Needs: Python 3 only.
"""
import datetime, hashlib, html, json, os, re, shutil
import content as C

INDEXABLE = C.INDEXABLE        # False = every page noindex,nofollow AND robots.txt blocks everything
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")
KEEP = {"CNAME", ".nojekyll"}
S = C.SITE
BASE = S.get("base", "")                    # "" on a custom domain; "/repo-name" on a github.io preview
DOMAIN = S["domain"]                        # full site root incl. BASE, no trailing slash
YEAR = datetime.date.today().year
E = html.escape
N = S["name"]

_O = 'viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
_S = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
IC = {
    "phone": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>',
    "text": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4 3h16a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H8l-5 4V5a2 2 0 0 1 1-2zm3 6v2h2V9zm4 0v2h2V9zm4 0v2h2V9z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm9 7.2L4.5 7v1.9l7.5 5.1 7.5-5.1V7z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a7 7 0 0 1 7 7c0 5.2-7 13-7 13S5 14.2 5 9a7 7 0 0 1 7-7zm0 4.5A2.5 2.5 0 1 0 12 11.5 2.5 2.5 0 0 0 12 6.5z"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4.5 12.5l5 5 10-11"/></svg>',
    "burger": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>',
    "logo": f'<svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="4" fill="{C.PALETTE["brand"]}"/><path d="M20 6c5.5 7 10 11.2 10 16.5a10 10 0 0 1-20 0C10 17.2 14.500 13 20 6z" fill="#fff"/><path d="M15 23.5a5 5 0 0 0 5 5" fill="none" stroke="{C.PALETTE["accent"]}" stroke-width="2.6" stroke-linecap="round"/></svg>',
    "drop": f'<svg {_S}><path d="M12 3c3 4 6 7 6 11a6 6 0 0 1-12 0c0-4 3-7 6-11z"/><path d="M9.5 15a2.5 2.5 0 0 0 2.5 2.5"/></svg>',
    # service icons
    "drain-cleaning": f'<svg {_S}><path d="M12 3v10m0 0-4-4m4 4 4-4M5 21h14M7 17h10"/></svg>',
    "water-heater": f'<svg {_S}><path d="M8 3h8v18H8zM8 8h8M12 12v4"/></svg>',
    "leak-repair": f'<svg {_S}><path d="M12 3c3 4 6 7 6 11a6 6 0 0 1-12 0c0-4 3-7 6-11z"/></svg>',
    "sewer-line": f'<svg {_S}><path d="M3 8h18M3 16h18M7 8v8M17 8v8"/></svg>',
    "toilet-faucet-fixtures": f'<svg {_S}><path d="M5 6h9a4 4 0 0 1 4 4v1M18 11v6M12 11v3M4 14h10"/></svg>',
    "repiping": f'<svg {_S}><path d="M3 7h8v10h10M3 7V4M21 17v3"/></svg>',
    "garbage-disposal": f'<svg {_S}><path d="M5 8h14l-2 12H7zM9 4h6M10 12v4M14 12v4"/></svg>',
    "emergency-plumbing": f'<svg {_S}><path d="M12 3 2 20h20zM12 10v5M12 18v.5"/></svg>',
    # why-us icons
    "focus": f'<svg {_O}><circle cx="24" cy="24" r="17"/><circle cx="24" cy="24" r="9"/><circle cx="24" cy="24" r="1.5" fill="currentColor"/></svg>',
    "owner": f'<svg {_O}><circle cx="24" cy="15" r="7"/><path d="M10 41c1.5-8 7-12 14-12s12.5 4 14 12"/></svg>',
    "local": f'<svg {_O}><path d="M24 44s14-13 14-24a14 14 0 0 0-28 0c0 11 14 24 14 24z"/><circle cx="24" cy="20" r="5"/></svg>',
    "call": f'<svg {_O}><path d="M13 7h6l3 9-4 3a24 24 0 0 0 11 11l3-4 9 3v6a4 4 0 0 1-4 4C21 39 9 27 9 11a4 4 0 0 1 4-4z"/></svg>',
    "doc": f'<svg {_O}><path d="M11 5h18l9 9v29H11z"/><path d="M29 5v9h9M17 24h14M17 31h14M17 38h8"/></svg>',
}

TEL = f'tel:{S["phone_tel"]}'
SMS = f'sms:{S["sms_tel"]}' if S.get("sms_tel") else None
MAILTO = f'mailto:{S["email"]}' if S.get("email") else None
SERVICES = C.SERVICES            # (slug, name, blurb)
AREAS = C.AREAS                  # (slug, city)
SV = {s: f"/services/{s}/" for s, _, _ in SERVICES}
CITY_PAGES = [(f"/service-areas/{s}/", c) for s, c in AREAS]
COPY = C.COPY


def inline(s):
    s = E(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = s.replace("{BIZ}", E(N, quote=False))
    s = s.replace("{call}", f'<a href="{TEL}">{S["phone_display"]}</a>')
    return s


def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def two_tone(t):
    """Template headings: dark words + a brand-coloured phrase. A tuple is (plain, coloured)."""
    if isinstance(t, tuple):
        return f'{E(t[0])} <span class="hl">{E(t[1])}</span>'
    if " in " in t:
        a, b = t.split(" in ", 1)
        return f'{E(a)} <span class="hl">in {E(b)}</span>'
    w = t.split()
    if len(w) < 2:
        return E(t)
    n = 2 if len(w) >= 4 else 1
    return f'{E(" ".join(w[:-n]))} <span class="hl">{E(" ".join(w[-n:]))}</span>'


def plain(t):
    return t if isinstance(t, str) else " ".join(t)


def call_btns(call_label=None):
    second = (f'<a class="btn ghost" href="{SMS}">{IC["text"]}Text us</a>' if SMS else
              f'<a class="btn ghost" href="/contact/">Contact us</a>')
    return (f'<div class="btns"><a class="btn pri" href="{TEL}">{IC["phone"]}{call_label or "Call " + S["phone_display"]}</a>'
            f'{second}</div>')


def cta_band():
    return (f'<section class="ctaband"><div class="wrap"><div class="ctabox"><h2>{two_tone(C.CTA["title"])}</h2>'
            f'<p>{E(C.CTA["text"])}</p>{call_btns()}</div></div></section>')


def services_cards():
    out = ['<div class="svc">']
    for slug, name, blurb in SERVICES:
        url = SV[slug]
        out.append(f'<article class="svc-card"><a class="svc-img icon" href="{url}" tabindex="-1" aria-hidden="true">{IC[slug]}</a>'
                   f'<div class="svc-body"><h3><a href="{url}">{E(name)}</a></h3><p>{E(blurb)}</p>'
                   f'<a class="btn pri sm" href="{url}">Learn more &rsaquo;</a></div></article>')
    out.append("</div>")
    return "".join(out)


def cities_list():
    items = "".join(f'<li><a href="{u}">{IC["pin"]}<b>{E(n)}</b><span>Plumber in {E(n)}</span></a></li>' for u, n in CITY_PAGES)
    return f'<ul class="cities" id="areas">{items}</ul>'


def copy_html(key):
    d = COPY[key]
    out = "".join(f"<p>{inline(p)}</p>" for p in d["paras"])
    if d.get("bullets"):
        out += '<ul class="sq">' + "".join(f"<li>{inline(b)}</li>" for b in d["bullets"]) + "</ul>"
    return out


def why_boxes():
    return "".join(f'<div class="ibox">{IC[ic]}<h3>{E(t)}</h3><p>{E(d)}</p></div>' for ic, t, d in C.WHY)


def link_list(items):
    return '<ul class="sq">' + "".join(f'<li><a href="{u}">{E(n)}</a></li>' for u, n in items) + "</ul>"


# ---------------------------------------------------------------- schema
def business_ld():
    d = {"@context": "https://schema.org", "@type": S.get("schema_type", "Plumber"), "@id": f"{DOMAIN}/#business",
         "name": N, "url": f"{DOMAIN}/", "telephone": S["phone_e164"]}
    if S.get("street"):
        d["address"] = {"@type": "PostalAddress", "streetAddress": S["street"], "addressLocality": S["city"],
                        "addressRegion": S["region"], "postalCode": S["zip"], "addressCountry": "US"}
    if S.get("founded_year"):
        d["foundingDate"] = str(S["founded_year"])
    d["areaServed"] = [{"@type": "City", "name": f"{c}, {S['region']}"} for _, c in AREAS]
    return d


def crumbs_for(pg):
    trail = [("/", "Home")]
    for u, lab in pg.get("crumbs", []):
        trail.append((u, lab))
    trail.append((pg["path"], pg["label"]))
    return trail


def ld_scripts(pg):
    blocks = [business_ld()]
    if pg["path"] != "/":
        blocks.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + u}
            for i, (u, n) in enumerate(crumbs_for(pg))]})
    return "".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in blocks)


# ---------------------------------------------------------------- page chrome
def head(pg, css_href, font_href):
    robots = "noindex, nofollow" if (not INDEXABLE or pg.get("noindex")) else "index, follow"
    canon = DOMAIN + pg["path"]
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(pg["title"])}</title>
<meta name="description" content="{E(pg["description"])}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{E(N)}">
<meta property="og:title" content="{E(pg["title"])}"><meta property="og:description" content="{E(pg["description"])}">
<meta property="og:url" content="{canon}">
<meta name="theme-color" content="{C.PALETTE["brand"]}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{font_href}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{css_href}">
{ld_scripts(pg)}
</head>"""


LOGO_IMG = getattr(C, "LOGO_IMG", None)    # client logo file (1x, 2x, w, h); None = template text logo
MASCOT = getattr(C, "MASCOT", None)        # client mascot (file, w, h); None = template icon panels


def logo_html():
    if LOGO_IMG:
        x1, x2, w, h = LOGO_IMG
        return (f'<a class="logo logo-img" href="/" aria-label="{E(N)} home"><img src="/assets/img/{x1}" '
                f'srcset="/assets/img/{x1} 1x, /assets/img/{x2} 2x" width="{w}" height="{h}" alt="{E(N)}"></a>')
    return (f'<a class="logo" href="/" aria-label="{E(N)} home">{IC["logo"]}'
            f'<span><b>{E(C.LOGO_TOP)}</b><small>{E(C.LOGO_SUB)}</small></span></a>')


def mascot_img(eager=False):
    f, w, h = MASCOT
    return f'<img src="/assets/img/{f}" width="{w}" height="{h}" alt=""{"" if eager else " loading=lazy"}>'


def panel(icon_svg, eager=False):
    """Image panel: the client's mascot when we have one, else the template icon."""
    if MASCOT:
        return f'<div class="hm mascot" aria-hidden="true">{mascot_img(eager)}</div>'
    return f'<div class="hm icon" aria-hidden="true">{icon_svg}</div>'


def header(pg):
    cur = pg["path"]
    ac = lambda u: ' aria-current="page"' if u == cur else ""
    svc_sub = f'<a href="/services/"{ac("/services/")}>All services</a>' + "".join(
        f'<a href="{SV[s]}"{ac(SV[s])}>{E(n)}</a>' for s, n, _ in SERVICES)
    area_sub = f'<a href="/service-areas/"{ac("/service-areas/")}>All service areas</a>' + "".join(
        f'<a href="{u}"{ac(u)}>{E(n)}</a>' for u, n in CITY_PAGES)
    in_svc = cur.startswith("/services/")
    in_area = cur.startswith("/service-areas/")
    desk = (f'<a href="/"{ac("/")}>Home</a><a href="/about/"{ac("/about/")}>About</a>'
            f'<div class="dd"><a href="/services/"{" class=on" if in_svc else ""}>Services</a><div class="ddm">{svc_sub}</div></div>'
            f'<div class="dd"><a href="/service-areas/"{" class=on" if in_area else ""}>Areas</a><div class="ddm">{area_sub}</div></div>'
            f'<a href="/contact/"{ac("/contact/")}>Contact</a>')
    mob = ['<a href="/">Home</a>', '<a href="/about/">About</a>', '<a href="/services/">Services</a>']
    mob += [f'<a class="sub" href="{SV[s]}">{E(n)}</a>' for s, n, _ in SERVICES]
    mob += ['<a href="/service-areas/">Areas</a>']
    mob += [f'<a class="sub" href="{u}">Plumber in {E(n)}</a>' for u, n in CITY_PAGES]
    mob += ['<a href="/contact/">Contact</a>']
    mob.append(f'<a class="btn pri" href="{TEL}">{IC["phone"]}Call {S["phone_display"]}</a>')
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><span>{IC["pin"]}{E(C.TOPBAR)}</span><span>{E(C.TOPBAR2)}</span><a href="{TEL}">{IC["phone"]}{E(C.TOPBAR_CALL)} {S["phone_display"]}</a></div></div>
<header class="site"><div class="wrap">
<a class="m-call" href="{TEL}" aria-label="Call {E(N)} {S["phone_display"]}">{IC["phone"]}<span>Call</span></a>
{logo_html()}
<nav class="desk" aria-label="Main">{desk}</nav>
<a class="btn pri hdr-cta" href="{TEL}">{IC["phone"]}{S["phone_display"]}</a>
<details class="menu"><summary>{IC["burger"]}<span>Menu</span></summary><nav aria-label="Mobile">{"".join(mob)}</nav></details>
</div></header>"""


def nap_html(strong=True):
    addr = f'{E(S["street"])}<br>{E(S["city"])}, {S["region"]} {S["zip"]}<br>' if S.get("street") else f'{E(S["city"])}, {S["region"]}<br>'
    return f'<strong>{E(N)}</strong><br>{addr}'


def aside(pg):
    cur = pg["path"]
    svc = "".join(f'<li><a href="{SV[s]}"' + (' aria-current="page"' if SV[s] == cur else "") + f">{E(n)}</a></li>" for s, n, _ in SERVICES)
    cities = "".join(f'<li><a href="{u}"' + (' aria-current="page"' if u == cur else "") + f">{E(n)}</a></li>" for u, n in CITY_PAGES)
    sms = f'<a class="btn ghost" href="{SMS}">{IC["text"]}Text</a>' if SMS else '<a class="btn ghost" href="/contact/">Contact</a>'
    return f"""<aside>
<div class="card callcard"><h2>{E(C.ASIDE_TITLE)}</h2><address class="nap">{nap_html()}
<a class="ph" href="{TEL}">{S["phone_display"]}</a></address>
<div class="btns"><a class="btn pri" href="{TEL}">{IC["phone"]}Call</a>{sms}</div></div>
<div class="card side"><h2>Services</h2><ul class="links">{svc}</ul></div>
<div class="card side"><h2>Areas we serve</h2><ul class="links">{cities}</ul></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SV[s]}">{E(n)}</a></li>' for s, n, _ in SERVICES)
    cities = "".join(f'<li><a href="{u}">{E(n)}</a></li>' for u, n in CITY_PAGES)
    co = "".join(f'<li><a href="{u}">{n}</a></li>' for u, n in [
        ("/about/", "About"), ("/services/", "Services"), ("/service-areas/", "Service areas"), ("/contact/", "Contact")])
    addr = f'{E(S["street"])}<br>{E(S["city"])}, {S["region"]} {S["zip"]}<br>' if S.get("street") else f'{E(S["city"])}, {S["region"]}<br>'
    mail = f'<br><a href="{MAILTO}">{S["email"]}</a>' if MAILTO else ""
    sms_bar = f'<a href="{SMS}">{IC["text"]}<span>Text</span></a>' if SMS else '<a href="/service-areas/">' + IC["pin"] + '<span>Areas</span></a>'
    return f"""<footer class="site"><div class="stripes" aria-hidden="true"></div><div class="wrap"><div class="grid">
<div class="fbrand">{logo_html()}<address class="nap">{addr}
<a href="{TEL}">{S["phone_display"]}</a>{mail}</address>
<a class="btn pri" href="{TEL}">{IC["phone"]}Call {S["phone_display"]}</a></div>
<div><h2>Services</h2><ul class="sq">{svc}</ul></div>
<div><h2>Areas</h2><ul class="sq">{cities}</ul></div>
<div><h2>Company</h2><ul class="sq">{co}</ul></div>
</div></div><div class="legal"><div class="wrap"><span>&copy; {YEAR} {E(N)} &middot; {E(C.LEGAL_LINE)}</span><a href="/contact/">Contact</a></div></div></footer>
<nav class="actbar" aria-label="Quick contact"><a href="{TEL}">{IC["phone"]}<span>Call</span></a>{sms_bar}<a href="/services/">{IC["drop"]}<span>Services</span></a><a href="/contact/">{IC["mail"]}<span>Contact</span></a></nav>
</body>
</html>
"""


# ---------------------------------------------------------------- home
def render_home(pg):
    hc = C.HERO_CARD
    ticks = "".join(f'<li>{IC["check"]}{E(t)}</li>' for t in hc["ticks"])
    card = f'<p>{E(hc["text"])}</p><ul class="ticks">{ticks}</ul>{call_btns(call_label="Call to book")}'
    strip_items = C.STRIP
    strip = "".join(f'<a href="{SV[s]}">{IC[s]}<span>{E(n)}</span></a>' for s, n in strip_items)
    nap_card = (f'<div class="card callcard"><h2>{E(C.ASIDE_TITLE)}</h2><address class="nap">{nap_html()}'
                f'<a class="ph" href="{TEL}">{S["phone_display"]}</a></address>{call_btns(call_label="Call")}</div>')
    return f"""<main id="main">
<section class="hero"><div class="hero-media slash">{panel(IC["drop"], eager=True)}</div>
<div class="wrap hero-grid"><div class="hero-txt">
<p class="eyebrow">{E(C.EYEBROW)}</p>
<h1>{two_tone(pg["h1"])}</h1>
<p class="lead">{inline(pg["lead"])}</p>
<a class="hero-phone" href="{TEL}">{IC["phone"]}{S["phone_display"]}</a>
<div class="btns"><a class="btn pri lg" href="{TEL}">{E(C.HERO_BTN)}</a></div>
</div>
<div class="hero-card"><h2>{E(hc["title"])}</h2><span class="bar" aria-hidden="true"></span>{card}</div>
</div></section>
<div class="wrap"><nav class="strip" style="--n:{len(strip_items)}" aria-label="Services">{strip}</nav></div>
<section class="band grey why" id="why"><div class="wrap why-grid">
<div class="why-l"><h2 class="sec">{two_tone(C.WHY_TITLE)}</h2>{f'<div class="why-img mascot" aria-hidden="true">{mascot_img()}</div>' if MASCOT else f'<div class="why-img icon" aria-hidden="true">{IC["drop"]}</div>'}</div>
<div class="iboxes">{why_boxes()}</div></div></section>
<section class="band about" id="about"><div class="wrap about-grid">
<div class="about-img">{nap_card}</div>
<div class="about-txt"><h2 class="sec">{two_tone(C.HOME_H2)}</h2><div class="dropcap">{copy_html("home")}</div></div>
</div></section>
<section class="band grey" id="services"><div class="wrap"><h2 class="sec">{two_tone("Plumbing services")}</h2>{services_cards()}</div></section>
<section class="band areas" id="service-areas"><div class="wrap"><h2 class="sec">{two_tone("Areas we serve")}</h2>{cities_list()}</div></section>
{cta_band()}
</main>"""


def page_hero(pg):
    trail = crumbs_for(pg)
    crumbs = " / ".join(f'<a href="{u}">{E(n)}</a>' for u, n in trail[:-1]) + f" / <span>{E(trail[-1][1])}</span>"
    lead = f'<p class="lead">{inline(pg["lead"])}</p>' if pg.get("lead") else ""
    icon = IC.get(pg.get("icon") or "drop")
    return f"""<section class="phero"><div class="phero-media slash" aria-hidden="true">{panel(icon, eager=True)}</div><div class="wrap"><div class="phero-txt">
<nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>
<h1>{two_tone(pg["h1"])}</h1>{lead}{call_btns()}
</div></div></section>"""


def render_contact(pg):
    trail = crumbs_for(pg)
    crumbs = " / ".join(f'<a href="{u}">{E(n)}</a>' for u, n in trail[:-1]) + f" / <span>{E(trail[-1][1])}</span>"
    cards = (f'<div class="contact"><a class="card big" href="{TEL}">{IC["phone"]}<div><b>{S["phone_display"]}</b><span>Call to book</span></div></a>')
    if SMS:
        cards += f'<a class="card" href="{SMS}">{IC["text"]}<div><b>Text us</b><span>{S["phone_display"]}</span></div></a>'
    if MAILTO:
        cards += f'<a class="card" href="{MAILTO}">{IC["mail"]}<div><b>Email</b><span>{S["email"]}</span></div></a>'
    cards += "</div>"
    nap = f'<address class="card nap">{nap_html()}</address>'
    return f"""<main id="main"><section class="csplit"><div class="csplit-txt">
<nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>
<h1>{two_tone(pg["h1"])}</h1><p class="lead">{inline(pg["lead"])}</p>
{cards}{nap}<p>{inline(pg["after"])}</p>
</div><div class="csplit-img" aria-hidden="true">{panel(IC["drop"], eager=True)}</div></section></main>"""


def render_page(pg, css_href, font_href):
    if pg.get("layout") == "home":
        main = render_home(pg)
    elif pg.get("layout") == "contact":
        main = render_contact(pg)
    else:
        inner = f'<div class="body">{pg["body"]}</div>'
        cols = f'<div class="cols">{inner}{aside(pg)}</div>'
        main = f'<main id="main">{page_hero(pg)}\n<div class="wrap">{cols}</div>\n{cta_band()}</main>'
    out = head(pg, css_href, font_href) + "\n" + header(pg) + "\n" + main + "\n" + footer()
    if BASE:
        out = re.sub(r'(href|src|action)="/(?!/)(?!' + re.escape(BASE.strip("/")) + '/)', lambda m: f'{m.group(1)}="{BASE}/', out)
    return out


# ---------------------------------------------------------------- pages (same slugs as before)
def build_pages():
    P = []
    P.append(dict(path="/", label="Home", layout="home", **C.HOME))
    P.append(dict(path="/services/", label="Services", icon="drop", title=C.SERVICES_HUB["title"],
                  description=C.SERVICES_HUB["description"], h1=C.SERVICES_HUB["h1"], lead=C.SERVICES_HUB["lead"],
                  body=services_cards()))
    for slug, name, blurb in SERVICES:
        P.append(dict(path=f"/services/{slug}/", label=name, icon=slug, crumbs=[("/services/", "Services")],
                      title=C.SERVICE_TITLE.format(n=name), description=C.SERVICE_DESC.format(n=name, b=blurb),
                      h1=C.SERVICE_H1.format(n=name), lead=blurb, body=copy_html(slug)))
    P.append(dict(path="/service-areas/", label="Service areas", icon="local", title=C.AREAS_HUB["title"],
                  description=C.AREAS_HUB["description"], h1=C.AREAS_HUB["h1"], lead=C.AREAS_HUB["lead"],
                  body=cities_list()))
    for slug, city in AREAS:
        body = (copy_html(slug) + f"<h2>Plumbing services in {E(city)}</h2>" + link_list([(SV[s], n) for s, n, _ in SERVICES]))
        P.append(dict(path=f"/service-areas/{slug}/", label=city, icon="pin", crumbs=[("/service-areas/", "Service areas")],
                      title=C.AREA_TITLE.format(c=city), description=C.AREA_DESC.format(c=city),
                      h1=C.AREA_H1.format(c=city), lead=C.AREA_LEAD.format(c=city), body=body))
    about_body = copy_html("about") + f'<h2>{two_tone(C.WHY_TITLE)}</h2><div class="iboxes">{why_boxes()}</div>'
    P.append(dict(path="/about/", label="About", icon="owner", title=C.ABOUT["title"], description=C.ABOUT["description"],
                  h1=C.ABOUT["h1"], lead=C.ABOUT["lead"], body=about_body))
    P.append(dict(path="/contact/", label="Contact", layout="contact", **C.CONTACT))
    return P


def write(rel, text):
    p = os.path.join(OUT, rel.lstrip("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f in KEEP:
            continue
        p = os.path.join(OUT, f)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    css = open(os.path.join(ROOT, "src", "site.css"), encoding="utf-8").read()
    hrefs = {}
    for fname in ["teko-latin.woff2"] + list(getattr(C, "FONTS", [])):   # {FONT} = Teko; {FONT:<file>} = any extra font
        font_src = os.path.join(ROOT, "src", "fonts", fname)
        fver = hashlib.md5(open(font_src, "rb").read()).hexdigest()[:8]
        shutil.copyfile(font_src, os.path.join(OUT, "assets", fname))
        hrefs[fname] = f"{BASE}/assets/{fname}?v={fver}"
        css = css.replace("{FONT:" + fname + "}", hrefs[fname])
    css = css.replace("{FONT}", hrefs["teko-latin.woff2"])
    font_href = hrefs[(getattr(C, "FONTS", None) or ["teko-latin.woff2"])[0]]
    img_src = os.path.join(ROOT, "src", "img")
    if os.path.isdir(img_src):
        shutil.copytree(img_src, os.path.join(OUT, "assets", "img"))
    P = C.PALETTE
    css = (css.replace("{BRAND}", P["brand"]).replace("{BRAND_DK}", P["brand_dk"])
              .replace("{ACCENT}", P["accent"]).replace("{DARK}", P["dark"]))
    ver = hashlib.md5(css.encode()).hexdigest()[:8]
    write("/assets/site.css", css)
    css_href = f"{BASE}/assets/site.css?v={ver}"
    write("/favicon.svg", IC["logo"].replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))

    pages = build_pages()
    for pg in pages:
        write(pg["path"] + "index.html", render_page(pg, css_href, font_href))
    nf = dict(path="/404/", label="Not found", noindex=True, title=f"Page not found | {N}", h1="Page not found",
              description="This page doesn't exist.", icon="drop",
              lead="That page isn't here. Pick a page from the menu or call {call}.", body=services_cards())
    write("/404.html", render_page(nf, css_href, font_href))

    today = datetime.date.today().isoformat()
    if INDEXABLE:
        urls = "".join(f"<url><loc>{DOMAIN}{p['path']}</loc><lastmod>{today}</lastmod></url>" for p in pages)
        write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
        write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    else:
        write("/robots.txt", "# DRAFT - not approved yet. Set INDEXABLE = True in content.py to open the site to search engines.\nUser-agent: *\nDisallow: /\n")
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    print(f"built {len(pages)} pages + 404 - INDEXABLE={INDEXABLE} -> {OUT}")


if __name__ == "__main__":
    main()
