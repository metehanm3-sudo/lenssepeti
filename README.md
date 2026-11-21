# Lenssepeti

Fiber lazer kesim kafası yedek parça ve sarf malzemesi sitesi (Raytools, BOCI, QBH koruma camı).

## Ürün eklemek veya değiştirmek

1. `tools/data.py` dosyasını açın. Ürünler `PRODUCTS` listesinde.
2. Değişiklikten sonra sayfaları yeniden üretin:

   ```bash
   python3 tools/build.py
   ```

WhatsApp numarası ve alan adı da `tools/data.py` içindeki `SITE` bölümünde.

## Yayınlama (GitHub Pages)

Depo ayarları → **Pages** → Source: **Deploy from a branch** → Branch: `main` / `(root)` → Save.

Kendi alan adınız için Pages ayarındaki **Custom domain** kutusuna `lenssepeti.com` yazın ve alan adı firmanızın DNS ayarına GitHub'ın verdiği kayıtları ekleyin.
