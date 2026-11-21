"""Lenssepeti statik site üreticisi.

Kullanım:  python3 tools/build.py
tools/data.py içindeki veriden tüm HTML sayfalarını, sitemap.xml ve robots.txt dosyasını üretir.
"""
import html
import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from data import SITE, HEADS, CATS, PRODUCTS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = SITE["base_url"].rstrip("/")
E = html.escape

ICONS = {
    "koruma": '<circle cx="36" cy="36" r="24" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="3"/><ellipse cx="29" cy="28" rx="6" ry="3" fill="var(--surface)" opacity=".8" transform="rotate(-30 29 28)"/>',
    "odak": '<path d="M36 10c10 8 10 44 0 52c-10-8-10-44 0-52Z" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="3"/><path d="M8 26h20M8 46h20M44 36h20" stroke="var(--signal)" stroke-width="2.5" stroke-linecap="round"/>',
    "kolimator": '<path d="M30 10c12 8 12 44 0 52h12c-6-14-6-38 0-52Z" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="3" stroke-linejoin="round"/><path d="M8 36l18-10M8 36l18 10M50 28h16M50 44h16" stroke="var(--signal)" stroke-width="2.5" stroke-linecap="round"/>',
    "nozul": '<path d="M20 14h32v14l-10 26h-12L20 28Z" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="3" stroke-linejoin="round"/><path d="M20 20h32" stroke="var(--accent)" stroke-width="2"/><circle cx="36" cy="58" r="3" fill="var(--signal)"/>',
    "seramik": '<rect x="14" y="22" width="44" height="28" rx="6" fill="var(--surface)" stroke="var(--ink)" stroke-width="3"/><rect x="28" y="22" width="16" height="28" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>',
    "cekmece": '<rect x="12" y="24" width="48" height="24" rx="4" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="3"/><circle cx="30" cy="36" r="7" fill="var(--surface)" stroke="var(--accent)" stroke-width="2"/><path d="M52 32v8" stroke="var(--ink)" stroke-width="3" stroke-linecap="round"/>',
    "qbh": '<rect x="22" y="10" width="28" height="40" rx="4" fill="var(--surface)" stroke="var(--ink)" stroke-width="3"/><circle cx="36" cy="54" r="8" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="3"/><path d="M36 20v22" stroke="var(--signal)" stroke-width="2.5"/>',
}

P = [dict(id=i, b=b, c=c, n=n, d=d, f=f, o=o, note=note) for (i, b, c, n, d, f, o, note) in PRODUCTS]


def model_path(brand, model):
    return f"{brand}/{model.lower()}/"


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def card(p):
    fits = ", ".join(p["f"][:6]) + (f" +{len(p['f']) - 6}" if len(p["f"]) > 6 else "")
    note = f" · {E(p['note'])}" if p["note"] else ""
    opts = "".join(f"<option>{E(o)}</option>" for o in p["o"])
    return (f'<article class="card"><div class="thumb"><svg viewBox="0 0 72 72" aria-hidden="true">{ICONS[p["c"]]}</svg></div>'
            f'<span class="cat">{E(CATS[p["c"]]["name"])}{note}</span>'
            f'<div><h3>{E(p["n"])}</h3><div class="dims">{E(p["d"])}</div></div>'
            f'<p class="fits">Uyumlu: <b title="{E(", ".join(p["f"]))}">{E(fits)}</b></p>'
            f'<div><div class="buy"><select id="o-{p["id"]}" aria-label="Seçenek">{opts}</select>'
            f'<button class="add" type="button" data-add="{p["id"]}">Sepete ekle</button></div>'
            f'<p class="price">Fiyat için sorun</p></div></article>')


