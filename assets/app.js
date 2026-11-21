(function () {
  var D = window.LS;
  var P = D.products, HEADS = D.heads, CATS = D.cats;
  var $ = function (id) { return document.getElementById(id); };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function findP(id) { for (var i = 0; i < P.length; i++) if (P[i].id === id) return P[i]; }

  // ---------- Sepet (her sayfada) ----------
  var cart = [];
  try { cart = JSON.parse(localStorage.getItem("lenssepeti-cart") || "[]").filter(function (l) { return findP(l.id); }); } catch (e) { cart = []; }
  function save() { try { localStorage.setItem("lenssepeti-cart", JSON.stringify(cart)); } catch (e) {} }
  function waNumber() { var n = D.site.whatsapp.replace(/\D/g, ""); if (n.charAt(0) === "0") n = "9" + n; return n; }
  function val(id) { return $(id).value.trim(); }
  function itemsText() {
    return cart.length ? cart.map(function (l) { var p = findP(l.id); return "• " + l.qty + " × " + p.n + " " + p.d + " (" + l.opt + ")"; }).join("\n") : "(sepet boş)";
  }
  function message() {
    var lines = [["Firma", val("firma")], ["Telefon", val("tel")], ["Adres", val("adres")], ["Not", val("not")]]
      .filter(function (x) { return x[1]; }).map(function (x) { return x[0] + ": " + x[1]; }).join("\n");
    return "Merhaba Lenssepeti, sipariş / fiyat teklifi istiyorum.\n" + (lines ? lines + "\n" : "") + "\n" + itemsText();
  }
  function renderCart() {
    $("badge").textContent = cart.reduce(function (s, l) { return s + l.qty; }, 0);
    $("dlist").innerHTML = cart.length ? cart.map(function (l, i) {
      var p = findP(l.id);
      return '<div class="line"><span class="n">' + esc(p.n) + '</span>' +
        '<div class="qty"><button type="button" data-dec="' + i + '" aria-label="Azalt">−</button><span>' + l.qty + '</span><button type="button" data-inc="' + i + '" aria-label="Artır">+</button></div>' +
        '<span class="v">' + esc(p.d) + ' · ' + esc(l.opt) + '</span></div>';
    }).join("") : '<p class="hint" style="padding:24px 0">Sepetiniz boş. Kafa modelinizi seçip parçaları ekleyin.</p>';
    var m = message();
    $("msg").textContent = m;
    $("waLink").href = "https://wa.me/" + waNumber() + "?text=" + encodeURIComponent(m);
  }
  function toast(t) { var el = $("toast"); el.textContent = t; el.hidden = false; clearTimeout(toast.t); toast.t = setTimeout(function () { el.hidden = true; }, 1800); }
  function openCart(v) { $("drawer").hidden = !v; $("scrim").hidden = !v; if (v) $("closeCart").focus(); }

  // ---------- Katalog (sadece ana sayfada) ----------
  var isCatalog = !!$("brands");
  var params = new URLSearchParams(location.search);
  var state = { brand: params.get("marka") || "all", model: params.get("model") || null, cat: params.get("parca") || "all", q: "" };
  if (state.model && state.brand === "all") {
    Object.keys(HEADS).forEach(function (b) { if (HEADS[b].models.indexOf(state.model) >= 0) state.brand = b; });
  }
  var ICON = D.icons;

  function cardHTML(p) {
    var fits = p.f.length > 6 ? p.f.slice(0, 6).join(", ") + " +" + (p.f.length - 6) : p.f.join(", ");
    return '<article class="card">' +
      '<div class="thumb"><svg viewBox="0 0 72 72" aria-hidden="true">' + ICON[p.c] + '</svg></div>' +
      '<span class="cat">' + esc(CATS[p.c].name) + (p.note ? ' · ' + esc(p.note) : '') + '</span>' +
      '<div><h3>' + esc(p.n) + '</h3><div class="dims">' + esc(p.d) + '</div></div>' +
      '<p class="fits">Uyumlu: <b title="' + esc(p.f.join(", ")) + '">' + esc(fits) + '</b></p>' +
      '<div><div class="buy"><select id="o-' + p.id + '" aria-label="Seçenek">' + p.o.map(function (o) { return '<option>' + esc(o) + '</option>'; }).join("") + '</select>' +
      '<button class="add" type="button" data-add="' + p.id + '">Sepete ekle</button></div>' +
      '<p class="price">Fiyat için sorun</p></div></article>';
  }

  function renderPicker() {
    var list = [["all", "Tümü", "Bütün markalar"], ["raytools", "Raytools", HEADS.raytools.models.length + " model"], ["boci", "BOCI (Bochu)", HEADS.boci.models.length + " model"], ["qbh", "QBH camı", "1–12 kW"]];
    $("brands").innerHTML = list.map(function (b) {
      return '<button type="button" class="tab" data-b="' + b[0] + '" aria-pressed="' + (state.brand === b[0]) + '">' + b[1] + '<small>' + b[2] + '</small></button>';
    }).join("");
    var models = HEADS[state.brand] ? HEADS[state.brand].models : [];
    $("modelBox").hidden = models.length === 0;
    $("models").innerHTML = ['<button type="button" class="chip" data-m="" aria-pressed="' + (!state.model) + '">Hepsi</button>'].concat(models.map(function (m) {
      return '<button type="button" class="chip" data-m="' + m + '" aria-pressed="' + (state.model === m) + '">' + m + '</button>';
    })).join("");
    $("cats").innerHTML = [["all", "Tümü"]].concat(Object.keys(CATS).map(function (k) { return [k, CATS[k].name]; })).map(function (c) {
      return '<button type="button" class="chip" data-c="' + c[0] + '" aria-pressed="' + (state.cat === c[0]) + '">' + c[1] + '</button>';
    }).join("");
  }

  function norm(s) { return s.toLowerCase().replace(/,/g, ".").replace(/×/g, "x").replace(/\s*x\s*/g, "x").replace(/\s+/g, " ").trim(); }
  function filtered() {
    var q = norm(state.q);
    return P.filter(function (p) {
      if (state.brand !== "all" && p.b !== state.brand) return false;
      if (state.model && p.f.indexOf(state.model) < 0) return false;
      if (state.cat !== "all" && p.c !== state.cat) return false;
      if (q) {
        var hay = norm(p.n + " " + p.d + " " + p.f.join(" ") + " " + (p.note || "") + " " + CATS[p.c].name + " " + (HEADS[p.b] ? HEADS[p.b].name : "qbh"));
        if (q.split(" ").some(function (w) { return hay.indexOf(w) < 0; })) return false;
      }
      return true;
    });
  }

  function renderGrid() {
    var items = filtered();
    $("resTitle").textContent = state.model ? state.model + " için parçalar" : state.brand === "all" ? "Tüm parçalar" : state.brand === "qbh" ? "QBH koruma camları" : HEADS[state.brand].name + " parçaları";
    $("resCount").textContent = items.length + " ürün";
    $("qbhBox").hidden = !(state.brand === "qbh" || state.cat === "qbh");
    $("grid").innerHTML = items.length ? items.map(cardHTML).join("") :
      '<div class="empty">Bu seçime uyan parça bulunamadı. Aramayı temizleyin ya da kafanızın fotoğrafını WhatsApp\'tan gönderin, biz bulalım.</div>';
    var u = new URLSearchParams();
    if (state.brand !== "all") u.set("marka", state.brand);
    if (state.model) u.set("model", state.model);
    if (state.cat !== "all") u.set("parca", state.cat);
    var qs = u.toString();
    history.replaceState(null, "", location.pathname + (qs ? "?" + qs : ""));
  }

  document.addEventListener("click", function (e) {
    var t = e.target.closest("button"); if (!t) return;
    if (t.dataset.b !== undefined) { state.brand = t.dataset.b; state.model = null; renderPicker(); renderGrid(); }
    else if (t.dataset.m !== undefined) { state.model = t.dataset.m || null; renderPicker(); renderGrid(); }
    else if (t.dataset.c !== undefined) { state.cat = t.dataset.c; renderPicker(); renderGrid(); }
    else if (t.dataset.add) {
      var opt = $("o-" + t.dataset.add).value, found = null;
      cart.forEach(function (l) { if (l.id === t.dataset.add && l.opt === opt) found = l; });
      if (found) found.qty++; else cart.push({ id: t.dataset.add, opt: opt, qty: 1 });
      save(); renderCart(); toast("Sepete eklendi");
    }
    else if (t.dataset.inc) { cart[+t.dataset.inc].qty++; save(); renderCart(); }
    else if (t.dataset.dec) { var i = +t.dataset.dec; cart[i].qty--; if (cart[i].qty < 1) cart.splice(i, 1); save(); renderCart(); }
  });
  $("openCart").addEventListener("click", function () { openCart(true); });
  $("closeCart").addEventListener("click", function () { openCart(false); });
  $("scrim").addEventListener("click", function () { openCart(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") openCart(false); });
  ["firma", "tel", "adres", "not"].forEach(function (id) { $(id).addEventListener("input", renderCart); });

  // ---------- E-posta ile sipariş (Web3Forms) ----------
  var KEY = (D.site.order_key || "").trim();
  var URL_ = (D.site.order_url || "").trim();
  if (!KEY && !URL_) { $("sendOrder").hidden = true; $("waLink").className = "primary"; }
  function sendOrder() {
    if (URL_) {
      // text/plain: Google Apps Script'e ön kontrol (preflight) olmadan gönderilir
      return fetch(URL_, { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" },
        body: JSON.stringify({ firma: val("firma"), tel: val("tel"), adres: val("adres"), not: val("not"), urunler: itemsText(), website: $("website").value })
      }).then(function (r) { return r.json(); });
    }
    return fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify({
        access_key: KEY, subject: "Yeni sipariş: " + val("firma"), from_name: "Lenssepeti sitesi",
        "Ad soyad / firma": val("firma"), "Telefon": val("tel"), "Adres": val("adres"), "Not": val("not"),
        "Ürünler": itemsText(), "Sayfa": location.href, botcheck: $("website").value
      })
    }).then(function (r) { return r.json(); });
  }
  function showErr(t) { $("orderErr").textContent = t; $("orderErr").hidden = !t; }
  $("orderForm").addEventListener("submit", function (e) {
    e.preventDefault();
    if (!KEY && !URL_) return;
    if (!cart.length) return showErr("Sepetiniz boş. Önce parça ekleyin.");
    if (!val("firma") || !val("tel")) return showErr("Ad soyad / firma ve telefon alanlarını doldurun.");
    showErr("");
    var btn = $("sendOrder"); btn.disabled = true; btn.textContent = "Gönderiliyor…";
    sendOrder().then(function (res) {
      if (!res.success) throw new Error(res.message || "");
      $("orderNo").textContent = res.no ? "Sipariş no: " + res.no : "";
      cart = []; save(); renderCart();
      $("orderForm").hidden = true; $("orderDone").hidden = false;
    }).catch(function () {
      showErr("Sipariş gönderilemedi. İnternet bağlantınızı kontrol edip tekrar deneyin ya da WhatsApp ile gönderin.");
    }).then(function () { btn.disabled = false; btn.textContent = "Siparişi gönder"; });
  });
  $("newOrder").addEventListener("click", function () { $("orderForm").hidden = false; $("orderDone").hidden = true; });

  if (isCatalog) {
    state.q = params.get("q") || "";
    $("q").value = state.q;
    $("q").closest("form").addEventListener("submit", function (e) { e.preventDefault(); });
    $("q").addEventListener("input", function (e) { state.q = e.target.value; renderGrid(); });
    renderPicker(); renderGrid();
  }
  renderCart();
})();
