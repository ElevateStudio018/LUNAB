#!/usr/bin/env python3
"""Bygger LUNAB Entreprenad & Transports webbplats till docs/.

All text, alla tjänster och kontaktuppgifter finns här. Ändra och kör:  python3 scripts/build.py
"""
from html import escape
from pathlib import Path
import json

# Elevate Studio's credit under every footer: the mark and the name, the whole of it one link to elevatestudio.nu.
ELEVATE_CREDIT = '''<!-- elevate-credit -->
<style>.elevate-credit{max-width:1240px;margin:24px auto 0;padding:20px 16px 0;border-top:1px solid rgba(128,128,128,.25);display:flex;justify-content:center;box-sizing:border-box}.elevate-credit a{display:inline-flex;align-items:center;gap:8px;padding:8px 0;font:inherit;font-size:13px;line-height:1;color:inherit;opacity:.55;text-decoration:none;transition:opacity .2s}.elevate-credit a:hover,.elevate-credit a:focus-visible{opacity:1}.elevate-credit svg{width:16px;height:16px;flex:none;display:block}@media(min-width:1024px){.elevate-credit a{font-size:14px}}</style>
<div class="elevate-credit"><a href="https://elevatestudio.nu" target="_blank" rel="noopener"><svg viewBox="0 0 1884.3 1353.9" aria-hidden="true"><path d="M0.0 1353.9 L1218.7 0.0 L1218.7 329.1 L479.7 1136.4 L786.7 1132.4 L1215.5 687.4 L1884.3 1349.9 L1590.1 1349.9 L1218.6 994.7 L865.4 1349.9Z" fill="currentColor"/></svg>Byggd av Elevate Studio</a></div>
'''


OUT = Path(__file__).resolve().parent.parent / "docs"

NAME = "LUNAB Entreprenad & Transport"
SHORT = "LUNAB"
TEL = "070-571 54 20"
TEL_HREF = "+46705715420"
EMAIL = "nicklas@lunab.eu"
STREET = "Ekås 180"
ZIP = "442 98"
CITY = "Kode"
OLD_SITE = "https://www.lunab.eu/"
# Förfrågningar skickas via FormSubmit. Under förhandsvisningen går de till Elevate Studio – byt till
# EMAIL vid lansering (första förfrågan till en ny adress skickar ett aktiveringsmejl).
FORM_EMAIL = "elevate.studio018@gmail.com"
SITE_URL = "https://elevatestudio018.github.io/LUNAB/"
MAP_Q = "LUNAB+Entreprenad,+Ek%C3%A5s+180,+442+98+Kode"

# Tjänsterna från företagsunderlaget. img=None ger ett grafiskt kort i stället för foto (inget eget foto passar).
SERVICES = [
    {"id": "gravning", "title": "Gräventreprenad", "img": "grav-villa", "icon": "dig",
     "short": "Schaktning och grävarbeten för husbyggen, tomter och anläggningar.",
     "long": "Vi utför grävarbeten inför byggen, vid ledningsdragning och när en tomt ska förberedas. "
             "Berätta vad som ska göras så går vi igenom förutsättningarna och lägger upp arbetet tillsammans med dig."},
    {"id": "mark", "title": "Mark- och grundarbeten", "img": "markarbete-grus", "icon": "layers",
     "short": "Markberedning och underarbete inför grund, uppfart och plan yta.",
     "long": "Ett hållbart resultat börjar under ytan. Vi arbetar med markberedning och grundläggande markarbeten – "
             "från att jämna av och fylla upp till att förbereda ytan inför grund, uppfart eller planering."},
    {"id": "transport", "title": "Transport", "img": None, "icon": "truck",
     "short": "Vägtransporter och godstransporter, även i samband med våra markjobb.",
     "long": "Vi har verksamhet inom vägtransporter och godstransporter. Det gör att material kan fraktas i samband "
             "med markarbetet eller som ett eget uppdrag. Hör av dig med vad som ska fraktas och vart."},
    {"id": "snorojning", "title": "Snöröjning", "img": "hjullastare-kvall", "icon": "snow",
     "short": "Snöröjning när vintern kommer – kontakta oss för upplägg.",
     "long": "Snöröjning är en av våra verksamheter. Kontakta oss om ytor som behöver hållas framkomliga under "
             "vintern så berättar vi hur vi kan hjälpa till."},
    {"id": "jord", "title": "Jordbearbetning", "img": "traktor-natt", "icon": "sprout",
     "short": "Bearbetning av jord och mark utifrån vad ytan ska användas till.",
     "long": "Vi utför jordbearbetning som en del av vårt arbete med mark. Beskriv ytan och vad den ska användas till, "
             "så tar vi det därifrån."},
    {"id": "personal", "title": "Personaluthyrning", "img": None, "icon": "people",
     "short": "Uthyrning av personal inom våra verksamhetsområden.",
     "long": "Vi hyr ut personal inom entreprenad, mark och transport. Kontakta oss och berätta om behovet och "
             "under vilken period det gäller."},
]

