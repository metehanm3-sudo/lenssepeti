# Lenssepeti

Fiber lazer kesim kafası yedek parça ve sarf malzemesi sitesi (Raytools, BOCI, QBH koruma camı).

## Ürün eklemek veya değiştirmek

1. `tools/data.py` dosyasını açın. Ürünler `PRODUCTS` listesinde.
2. Değişiklikten sonra sayfaları yeniden üretin:

   ```bash
   python3 tools/build.py
   ```

WhatsApp numarası ve alan adı da `tools/data.py` içindeki `SITE` bölümünde.

## Siteyi kendiniz güncellemek (GitHub üzerinden)

1. GitHub'da `tools/data.py` dosyasını açın, sağ üstteki **kalem** simgesine basın.
2. Değişikliği yapın (WhatsApp numarası en üstte, ürünler `PRODUCTS` listesinde).
3. **Commit changes** düğmesine basın.
4. 1–2 dakika içinde site kendiliğinden güncellenir. İlerlemeyi depodaki **Actions** sekmesinden görebilirsiniz; yeşil tik = yayında, kırmızı çarpı = dosyada yazım hatası var.

Ürün satırı örneği (virgüllere ve tırnaklara dikkat):

```python
("r-k7", "raytools", "koruma", "Raytools koruma camı", "D21.5 × 2 mm", ["BM109", "BM111"], PACK, ""),
```

## Yayınlama (GitHub Pages) — bir kez yapılır

Depo ayarları → **Pages** → Source: **Deploy from a branch** → Branch: `main` / `(root)` → Save. `tools/` içindeki bir dosya değişince **Siteyi güncelle** işlemi sayfaları yeniden üretir, Pages de yayınlar.

Kendi alan adınız için Pages ayarındaki **Custom domain** kutusuna `lenssepeti.com` yazın ve alan adı firmanızın DNS ayarına GitHub'ın verdiği kayıtları ekleyin.

## Hazır e-ticaret altyapısına yükleme

```bash
python3 tools/export.py
```

- `exports/shopify-urunler.csv` → Shopify: Ürünler → İçe aktar. Fiyatlar 0 ve ürünler taslak olarak gelir; fiyatı girip yayınlayın.
- `exports/urun-listesi.csv` → ikas, Ticimax, IdeaSoft vb. Excel'de açın, fiyat ve stok sütunlarını doldurun, platformun toplu ürün yükleme şablonuna kopyalayın.
