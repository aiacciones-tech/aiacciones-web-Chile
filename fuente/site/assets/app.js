(function () {
  var fmt = function (v, suf) {
    if (v === null || v === undefined) return "n/a";
    var s = Math.abs(v).toLocaleString("es-CL", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
    return (v < 0 ? "−" : "") + s + (suf || "");
  };

  // ---------- Rankings y filtros
  var rank = document.getElementById("rank");
  if (rank && window.RANK_DATA) {
    var $ = function (id) { return document.getElementById(id); };
    var f = { pe: $("f-pe"), epsg: $("f-epsg"), dy: $("f-dy"), chg: $("f-chg"), sort: $("f-sort") };
    var presets = document.querySelectorAll("[data-preset]");
    var defaults = { pe: 30, epsg: -20, dy: 0, chg: 0, sort: "pe:asc" };
    var PRESETS = {
      pe: { pe: 12, sort: "pe:asc" },
      epsg: { epsg: 10, sort: "epsg:desc" },
      dy: { dy: 5, sort: "dy:desc" },
      chg: { chg: 5, sort: "chg:asc" },
      reset: {}
    };
    var render = function () {
      var pe = +f.pe.value, eg = +f.epsg.value, dy = +f.dy.value, ch = +f.chg.value;
      $("o-pe").textContent = pe >= 30 ? "sin límite" : "≤ " + fmt(pe, "x");
      $("o-epsg").textContent = eg <= -20 ? "sin límite" : "≥ " + fmt(eg, "%");
      $("o-dy").textContent = dy <= 0 ? "sin límite" : "≥ " + fmt(dy, "%");
      $("o-chg").textContent = ch <= 0 ? "sin límite" : "≥ " + fmt(ch, "%");
      var parts = f.sort.value.split(":"), key = parts[0], dir = parts[1] === "asc" ? 1 : -1;
      var rows = window.RANK_DATA.filter(function (d) {
        return (pe >= 30 || d.pe <= pe) && (eg <= -20 || d.epsg >= eg) && d.dy >= dy && (ch <= 0 || d.chg <= -ch);
      }).sort(function (a, b) { return (a[key] - b[key]) * dir; });
      var tb = rank.tBodies[0];
      $("count").textContent = rows.length + " de " + window.RANK_DATA.length + " acciones cumplen los filtros";
      if (!rows.length) { tb.innerHTML = '<tr><td class="empty" colspan="7">Ninguna acción cumple todos los filtros. Relaja alguno.</td></tr>'; return; }
      tb.innerHTML = rows.map(function (d, i) {
        var t = d.link ? '<a href="../acciones/' + d.id + '/index.html">' + d.t + "</a>" : d.t;
        return "<tr><td>" + (i + 1) + '</td><th scope="row">' + t + '</th><td class="txt">' + d.s + "</td><td>" + fmt(d.pe, "x") +
          '</td><td class="' + (d.epsg < 0 ? "neg" : "") + '">' + fmt(d.epsg, "%") + "</td><td>" + fmt(d.dy, "%") +
          '</td><td class="' + (d.chg < 0 ? "down" : "up") + '">' + (d.chg > 0 ? "+" : "") + fmt(d.chg, "%") + "</td></tr>";
      }).join("");
    };
    var setPressed = function (name) {
      presets.forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.preset === name && name !== "reset")); });
    };
    Object.keys(f).forEach(function (k) { f[k].addEventListener("input", function () { setPressed(null); render(); }); });
    presets.forEach(function (b) {
      b.addEventListener("click", function () {
        var p = PRESETS[b.dataset.preset];
        Object.keys(defaults).forEach(function (k) { f[k].value = k in p ? p[k] : defaults[k]; });
        setPressed(b.dataset.preset); render();
      });
    });
    render();
  }

  // ---------- Consentimiento de cookies (Google Consent Mode v2)
  var consent = document.getElementById("consent");
  if (consent) {
    var saved = null;
    try { saved = localStorage.getItem("aia-consent"); } catch (e) {}
    if (!saved) consent.hidden = false;
    document.querySelectorAll("[data-consent]").forEach(function (b) {
      b.addEventListener("click", function () {
        var v = b.dataset.consent;
        try { localStorage.setItem("aia-consent", v); } catch (e) {}
        if (typeof gtag === "function") gtag("consent", "update", { ad_storage: v, ad_user_data: v, ad_personalization: v, analytics_storage: v });
        consent.hidden = true;
      });
    });
    document.querySelectorAll("[data-consent-open]").forEach(function (b) {
      b.addEventListener("click", function () { consent.hidden = false; });
    });
  }

  // ---------- Gráficos de análisis técnico: línea vertical y tooltip
  document.querySelectorAll("script[data-tip-for]").forEach(function (sc) {
    var svg = document.getElementById(sc.getAttribute("data-tip-for"));
    if (!svg) return;
    var data; try { data = JSON.parse(sc.textContent); } catch (e) { return; }
    var wrap = svg.parentNode, tipEl = wrap.querySelector(".tc-tip"), cross = svg.querySelector(".tc-cross");
    var n = data.d.length;
    var f = function (v) { return v === null ? "–" : v.toLocaleString("es-CL", { maximumFractionDigits: Math.abs(v) >= 1000 ? 0 : 2 }); };
    var move = function (ev) {
      var r = svg.getBoundingClientRect();
      var vx = (ev.clientX - r.left) / r.width * data.w;
      var i = Math.round((vx - data.x0) / data.pw * (n - 1));
      if (i < 0 || i >= n) { hide(); return; }
      var x = data.x0 + i * data.pw / (n - 1);
      cross.setAttribute("x1", x); cross.setAttribute("x2", x); cross.setAttribute("visibility", "visible");
      tipEl.innerHTML = "<b>" + data.d[i] + "</b>" + data.s.map(function (s) {
        return '<span><em><i style="background:' + s[1] + '"></i>' + s[0] + "</em>" + f(s[2][i]) + "</span>";
      }).join("");
      tipEl.hidden = false;
      var px = x / data.w * r.width, tw = tipEl.offsetWidth;
      tipEl.style.left = (px + 14 + tw > r.width ? px - tw - 14 : px + 14) + "px";
    };
    var hide = function () { tipEl.hidden = true; cross.setAttribute("visibility", "hidden"); };
    svg.addEventListener("pointermove", move);
    svg.addEventListener("pointerdown", move);
    svg.addEventListener("pointerleave", hide);
  });

  // ---------- Copiar correo
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var done = function () { b.textContent = "Copiado"; setTimeout(function () { b.textContent = "Copiar"; }, 1600); };
      try {
        navigator.clipboard.writeText(b.dataset.copy).then(done, function () {});
      } catch (e) {}
    });
  });

  // ---------- Tablas ordenables (clic en el título de la columna)
  var numOf = function (txt) {
    var t = txt.replace(/[~$%x\s]/g, "").replace(/\./g, "").replace(",", ".").replace("\u2212", "-");
    var v = parseFloat(t);
    return isNaN(v) ? null : v;
  };
  document.querySelectorAll("table.sortable").forEach(function (tb) {
    var ths = tb.querySelectorAll("thead th"), body = tb.tBodies[0];
    ths.forEach(function (th, i) {
      th.setAttribute("data-k", i);
      th.tabIndex = 0;
      var go = function () {
        var asc = th.getAttribute("aria-sort") !== "ascending";
        ths.forEach(function (o) { o.removeAttribute("aria-sort"); });
        th.setAttribute("aria-sort", asc ? "ascending" : "descending");
        var rows = Array.prototype.slice.call(body.rows), txt = th.classList.contains("txt") || i === 0;
        rows.sort(function (a, b) {
          var x = a.cells[i].textContent.trim(), y = b.cells[i].textContent.trim();
          if (txt) return (asc ? 1 : -1) * x.localeCompare(y, "es");
          var nx = numOf(x), ny = numOf(y);
          if (nx === null && ny === null) return 0;
          if (nx === null) return 1;
          if (ny === null) return -1;
          return (asc ? 1 : -1) * (nx - ny);
        });
        rows.forEach(function (r) { body.appendChild(r); });
      };
      th.addEventListener("click", go);
      th.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); } });
    });
  });

  // ---------- Formulario de contacto (enviar.php en el propio hosting)
  var form = document.getElementById("contact");
  if (form) {
    var msg = document.getElementById("c-msg"), send = document.getElementById("c-send");
    var show = function (text, ok) { msg.textContent = text; msg.className = "form-msg " + (ok ? "ok" : "err"); msg.hidden = false; };
    var ERR = "No se pudo enviar el mensaje. Inténtalo más tarde o escríbenos directamente a contacto@aiacciones.cl.";
    var t0 = form.querySelector('input[name="_t"]'), start = Date.now();
    if (location.hash === "#enviado") show("Mensaje enviado. Te responderemos a tu correo.", true);
    if (location.hash === "#error") show(ERR, false);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (t0) t0.value = Date.now() - start;
      send.disabled = true; send.textContent = "Enviando…";
      fetch(form.getAttribute("action"), { method: "POST", headers: { Accept: "application/json" }, body: new FormData(form) })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j.ok) throw new Error(j.message || "error");
          form.reset();
          show("Mensaje enviado. Te responderemos a tu correo.", true);
        })
        .catch(function () { show(ERR, false); })
        .then(function () { send.disabled = false; send.textContent = "Enviar mensaje"; });
    });
  }
})();
