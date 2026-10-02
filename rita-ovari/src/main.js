(function () {
  // Contact form: posts to the endpoint in data-endpoint (e.g. Formspree). Without a real endpoint it only shows a preview note.
  document.querySelectorAll('form[data-contact]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var msg = form.querySelector('[data-msg]');
      var ep = form.getAttribute('data-endpoint') || '';
      var show = function (text) { msg.textContent = text; msg.hidden = false; };
      if (!ep || ep.indexOf('YOUR_FORM_ID') !== -1) { show(form.getAttribute('data-preview')); return; }
      fetch(ep, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) { if (!r.ok) throw r; form.reset(); show(form.getAttribute('data-ok')); })
        .catch(function () { show(form.getAttribute('data-error')); });
    });
  });
  // Single-file preview only: switch between the HU and EN blocks in place.
  var blocks = document.querySelectorAll('[data-lang-block]');
  if (blocks.length > 1) {
    document.querySelectorAll('[data-lang-switch]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var lang = a.getAttribute('data-lang-switch');
        blocks.forEach(function (b) { b.hidden = b.getAttribute('data-lang-block') !== lang; });
        document.documentElement.lang = lang;
        try { localStorage.setItem('ro-lang', lang); } catch (err) {}
        window.scrollTo(0, 0);
      });
    });
    try { var saved = localStorage.getItem('ro-lang'); if (saved) { var t = document.querySelector('[data-lang-switch="' + saved + '"]'); if (t) t.click(); } } catch (err) {}
  }
})();
