"""Lenssepeti ürün verisi — sitenin tek veri kaynağı.

Ürün eklemek/değiştirmek için bu dosyayı düzenleyip `python3 tools/build.py` çalıştırın.
"""

SITE = {
    "name": "Lenssepeti",
    # Alan adı alınınca burayı değiştirin (sonunda / olmadan)
    "base_url": "https://metehanm3-sudo.github.io/lenssepeti",
    "whatsapp": "0500 000 00 00",  # örnek numara
    # Siparişlerin e-postanıza gelmesi için web3forms.com'dan aldığınız "Access Key"i tırnakların içine yapıştırın.
    # Boş bırakılırsa sepette sadece WhatsApp ile sipariş görünür.
    "order_key": "",
}

HEADS = {
    "raytools": {
        "name": "Raytools",
        "models": ["BT210S", "BT240S", "BM109", "BM110", "BM111", "BM114S", "BM115", "BM06K",
                   "BD04K", "BS04K", "BS06K", "BS08K", "BS12K", "BS15K", "BS20K"],
    },
    "boci": {
        "name": "BOCI (Bochu)",
        "models": ["BLT310", "BLT310T", "BLT420", "BLT420S", "BLT421", "BLT421T", "BLT441", "BLT442",
                   "BLT461", "BLT640", "BLT641", "BLT641H", "BLT642H", "BLT661", "BLT662M", "BLT663H"],
    },
}

CATS = {
    "koruma": {"name": "Koruma camı", "slug": "koruma-cami",
               "intro": "Fiber lazer kesim kafası koruma camları (protective window). Raytools ve BOCI kafalar için tüm çap ve kalınlıklar."},
    "odak": {"name": "Odak lensi", "slug": "odak-lensi",
             "intro": "Fiber lazer kesim kafası odak (focus) lensleri. D28 ve D30 çap, F125, F150 ve F200 odak uzaklığı."},
    "kolimator": {"name": "Kolimatör lensi", "slug": "kolimator-lensi",
                  "intro": "Kolimatör (collimating) lensleri. Lazer ışınını paralel hale getiren lens, D28 ve D30 çap F100."},
    "nozul": {"name": "Nozul", "slug": "nozul",
              "intro": "Lazer kesim nozulları: tek kat, çift kat, pah (bevel) ve boru kesim nozulları. Ø0.8 – Ø5.0 mm."},
    "seramik": {"name": "Seramik", "slug": "seramik",
                "intro": "Lazer kesim kafası seramik halkaları (nozul tutucu). Raytools D28 / D32 ve BOCI D41 M11."},
    "cekmece": {"name": "Çekmece & kartuş", "slug": "cekmece-kartus",
                "intro": "BOCI koruma camı çekmeceleri, kolimatör ve odak kartuşları, orijinal parça numaralarıyla."},
    "qbh": {"name": "QBH koruma camı", "slug": "qbh-koruma-cami",
            "intro": "Fiber lazer kaynağı QBH çıkış koruma camları. Raycus, MAX, IPG ve diğer kaynaklar için 1 kW'tan 12 kW'a kadar tüm güçler stokta."},
}