def page(rel_dir, title, description, body, crumbs=None, search_here=False):
    """rel_dir: sayfanın kök dizine göre klasörü ('' = kök)."""
    depth = rel_dir.count("/")
    up = "../" * depth
    canonical = f"{BASE}/{rel_dir}"
    ld = [{
        "@context": "https://schema.org", "@type": "Store", "name": SITE["name"], "url": BASE + "/",
        "description": "Fiber lazer kesim kafası yedek parça ve sarf malzemesi: koruma camı, lens, nozul, seramik, QBH koruma camı.",
        "telephone": SITE["whatsapp"],
    }]
    if crumbs:
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": f"{BASE}/{href}"} for i, (name, href) in enumerate(crumbs)]})
    search_action = "" if search_here else f' action="{up}index.html" method="get"'
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
<link rel="canonical" href="{E(canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:url" content="{E(canonical)}">
<meta property="og:locale" content="tr_TR">
<meta name="theme-color" content="#0d7f72">
<meta name="robots" content="index, follow">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{up}assets/style.css">
<script type="application/ld+json">{json.dumps(ld if len(ld) > 1 else ld[0], ensure_ascii=False)}</script>
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="logo" href="{up}index.html" aria-label="Lenssepeti ana sayfa">
      <svg viewBox="0 0 32 32" aria-hidden="true"><ellipse cx="16" cy="11" rx="10" ry="4" fill="none" stroke="var(--accent)" stroke-width="2.2"/><path d="M6 11l2.5 14h15L26 11" fill="none" stroke="var(--ink)" stroke-width="2.2" stroke-linejoin="round"/><path d="M11 18h10" stroke="var(--ink)" stroke-width="2.2" stroke-linecap="round"/></svg>
      <span>Lens<b>sepeti</b></span>
    </a>
    <form class="search" role="search"{search_action}>
      <svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M11 11l3.5 3.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
      <input id="q" name="q" type="search" placeholder="Ara: 27.9x4.1, nozul, BM111, BLT641…" autocomplete="off" aria-label="Parça ara">
    </form>
    <button class="cartbtn" id="openCart" type="button">Sepet <span class="badge" id="badge">0</span></button>
  </div>
</header>
<main>
{body}
</main>
<footer>
  <div class="wrap">
    <span>© {date.today().year} Lenssepeti · Fiber lazer yedek parça ve sarf malzemesi</span>
    <span>WhatsApp: <span class="mono">{E(SITE['whatsapp'])}</span></span>
  </div>
</footer>
<div class="scrim" id="scrim" hidden></div>
<aside class="drawer" id="drawer" hidden aria-label="Sepet">
  <div class="dhead"><h2>Sepetiniz</h2><button class="x" type="button" id="closeCart">Kapat</button></div>
  <div class="dlist" id="dlist"></div>
  <form class="dfoot" id="orderForm" novalidate>
    <div class="ofields">
      <label for="firma">Ad soyad / firma *</label>
      <input id="firma" name="firma" placeholder="ör. Yılmaz Metal" autocomplete="organization" required>
      <label for="tel">Telefon *</label>
      <input id="tel" name="tel" type="tel" placeholder="05xx xxx xx xx" autocomplete="tel" required>
      <label for="adres">Teslimat adresi / il</label>
      <input id="adres" name="adres" placeholder="ör. İkitelli OSB, İstanbul" autocomplete="street-address">
      <label for="not">Not</label>
      <input id="not" name="not" placeholder="ör. Kafa modelim BM111, fatura kesilsin">
    </div>
    <input class="hp" name="website" id="website" tabindex="-1" autocomplete="off" aria-hidden="true">
    <p class="err" id="orderErr" hidden></p>
    <button class="primary" type="submit" id="sendOrder">Siparişi gönder</button>
    <a class="ghost" id="waLink" href="#" target="_blank" rel="noopener">WhatsApp ile gönder</a>
    <pre id="msg" hidden></pre>
  </form>
  <div class="done" id="orderDone" hidden>
    <h3>Siparişiniz alındı</h3>
    <p class="mono" id="orderNo"></p>
    <p>Fiyat ve kargo bilgisi için en kısa sürede sizi arayacağız.</p>
    <button class="ghost" type="button" id="newOrder">Yeni sipariş</button>
  </div>
