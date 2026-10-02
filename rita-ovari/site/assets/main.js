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

  var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var COLORS = ['var(--sticky)', 'var(--blush)', 'var(--lagoon)', 'var(--sky)', 'var(--spark)', 'var(--lilac)'];
  function confetti(x, y, n) {
    if (calm) return;
    for (var i = 0; i < (n || 18); i++) {
      var c = document.createElement('span');
      c.className = 'confetti';
      c.style.left = x + 'px'; c.style.top = y + 'px';
      c.style.background = COLORS[i % COLORS.length];
      var a = Math.random() * Math.PI * 2, d = 60 + Math.random() * 120;
      c.style.setProperty('--x', Math.cos(a) * d + 'px');
      c.style.setProperty('--y', Math.sin(a) * d + 80 + 'px');
      c.style.setProperty('--r', (Math.random() * 720 - 360) + 'deg');
      document.body.appendChild(c);
      setTimeout(c.remove.bind(c), 1400);
    }
  }

  // Hero figure: eyes follow the pointer.
  var eyes = document.querySelectorAll('.eye');
  window.addEventListener('pointermove', function (e) {
    eyes.forEach(function (eye) {
      var r = eye.getBoundingClientRect();
      if (!r.width) return;
      var dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
      var a = Math.atan2(dy, dx), m = Math.min(5, Math.hypot(dx, dy) / 40);
      eye.style.transform = 'translate(' + Math.cos(a) * m + 'px,' + Math.sin(a) * m + 'px)';
    });
  }, { passive: true });

  // Hero sticky notes: drag them around the artwork.
  document.querySelectorAll('[data-art] .float').forEach(function (n) {
    var sx, sy, ox, oy;
    n.addEventListener('pointerdown', function (e) {
      n.setPointerCapture(e.pointerId); n.classList.add('drag');
      var box = n.parentNode.getBoundingClientRect(), r = n.getBoundingClientRect();
      n.style.left = (r.left - box.left) + 'px'; n.style.top = (r.top - box.top) + 'px';
      n.style.right = 'auto'; n.style.bottom = 'auto';
      sx = e.clientX; sy = e.clientY; ox = r.left - box.left; oy = r.top - box.top;
    });
    n.addEventListener('pointermove', function (e) {
      if (!n.classList.contains('drag')) return;
      n.style.left = ox + e.clientX - sx + 'px'; n.style.top = oy + e.clientY - sy + 'px';
    });
    function drop(e) {
      if (!n.classList.contains('drag')) return;
      n.classList.remove('drag');
      n.style.setProperty('--r', (Math.random() * 10 - 5).toFixed(1) + 'deg');
      if (Math.hypot(e.clientX - sx, e.clientY - sy) > 30) confetti(e.clientX, e.clientY, 10);
    }
    n.addEventListener('pointerup', drop); n.addEventListener('pointercancel', drop);
  });

  // Service board: pick notes, collect them in a tray, prefill the contact message.
  document.querySelectorAll('[data-board]').forEach(function (board) {
    var scope = board.closest('[data-lang-block]') || document;
    var tray = scope.querySelector('[data-tray]'), count = tray.querySelector('[data-count]');
    var go = tray.querySelector('[data-tray-go]');
    function picked() { return [].slice.call(board.querySelectorAll('.pick[aria-pressed="true"]')); }
    board.addEventListener('click', function (e) {
      var b = e.target.closest('.pick'); if (!b) return;
      var on = b.getAttribute('aria-pressed') !== 'true';
      b.setAttribute('aria-pressed', on); b.textContent = b.getAttribute(on ? 'data-on' : 'data-off');
      b.closest('.note').classList.toggle('picked', on);
      if (on) { var r = b.getBoundingClientRect(); confetti(r.left + r.width / 2, r.top, 14); }
      var n = picked().length; count.textContent = n;
      tray.classList.toggle('show', n > 0);
      tray.classList.remove('bump'); void tray.offsetWidth; tray.classList.add('bump');
    });
    go.addEventListener('click', function () {
      var msg = scope.querySelector('textarea[name="message"]');
      if (msg) msg.value = go.getAttribute('data-prefill') + '\n' + picked().map(function (b) { return '• ' + b.getAttribute('data-title'); }).join('\n') + '\n\n';
      tray.classList.remove('show');
      setTimeout(function () { if (msg) msg.focus({ preventScroll: true }); }, 600);
    });
  });

  // Scroll reveal (elements are visible at rest; .in replays a pop as they enter).
  if ('IntersectionObserver' in window && !calm) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.rv').forEach(function (el) {
      if (el.getBoundingClientRect().top > window.innerHeight) io.observe(el);
    });
  }

  // Process line fills as you scroll through it.
  var steps = document.querySelectorAll('[data-steps]');
  function progress() {
    steps.forEach(function (s) {
      var r = s.getBoundingClientRect(); if (!r.height) return;
      var p = Math.max(0, Math.min(1, (window.innerHeight * 0.85 - r.top) / (window.innerHeight * 0.5)));
      s.style.setProperty('--p', p);
    });
  }
  window.addEventListener('scroll', progress, { passive: true }); progress();

  // Hobby chips: the diving one blows bubbles.
  document.querySelectorAll('.offclock span:nth-child(2)').forEach(function (chip) {
    chip.addEventListener('pointerenter', function () {
      if (calm) return;
      for (var i = 0; i < 5; i++) (function (i) {
        setTimeout(function () {
          var b = document.createElement('i'); b.className = 'bubble';
          b.style.left = 10 + Math.random() * 70 + '%';
          chip.appendChild(b); setTimeout(b.remove.bind(b), 1300);
        }, i * 130);
      })(i);
    });
  });

  // Celebrate a sent form.
  document.querySelectorAll('form[data-contact]').forEach(function (f) {
    f.addEventListener('submit', function () {
      if (!f.checkValidity()) return;
      var r = f.querySelector('[type="submit"]').getBoundingClientRect();
      confetti(r.left + r.width / 2, r.top, 28);
    });
  });
})();
