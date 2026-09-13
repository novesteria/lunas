/* Lunas site: mobile nav, recently verified list, docs nav highlight. */
(function () {
  var nav = document.querySelector('.nav');
  var tg = document.querySelector('.nav-toggle');
  if (nav && tg) tg.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    tg.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function badge(p) {
    var stale = p.state === 'stale';
    var cls = stale ? 'badge stale' : (p.engine === 'core' ? 'badge core' : 'badge');
    var right = stale ? 'Verified <em>· ' + esc(p.commits_since) + ' commits ago</em>' : 'Verified <em>· ' + (p.engine === 'core' ? 'Core' : 'Full') + '</em>';
    return '<span class="' + cls + '"><span class="a"><svg width="12" height="12" viewBox="0 0 100 100" aria-hidden="true"><g transform="translate(50 50) rotate(200) translate(-50 -50)"><path d="M68.99 12.54 A42 42 0 1 0 68.99 87.46 A50 50 0 0 1 68.99 12.54 Z" fill="currentColor"/></g></svg>Lunas</span><span class="b">' + right + '</span></span>';
  }
  function meta(p) {
    if (p.state === 'stale') return 'Stale · last pass ' + esc(p.commit || '') + ' · ' + esc(p.commits_since) + ' commits since';
    var parts = [esc(p.passed) + ' of ' + esc(p.total), esc(p.commit || 'upload'), esc(p.when || '')];
    if (p.built_by) parts.push('built by ' + esc(p.built_by));
    return parts.join(' · ');
  }
  /* Recently verified: the page ships with examples; real data replaces them when the API answers. */
  var lists = document.querySelectorAll('[data-verified]');
  if (lists.length && window.fetch) {
    var limit = 0; lists.forEach(function (l) { limit = Math.max(limit, +l.getAttribute('data-verified') || 3); });
    fetch('/api/public/verified?limit=' + limit, { credentials: 'omit' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
      if (!d || !d.projects || !d.projects.length) return;
      lists.forEach(function (l) {
        var n = +l.getAttribute('data-verified') || 3, kind = l.getAttribute('data-kind') || 'recent';
        var html = d.projects.slice(0, n).map(function (p) {
          if (kind === 'vcard') return '<a class="vcard" href="' + esc(p.page_url) + '">' + badge(p) + '<b>' + esc(p.name) + '</b><span>' + meta(p) + '</span><span class="go">' + esc(p.page_url.replace(/^https?:\/\//, '')) + ' →</span></a>';
          return '<a href="' + esc(p.page_url) + '">' + badge(p) + '<b>' + esc(p.name) + '</b><span>' + meta(p) + '</span></a>';
        }).join('');
        var keep = l.querySelector('.vcard.empty');
        l.innerHTML = html + (keep ? keep.outerHTML : '');
      });
    }).catch(function () {});
  }
  /* Verification pages search: filter what is on the page, then ask the API. */
  var q = document.querySelector('#vq');
  if (q) {
    var t; q.addEventListener('input', function () {
      var v = q.value.trim().toLowerCase();
      document.querySelectorAll('[data-verified] .vcard:not(.empty)').forEach(function (c) { c.hidden = !!v && c.textContent.toLowerCase().indexOf(v) < 0; });
      clearTimeout(t);
      if (v.length < 2 || !window.fetch) return;
      t = setTimeout(function () {
        fetch('/api/public/verified?q=' + encodeURIComponent(v) + '&limit=12', { credentials: 'omit' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
          if (!d || !d.projects) return;
          var l = document.querySelector('[data-verified]'); if (!l) return;
          l.innerHTML = d.projects.map(function (p) { return '<a class="vcard" href="' + esc(p.page_url) + '">' + badge(p) + '<b>' + esc(p.name) + '</b><span>' + meta(p) + '</span><span class="go">' + esc(p.page_url.replace(/^https?:\/\//, '')) + ' →</span></a>'; }).join('') || '<div class="vcard empty"><b>Nothing with that name</b><span>Only projects whose owner turned the public page on are listed.</span></div>';
        }).catch(function () {});
      }, 250);
    });
  }
  /* Docs: highlight the section in view. */
  var links = document.querySelectorAll('.docs-nav a[href^="#"]');
  if (links.length && 'IntersectionObserver' in window) {
    var map = {}; links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { links.forEach(function (a) { a.classList.remove('on'); }); if (map[e.target.id]) map[e.target.id].classList.add('on'); } });
    }, { rootMargin: '-10% 0px -80% 0px' });
    document.querySelectorAll('.doc[id]').forEach(function (s) { io.observe(s); });
  }
})();