</aside>
<div class="toast" id="toast" hidden></div>
<script src="{up}assets/data.js"></script>
<script src="{up}assets/app.js"></script>
</body>
</html>
"""


def crumbs_html(crumbs, up):
    parts = []
    for i, (name, href) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            parts.append(E(name))
        else:
            parts.append(f'<a href="{up}{href or "index.html"}">{E(name)}</a>')
    return '<nav class="crumbs" aria-label="Konum">' + " › ".join(parts) + "</nav>"


def parts_table(items):
    rows = "".join(
        f'<tr><td>{E(p["n"])}</td><td class="mono">{E(p["d"])}</td><td>{E(CATS[p["c"]]["name"])}</td><td>{E(", ".join(p["o"][:4]) + ("…" if len(p["o"]) > 4 else ""))}</td></tr>'
        for p in items)
    return ('<div class="tablewrap"><table class="parts"><thead><tr><th>Parça</th><th>Ölçü</th><th>Tür</th><th>Seçenekler</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def link_lists(up):
    out = []
    for b, h in HEADS.items():
        chips = "".join(f'<a class="chip" href="{up}{model_path(b, m)}">{m}</a>' for m in h["models"])
        out.append(f'<div><h2>{E(h["name"])} kafa yedek parçaları</h2><div class="chips" style="margin-top:10px">{chips}</div></div>')
    cats = "".join(f'<a class="chip" style="font-family:var(--body)" href="{up}{c["slug"]}/">{E(c["name"])}</a>' for c in CATS.values())
    out.append(f'<div><h2>Parça türleri</h2><div class="chips" style="margin-top:10px">{cats}</div></div>')
    return '<section class="wrap links">' + "".join(out) + "</section>"


INFO = """<section class="wrap info">
  <div><h3>Ölçüyü nasıl bulurum?</h3><p>Eski camın çapını ve kalınlığını kumpasla ölçün ya da kafanın etiketindeki modeli yazın. Emin değilseniz fotoğrafını WhatsApp'tan gönderin.</p></div>
  <div><h3>Sipariş nasıl verilir?</h3><p>Parçaları sepete ekleyin, “WhatsApp ile gönder” düğmesine basın. Fiyat ve kargo bilgisini hemen dönüyoruz.</p></div>
  <div><h3>Uyumluluk</h3><p>Uyumluluk listeleri üretici kataloglarından derlendi. Aynı modelin farklı yıllarında ölçü değişebilir; sipariş öncesi teyit ediyoruz.</p></div>
</section>"""


def build():
    urls = []

    # data.js
    data = {"site": SITE, "heads": HEADS, "cats": CATS, "products": P, "icons": ICONS}
    write("assets/data.js", "window.LS = " + json.dumps(data, ensure_ascii=False) + ";\n")

    # Ana sayfa
    n_r, n_b = len(HEADS["raytools"]["models"]), len(HEADS["boci"]["models"])
    body = f"""<div class="hero"><div class="wrap">
  <span class="eyebrow">Fiber lazer kesim kafası yedek parça &amp; sarf</span>
  <h1>Lazer lens, koruma camı ve nozul: kafanıza uyanı bulun.</h1>
  <p>Raytools ve BOCI (Bochu) fiber lazer kesim kafaları için koruma camı, odak lensi, kolimatör lensi, nozul ve seramik. 1 kW'tan 12 kW'a kadar tüm güçlerde QBH koruma camı stokta.</p>
  <div class="facts"><span class="fact">Raytools · {n_r} kafa modeli</span><span class="fact">BOCI · {n_b} kafa modeli</span><span class="fact">QBH koruma camı · 1–12 kW</span></div>
</div></div>
<div class="wrap"><div class="picker">
  <h2>Kesim kafanız hangisi?</h2>
  <div class="tabs" id="brands" role="group" aria-label="Marka"></div>
  <div id="modelBox" hidden><div class="picklabel">Model</div><div class="chips" id="models" role="group" aria-label="Kafa modeli"></div></div>
  <div><div class="picklabel">Parça türü</div><div class="chips cats" id="cats" role="group" aria-label="Parça türü"></div></div>
</div></div>
<section class="wrap results">
  <div class="resbar"><h2 id="resTitle">Tüm parçalar</h2><span id="resCount">{len(P)} ürün</span></div>
  <div class="qbh" id="qbhBox" hidden><h2>QBH koruma camları</h2><p>Lazer kaynağının çıkışındaki (QBH konnektör) koruma camı. Tüm güç sınıfları stokta. Siparişte kaynağınızın markasını ve gücünü yazın, doğru ölçüyü biz eşleştirelim.</p><div class="pw"><span>1 kW</span><span>1,5 kW</span><span>2 kW</span><span>3 kW</span><span>4 kW</span><span>6 kW</span><span>8 kW</span><span>10 kW</span><span>12 kW</span></div></div>
  <div class="grid" id="grid">{"".join(card(p) for p in P)}</div>
