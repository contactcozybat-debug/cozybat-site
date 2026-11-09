/* Cozybat — coupe 3D du système (chargée uniquement sur les pages qui l'affichent) */
(function () {
  'use strict';
  var reduce = false;
  /* ======================================================================
     COUPE 3D
     ====================================================================== */
  var TEINTE = '#F3EFE5';
  function mixWhite(hex, k) {
    var n = parseInt(hex.slice(1), 16);
    return '#' + [n >> 16, (n >> 8) & 255, n & 255].map(function (v) {
      v = Math.round(v + (255 - v) * k); return (v < 16 ? '0' : '') + v.toString(16);
    }).join('');
  }
  var BASE = [
    { id: 'support', name: 'Votre mur', detail: 'parpaing, brique, béton', t: 70, tex: 'parpaing', color: '#969792' },
    { id: 'colle', name: 'Colle', detail: 'en boudin et en plots', t: 5, tex: 'colle', color: 'transparent', noSides: true, leftAs: 2, inset: 34 },
    { id: 'isolant', name: 'Isolant PSE graphité', detail: '14 à 20 cm d’épaisseur', t: 52, tex: 'pse', color: '#5C5F63' },
    { id: 'fixation', name: 'Chevilles', detail: 'renfort de fixation', t: 1, tex: '', color: 'transparent', dowels: true },
    { id: 'sousenduit', name: 'Enduit de base', detail: 'protège l’isolant', t: 4, tex: 'sousenduit', color: '#A8AAA6' },
    { id: 'armature', name: 'Filet d’armature', detail: 'évite les fissures', t: 2, tex: 'treillis', color: 'transparent', mesh: true },
    { id: 'intermediaire', name: 'Sous-couche', detail: 'favorise l’accroche', t: 2, tex: 'impression', color: '#ECEAE2' },
    { id: 'regulateur', name: 'Régulateur de fond', detail: 'uniformise la couleur', t: 2, tex: 'regulateur', color: mixWhite(TEINTE, .35) },
    { id: 'finition', name: 'Enduit de finition', detail: 'aspect et couleur', t: 4, tex: 'talochee', color: TEINTE }
  ];
  function layersFor(sys) {
    var L = BASE.map(function (l) { return Object.assign({}, l); });
    if (sys === 'd3') {
      L = L.filter(function (l) { return ['colle', 'isolant', 'fixation'].indexOf(l.id) < 0; });
      L.forEach(function (l) {
        if (l.id === 'support') Object.assign(l, { name: 'Votre façade', detail: 'enduit ancien fissuré', tex: 'ancien', color: '#C4BCAC' });
        if (l.id === 'sousenduit') Object.assign(l, { name: 'Couche de base', detail: 'reçoit le filet', t: 6 });
        if (l.id === 'armature') l.detail = 'ponte les fissures';
      });
    }
    L.forEach(function (l, i) { l.num = '0' + i; });
    return L;
  }
  var DOWELS = [[8, 40], [8, 150], [8, 262], [98, 95], [98, 205], [188, 40], [188, 150], [188, 262]];
  var STEP = 30, W = 380;

  function Stack(host, opts) {
    this.host = host;
    this.o = Object.assign({ system: 'ite', applied: 99, explode: 36, rot: -32, tilt: -14, sel: null, callouts: true, accent: '#EDAA30', labelColor: '#FFFFFF' }, opts || {});
    this.build();
    this.render();
  }
  Stack.prototype.build = function () {
    var o = this.o, self = this;
    this.L = layersFor(o.system);
    this.built = o.system;
    this.host.innerHTML = '';
    var root = el('div', 'stk'); root.setAttribute('aria-hidden', 'true');
    var scale = el('div', 'stk-scale'); var scene = el('div', 'stk-scene');
    var floor = el('div', 'stk-floor'); scene.appendChild(floor);
    this.floor = floor; this.scene = scene; this.parts = [];
    this.L.forEach(function (l, i) {
      var b = el('div', 'stk-l');
      var li = l.leftAs != null ? l.leftAs : i; l.li = li;
      var ins = l.inset || 0;
      b.style.left = (li * STEP + ins) + 'px'; b.style.width = (W - li * STEP - ins) + 'px';
      var f = el('span', 'stk-f' + (l.tex ? ' tx tx-f-' + l.tex : ''));
      f.style.backgroundColor = l.color;
      if (l.dowels) DOWELS.forEach(function (d) { var s = el('span', 'stk-dw'); s.style.left = d[0] + 'px'; s.style.top = d[1] + 'px'; f.appendChild(s); });
      var side = el('span', 'stk-s'), top = el('span', 'stk-t'), lside = el('span', 'stk-s stk-ls');
      var t = Math.max(l.t, 1);
      side.style.width = t + 'px'; top.style.height = t + 'px'; lside.style.width = t + 'px';
      if (l.tex && !l.mesh && !l.noSides) { side.className += ' tx tx-s-' + l.tex; top.className += ' tx tx-t-' + l.tex; lside.className += ' tx tx-t-' + l.tex; side.style.backgroundColor = l.color; top.style.backgroundColor = l.color; lside.style.backgroundColor = l.color; }
      else if (l.mesh) { side.style.background = 'rgba(240,236,214,.7)'; top.style.background = 'rgba(240,236,214,.7)'; lside.style.background = 'rgba(240,236,214,.7)'; }
      if (!l.mesh && !l.dowels && !l.noSides) f.style.boxShadow = '-6px 0 14px rgba(0,0,0,.18)';
      b.appendChild(f); b.appendChild(side); b.appendChild(top); b.appendChild(lside); scene.appendChild(b);
      self.parts.push({ b: b, f: f, s: side, t: top, ls: lside });
    });
    scale.appendChild(scene); root.appendChild(scale);
    var over = el('div', 'stk-over'), oc = el('div', 'stk-o');
    this.labels = this.L.map(function (l) {
      var ln = el('div', 'stk-ln'), dot = el('div', 'stk-dot'), lb = el('div', 'stk-lb');
      lb.innerHTML = '<span class="tx2"><b></b><small></small></span><i></i>';
      lb.querySelector('b').textContent = l.name; lb.querySelector('small').textContent = l.detail; lb.querySelector('i').textContent = l.num;
      oc.appendChild(ln); oc.appendChild(dot); oc.appendChild(lb);
      return { ln: ln, dot: dot, lb: lb };
    });
    over.appendChild(oc); root.appendChild(over);
    this.over = over;
    this.host.appendChild(root);
  };
  Stack.prototype.set = function (p) {
    Object.assign(this.o, p);
    if (this.o.system !== this.built) this.build();
    this.render();
  };
  Stack.prototype.render = function () {
    var o = this.o, L = this.L, self = this;
    var applied = Math.min(o.applied, L.length);
    var cum = 0;
    var zs = L.map(function (l, i) { cum += l.t; return cum + i * o.explode; });
    var zC = zs[Math.max(1, applied) - 1];
    var sceneZ = -Math.round(zC / 2);
    this.scene.style.transform = 'rotateX(' + o.tilt + 'deg) rotateY(' + o.rot + 'deg) translateZ(' + sceneZ + 'px)';
    this.floor.style.height = (zC + 240) + 'px';
    this.floor.style.transform = 'translateZ(-120px) rotateX(90deg)';
    L.forEach(function (l, i) {
      var p = self.parts[i], shown = i < applied, on = o.sel === l.id;
      p.b.style.transform = 'translateZ(' + (shown ? zs[i] : zs[i] + 260) + 'px)';
      var op = shown ? 1 : 0;
      p.f.style.opacity = op; p.s.style.opacity = op; p.t.style.opacity = op; p.ls.style.opacity = op;
      p.f.style.outline = on && !l.dowels ? '2px solid ' + o.accent : '0 solid transparent';
    });
    this.over.style.display = o.callouts ? '' : 'none';
    if (!o.callouts) return;
    var D = 1700, CX = 80, CY = 30, ry = o.rot * Math.PI / 180, rx = o.tilt * Math.PI / 180;
    function proj(x, y, z) {
      var X = x - 190, Y = y - 160, Z = z + sceneZ;
      var X1 = X * Math.cos(ry) + Z * Math.sin(ry), Z1 = -X * Math.sin(ry) + Z * Math.cos(ry);
      var Y2 = Y * Math.cos(rx) - Z1 * Math.sin(rx), Z2 = Y * Math.sin(rx) + Z1 * Math.cos(rx);
      var s = D / (D - Z2); return [(CX + X1) * s, (CY + Y2) * s];
    }
    var LX = -235, gap = L.length > 6 ? 43 : 56, y0 = -((L.length - 1) * gap) / 2 + 4;
    L.forEach(function (l, i) {
      var lab = self.labels[i], shown = i < applied, on = o.sel === l.id;
      var last = i === L.length - 1;
      var a = proj(last ? i * STEP + 70 : (l.li != null ? l.li : i) * STEP + 15, 50 + i * 27, zs[i]);
      var ly = y0 + i * gap, dx = a[0] - LX, dy = a[1] - ly;
      lab.ln.style.left = LX + 'px'; lab.ln.style.top = ly + 'px';
      lab.ln.style.width = Math.round(Math.sqrt(dx * dx + dy * dy)) + 'px';
      lab.ln.style.transform = 'rotate(' + (Math.atan2(dy, dx) * 180 / Math.PI).toFixed(1) + 'deg)';
      lab.ln.style.background = o.accent;
      lab.dot.style.left = Math.round(a[0]) + 'px'; lab.dot.style.top = Math.round(a[1]) + 'px';
      lab.dot.style.background = o.accent; lab.dot.style.boxShadow = '0 0 0 3px rgba(237,170,48,.3)';
      lab.lb.style.left = LX + 'px'; lab.lb.style.top = ly + 'px'; lab.lb.style.color = o.labelColor;
      lab.lb.querySelector('b').style.fontWeight = on ? 800 : 600;
      var badge = lab.lb.querySelector('i');
      badge.style.border = '1px solid ' + o.accent; badge.style.background = on ? o.accent : 'transparent'; badge.style.color = on ? '#2E3A47' : o.accent;
      var op = shown ? 1 : 0; lab.ln.style.opacity = op; lab.dot.style.opacity = op; lab.lb.style.opacity = op;
    });
  };
  function el(tag, cls) { var e = document.createElement(tag); if (cls) e.className = cls; return e; }
  window.CozyStack = Stack;

  /* ---------- coupe du haut de page ---------- */
  var heroHost = document.querySelector('[data-stack="hero"]');
  if (heroHost) {
    var sys0 = heroHost.getAttribute('data-system') || 'ite';
    var hero = new Stack(heroHost, { system: sys0, applied: reduce ? 99 : 1, explode: reduce ? 48 : 0, rot: 18, tilt: -4, accent: '#EDAA30', labelColor: '#2E3A47' });
    var countEl = document.querySelector('[data-hero-count]');
    var iv;
    function play() {
      clearInterval(iv);
      var total = hero.L.length, n = 1;
      if (reduce) { hero.set({ applied: total, explode: 48 }); upd(total); return; }
      hero.set({ applied: 1, explode: 0 }); upd(1);
      iv = setInterval(function () {
        n++;
        if (n <= total) { hero.set({ applied: n }); upd(n); }
        else { clearInterval(iv); hero.set({ explode: 48 }); }
      }, 420);
    }
    function upd(n) { if (countEl) countEl.textContent = n <= 1 ? 'VOTRE MUR' : '0' + (n - 1) + ' / 0' + (hero.L.length - 1) + ' COUCHES'; }
    play();
    var heroSec = heroHost.closest('.hero');
    if (heroSec && !reduce) {
      heroSec.addEventListener('pointermove', function (e) {
        if (e.pointerType !== 'mouse') return;
        var r = heroSec.getBoundingClientRect();
        var mx = (e.clientX - r.left) / r.width - .5, my = (e.clientY - r.top) / r.height - .5;
        hero.set({ rot: Math.round(18 + mx * 14), tilt: Math.round(-4 - my * 6) });
      });
      heroSec.addEventListener('pointerleave', function () { hero.set({ rot: 18, tilt: -4 }); });
    }
    /* onglets ITE / ravalement de la page d'accueil */
    var tabs = document.querySelectorAll('[data-sys-tab]');
    tabs.forEach(function (t) {
      t.addEventListener('click', function () {
        var k = t.getAttribute('data-sys-tab');
        if (hero.o.system === k) return;
        tabs.forEach(function (x) { x.setAttribute('aria-pressed', x === t ? 'true' : 'false'); });
        document.querySelectorAll('[data-sys-copy]').forEach(function (c) { c.hidden = c.getAttribute('data-sys-copy') !== k; });
        hero.set({ system: k });
        play();
      });
    });
  }

  /* ---------- coupe au défilement (pages ITE et ravalement) ---------- */
  var storyHost = document.querySelector('[data-stack="story"]');
  if (storyHost) {
    var sysS = storyHost.getAttribute('data-system') || 'ite';
    var story = new Stack(storyHost, { system: sysS, applied: 1, explode: 26, rot: -20, tilt: -16, labelColor: '#FFFFFF' });
    var steps = Array.prototype.slice.call(document.querySelectorAll('.step'));
    var bar = document.querySelector('[data-story-prog]'), metaN = document.querySelector('[data-story-num]'), metaT = document.querySelector('[data-story-name]');
    var cur = -1;
    function activate(i) {
      if (i === cur) return; cur = i;
      steps.forEach(function (s, k) { s.classList.toggle('on', k === i); });
      story.set({ applied: i + 1, sel: story.L[i] ? story.L[i].id : null, rot: -20 - i * 3 });
      if (bar) bar.style.width = Math.round(i / (steps.length - 1) * 100) + '%';
      if (metaN) metaN.textContent = 'COUCHE ' + steps[i].getAttribute('data-num') + ' / 0' + (steps.length - 1);
      if (metaT) metaT.textContent = steps[i].getAttribute('data-name');
    }
    activate(0);
    if ('IntersectionObserver' in window) {
      var so = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) activate(steps.indexOf(en.target)); });
      }, { rootMargin: window.matchMedia('(max-width: 860px)').matches ? '-62% 0px -30% 0px' : '-45% 0px -45% 0px' });
      steps.forEach(function (s) { so.observe(s); });
    } else activate(steps.length - 1);
  }

})();