NAV = [("index.html", "Hem"), ("tjanster.html", "Tjänster"), ("om-oss.html", "Om oss"), ("kontakt.html", "Kontakt")]

ICONS = {
    "phone": '<path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/>',
    "mail": '<path d="M3 5h18v14H3z" fill="none" stroke="currentColor" stroke-width="2"/><path d="m3 6 9 7 9-7" fill="none" stroke="currentColor" stroke-width="2"/>',
    "pin": '<path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/>',
    "arrow": '<path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "dig": '<path d="M3 20h18M5 20l3-7h5l2 3M8 13l4-8 6 3-2 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5zM3 13l9 5 9-5M3 17l9 5 9-5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
    "truck": '<path d="M2 6h12v10H2zM14 10h4l4 4v2h-8z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><circle cx="6" cy="18" r="2" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="18" cy="18" r="2" fill="none" stroke="currentColor" stroke-width="1.8"/>',
    "snow": '<path d="M12 2v20M4 6.5l16 11M20 6.5 4 17.5M9 3l3 3 3-3M9 21l3-3 3 3" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "sprout": '<path d="M12 21v-8M12 13c0-4 3-7 8-7 0 4-3 7-8 7zM12 15c0-3-2.5-5.5-7-5.5 0 3 2.5 5.5 7 5.5zM4 21h16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
    "people": '<circle cx="9" cy="8" r="3.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M2.5 20c.5-3.5 3.2-5.5 6.5-5.5s6 2 6.5 5.5M16 4.8a3.3 3.3 0 0 1 0 6.4M18 14.8c2 .6 3.3 2.4 3.5 5.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "clock": '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
}


def icon(name, cls="ic"):
    fill = "currentColor" if name in ("phone", "pin") else "none"
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="{fill}" aria-hidden="true">{ICONS[name]}</svg>'


def img(name, alt, cls="", eager=False, sizes="(min-width: 960px) 50vw, 100vw"):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="img/{name}.jpg" srcset="img/{name}-s.jpg 820w, img/{name}.jpg 1920w" '
            f'sizes="{sizes}" alt="{escape(alt)}" {load}>')


def eyebrow(num, text):
    return f'<p class="eyebrow"><span class="eb-num">{num}</span><span class="eb-line"></span>{escape(text)}</p>'


def call_pill(cls="pill-orange"):
    return f'<a class="pill {cls}" href="tel:{TEL_HREF}">{icon("phone", "pi")}Ring {TEL}</a>'


def head(page, title, desc, image="hero-maskin"):
    url = SITE_URL + ("" if page == "index.html" else page)
    ld = {
        "@context": "https://schema.org", "@type": "GeneralContractor", "name": NAME, "url": SITE_URL,
        "telephone": "+46 70 571 54 20", "email": EMAIL, "image": SITE_URL + "img/hero-maskin.jpg",
        "logo": SITE_URL + "img/symbol-512.png", "sameAs": [OLD_SITE],
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "postalCode": ZIP,
                    "addressLocality": CITY, "addressCountry": "SE"},
        "areaServed": "Kode med omnejd",
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["title"]}} for s in SERVICES],
    }
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == page else ""}>{label}</a>' for href, label in NAV)
    mlinks = "".join(f'<li><a href="{href}">{label}</a></li>' for href, label in NAV)
    return f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="sv_SE">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}img/{image}.jpg">