</section>
{INFO}
{link_lists("")}"""
    write("index.html", page("", "Lenssepeti | Lazer Lens, Koruma Camı, Nozul – Raytools & BOCI Yedek Parça",
                             "Fiber lazer kesim kafası lens, koruma camı, nozul ve seramik. Raytools ve BOCI (Bochu) tüm modeller, 1–12 kW QBH koruma camı. WhatsApp ile hızlı sipariş.",
                             body, search_here=True))
    urls.append(("", "1.0"))

    # Kafa modeli sayfaları
    for b, h in HEADS.items():
        for m in h["models"]:
            rel = model_path(b, m)
            up = "../../"
            items = [p for p in P if p["b"] == b and m in p["f"]]
            crumbs = [("Ana sayfa", ""), (h["name"], f"index.html?marka={b}"), (m, rel)]
            kinds = sorted({CATS[p["c"]]["name"].lower() for p in items})
            sizes = ", ".join(p["d"] for p in items if p["c"] == "koruma")
            body = f"""<div class="hero"><div class="wrap">
  {crumbs_html(crumbs, up)}
  <span class="eyebrow">{E(h["name"])} fiber lazer kesim kafası</span>
  <h1>{E(h["name"].split(" ")[0])} {m} yedek parça ve sarf malzemesi</h1>
  <p>{E(h["name"].split(" ")[0])} {m} lazer kesim kafası için {E(", ".join(kinds))}. {("Koruma camı ölçüleri: " + E(sizes) + ".") if sizes else ""} Tüm parçalar stokta, WhatsApp ile sipariş verin.</p>
</div></div>
<section class="wrap results">
  <div class="resbar"><h2>{m} ile uyumlu {len(items)} parça</h2><a href="{up}index.html?model={m}">Katalogda filtrele</a></div>
  <div class="grid">{"".join(card(p) for p in items)}</div>
  <h2 style="font-size:18px;margin-top:16px">{m} parça listesi</h2>
  {parts_table(items)}
</section>
{INFO}
{link_lists(up)}"""
            brand_short = h["name"].split(" ")[0]
            write(rel + "index.html", page(rel, f"{brand_short} {m} Koruma Camı, Lens, Nozul, Seramik | Lenssepeti",
                                           f"{brand_short} {m} lazer kesim kafası yedek parçaları: {', '.join(kinds)}. Uyumlu ölçüler, stokta, WhatsApp ile sipariş.",
                                           body, crumbs=crumbs))
            urls.append((rel, "0.8"))

    # Kategori sayfaları
    for key, c in CATS.items():
        rel = c["slug"] + "/"
        up = "../"
        items = [p for p in P if p["c"] == key]
        crumbs = [("Ana sayfa", ""), (c["name"], rel)]
        extra = ""
        if key == "qbh":
            extra = '<div class="qbh"><h2>Hangi güç?</h2><p>1 kW, 1,5 kW, 2 kW, 3 kW, 4 kW, 6 kW, 8 kW, 10 kW ve 12 kW kaynaklar için QBH koruma camı mevcut. Kaynağınızın markasını (Raycus, MAX, IPG, JPT…) ve gücünü yazın, doğru ölçüyü eşleştirelim.</p></div>'
        body = f"""<div class="hero"><div class="wrap">
  {crumbs_html(crumbs, up)}
  <span class="eyebrow">Lazer yedek parça</span>
  <h1>{E(c["name"])}</h1>
  <p>{E(c["intro"])}</p>
</div></div>
<section class="wrap results">
  {extra}
  <div class="resbar"><h2>{len(items)} ürün</h2><a href="{up}index.html?parca={key}">Katalogda filtrele</a></div>
  <div class="grid">{"".join(card(p) for p in items)}</div>
</section>
{INFO}
{link_lists(up)}"""
        title = f"{c['name']} – Raytools & BOCI Lazer {c['name']} | Lenssepeti" if key != "qbh" else "QBH Koruma Camı 1–12 kW – Raycus, MAX, IPG | Lenssepeti"
        write(rel + "index.html", page(rel, title, c["intro"], body, crumbs=crumbs))
        urls.append((rel, "0.9"))

    # 404
    write("404.html", page("404.html", "Sayfa bulunamadı | Lenssepeti", "Aradığınız sayfa bulunamadı.",
                           f'<div class="hero"><div class="wrap"><h1>Bu sayfa bulunamadı</h1><p>Adres değişmiş olabilir. <a href="{BASE}/">Ana sayfadan</a> kafa modelinizi seçin.</p></div></div>'))

    # sitemap + robots
    today = date.today().isoformat()
    sm = "".join(f"<url><loc>{BASE}/{u}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n" for u, pr in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    write(".nojekyll", "")
    print(f"{len(urls)} sayfa üretildi.")


if __name__ == "__main__":
    build()
