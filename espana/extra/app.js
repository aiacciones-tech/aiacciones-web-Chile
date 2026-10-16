// Formulario de contacto de AIAcciones España (enviar.php en el propio hosting).
(function () {
  var form = document.getElementById("contact");
  if (!form) return;
  var msg = document.getElementById("c-msg"), send = document.getElementById("c-send");
  var show = function (text, ok) { msg.textContent = text; msg.className = "form-msg " + (ok ? "ok" : "err"); msg.hidden = false; };
  var OK = "Mensaje enviado. Te responderemos a tu correo.";
  var ERR = "No se pudo enviar el mensaje. Inténtalo de nuevo más tarde o escríbenos en los comentarios de nuestros vídeos de YouTube.";
  var t0 = form.querySelector('input[name="_t"]'), start = Date.now();
  if (location.hash === "#enviado") show(OK, true);
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
        show(OK, true);
      })
      .catch(function () { show(ERR, false); })
      .then(function () { send.disabled = false; send.textContent = "Enviar mensaje"; });
  });
})();

// Correo del titular oculto: se arma al pulsar el botón para que los robots de spam no lo lean en el HTML.
(function () {
  document.querySelectorAll(".mail-btn").forEach(function (b) {
    b.addEventListener("click", function () {
      var rev = function (s) { return s.split("").reverse().join(""); };
      var m = rev(b.dataset.u) + "@" + rev(b.dataset.d);
      var a = document.createElement("a");
      a.href = "mailto:" + m; a.textContent = m;
      b.replaceWith(a);
    });
  });
})();

// Aviso de cookies: Google Analytics solo se carga si el visitante pulsa «Aceptar» (RGPD/LSSI).
// La elección se guarda en localStorage (no es una cookie) y se vuelve a pedir pasados 12 meses.
(function () {
  var bar = document.getElementById("cookie-bar");
  if (!bar) return;
  var GA = bar.dataset.ga, KEY = "aiacc-es-cookies", YEAR = 365 * 24 * 3600 * 1000;
  var leer = function () {
    try { var v = JSON.parse(localStorage.getItem(KEY)); return v && Date.now() - v.t < YEAR ? v.c : null; } catch (e) { return null; }
  };
  var guardar = function (c) { try { localStorage.setItem(KEY, JSON.stringify({ c: c, t: Date.now() })); } catch (e) {} };
  // La etiqueta de Google (con consentimiento denegado por defecto) está en el <head> de cada página; aquí solo se cambia el permiso.
  var consentir = function (si) {
    if (window.gtag) gtag("consent", "update", { analytics_storage: si ? "granted" : "denied" });
  };
  var borrarGA = function () {
    var dom = location.hostname.replace(/^www\./, "");
    document.cookie.split(";").forEach(function (c) {
      var n = c.split("=")[0].trim();
      if (n.indexOf("_ga") !== 0) return;
      [dom, "." + dom, ""].forEach(function (d) {
        document.cookie = n + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/" + (d ? "; domain=" + d : "");
      });
    });
  };
  var elegido = leer();
  if (elegido === null) bar.hidden = false;
  document.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-cookies]");
    if (!b) return;
    var c = b.dataset.cookies;
    if (c === "config") { bar.hidden = false; return; }
    var antes = leer();
    guardar(c); bar.hidden = true;
    consentir(c === "si");
    if (c !== "si") { borrarGA(); if (antes === "si") location.reload(); }
  });
})();