<meta name="theme-color" content="#151618">
<link rel="icon" href="img/symbol-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="img/symbol-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..900&display=swap">
<link rel="stylesheet" href="assets/site.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Hoppa till innehållet</a>
<header class="head" id="head">
  <div class="wrap bar">
    <a class="logo" href="index.html" aria-label="{NAME} – startsidan"><img class="logo-img" src="img/lunab-logo-ljus.png" alt="LUNAB.eu Entreprenad &amp; Transport" width="444" height="117"></a>
    <nav class="nav" aria-label="Huvudmeny">{links}</nav>
    <a class="pill pill-orange head-cta" href="kontakt.html#offert">Begär offert {icon("arrow", "pi")}</a>
    <a class="round round-orange head-round" href="tel:{TEL_HREF}" aria-label="Ring {TEL}">{icon("phone", "pi")}</a>
    <button class="burger" id="menuBtn" type="button" aria-expanded="false" aria-controls="menu" aria-label="Meny"><span></span><span></span></button>
  </div>
  <div class="menu" id="menu" hidden>
    <div class="wrap">
      <ul class="menu-main">{mlinks}</ul>
      <div class="btns">{call_pill()}<a class="pill pill-line" href="kontakt.html#offert">Begär offert</a></div>
    </div>
  </div>
</header>
<main id="main">
'''


def foot():
    links = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV)
    svc = "".join(f'<li><a href="tjanster.html#{s["id"]}">{s["title"]}</a></li>' for s in SERVICES)
    return f'''</main>
<section class="cta-band">
  <div class="wrap cta-in">
    <div>
      <h2>Har du ett projekt på gång?</h2>
      <p>Ring, mejla eller skicka en förfrågan – så pratar vi om vad som ska göras.</p>
    </div>
    <div class="btns">{call_pill()}<a class="pill pill-light" href="kontakt.html#offert">Begär offert {icon("arrow", "pi")}</a></div>
  </div>
