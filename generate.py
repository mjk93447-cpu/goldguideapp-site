#!/usr/bin/env python3
"""Generate GoldMeet SEO pages. Run from repo root: python site/generate.py"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORIGIN = "https://mjk93447-cpu.github.io/goldguideapp-site"
BRAND = "GoldMeet"
SUPPORT = "support@goldguideapp.com"

CITIES = [
    ("mumbai", "Mumbai", "मुंबई", "Zaveri Bazaar and Opera House", "Meet at a jeweller or bank in Zaveri Bazaar, Opera House, or Fort. Assay on site. Never at a private home."),
    ("delhi", "Delhi", "दिल्ली", "Chandni Chowk and Karol Bagh", "Meet in Chandni Chowk, Karol Bagh, or a bank branch with CCTV. Test karat and weight before you pay."),
    ("bangalore", "Bangalore", "बेंगलुरु", "Commercial Street and Jayanagar", "Commercial Street and Jayanagar jewellers plus bank branches. Fair metal price uses Bengaluru's city spread."),
    ("chennai", "Chennai", "चेन्नई", "T. Nagar and Sowcarpet", "T. Nagar and Sowcarpet gold streets. Chennai spread is slightly below Mumbai on our board."),
    ("kolkata", "Kolkata", "कोलकाता", "Bowbazar", "Bowbazar jewellers and public-sector banks. Bring HUID or hallmark card if you have it."),
    ("hyderabad", "Hyderabad", "हैदराबाद", "Pathergatti", "Pathergatti and Laad Bazaar belt. Confirm purity with a tester at the shop."),
    ("ahmedabad", "Ahmedabad", "अहमदाबाद", "Manek Chowk", "Manek Chowk jewellery cluster. Platform does not escrow cash or hold your gold."),
    ("pune", "Pune", "पुणे", "Laxmi Road", "Laxmi Road and nearby banks. Ranked by travel for both buyer and seller."),
    ("jaipur", "Jaipur", "जयपुर", "Johari Bazaar", "Johari Bazaar. Unverified tester badges stay labelled unverified."),
    ("surat", "Surat", "सूरत", "Mahidharpura", "Mahidharpura jewellery market. Used gold only — no making charges in fair price."),
]


def page(title: str, desc: str, path: str, body: str, lang: str = "en", extra_json: str = "") -> str:
    canonical = ORIGIN + "/" if path in ("", "index.html") else f"{ORIGIN}/{path.lstrip('/')}"
    hi = f"{ORIGIN}/hi/" if lang == "en" else f"{ORIGIN}/hi/{path}" if path.startswith("cities") else f"{ORIGIN}/hi/"
    en = f"{ORIGIN}/" if path in ("", "index.html") else f"{ORIGIN}/{path}"
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="googlebot" content="index,follow">
  <meta name="theme-color" content="#1A2B3C">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="en-IN" href="{en if lang=='en' else ORIGIN + '/'}">
  <link rel="alternate" hreflang="hi-IN" href="{hi}">
  <link rel="alternate" hreflang="x-default" href="{ORIGIN}/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:locale" content="{'hi_IN' if lang=='hi' else 'en_IN'}">
  <meta name="twitter:card" content="summary">
  <link rel="stylesheet" href="{'../' if '/' in path else ''}assets/style.css">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"WebPage","name":{json.dumps(title)},"description":{json.dumps(desc)},"url":{json.dumps(canonical)},"isPartOf":{{"@type":"WebSite","name":"GoldMeet","url":{json.dumps(ORIGIN + "/")}}}}}
  </script>
  {extra_json}
</head>
<body>
<header>
  <a class="brand" href="{'../' if '/' in path else ''}index.html">GoldMeet</a>
  <nav>
    <a href="{'../' if '/' in path else ''}index.html">Home</a>
    <a href="{'../' if '/' in path else ''}rates.html">Today's rate</a>
    <a href="{'../' if '/' in path else ''}how-it-works.html">How it works</a>
    <a href="{'../' if '/' in path else ''}safety.html">Safety</a>
    <a href="{'../' if '/' in path else ''}faq.html">FAQ</a>
    <a href="{'../' if '/' in path else ''}join.html">Join</a>
    <a class="lang" href="{'hi/index.html' if '/' not in path else '../hi/index.html'}">हिन्दी</a>
  </nav>
</header>
{body}
<footer>
  <div class="wrap">
    <p><strong>GoldMeet</strong> by Gold Guide · {SUPPORT}</p>
    <p>We match buyers and sellers of used gold in India. We do not hold gold, do not escrow money, and do not certify purity. Meet only in a shop or bank.</p>
    <p>
      <a href="{'../' if '/' in path else ''}privacy.html">Privacy</a> ·
      <a href="{'../' if '/' in path else ''}deletion.html">Data deletion</a> ·
      <a href="{'../' if '/' in path else ''}llms.txt">llms.txt</a> ·
      <a href="https://github.com/mjk93447-cpu/goldguideapp-site">Source</a>
    </p>
  </div>
</footer>
<script src="{'../' if '/' in path else ''}assets/config.js"></script>
<script src="{'../' if '/' in path else ''}assets/app.js"></script>
</body>
</html>
"""


