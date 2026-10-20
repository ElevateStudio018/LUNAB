(function () {
  "use strict";
  document.documentElement.classList.add("js");

  // Meny på små skärmar
  var btn = document.getElementById("menuBtn");
  var menu = document.getElementById("menu");
  if (btn && menu) {
    function setOpen(open) {
      menu.hidden = !open;
      btn.setAttribute("aria-expanded", String(open));
      btn.setAttribute("aria-label", open ? "Stäng menyn" : "Meny");
    }
    btn.addEventListener("click", function () { setOpen(menu.hidden); });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) setOpen(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !menu.hidden) { setOpen(false); btn.focus(); }
    });
  }

  document.querySelectorAll("[data-year]").forEach(function (y) { y.textContent = new Date().getFullYear(); });

  // Element tonas in när de syns
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  // Offertformulär: valideras här, skickas via FormSubmit, tackmeddelande bara när det faktiskt gått fram
  var form = document.getElementById("qform");
  if (!form) return;
  var done = document.getElementById("qdone");
  var sendErr = document.getElementById("send-err");
  var f = {
    namn: document.getElementById("f-namn"),
    foretag: document.getElementById("f-foretag"),
    tel: document.getElementById("f-tel"),
    epost: document.getElementById("f-epost"),
    typ: document.getElementById("f-typ"),
    besk: document.getElementById("f-besk"),
    web: document.getElementById("f-web")
  };

  // "Begär offert" från tjänstesidan kommer med ?typ=… och väljer den tjänsten
  var typ = new URLSearchParams(location.search).get("typ");
  if (typ) {
    for (var i = 0; i < f.typ.options.length; i++) if (f.typ.options[i].text === typ) f.typ.selectedIndex = i;
  }

  function mark(key, input, bad) {
    document.getElementById("e-" + key).hidden = !bad;
    input.setAttribute("aria-invalid", bad ? "true" : "false");
    if (bad) input.setAttribute("aria-describedby", "e-" + key); else input.removeAttribute("aria-describedby");
  }
  function validate() {
    var bad = [];
    var checks = [
      ["namn", !f.namn.value.trim()],
      ["tel", f.tel.value.replace(/[^\d]/g, "").length < 7],
      ["epost", !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.epost.value.trim())],
      ["typ", !f.typ.value],
      ["besk", !f.besk.value.trim()]
    ];
    checks.forEach(function (c) { mark(c[0], f[c[0]], c[1]); if (c[1]) bad.push(f[c[0]]); });
    return bad;
  }
  var tried = false;
  form.addEventListener("input", function () { if (tried) validate(); });
  form.addEventListener("change", function () { if (tried) validate(); });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    tried = true;
    var bad = validate();
    if (bad.length) { bad[0].focus(); return; }
    var submit = form.querySelector("button[type=submit]");
    var label = submit.innerHTML;
    submit.disabled = true;
    submit.textContent = "Skickar …";
    sendErr.hidden = true;
    var payload = {
      _subject: "Förfrågan från hemsidan – " + f.namn.value.trim(),
      _template: "table",
      _captcha: "false",
      _honey: f.web.value,
      _replyto: f.epost.value.trim(),
      Namn: f.namn.value.trim(),
      "Företag": f.foretag.value.trim() || "–",
      Telefon: f.tel.value.trim(),
      "E-post": f.epost.value.trim(),
      "Förfrågan gäller": f.typ.value,
      Beskrivning: f.besk.value.trim()
    };
    fetch(form.getAttribute("data-endpoint"), {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(payload)
    }).then(function (r) {
      return r.json().catch(function () { return null; }).then(function (j) {
        if (!r.ok || !j || String(j.success) !== "true") throw new Error("not sent");
      });
    }).then(function () {
      form.reset();
      tried = false;
      form.hidden = true;
      done.hidden = false;
      done.focus();
    }).catch(function () {
      // Texten ligger kvar så att den kan skickas igen
      sendErr.hidden = false;
    }).then(function () {
      submit.disabled = false;
      submit.innerHTML = label;
    });
  });

  document.getElementById("qagain").addEventListener("click", function () {
    done.hidden = true;
    form.hidden = false;
    f.namn.focus();
  });
})();