</section>
<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img class="foot-logo" src="img/lunab-logo-ljus.png" alt="{NAME}" width="444" height="117" loading="lazy">
        <p class="foot-tag">Gräventreprenad, markarbeten och transport från {STREET} i {CITY}.</p>
      </div>
      <div><p class="foot-h">Sidor</p><ul>{links}</ul></div>
      <div><p class="foot-h">Tjänster</p><ul>{svc}</ul></div>
      <div>
        <p class="foot-h">Kontakt</p>
        <p><a href="tel:{TEL_HREF}">{TEL}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p>{NAME}<br>{STREET}<br>{ZIP} {CITY}</p>
      </div>
    </div>
    <div class="foot-end">
      <span>© <span data-year></span> {NAME}</span>
      <a href="{OLD_SITE}">lunab.eu</a>
    </div>
  </div>
{ELEVATE_CREDIT}</footer>
<a class="fab" href="tel:{TEL_HREF}" aria-label="Ring {TEL}">{icon("phone", "pi")}</a>
<script src="assets/site.js" defer></script>
</body>
</html>
'''


def service_card(s, link=True):
    if s["img"]:
        media = f'<div class="card-ph">{img(s["img"], s["title"] + " – LUNAB", sizes="(min-width: 1100px) 33vw, (min-width: 760px) 50vw, 100vw")}</div>'
    else:
        media = f'<div class="card-ph card-ph--brand">{icon(s["icon"], "card-ic")}<span class="card-l" aria-hidden="true"></span></div>'
    inner = f'''{media}
      <div class="card-body">
        <span class="card-icon">{icon(s["icon"])}</span>
        <h3>{s["title"]}</h3>
        <p>{s["short"]}</p>
        <span class="more">Läs mer {icon("arrow", "pi")}</span>
      </div>'''
    href = f"tjanster.html#{s['id']}"
    return f'<li class="card reveal"><a href="{href}">{inner}</a></li>'


def contact_list():
    return f'''<ul class="clist">
      <li><span class="round round-orange">{icon("phone", "pi")}</span><div><span class="cl-h">Telefon</span><a href="tel:{TEL_HREF}">{TEL}</a></div></li>
      <li><span class="round round-dark">{icon("mail", "pi")}</span><div><span class="cl-h">E-post</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
      <li><span class="round round-dark">{icon("pin", "pi")}</span><div><span class="cl-h">Adress</span><a href="https://www.google.com/maps/search/?api=1&amp;query={MAP_Q}" rel="noopener">{STREET}, {ZIP} {CITY}</a></div></li>
      <li><span class="round round-dark">{icon("clock", "pi")}</span><div><span class="cl-h">Öppettider</span><span>Öppet till kl. 18.00 enligt Google Maps</span></div></li>
    </ul>'''


def form():
    opts = "".join(f"<option>{s['title']}</option>" for s in SERVICES) + "<option>Annat</option>"
    return f'''<form class="form" id="qform" novalidate data-endpoint="https://formsubmit.co/ajax/{FORM_EMAIL}">
      <div class="row2">
        <div class="field"><label for="f-namn">Namn<span class="req" aria-hidden="true">*</span></label>
          <input id="f-namn" name="namn" autocomplete="name" required><span class="err" id="e-namn" hidden>Skriv ditt namn.</span></div>
        <div class="field"><label for="f-foretag">Företag <span class="opt">(valfritt)</span></label>
          <input id="f-foretag" name="foretag" autocomplete="organization"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="f-tel">Telefonnummer<span class="req" aria-hidden="true">*</span></label>
          <input id="f-tel" name="tel" type="tel" autocomplete="tel" inputmode="tel" required><span class="err" id="e-tel" hidden>Skriv ett telefonnummer vi kan nå dig på.</span></div>
        <div class="field"><label for="f-epost">E-post<span class="req" aria-hidden="true">*</span></label>
          <input id="f-epost" name="epost" type="email" autocomplete="email" required><span class="err" id="e-epost" hidden>Skriv en giltig e-postadress, t.ex. namn@exempel.se.</span></div>
      </div>
      <div class="field"><label for="f-typ">Vad gäller din förfrågan?<span class="req" aria-hidden="true">*</span></label>
        <select id="f-typ" name="typ" required><option value="">Välj …</option>{opts}</select><span class="err" id="e-typ" hidden>Välj vad förfrågan gäller.</span></div>
      <div class="field"><label for="f-besk">Beskrivning av projektet<span class="req" aria-hidden="true">*</span></label>
        <textarea id="f-besk" name="besk" rows="6" placeholder="Vad ska göras, var och ungefär när?" required></textarea><span class="err" id="e-besk" hidden>Beskriv kort vad det gäller.</span></div>
      <div class="hp" aria-hidden="true"><label for="f-web">Lämna tomt</label><input id="f-web" name="web" tabindex="-1" autocomplete="off"></div>
      <p class="small">Fält markerade med <span class="req">*</span> är obligatoriska. Uppgifterna används bara för att besvara din förfrågan.</p>
      <div><button class="pill pill-orange" type="submit">Skicka förfrågan {icon("arrow", "pi")}</button></div>
      <p class="send-err" id="send-err" role="alert" hidden>Förfrågan kunde inte skickas just nu. Försök igen, ring <a href="tel:{TEL_HREF}">{TEL}</a> eller mejla <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </form>
    <div class="done" id="qdone" tabindex="-1" hidden role="status">
      <p class="done-h">Tack – din förfrågan är skickad!</p>
      <p>Vi återkommer så snart vi kan. Brådskar det går det bra att ringa <a href="tel:{TEL_HREF}">{TEL}</a>.</p>
      <p><button class="link" type="button" id="qagain">Skicka en till förfrågan</button></p>
    </div>'''


def map_block():
    return (f'<div class="map"><iframe title="Karta: {STREET}, {ZIP} {CITY}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
            f'src="https://maps.google.com/maps?q={MAP_Q}&amp;z=13&amp;output=embed"></iframe></div>')


SWOOSH = '''<svg class="swoosh" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true">
  <path d="M0 90V62C360 20 900 6 1440 30v60z" fill="var(--paper)"/>
  <path d="M0 62C360 20 900 6 1440 30" fill="none" stroke="var(--orange)" stroke-width="6"/>
  <path d="M0 74C420 34 960 22 1440 44" fill="none" stroke="var(--steel)" stroke-width="3" opacity=".8"/>
</svg>'''


def page_index():
    cards = "".join(service_card(s) for s in SERVICES)
    return head("index.html", "LUNAB Entreprenad & Transport – gräventreprenad, markarbeten och transport i Kode",
                "LUNAB Entreprenad & Transport i Kode utför gräventreprenad, mark- och grundarbeten, transporter, "
                "snöröjning, jordbearbetning och personaluthyrning. Ring 070-571 54 20.") + f'''