ORG_JSON = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"SoftwareApplication","name":"GoldMeet","applicationCategory":"FinanceApplication","operatingSystem":"Android, Web","offers":{"@type":"Offer","price":"0","priceCurrency":"INR"},"description":"P2P used-gold matching in India. Meet at a jeweller or bank that can assay gold. Fair metal price from daily city rates.","url":"ORIGIN/","email":"SUPPORT","areaServed":"IN"}
</script>""".replace("ORIGIN", ORIGIN).replace("SUPPORT", SUPPORT)

FAQ = [
    ("What is GoldMeet?", "GoldMeet matches people who want to buy or sell used gold in India. You meet at a nearby jeweller or bank that can test purity. The app does not take your gold or your money."),
    ("How is fair price calculated?", "Fair metal value = today's city rate for 24K, 22K, or 18K (INR per 10 g) × weight in grams ÷ 10. No making charges, stones, or hallmark fee."),
    ("Do you buy gold?", "No. We are not a jeweller and not a pawn shop. Two people agree a price and meet in public."),
    ("Is my home address shown?", "No. Exact home is hidden. After both confirm a venue you only see distance to that shop."),
    ("Which cities?", "Mumbai first, then Delhi, Bangalore, Chennai, Kolkata, Hyderabad, Ahmedabad, Pune, Jaipur, Surat."),
    ("Is large cash allowed?", "Follow current Indian cash and PMLA rules. Prefer bank transfer. We do not escrow."),
]


def main() -> None:
    (ROOT / "cities").mkdir(exist_ok=True)
    (ROOT / "hi").mkdir(exist_ok=True)

    city_links = "".join(
        f'<div class="card"><h3><a href="cities/{slug}.html">Used gold in {en}</a></h3><p>{hook}.</p></div>'
        for slug, en, _hi, hook, _b in CITIES
    )

    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FAQ)
    faq_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ],
    })

    home_body = f"""
<section class="hero"><div class="wrap">
  <h1>Sell or buy used gold in India — meet at a jeweller, not a stranger's house</h1>
  <p class="lead">GoldMeet is a P2P matcher. Fair metal price from today's 24K / 22K / 18K city rate. Test karat and weight on site. No escrow. No custody.</p>
  <p><a class="btn" href="join.html">Join with mobile number</a>
     <a class="btn ghost" href="rates.html">Today's gold rate</a></p>
