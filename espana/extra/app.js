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