<section class="hero">
  <div class="hero-ph">{img("hero-maskin", "LUNAB:s grävlastare på en arbetsplats i skymningen", eager=True, sizes="100vw")}</div>
  <div class="wrap hero-in">
    <p class="hero-kicker"><span class="dot"></span>Entreprenad &amp; Transport · {CITY}</p>
    <h1>Entreprenad och transport med fokus på ett väl utfört arbete</h1>
    <div class="hero-row">
      <p class="hero-lead">LUNAB Entreprenad &amp; Transport arbetar med markarbeten, gräventreprenad och transportlösningar. Kontakta oss för att diskutera ditt projekt och dina behov.</p>
      <div class="btns">
        <a class="pill pill-orange" href="kontakt.html#offert">Kontakta oss {icon("arrow", "pi")}</a>
        <a class="pill pill-glass" href="tjanster.html">Se våra tjänster</a>
      </div>
    </div>
  </div>
  {SWOOSH}
</section>

<section class="facts">
  <div class="wrap facts-grid">
    <div class="fact reveal"><p class="fact-h">Verksamhet</p><p class="fact-big">6</p><p>områden – från grävning och mark till transport och snöröjning</p></div>
    <div class="fact reveal"><p class="fact-h">Bas</p><p class="fact-big">{CITY}</p><p>{STREET}, {ZIP} {CITY}</p></div>
    <div class="fact reveal"><p class="fact-h">Ring direkt</p><p class="fact-big fact-tel"><a href="tel:{TEL_HREF}">{TEL}</a></p><p>Prata med oss om ditt projekt</p></div>
    <div class="fact reveal"><p class="fact-h">Öppettider</p><p class="fact-big">18.00</p><p>Öppet till kl. 18 enligt Google Maps</p></div>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <figure class="ph reveal">{img("grav-villa", "LUNAB:s grävlastare vid ett nybyggt hus")}</figure>
    <div class="reveal">
      {eyebrow("01", "Om LUNAB")}
      <h2>Maskiner, mark och transport – från en och samma kontakt</h2>
      <p class="lead">LUNAB Entreprenad &amp; Transport utför gräventreprenad, mark- och grundarbeten och transporter. Vi utgår från {STREET} i {CITY}.</p>
      <p>Hos oss pratar du direkt med den som planerar och utför arbetet. Berätta vad du behöver hjälp med, så går vi igenom förutsättningarna tillsammans.</p>
      <div class="btns">
        <a class="pill pill-dark" href="om-oss.html">Mer om oss</a>
        <a class="pill pill-line-dark" href="tjanster.html">Våra tjänster</a>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-dark" id="tjanster">
  <div class="wrap">
    <div class="sec-head">
      <div>{eyebrow("02", "Tjänster")}<h2>Det här arbetar vi med</h2></div>
      <a class="arrow-link" href="tjanster.html">Alla tjänster <span class="round round-line">{icon("arrow", "pi")}</span></a>
    </div>
    <ul class="cards">{cards}</ul>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <div>{eyebrow("03", "Varför LUNAB?")}<h2>Enkelt att ta kontakt, tydligt vad vi gör</h2></div>
    </div>
    <ol class="why">
      <li class="reveal"><span class="why-n">01</span><h3>Flera tjänster, en kontakt</h3><p>Grävning, markarbeten och transport hos samma företag – färre led när arbetet ska planeras.</p></li>
      <li class="reveal"><span class="why-n">02</span><h3>Direkt kontakt</h3><p>Ring {TEL} eller mejla – du pratar med oss direkt, inte med en växel.</p></li>
      <li class="reveal"><span class="why-n">03</span><h3>Lokalt i {CITY}</h3><p>Vi finns på {STREET} i {CITY} och tar gärna uppdrag i närområdet.</p></li>
      <li class="reveal"><span class="why-n">04</span><h3>Hela året</h3><p>Markarbete när marken tillåter, snöröjning när vintern kommer.</p></li>
    </ol>
  </div>
</section>

<section class="gallery" aria-label="Bilder från LUNAB">
  <div class="wrap">
    <div class="gal">
      <figure class="g1 reveal">{img("markarbete-grus", "Grävmaskin som planerar en grusyta", sizes="(min-width: 960px) 60vw, 100vw")}</figure>
      <figure class="g2 reveal">{img("traktor-natt", "Traktor med lastare i arbete på kvällen", sizes="(min-width: 960px) 30vw, 50vw")}</figure>
      <figure class="g3 reveal">{img("gator", "LUNAB:s terrängfordon på en klipphäll", sizes="(min-width: 960px) 30vw, 50vw")}</figure>
      <figure class="g4 reveal">{img("hjullastare-kvall", "Grävlastare på en arbetsplats en vinterkväll", sizes="(min-width: 960px) 60vw, 100vw")}</figure>
    </div>
  </div>