</div></section>
<div class="wrap">
  <div class="notice">Launch city: <strong>Mumbai</strong> (Zaveri Bazaar). Other cities listed below get the same fair-price board.</div>
  <h2>How it works</h2>
  <div class="grid">
    <div class="card"><h3>1. List or browse</h3><p>Seller posts photos, claimed karat, grams, HUID, ask in INR. Exact home stays hidden.</p></div>
    <div class="card"><h3>2. Fair venue</h3><p>We rank jewellers and banks by travel for both of you. OSM map. Google rating labelled as Google.</p></div>
    <div class="card"><h3>3. Check in &amp; test</h3><p>150 m geofence at the shop. Assay is your job. Then rate and report.</p></div>
  </div>
  <h2>Cities</h2>
  <div class="grid">{city_links}</div>
  <h2>Fair price formula</h2>
  <p><code>fair INR = (city rate per 10 g for that karat) × weight_g / 10</code></p>
  <p>Rates come from GoldAPI XAU/INR once per IST day, then a small city spread. Stones and making charges are not included.</p>
</div>
"""
    (ROOT / "index.html").write_text(
        page(
            "GoldMeet — used gold P2P matching in India | Meet at a jeweller",
            "Buy or sell used gold in Mumbai and other Indian cities. Fair 24K/22K/18K metal price. Meet at a shop or bank with a tester. No escrow.",
            "index.html",
            home_body,
            extra_json=ORG_JSON,
        ),
        encoding="utf-8",
    )

    rates_body = """
<div class="wrap">
  <h1>Today's gold rate in India (city board)</h1>
  <p class="lead">24K, 22K, 18K per 10 grams. Fair metal value for used gold has no making charges.</p>
  <label>City</label>
  <select name="city">""" + "".join(f'<option>{en}</option>' for _, en, *_ in CITIES) + """</select>
  <div id="rate-box" class="card" style="margin-top:1rem"></div>
  <h2>Fair price calculator</h2>
  <label>Purity</label>
  <select name="karat"><option value="24">24K</option><option value="22" selected>22K</option><option value="18">18K</option></select>
  <label>Weight (g)</label>
  <input name="weight" type="number" min="0.1" step="0.01" value="10">
  <p id="fair-box" class="price"></p>
</div>
"""
    (ROOT / "rates.html").write_text(
        page("Today's gold rate India — 24K 22K 18K per 10 g | GoldMeet", "Daily IST city gold rates and used-gold fair metal calculator for 24K, 22K, 18K.", "rates.html", rates_body),
        encoding="utf-8",
    )

    how = """
<div class="wrap">
  <h1>How GoldMeet works</h1>
  <ol>
    <li>Sign in with an Indian mobile OTP.</li>
    <li>Seller lists used gold: photos, claimed karat, grams, HUID, ask.</li>
    <li>Buyer offers. Seller accepts. A meet is created.</li>
    <li>Both pick a fair jeweller or bank (travel both sides, not one home).</li>
    <li>Chat in-app. Check in within 150 m. Test gold. Pay how you both agree.</li>
    <li>Rate the other party. Report abuse. Optionally tag venue equipment.</li>
  </ol>
  <p>Partner claim, coupons, and ads are schema-ready and locked until a shop signs a contract.</p>
</div>
"""
    (ROOT / "how-it-works.html").write_text(
        page("How GoldMeet works — used gold P2P in India", "OTP, listing, fair venue, geofence check-in, assay at a jeweller or bank.", "how-it-works.html", how),
        encoding="utf-8",
    )

    safety = """
<div class="wrap">
  <h1>Safety</h1>
  <ul>
    <li>Meet only in a staffed jeweller or bank. Never a private home or parking lot.</li>
    <li>Purity and weight are seller claims until tested on site.</li>
    <li>Tester / scale / CCTV badges may be inferred or user-reported. Unverified stays labelled unverified.</li>
    <li>We do not hold gold and do not escrow INR.</li>
    <li>Follow PMLA and cash limits. Prefer bank transfer.</li>
    <li>Flag any request to skip the shop test.</li>
  </ul>
