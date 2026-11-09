/* Cozybat — scripts communs : menu, apparitions, bandeau d'avis, avant/après, questionnaire, formulaire, suivi */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.remove('no-js');
  doc.classList.add('js');

  /* ---------- bandeau d'avis : duplication pour la boucle (copie masquée aux lecteurs d'écran et aux moteurs) ---------- */
  document.querySelectorAll('.ticker-track').forEach(function (t) {
    Array.prototype.slice.call(t.children).forEach(function (c) {
      var k = c.cloneNode(true); k.setAttribute('aria-hidden', 'true'); t.appendChild(k);
    });
    t.classList.add('loop');
  });
  var reduce = false; // les animations restent actives même si Windows / iOS demande de les réduire

  /* ---------- suivi des contacts (actif seulement si Plausible est installé) ---------- */
  function track(name, props) {
    if (typeof window.plausible === 'function') window.plausible(name, props ? { props: props } : undefined);
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="tel:"], [data-track]');
    if (!a) return;
    if (a.getAttribute('href') && a.getAttribute('href').indexOf('tel:') === 0) track('Appel', { page: location.pathname });
    else track(a.getAttribute('data-track'), { page: location.pathname });
  });

  /* ---------- menu mobile ---------- */
  var burger = document.querySelector('[data-menu-btn]');
  var mnav = document.getElementById('mnav');
  if (burger && mnav) {
    var iconOpen = 'M4 7h16M4 12h16M4 17h16', iconClose = 'M6 6l12 12M18 6L6 18';
    function setMenu(open) {
      mnav.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.querySelector('path').setAttribute('d', open ? iconClose : iconOpen);
    }
    burger.addEventListener('click', function () { setMenu(!mnav.classList.contains('open')); });
    mnav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  }

  /* ---------- apparition au défilement ---------- */
  var revealEls = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window && revealEls.length) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); ro.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -12% 0px' });
    revealEls.forEach(function (el) { ro.observe(el); });
  } else revealEls.forEach(function (el) { el.classList.add('is-in'); });

  /* ---------- avant / après ---------- */
  document.querySelectorAll('.ba input[type=range]').forEach(function (r) {
    var box = r.closest('.ba');
    function u() { box.style.setProperty('--pos', r.value + '%'); }
    r.addEventListener('input', u); u();
  });
  var filters = document.querySelectorAll('[data-filter]');
  filters.forEach(function (b) {
    b.addEventListener('click', function () {
      var k = b.getAttribute('data-filter');
      filters.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      document.querySelectorAll('.ba-card[data-type]').forEach(function (c) { c.hidden = k !== 'all' && c.getAttribute('data-type') !== k; });
    });
  });

  /* ---------- questionnaire ITE ou ravalement ---------- */
  var quiz = document.querySelector('[data-quiz]');
  if (quiz) {
    var res = quiz.querySelector('[data-quiz-res]');
    quiz.addEventListener('change', function () {
      var v = {};
      ['froid', 'fissures', 'ancienne'].forEach(function (k) {
        var c = quiz.querySelector('input[name="' + k + '"]:checked'); v[k] = c ? c.value === 'oui' : null;
      });
      var done = v.froid !== null && v.fissures !== null && v.ancienne !== null;
      var r;
      if (!done) r = { cls: '', k: 'RÉSULTAT', t: 'Répondez aux 3 questions', x: 'La solution adaptée s’affichera ici.', cta: null };
      else if (v.froid || v.ancienne) r = { cls: 'ok', k: 'NOTRE CONSEIL', t: 'Isolation par l’extérieur', x: v.fissures ? 'Votre façade est isolée et entièrement refaite en une seule opération : les fissures sont traitées au passage.' : 'Votre maison gagne en confort et votre façade est refaite à neuf en une seule opération.', cta: ['/isolation-exterieure/', 'Découvrir l’isolation par l’extérieur →'] };
      else if (v.fissures) r = { cls: 'alt', k: 'NOTRE CONSEIL', t: 'Ravalement D3 armé', x: 'Votre maison n’a pas besoin d’isolation : un ravalement armé traite les fissures et redonne un aspect neuf à la façade.', cta: ['/ravalement-facade/', 'Découvrir le ravalement D3 armé →'] };
      else r = { cls: 'alt', k: 'NOTRE CONSEIL', t: 'Visite conseil', x: 'Un nettoyage ou une peinture de façade peut suffire. Le plus simple : une visite gratuite pour en juger sur place.', cta: ['/devis/', 'Demander une visite gratuite →'] };
      res.className = 'quiz-res ' + r.cls;
      res.querySelector('.k').textContent = r.k; res.querySelector('.t').textContent = r.t; res.querySelector('.x').textContent = r.x;
      var a = res.querySelector('a');
      if (r.cta) { a.hidden = false; a.href = r.cta[0]; a.textContent = r.cta[1]; } else a.hidden = true;
      if (done) track('Questionnaire', { resultat: r.t });
    });
  }

  /* ---------- formulaire de devis en 3 étapes ---------- */
  document.querySelectorAll('[data-wizard]').forEach(function (form) {
    var fss = Array.prototype.slice.call(form.querySelectorAll('.fs'));
    var i = 0;
    var bar = form.querySelector('[data-form-prog]'), num = form.querySelector('[data-form-num]'), name = form.querySelector('[data-form-name]');
    var err = form.querySelector('.form-err');
    form.noValidate = true;
    var ts = form.querySelector('input[name=ts]'); if (ts) ts.value = String(Date.now());
    var q = new URLSearchParams(location.search).get('projet');
    if (q) { var pre = form.querySelector('input[name=projet][value="' + q + '"]'); if (pre) pre.checked = true; }
    function show(k) {
      i = Math.max(0, Math.min(fss.length - 1, k));
      fss.forEach(function (f, n) { f.classList.toggle('cur', n === i); });
      if (bar) bar.style.width = Math.round((i + 1) / fss.length * 100) + '%';
      if (num) num.textContent = 'ÉTAPE ' + (i + 1) + ' / ' + fss.length;
      if (name) name.textContent = fss[i].getAttribute('data-name');
      if (err) err.classList.remove('show');
    }
    show(0);
    if (new URLSearchParams(location.search).get('erreur') && err) {
      show(fss.length - 1);
      err.textContent = 'Votre demande n’a pas pu être envoyée : merci de vérifier votre nom, votre téléphone et la case de consentement.';
      err.classList.add('show');
    }
    form.addEventListener('change', function (e) {
      if (e.target.name === 'projet' && i === 0) setTimeout(function () { show(1); }, 220);
    });
    form.querySelectorAll('[data-next]').forEach(function (b) { b.addEventListener('click', function () { show(i + 1); }); });
    form.querySelectorAll('[data-prev]').forEach(function (b) { b.addEventListener('click', function () { show(i - 1); }); });
    form.addEventListener('submit', function (e) {
      var missing = Array.prototype.slice.call(form.querySelectorAll('[required]')).filter(function (f) {
        return f.type === 'checkbox' ? !f.checked : !f.value.trim();
      });
      var files = form.querySelector('input[type=file]');
      var tooBig = files && files.files && Array.prototype.some.call(files.files, function (f) { return f.size > 8 * 1024 * 1024; });
      if (missing.length || tooBig) {
        e.preventDefault();
        show(fss.length - 1);
        if (err) { err.textContent = tooBig ? 'Une photo dépasse 8 Mo : choisissez une photo plus légère.' : 'Merci de renseigner votre nom, votre téléphone et d’accepter d’être recontacté.'; err.classList.add('show'); }
        if (missing[0]) missing[0].focus();
        return;
      }
      track('Demande de devis', { projet: (form.querySelector('input[name=projet]:checked') || {}).value || 'nc' });
    });
  });
})();