</section>

<section class="sec sec-tint" id="kontakt">
  <div class="wrap split split-top">
    <div class="reveal">
      {eyebrow("04", "Kontakt")}
      <h2>Kontakta oss</h2>
      <p class="lead">Ring, mejla eller skicka en förfrågan. Berätta gärna vad som ska göras, var och ungefär när.</p>
      {contact_list()}
      <div class="btns">{call_pill()}<a class="pill pill-dark" href="kontakt.html#offert">Begär offert {icon("arrow", "pi")}</a></div>
    </div>
    <div class="reveal">{map_block()}</div>
  </div>
</section>
''' + foot()


def page_services():
    blocks = []
    for i, s in enumerate(SERVICES):
        if s["img"]:
            media = f'<figure class="ph">{img(s["img"], s["title"] + " – LUNAB")}</figure>'
        else:
            media = f'<div class="ph ph-brand">{icon(s["icon"], "card-ic")}<span class="card-l" aria-hidden="true"></span></div>'
        blocks.append(f'''<article class="svc reveal{' svc-flip' if i % 2 else ''}" id="{s["id"]}">
      {media}
      <div>
        {eyebrow(f"{i + 1:02d}", "Tjänst")}
        <h2>{s["title"]}</h2>
        <p class="lead">{s["short"]}</p>
        <p>{s["long"]}</p>
        <div class="btns">
          <a class="pill pill-orange" href="kontakt.html?typ={escape(s["title"])}#offert">Begär offert {icon("arrow", "pi")}</a>
          <a class="pill pill-line-dark" href="tel:{TEL_HREF}">{icon("phone", "pi")}{TEL}</a>
        </div>
      </div>
    </article>''')
    chips = "".join(f'<a class="pill pill-dark pill-sm" href="#{s["id"]}">{s["title"]}</a>' for s in SERVICES)
    return head("tjanster.html", "Tjänster – gräventreprenad, markarbeten, transport | LUNAB",
                "LUNAB:s tjänster: gräventreprenad, mark- och grundarbeten, transport, snöröjning, jordbearbetning "
                "och personaluthyrning i Kode med omnejd.", "markarbete-grus") + f'''
<section class="hero hero-small">
  <div class="hero-ph">{img("markarbete-grus", "Grävmaskin som planerar en grusyta", eager=True, sizes="100vw")}</div>
  <div class="wrap hero-in">
    <p class="crumbs"><a href="index.html">Hem</a> / Tjänster</p>
    <h1>Våra tjänster</h1>
    <p class="hero-lead">Entreprenad, markarbeten och transport – sex verksamhetsområden hos samma företag.</p>
    <div class="btns chips">{chips}</div>
  </div>
  {SWOOSH}
</section>
<section class="sec">
  <div class="wrap svcs">{''.join(blocks)}</div>
</section>
''' + foot()


def page_about():
    return head("om-oss.html", "Om oss – LUNAB Entreprenad & Transport i Kode",
                "LUNAB Entreprenad & Transport är ett företag inom entreprenad, markarbeten och transporter med bas "
                "på Ekås 180 i Kode.", "grav-villa") + f'''
<section class="hero hero-small">
  <div class="hero-ph">{img("grav-villa", "LUNAB:s grävlastare vid ett nybyggt hus", eager=True, sizes="100vw")}</div>
  <div class="wrap hero-in">
    <p class="crumbs"><a href="index.html">Hem</a> / Om oss</p>
    <h1>Om LUNAB</h1>
    <p class="hero-lead">Ett företag inom entreprenad, markarbeten och transport – med bas i {CITY}.</p>
  </div>
  {SWOOSH}