</div>
"""
    (ROOT / "safety.html").write_text(
        page("Safety tips for P2P used gold deals in India | GoldMeet", "Public venue, on-site assay, no escrow, cash-limit warning.", "safety.html", safety),
        encoding="utf-8",
    )

    (ROOT / "faq.html").write_text(
        page(
            "GoldMeet FAQ — used gold, fair price, Mumbai meetings",
            "Answers on fair metal price, escrow, cities, and meeting at jewellers.",
            "faq.html",
            f'<div class="wrap"><h1>FAQ</h1>{faq_html}</div>',
            extra_json=f'<script type="application/ld+json">{faq_json}</script>',
        ),
        encoding="utf-8",
    )

    join = """
<div class="wrap">
  <h1>Join GoldMeet with your Indian mobile</h1>
  <p class="lead">Phone OTP when Supabase is linked. Until then, join the Mumbai waitlist — we email support@goldguideapp.com.</p>
  <div class="card">
    <h2>OTP (live backend)</h2>
    <form id="otp-form">
      <label>Mobile</label>
      <input name="phone" required placeholder="9876543210" inputmode="numeric">
      <label>OTP (after send)</label>
      <input name="code" placeholder="6 digits" inputmode="numeric" maxlength="6">
      <p><button class="btn" type="submit">Send / verify OTP</button></p>
      <p id="otp-status" class="muted">If send fails, use the waitlist form.</p>
    </form>
  </div>
  <div class="card" style="margin-top:1rem">
    <h2>Waitlist (works now)</h2>
    <form action="https://formsubmit.co/support@goldguideapp.com" method="POST">
      <input type="hidden" name="_subject" value="GoldMeet waitlist">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_template" value="table">
      <label>Name</label>
      <input name="name" required>
      <label>Indian mobile</label>
      <input name="phone" required placeholder="9876543210">
      <label>City</label>
      <select name="city">""" + "".join(f"<option>{en}</option>" for _, en, *_ in CITIES) + """</select>
      <label>I want to</label>
      <select name="role"><option>Sell used gold</option><option>Buy used gold</option><option>Both</option></select>
      <p><button class="btn" type="submit">Join waitlist</button></p>
    </form>
  </div>
</div>
"""
    (ROOT / "join.html").write_text(
        page("Join GoldMeet — Indian mobile OTP / waitlist", "Sign in with phone OTP or join the Mumbai used-gold waitlist.", "join.html", join),
        encoding="utf-8",
    )

    privacy = f"""
<div class="wrap">
  <h1>Privacy</h1>
  <p>Controller: Gold Guide / GoldMeet · {SUPPORT}</p>
  <p>We collect Indian mobile number, coarse location (not exact home on listings), listing photos you upload, chat on a meet, and optional ratings/reports.</p>
  <p>GoldAPI rates are fetched to show fair metal value. OSM/Google place data is cached for venue ranking.</p>
  <p>We do not sell your gold. We do not process payments. Delete account: {ORIGIN}/deletion.html</p>
</div>
"""
    (ROOT / "privacy.html").write_text(
        page("Privacy policy | GoldMeet", "What GoldMeet stores: phone, coarse location, listings, chat.", "privacy.html", privacy),
        encoding="utf-8",
    )
    deletion = f"""
<div class="wrap">
  <h1>Data deletion</h1>
  <p>Email {SUPPORT} from the same mobile/email you used. Subject: Delete my GoldMeet account.</p>
  <p>We delete profile, listings you own, and chat you can access, unless a legal hold applies. Play Store URL may also use goldguide-data-deletion.io.</p>
</div>
"""
    (ROOT / "deletion.html").write_text(
        page("Delete GoldMeet account / data", "How to request deletion of your GoldMeet account and data.", "deletion.html", deletion),
        encoding="utf-8",
    )

    for slug, en, hi_name, hook, body in CITIES:
        html = f"""
