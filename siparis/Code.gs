/**
 * Lenssepeti sipariş sistemi — Google E-Tablo + Apps Script
 *
 * Sitedeki "Siparişi gönder" düğmesi siparişi buraya yollar:
 *   1. Sipariş, "Siparişler" sayfasına yeni satır olarak eklenir (Durum: Yeni).
 *   2. Size bildirim e-postası gider.
 * Durumu tablodan değiştirirsiniz: Yeni → Hazırlanıyor → Gönderime hazır → Kargoya verildi.
 *
 * Kurulum adımları için depodaki siparis/KURULUM.md dosyasına bakın.
 */

var SAYFA = "Siparişler";
var BASLIKLAR = ["Sipariş no", "Tarih", "Durum", "Ad soyad / firma", "Telefon", "Adres", "Not", "Ürünler", "Kargo takip no"];
var DURUMLAR = ["Yeni", "Hazırlanıyor", "Gönderime hazır", "Kargoya verildi", "İptal"];
var RENKLER = { "Yeni": "#fde68a", "Hazırlanıyor": "#bfdbfe", "Gönderime hazır": "#bbf7d0", "Kargoya verildi": "#e5e7eb", "İptal": "#fecaca" };

/** Bir kez çalıştırın: tabloyu hazırlar (başlıklar, durum listesi, renkler). */
function kurulum() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(SAYFA) || ss.insertSheet(SAYFA);
  sh.getRange(1, 1, 1, BASLIKLAR.length).setValues([BASLIKLAR]).setFontWeight("bold").setBackground("#12212a").setFontColor("#ffffff");
  sh.setFrozenRows(1);
  sh.setColumnWidth(1, 130); sh.setColumnWidth(2, 130); sh.setColumnWidth(3, 140);
  sh.setColumnWidth(4, 180); sh.setColumnWidth(5, 130); sh.setColumnWidth(6, 220);
  sh.setColumnWidth(7, 200); sh.setColumnWidth(8, 380); sh.setColumnWidth(9, 140);

  var durumSutunu = sh.getRange(2, 3, sh.getMaxRows() - 1, 1);
  durumSutunu.setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(DURUMLAR, true).build());

  var kurallar = Object.keys(RENKLER).map(function (d) {
    return SpreadsheetApp.newConditionalFormatRule()
      .whenFormulaSatisfied('=$C2="' + d + '"')
      .setBackground(RENKLER[d])
      .setRanges([sh.getRange(2, 1, sh.getMaxRows() - 1, BASLIKLAR.length)])
      .build();
  });
  sh.setConditionalFormatRules(kurallar);
  // İzin penceresinin e-posta iznini de sorması için:
  MailApp.getRemainingDailyQuota();
}

/** Siteden gelen siparişi alır. */
function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var v = JSON.parse(e.postData.contents);
    if (v.website) return cevap({ success: true }); // bot tuzağı: insanlar bu alanı görmez
    var firma = metin(v.firma, 120), tel = metin(v.tel, 40);
    if (!firma || !tel || !v.urunler) return cevap({ success: false, message: "Eksik bilgi" });

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sh = ss.getSheetByName(SAYFA) || (kurulum(), ss.getSheetByName(SAYFA));
    var simdi = new Date();
    var tz = ss.getSpreadsheetTimeZone();
    var no = "LS-" + Utilities.formatDate(simdi, tz, "yyMMdd") + "-" + ("000" + sh.getLastRow()).slice(-3);
    var urunler = metin(v.urunler, 4000);

    sh.appendRow([no, Utilities.formatDate(simdi, tz, "dd.MM.yyyy HH:mm"), "Yeni", firma, tel.charAt(0) === "'" ? tel : "'" + tel,
                  metin(v.adres, 300), metin(v.not, 500), urunler, ""]);

    MailApp.sendEmail({
      to: Session.getEffectiveUser().getEmail(),
      subject: "🛒 Yeni sipariş " + no + " — " + firma,
      body: "Yeni sipariş geldi.\n\n" +
            "Sipariş no: " + no + "\n" +
            "Ad soyad / firma: " + firma + "\n" +
            "Telefon: " + tel + "\n" +
            (v.adres ? "Adres: " + metin(v.adres, 300) + "\n" : "") +
            (v.not ? "Not: " + metin(v.not, 500) + "\n" : "") +
            "\nÜrünler:\n" + urunler + "\n\n" +
            "Sipariş tablosu: " + ss.getUrl()
    });
    return cevap({ success: true, no: no });
  } catch (err) {
    return cevap({ success: false, message: String(err) });
  } finally {
    lock.releaseLock();
  }
}

function metin(x, max) { return String(x == null ? "" : x).replace(/^[=+\-@]/, "'$&").slice(0, max).trim(); }
function cevap(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