</section>
<section class="sec">
  <div class="wrap split">
    <div class="reveal">
      {eyebrow("01", "Vilka vi är")}
      <h2>Entreprenad och transport från {CITY}</h2>
      <p class="lead">LUNAB Entreprenad &amp; Transport arbetar med gräventreprenad, mark- och grundarbeten, vägtransporter och godstransporter.</p>
      <p>Utöver det utför vi snöröjning och jordbearbetning, och vi hyr ut personal inom våra verksamhetsområden. Det betyder att flera delar av ett markprojekt kan samordnas hos samma företag.</p>
      <p>Vi tror på rak kommunikation: du berättar vad som behöver göras, vi går igenom förutsättningarna och lägger upp arbetet därefter.</p>
    </div>
    <figure class="ph reveal">{img("gator", "LUNAB:s terrängfordon på en klipphäll")}</figure>
  </div>
</section>
<section class="sec sec-dark">
  <div class="wrap">
    <div class="sec-head"><div>{eyebrow("02", "Verksamhetsområden")}<h2>Det vi gör</h2></div>
      <a class="arrow-link" href="tjanster.html">Läs om tjänsterna <span class="round round-line">{icon("arrow", "pi")}</span></a></div>
    <ul class="areas">{''.join(f'<li class="reveal"><a href="tjanster.html#{s["id"]}"><span class="card-icon">{icon(s["icon"])}</span>{s["title"]}</a></li>' for s in SERVICES)}</ul>
  </div>
</section>
<section class="sec">
  <div class="wrap split">
    <figure class="ph reveal">{img("hjullastare-kvall", "Grävlastare på en arbetsplats en vinterkväll")}</figure>
    <div class="reveal">
      {eyebrow("03", "Kontakt")}
      <h2>Prata med oss direkt</h2>
      <p class="lead">Har du ett projekt, en fråga eller ett behov av transport? Hör av dig.</p>
      {contact_list()}
    </div>
  </div>
</section>
''' + foot()


def page_contact():
    return head("kontakt.html", "Kontakt och offert – LUNAB Entreprenad & Transport, Kode",
                "Kontakta LUNAB Entreprenad & Transport: ring 070-571 54 20, mejla nicklas@lunab.eu eller skicka en "
                "offertförfrågan. Ekås 180, 442 98 Kode.", "hjullastare-kvall") + f'''
<section class="hero hero-small">
  <div class="hero-ph">{img("hjullastare-kvall", "Grävlastare på en arbetsplats en vinterkväll", eager=True, sizes="100vw")}</div>
  <div class="wrap hero-in">
    <p class="crumbs"><a href="index.html">Hem</a> / Kontakt</p>
    <h1>Kontakta oss</h1>
    <p class="hero-lead">Ring, mejla eller skicka en förfrågan om ditt projekt.</p>
    <div class="btns">{call_pill()}<a class="pill pill-glass" href="mailto:{EMAIL}">{icon("mail", "pi")}{EMAIL}</a></div>
  </div>
  {SWOOSH}
</section>
<section class="sec" id="offert">
  <div class="wrap split split-top">
    <div class="reveal">
      {eyebrow("01", "Kontaktuppgifter")}
      <h2>{NAME}</h2>
      {contact_list()}
      {map_block()}
    </div>
    <div class="reveal form-card">
      {eyebrow("02", "Offertförfrågan")}
      <h2>Begär offert</h2>
      <p>Beskriv kort vad som ska göras så återkommer vi.</p>
      {form()}
    </div>
  </div>
</section>
''' + foot()


def page_404():
    return head("404.html", "Sidan finns inte – LUNAB", "Sidan kunde inte hittas.") + f'''
<section class="hero hero-small">
  <div class="hero-ph">{img("traktor-natt", "", eager=True, sizes="100vw")}</div>
  <div class="wrap hero-in">
    <h1>Sidan finns inte</h1>
    <p class="hero-lead">Länken kan vara gammal eller felstavad.</p>
    <div class="btns"><a class="pill pill-orange" href="index.html">Till startsidan</a>{call_pill("pill-glass")}</div>
  </div>
</section>
''' + foot()


def main():
    pages = {"index.html": page_index, "tjanster.html": page_services, "om-oss.html": page_about,
             "kontakt.html": page_contact, "404.html": page_404}
    for name, fn in pages.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
    locs = "".join(f"<url><loc>{SITE_URL}{'' if u == 'index.html' else u}</loc></url>" for u in pages if u != "404.html")
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{locs}</urlset>\n',
        encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print("Byggt:", ", ".join(pages))


if __name__ == "__main__":
    main()