PACK = ["1 adet", "10'lu paket"]
LENS = ["Sadece lens", "Yuvalı (holder)"]
CAL = ["Ø" + c + " mm" for c in ["0.8", "1.0", "1.2", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"]]
CER = ["Orijinal", "Muadil"]
KW_ALL = ["1 kW", "1,5 kW", "2 kW", "3 kW", "4 kW", "6 kW", "8 kW", "10 kW", "12 kW"]

R_M11 = ["BM114S", "BM115", "BM06K", "BD04K", "BS04K", "BS06K", "BS08K", "BS12K", "BS15K", "BS20K"]
R_M14 = ["BT210S", "BT240S", "BM109", "BM110", "BM111"]
B_M11 = ["BLT310", "BLT420", "BLT420S", "BLT421", "BLT441", "BLT442", "BLT461", "BLT640", "BLT641",
         "BLT641H", "BLT642H", "BLT661", "BLT662M", "BLT663H"]
B_T = ["BLT310T", "BLT421T"]

# id, marka, kategori, ad, ölçü, uyumlu modeller, seçenekler, not
PRODUCTS = [
    ("r-k1", "raytools", "koruma", "Raytools koruma camı", "D24.9 × 1.5 mm", ["BT210S", "BT240S", "BM109", "BM111"], PACK, ""),
    ("r-k2", "raytools", "koruma", "Raytools koruma camı", "D27.9 × 4.1 mm", ["BT210S", "BT240S", "BM109", "BM110", "BM111", "BM114S"], PACK, "Genelde 0–4 kW"),
    ("r-k3", "raytools", "koruma", "Raytools koruma camı", "D37 × 7 mm", ["BT240S", "BM109", "BM111", "BM114S", "BM115", "BM06K", "BS06K"], PACK, ""),
    ("r-k4", "raytools", "koruma", "Raytools koruma camı", "D37 × 1.6 mm", ["BM115", "BM06K"], PACK, ""),
    ("r-k5", "raytools", "koruma", "Raytools koruma camı", "D30 × 5 mm", ["BD04K", "BS04K", "BS06K", "BS08K", "BS12K", "BS15K", "BS20K"], PACK, "Yüksek güç"),
    ("r-k6", "raytools", "koruma", "Raytools koruma camı", "D38.1 × 1.6 mm", ["BS08K", "BS12K", "BS15K", "BS20K"], PACK, ""),
    ("r-o1", "raytools", "odak", "Raytools odak lensi", "D28 F125", ["BT210S", "BT240S", "BM109"], LENS, ""),
    ("r-o2", "raytools", "odak", "Raytools odak lensi", "D28 F150", ["BT210S", "BT240S", "BM109"], LENS, ""),
    ("r-o3", "raytools", "odak", "Raytools odak lensi", "D30 F125", ["BM110", "BM111", "BM114S"], LENS, ""),
    ("r-o4", "raytools", "odak", "Raytools odak lensi", "D30 F150", ["BM111", "BM114S", "BM115", "BM06K"], LENS, ""),
    ("r-o5", "raytools", "odak", "Raytools odak lensi", "D30 F200", ["BM115", "BM06K", "BD04K", "BS04K", "BS06K", "BS08K", "BS12K", "BS15K", "BS20K"], LENS, ""),
    ("r-c1", "raytools", "kolimator", "Raytools kolimatör lensi", "D28 F100", ["BT210S", "BT240S", "BM109"], LENS, ""),
    ("r-c2", "raytools", "kolimator", "Raytools kolimatör lensi", "D30 F100", ["BM110", "BM111", "BM114S", "BM115", "BM06K", "BD04K", "BS04K", "BS06K", "BS08K", "BS12K", "BS15K", "BS20K"], LENS, ""),
    ("r-n1", "raytools", "nozul", "Raytools nozul, tek kat", "D28 · H15 · M11", R_M11, CAL, ""),
    ("r-n2", "raytools", "nozul", "Raytools nozul, çift kat", "D28 · H15 · M11", R_M11, CAL, ""),
    ("r-n3", "raytools", "nozul", "Raytools nozul, tek kat", "D32 · H15 · M14", R_M14, CAL, ""),
    ("r-n4", "raytools", "nozul", "Raytools nozul, çift kat", "D32 · H15 · M14", R_M14, CAL, ""),
    ("r-s1", "raytools", "seramik", "Raytools seramik", "D28 · H12 · M11", R_M11, CER, ""),
    ("r-s2", "raytools", "seramik", "Raytools seramik", "D32 · M14", R_M14, CER, ""),
    ("b-k1", "boci", "koruma", "BOCI koruma camı", "D25.4 × 4 mm", ["BLT310", "BLT310T", "BLT420", "BLT420S", "BLT421", "BLT421T"], PACK, ""),
    ("b-k2", "boci", "koruma", "BOCI koruma camı", "D34 × 5 mm", ["BLT441", "BLT442", "BLT461", "BLT640", "BLT641", "BLT641H", "BLT642H", "BLT661", "BLT662M", "BLT663H"], PACK, ""),
    ("b-n1", "boci", "nozul", "BOCI nozul, tek kat", "D28 · H15 · M11×0.75", B_M11, CAL, ""),
    ("b-n2", "boci", "nozul", "BOCI nozul, çift kat", "D28 · H15 · M11×0.75", B_M11, CAL, ""),
    ("b-n3", "boci", "nozul", "BOCI pah (bevel) nozul", "Sivri uç · M11×0.75", ["BLT310", "BLT420", "BLT421", "BLT641", "BLT661"], CAL, ""),
    ("b-n4", "boci", "nozul", "BOCI boru kesim nozulu", "M8×0.75", B_T, CAL, ""),
    ("b-s1", "boci", "seramik", "BOCI seramik", "D41 · H34 · M11", B_M11, CER, ""),
    ("b-s2", "boci", "seramik", "BOCI seramik, T serisi", "M8×0.75", B_T, CER, ""),
    ("b-c1", "boci", "cekmece", "BOCI kolimatör kartuşu", "DP.M.Q0421AA", ["BLT310", "BLT310T"], ["1 adet"], ""),
    ("b-c2", "boci", "cekmece", "BOCI kolimatör kartuşu", "P.S.M0220", ["BLT420", "BLT420S"], ["1 adet"], ""),
    ("b-c3", "boci", "cekmece", "BOCI kolimatör kartuşu", "DP.M.Q0011AA", ["BLT640", "BLT641", "BLT641H"], ["1 adet"], ""),
    ("b-c4", "boci", "cekmece", "BOCI odak kartuşu", "F150 / F200", ["BLT441", "BLT442", "BLT461"], ["F150", "F200"], ""),
    ("b-c5", "boci", "cekmece", "BOCI alt koruma camı çekmecesi", "DP.M.Q0208AA", ["BLT310", "BLT310T"], ["1 adet"], ""),
    ("b-c6", "boci", "cekmece", "BOCI alt koruma camı çekmecesi", "P.S.M0131", ["BLT640", "BLT641"], ["1 adet"], ""),
    ("b-c7", "boci", "cekmece", "BOCI üst koruma camı çekmecesi", "Üst çekmece", ["BLT310", "BLT420", "BLT421", "BLT641", "BLT661"], ["1 adet"], ""),
    ("q-1", "qbh", "qbh", "QBH koruma camı (Raycus)", "D12.8 × H17 mm", ["Raycus"], KW_ALL, ""),
    ("q-2", "qbh", "qbh", "QBH koruma camı (Raycus)", "D12.8 × H19.7 mm", ["Raycus"], KW_ALL, ""),
    ("q-3", "qbh", "qbh", "QBH koruma camı (Raycus)", "D13 × H16 mm", ["Raycus"], KW_ALL, ""),
    ("q-4", "qbh", "qbh", "QBH koruma camı (Raycus)", "D22 × H16.8 mm", ["Raycus"], ["3 kW", "4 kW", "6 kW", "8 kW", "10 kW", "12 kW"], ""),
    ("q-5", "qbh", "qbh", "QBH koruma camı (MAX)", "9.4 × 12.8 mm", ["MAX"], ["1 kW", "1,5 kW", "2 kW", "3 kW"], ""),
    ("q-6", "qbh", "qbh", "QBH koruma camı (MAX)", "16.9 × 12.8 mm", ["MAX"], ["3 kW", "4 kW", "6 kW"], ""),
    ("q-7", "qbh", "qbh", "QBH koruma camı (MAX)", "18.7 × 12.8 mm", ["MAX"], ["6 kW", "8 kW", "10 kW", "12 kW"], ""),
    ("q-8", "qbh", "qbh", "QBH koruma camı (MAX)", "19.8 × 13 mm", ["MAX"], ["6 kW", "8 kW", "10 kW", "12 kW"], ""),
    ("q-9", "qbh", "qbh", "QBH koruma camı (IPG / diğer)", "Ölçüye göre", ["IPG", "JPT", "Reci"], KW_ALL, ""),
    ("q-10", "qbh", "qbh", "QBH çıkış koruma lens grubu", "Kapaklı set", ["Raycus", "MAX"], ["3,3 kW", "4 kW", "6 kW", "12 kW"], ""),
]
