/* sbrfc.com shared script, loaded with "defer" on every page.
   1. Mobile menu
   2. Google Analytics events (contact clicks, club sites, Stingrays
      registration, thank-you pages). Every call fails silently if the
      Google tag is missing or blocked.
   3. Sign-up forms: fills the hidden ad-tracking fields and routes the
      /play form to the right club's form.
   4. Dated items: anything with data-until="YYYY-MM-DD" hides itself
      the day after that date (the youth Upcoming box uses this).
   The IDs for Google Analytics and Google Ads live in build.py, not here. */
(function () {
  'use strict';
  var doc = document;
  var each = function (list, fn) { Array.prototype.forEach.call(list, fn); };

  /* ---------- 1. Mobile menu ---------- */
  var toggle = doc.querySelector('.nav-toggle');
  var nav = doc.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.textContent = open ? 'Close' : 'Menu';
    });
  }

  /* ---------- 2. Analytics ---------- */
  function track(name, params) {
    try {
      if (typeof window.gtag === 'function') { window.gtag('event', name, params || {}); }
    } catch (e) { /* never break the page for analytics */ }
  }
  var page = (location.pathname || '/').replace(/\.html$/, '').replace(/\/index$/, '/') || '/';

  // Thank-you pages say what to send: <body data-track="player_signup" data-team="mens">
  var body = doc.body;
  if (body && body.getAttribute('data-track')) {
    var evParams = {};
    if (body.getAttribute('data-team')) { evParams.team = body.getAttribute('data-team'); }
    track(body.getAttribute('data-track'), evParams);
  }

  var CLUBS = { 'grunionrugby.com': 'grunion', 'sbwomensrugby.com': 'mermaids', 'stingraysrfc.com': 'stingrays' };
  doc.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) { return; }
    var href = a.getAttribute('href') || '';
    var scheme = href.match(/^\s*(tel|sms|mailto):/i);
    if (scheme) {
      track('contact_click', { method: scheme[1].toLowerCase(), page: page });
      return;
    }
    var host = (a.hostname || '').toLowerCase().replace(/^www\./, '');
    if (host === 'rugby-register.vercel.app') {
      track('youth_register_click', { page: page, transport_type: 'beacon' });
      return;
    }
    if (CLUBS[host]) {
      track('club_site_click', { club: CLUBS[host], page: page, transport_type: 'beacon' });
      // Google Ads conversion that /landing used to fire on clicks through to a club site.
      if (window.sbrfcClubConversion) {
        track('conversion', { send_to: window.sbrfcClubConversion, transport_type: 'beacon' });
      }
    }
  }, true);

  /* ---------- 3. Sign-up forms ---------- */
  var query = null;
  try { query = new URLSearchParams(location.search); } catch (e) { query = null; }
  var store = null, session = null;
  try { store = window.localStorage; store.setItem('sbrfcT', '1'); store.removeItem('sbrfcT'); } catch (e) { store = null; }
  try { session = window.sessionStorage; session.setItem('sbrfcT', '1'); session.removeItem('sbrfcT'); } catch (e) { session = null; }

  // Ad and campaign details: from the URL when present, otherwise from an
  // ad visit in the last 30 days (a later ad visit replaces an earlier one).
  var KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'gclid'];
  var attrib = null;
  if (query) {
    var found = {}, tagged = false;
    KEYS.forEach(function (k) {
      var v = query.get(k);
      if (v) { found[k] = v.slice(0, 200); tagged = true; }
    });
    if (tagged) {
      attrib = { v: found, landing: page, t: new Date().getTime() };
      try { if (store) { store.setItem('sbrfcAttrib', JSON.stringify(attrib)); } } catch (e) {}
    }
  }
  if (!attrib) {
    try {
      var saved = store ? JSON.parse(store.getItem('sbrfcAttrib') || 'null') : null;
      if (saved && saved.v && saved.t && (new Date().getTime() - saved.t) < 30 * 864e5) { attrib = saved; }
    } catch (e) {}
  }
  // Landing page: the page an ad brought them to, else the first page of this visit.
  var landing = attrib && attrib.landing ? attrib.landing : null;
  if (!landing) {
    try {
      if (session) {
        landing = session.getItem('sbrfcLanding');
        if (!landing) { session.setItem('sbrfcLanding', page); landing = page; }
      }
    } catch (e) {}
  }
  landing = landing || page;

  each(doc.querySelectorAll('form.lp-form'), function (f) {
    KEYS.forEach(function (k) {
      var el = f.querySelector('input[name="' + k + '"]');
      if (el && attrib && attrib.v && attrib.v[k]) { el.value = attrib.v[k]; }
    });
    var lp = f.querySelector('input[name="landing_page"]');
    if (lp) { lp.value = landing; }
  });

  // /play: the "Which team?" choice decides which club's form receives the
  // sign-up and which thank-you page follows. With scripting off, the form
  // stays as the general form and lands on /thanks-play.
  var ROUTES = {
    mens: ['mens-interest', '/thanks-mens'],
    womens: ['womens-interest', '/thanks-womens'],
    youth: ['youth-interest', '/thanks-youth'],
    general: ['general-interest', '/thanks-play']
  };
  var routed = doc.querySelector('form[data-route]');
  if (routed) {
    var teamSel = routed.querySelector('select[name="team"]');
    var ageWrap = routed.querySelector('[data-youth-only]');
    var ageSel = routed.querySelector('[name="child_age"]');
    var nameLabel = routed.querySelector('[data-label-name]');
    var expLabel = routed.querySelector('[data-label-experience]');
    var applyRoute = function () {
      var team = teamSel ? teamSel.value : '';
      var route = ROUTES[team] || ROUTES.general;
      routed.setAttribute('action', route[1]);
      each(routed.querySelectorAll('input[name="form-name"]'), function (i) { i.value = route[0]; });
      var youth = team === 'youth';
      if (ageWrap) { ageWrap.hidden = !youth; }
      if (ageSel) { ageSel.required = youth; if (!youth) { ageSel.value = ''; } }
      if (nameLabel) { nameLabel.textContent = youth ? 'Parent/guardian name' : 'Your name'; }
      if (expLabel) { expLabel.textContent = youth ? 'Has your child played before?' : 'Have you played rugby?'; }
    };
    if (teamSel) {
      var want = query ? query.get('team') : null;
      if (want && ROUTES[want] && want !== 'general') { teamSel.value = want; }
      teamSel.addEventListener('change', applyRoute);
    }
    routed.addEventListener('submit', applyRoute);
    applyRoute();
  }

  // ?team=mens|womens|youth|new (ad sitelinks, old /landing links): scroll to
  // that team's card or the beginner questions and highlight it briefly.
  if (query && query.get('team')) {
    var target = doc.getElementById(query.get('team'));
    if (target && target.closest('main')) {
      setTimeout(function () {
        try { target.scrollIntoView({ behavior: 'smooth', block: 'start' }); } catch (e) { target.scrollIntoView(); }
        target.classList.add('is-target');
        setTimeout(function () { target.classList.remove('is-target'); }, 3000);
      }, 150);
    }
  }

  /* ---------- 4. Dated items ---------- */
  var d = new Date();
  var today = d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
  each(doc.querySelectorAll('[data-until]'), function (el) {
    if (today > el.getAttribute('data-until')) { el.hidden = true; }
  });
  each(doc.querySelectorAll('[data-upcoming]'), function (box) {
    var left = box.querySelectorAll('li:not([hidden])').length;
    var empty = box.querySelector('[data-upcoming-empty]');
    if (!left && empty) { empty.hidden = false; }
  });
})();
