"""Ürünleri hazır e-ticaret altyapılarına toplu yükleme dosyası olarak dışa aktarır.

Kullanım:  python3 tools/export.py
Çıktılar:
  exports/shopify-urunler.csv  — Shopify ürün içe aktarma biçimi
  exports/urun-listesi.csv     — Genel liste (ikas, Ticimax, IdeaSoft vb. için Excel'de açılır)
"""
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from data import HEADS, CATS, PRODUCTS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "exports")
TR = str.maketrans("çğıöşüÇĞİÖŞÜ×·", "cgiosuCGIOSUx-")


def slug(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.translate(TR).lower())).strip("-")


def brand_name(b):
    return HEADS[b]["name"] if b in HEADS else "QBH"


def option_name(opts):
    if opts[0].startswith("Ø"):
        return "Nozul çapı"
    if "kW" in opts[0]:
        return "Lazer gücü"
    if opts[0] in ("Orijinal", "Muadil"):
        return "Tip"
    if opts[0].startswith("F"):
        return "Odak uzaklığı"
    if "lens" in opts[0].lower():
        return "Paket"
    return "Paket"


def describe(n, d, c, fits, note):
    cat = CATS[c]["name"].lower()
    text = (f"{n}, ölçü {d}. Fiber lazer kesim kafası {cat}. "
            f"Uyumlu modeller: {', '.join(fits)}.")
    if note:
        text += f" {note}."
    text += " Sipariş öncesi kafa modelinizi veya eski parçanın ölçüsünü yazın, uyumluluğu teyit edelim."
    return text


def main():
    os.makedirs(OUT, exist_ok=True)
    shop_cols = ["Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published",
                 "Option1 Name", "Option1 Value", "Variant SKU", "Variant Inventory Tracker",
                 "Variant Inventory Qty", "Variant Inventory Policy", "Variant Fulfillment Service",
                 "Variant Price", "Variant Requires Shipping", "Variant Taxable",
                 "SEO Title", "SEO Description", "Status"]
    gen_cols = ["Stok kodu", "Ürün adı", "Marka", "Kategori", "Ölçü", "Seçenek adı", "Seçenek",
                "Uyumlu kafa modelleri", "Açıklama", "Fiyat (TL)", "Stok adedi", "SEO başlık", "SEO açıklama"]
    shop_rows, gen_rows = [], []

    for (pid, b, c, n, d, fits, opts, note) in PRODUCTS:
        title = f"{n} {d}"
        handle = slug(title)
        body = describe(n, d, c, fits, note)
        seo_t = f"{title} | Lenssepeti"[:70]
        seo_d = body[:160]
        tags = ", ".join([brand_name(b), CATS[c]["name"], "lazer yedek parça"] + list(fits))
        oname = option_name(opts)
        for i, o in enumerate(opts):
            sku = f"LS-{pid.upper()}-{i + 1:02d}"
            first = i == 0
            shop_rows.append({
                "Handle": handle,
                "Title": title if first else "",
                "Body (HTML)": f"<p>{body}</p>" if first else "",
                "Vendor": brand_name(b) if first else "",
                "Type": CATS[c]["name"] if first else "",
                "Tags": tags if first else "",
                "Published": "TRUE" if first else "",
                "Option1 Name": oname if first else "",
                "Option1 Value": o,
                "Variant SKU": sku,
                "Variant Inventory Tracker": "shopify",
                "Variant Inventory Qty": "0",
                "Variant Inventory Policy": "deny",
                "Variant Fulfillment Service": "manual",
                "Variant Price": "0",
                "Variant Requires Shipping": "TRUE",
                "Variant Taxable": "TRUE",
                "SEO Title": seo_t if first else "",
                "SEO Description": seo_d if first else "",
                "Status": "draft" if first else "",
            })
            gen_rows.append({
                "Stok kodu": sku, "Ürün adı": title, "Marka": brand_name(b), "Kategori": CATS[c]["name"],
                "Ölçü": d, "Seçenek adı": oname, "Seçenek": o, "Uyumlu kafa modelleri": ", ".join(fits),
                "Açıklama": body, "Fiyat (TL)": "", "Stok adedi": "", "SEO başlık": seo_t, "SEO açıklama": seo_d,
            })

    with open(os.path.join(OUT, "shopify-urunler.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=shop_cols)
        w.writeheader()
        w.writerows(shop_rows)
    # utf-8-sig + ; ayırıcı: Türkçe Excel'de çift tıklayınca düzgün açılır
    with open(os.path.join(OUT, "urun-listesi.csv"), "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=gen_cols, delimiter=";")
        w.writeheader()
        w.writerows(gen_rows)
    print(f"{len(PRODUCTS)} ürün, {len(gen_rows)} varyant satırı yazıldı.")


if __name__ == "__main__":
    main()