<div class="wrap">
  <h1>Used gold in {en} — buy or sell at a jeweller</h1>
  <p class="lead">{hook}. GoldMeet shows today's {en} 24K / 22K / 18K metal rate and a fair price for your grams.</p>
  <p>{body}</p>
  <p><a class="btn" href="../join.html">Join with mobile</a> <a href="../rates.html">Open city rate board</a></p>
  <h2>Fair price in {en}</h2>
  <p>Same national XAU/INR print, plus {en}'s spread vs Mumbai. Formula: city 10 g rate × weight / 10.</p>
  <h2>Meeting places</h2>
  <p>Jewellery shops, banks, pawnbrokers from OSM. Top ranked spots may get Google rating + review keywords (tester, scale, CCTV) with an unverified badge until reported.</p>
</div>
"""
        (ROOT / "cities" / f"{slug}.html").write_text(
            page(
                f"Used gold in {en} — P2P meet at a jeweller | GoldMeet",
                f"Sell or buy used gold in {en}. Fair 22K/24K/18K metal price. Meet at {hook}.",
                f"cities/{slug}.html",
                html,
            ),
            encoding="utf-8",
        )

    hi_body = """
<section class="hero"><div class="wrap">
  <h1>भारत में पुराना सोना बेचें या खरीदें — घर नहीं, ज्वेलर की दुकान पर मिलें</h1>
  <p class="lead">GoldMeet P2P मैचर है। आज के 24K / 22K / 18K शहर रेट से फ़ेयर मेटल प्राइस। शुद्धता दुकान पर जाँचें। गोल्ड या पैसे हम नहीं रखते।</p>
  <p><a class="btn" href="../join.html">मोबाइल से जुड़ें</a></p>
</div></section>
<div class="wrap">
  <p>पहला शहर: मुंबई (ज़वेरी बाज़ार)। फ़ेयर दाम = (10 ग्राम का शहर रेट) × वज़न / 10। मेकिंग चार्ज शामिल नहीं。</p>
  <p><a href="../index.html">English</a></p>
</div>
"""
    (ROOT / "hi" / "index.html").write_text(
        page(
            "गोल्डमीट — भारत में पुराना सोना P2P | ज्वेलर पर मिलें",
            "मुंबई और अन्य शहरों में पुराना सोना बेचें/खरीदें। फ़ेयर 24K 22K 18K दाम। दुकान या बैंक में टेस्ट।",
            "hi/index.html",
            hi_body,
            lang="hi",
        ),
        encoding="utf-8",
    )

    urls = [
        "index.html", "rates.html", "how-it-works.html", "safety.html", "faq.html",
        "join.html", "privacy.html", "deletion.html", "hi/index.html",
    ] + [f"cities/{s}.html" for s, *_ in CITIES]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        loc = ORIGIN + "/" if u == "index.html" else f"{ORIGIN}/{u}"
        sm.append(f"<url><loc>{loc}</loc><changefreq>daily</changefreq></url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")

    (ROOT / "robots.txt").write_text(
        f"""User-agent: *
Allow: /
Sitemap: {ORIGIN}/sitemap.xml

User-agent: GPTBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Applebot-Extended
Allow: /
""",
        encoding="utf-8",
    )

    (ROOT / "llms.txt").write_text(
        f"""# GoldMeet
> P2P used-gold matching for India. Buyers and sellers meet at a jeweller or bank that can assay gold. No escrow. No custody.

- Home: {ORIGIN}/
- Rates: {ORIGIN}/rates.html
- How it works: {ORIGIN}/how-it-works.html
- Safety: {ORIGIN}/safety.html
- FAQ: {ORIGIN}/faq.html
- Join: {ORIGIN}/join.html
- Hindi: {ORIGIN}/hi/

Fair price: city rate per 10 g (24K/22K/18K) × weight_g / 10. No making charges.
Launch city: Mumbai. Support: {SUPPORT}
""",
        encoding="utf-8",
    )

    (ROOT / "404.html").write_text(
        page("Not found | GoldMeet", "Page missing.", "404.html", '<div class="wrap"><h1>404</h1><p><a href="index.html">Home</a></p></div>'),
        encoding="utf-8",
    )
    print("wrote", ROOT)


if __name__ == "__main__":
    main()
