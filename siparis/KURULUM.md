# Sipariş sistemi kurulumu (bir kez, ~5 dakika)

Bitince: sitedeki her sipariş Google E-Tablonuza yeni satır olarak düşer ve size e-posta bildirimi gelir.

## 1. Tabloyu oluşturun
1. Bilgisayardan **https://sheets.new** adresini açın (Google hesabınızla).
2. Sol üstteki "Adsız e-tablo" yazısına tıklayıp adını **Lenssepeti Siparişler** yapın.

## 2. Kodu yapıştırın
1. Üst menüden **Uzantılar → Apps Script**'e tıklayın. Yeni bir sekme açılır.
2. Ekranda gördüğünüz `function myFunction() { }` yazısının hepsini silin.
3. Bu depodaki `siparis/Code.gs` dosyasının içindekilerin tamamını kopyalayıp oraya yapıştırın.
4. Üstteki **💾 Kaydet** simgesine basın.

## 3. Tabloyu hazırlayın
1. Üstteki fonksiyon seçme kutusunda **kurulum** seçili olsun, **▶ Çalıştır**'a basın.
2. "Yetkilendirme gerekli" penceresi çıkar → **İzinleri incele** → Google hesabınızı seçin.
3. "Google bu uygulamayı doğrulamadı" uyarısı çıkarsa: **Gelişmiş** → **Lenssepeti Siparişler (güvenli değil) sayfasına git** → **İzin ver**.
   (Bu uyarı, kodu kendiniz eklediğiniz için çıkar; kod sadece sizin tablonuza yazar ve size e-posta gönderir.)
4. Tabloya dönün: **Siparişler** sayfası başlıklarıyla oluşmuş olmalı.

## 4. Siteye bağlayın
1. Apps Script sekmesinde sağ üstteki **Dağıt → Yeni dağıtım**'a tıklayın.
2. Sol üstteki ⚙️ çarkına basıp **Web uygulaması**'nı seçin.
3. **Şu kullanıcı olarak çalıştır:** Ben  ·  **Erişimi olanlar:** Herkes
4. **Dağıt**'a basın. Çıkan **Web uygulaması URL'sini** kopyalayın (`https://script.google.com/macros/s/.../exec`).
5. Bu adresi Claude'a gönderin **ya da** `tools/data.py` dosyasında `"order_url": ""` tırnaklarının içine yapıştırıp kaydedin.

## Günlük kullanım
- Yeni sipariş gelince e-posta gelir (konu: **🛒 Yeni sipariş LS-…**). Telefonda Gmail bildirimini açık tutun.
- Tabloda **Durum** sütunundan siparişin durumunu seçin:

| Durum | Renk | Anlamı |
|---|---|---|
| Yeni | Sarı | Sipariş geldi, bakılmadı |
| Hazırlanıyor | Mavi | Paketleniyor |
| Gönderime hazır | Yeşil | Kargoya verilmeyi bekliyor |
| Kargoya verildi | Gri | Gönderildi (takip no'yu son sütuna yazın) |
| İptal | Kırmızı | İptal edildi |

- Telefondan takip için **Google E-Tablolar** uygulamasını indirin; tablo orada da açılır.

## Kodu değiştirirseniz
Apps Script'te kodu değiştirdikten sonra **Dağıt → Dağıtımları yönet → ✏️ → Sürüm: Yeni sürüm → Dağıt** yapın. Adres aynı kalır.
