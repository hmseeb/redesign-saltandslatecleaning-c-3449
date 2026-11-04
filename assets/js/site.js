/* Salt & Slate Cleaning Company — site behaviour
   Progressive enhancement only: every feature degrades to working HTML. */
(function () {
  'use strict';

  /* ---------------------------------------------------- mobile drawer */
  var drawer = document.getElementById('drawer');
  var burger = document.querySelector('.burger');
  var closeBtn = document.querySelector('.drawer-close');

  function setDrawer(open) {
    if (!drawer || !burger) return;
    drawer.setAttribute('data-open', open ? 'true' : 'false');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.documentElement.style.overflow = open ? 'hidden' : '';
    if (open) {
      var first = drawer.querySelector('.drawer-close');
      if (first) first.focus();
    } else {
      burger.focus();
    }
  }

  if (burger) burger.addEventListener('click', function () {
    setDrawer(drawer.getAttribute('data-open') !== 'true');
  });
  if (closeBtn) closeBtn.addEventListener('click', function () { setDrawer(false); });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (drawer && drawer.getAttribute('data-open') === 'true') setDrawer(false);
    closeAllSubmenus();
  });

  /* close drawer when a link inside is followed */
  if (drawer) {
    drawer.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (a && a.getAttribute('href')) setDrawer(false);
    });
  }

  /* --------------------------------------------- drawer accordions */
  Array.prototype.forEach.call(document.querySelectorAll('.drawer-group > button'), function (btn) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', open ? 'false' : 'true');
    });
  });

  /* ------------------------------------------------- desktop submenus */
  var navToggles = Array.prototype.slice.call(document.querySelectorAll('.nav-toggle'));

  function closeAllSubmenus(except) {
    navToggles.forEach(function (t) {
      if (t !== except) t.setAttribute('aria-expanded', 'false');
    });
  }

  navToggles.forEach(function (t) {
    t.addEventListener('click', function (e) {
      e.preventDefault();
      var open = t.getAttribute('aria-expanded') === 'true';
      closeAllSubmenus(t);
      t.setAttribute('aria-expanded', open ? 'false' : 'true');
    });
  });

  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-list')) closeAllSubmenus();
  });

  /* mark current nav item */
  var here = window.location.pathname.replace(/\/+$/, '') || '/';
  Array.prototype.forEach.call(document.querySelectorAll('.nav-link[href^="/"]'), function (a) {
    var href = a.getAttribute('href').replace(/\/+$/, '') || '/';
    if (href !== '/' && (here === href || here.indexOf(href + '/') === 0)) {
      a.setAttribute('aria-current', 'page');
    }
  });

  /* ---------------------------------------------- header scroll shadow */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () {
      header.style.boxShadow = window.scrollY > 8 ? '0 1px 16px rgba(27,32,38,.09)' : 'none';
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ------------------------------------------ before / after sliders */
  Array.prototype.forEach.call(document.querySelectorAll('.ba'), function (ba) {
    var input = ba.querySelector('input[type=range]');
    if (!input) return;
    var paint = function () { ba.style.setProperty('--pos', input.value + '%'); };
    input.addEventListener('input', paint);
    input.addEventListener('change', paint);
    paint();
  });

  /* ----------------------------------------------------------- forms */
  var ACTION = 'https://vision.leadrai.com/api/forms/8e89c62d8b1083f389e7b97ba98bc588';
  var forms = Array.prototype.slice.call(document.querySelectorAll('form[data-leadr]'));

  /* stamp the current page url into every _page field on load */
  Array.prototype.forEach.call(document.querySelectorAll('input[name="_page"]'), function (i) {
    i.value = window.location.href;
  });

  function showConfirmation(scope) {
    var ok = scope ? scope.querySelector('.form-ok') : document.querySelector('.form-ok');
    if (!ok) return;
    ok.setAttribute('data-show', 'true');
    ok.setAttribute('tabindex', '-1');
    try { ok.focus({ preventScroll: true }); } catch (err) { /* older browsers */ }
    ok.scrollIntoView({ block: 'center', behavior: 'smooth' });
  }

  /* plain-HTML return path: ?submitted=1 */
  try {
    if (new URLSearchParams(window.location.search).get('submitted') === '1') {
      var target = document.querySelector('.form-ok');
      if (target) {
        var card = target.closest('.form-card') || document;
        var f = card.querySelector ? card.querySelector('form[data-leadr]') : null;
        if (f) f.reset();
        showConfirmation(card === document ? null : card);
      }
    }
  } catch (err) { /* URLSearchParams unsupported: plain submit still worked */ }

  forms.forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (!window.fetch || !window.FormData) return; /* fall back to plain POST */
      e.preventDefault();

      var card = form.closest('.form-card') || form.parentNode;
      var submit = form.querySelector('button[type=submit]');
      var original = submit ? submit.textContent : '';
      if (submit) { submit.disabled = true; submit.textContent = 'Sending…'; }

      var fd = new FormData(form);
      var body = {};
      fd.forEach(function (value, key) { body[key] = value; });
      body._page = window.location.href;

      fetch(ACTION, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(body)
      })
        .then(function (res) { return res.json().catch(function () { return { ok: res.ok }; }); })
        .then(function (data) {
          if (data && data.ok === false) throw new Error('rejected');
          form.reset();
          Array.prototype.forEach.call(form.querySelectorAll('input[name="_page"]'), function (i) {
            i.value = window.location.href;
          });
          showConfirmation(card);
        })
        .catch(function () {
          /* network/JS failure: hand the browser a real POST so nothing is lost */
          form.removeAttribute('data-leadr');
          form.submit();
        })
        .then(function () {
          if (submit) { submit.disabled = false; submit.textContent = original; }
        });
    });
  });
})();
