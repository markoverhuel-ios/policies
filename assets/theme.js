// Light/dark toggle, shared by freshcoastrf.com and apps.freshcoastrf.com (same file on both).
// Runs in <head> so the saved choice applies before the page draws. The choice is kept in a cookie
// on .freshcoastrf.com so it follows the visitor between the two sites; localStorage is the fallback.
(function () {
  var root = document.documentElement;
  var shared = /(^|\.)freshcoastrf\.com$/.test(location.hostname);

  function read() {
    var m = document.cookie.match(/(?:^|; )theme=(dark|light)/);
    if (m) return m[1];
    try { var v = localStorage.getItem('theme'); if (v === 'dark' || v === 'light') return v; } catch (e) {}
    return null;
  }
  function save(v) {
    document.cookie = 'theme=' + v + '; path=/; max-age=31536000; SameSite=Lax' +
      (shared ? '; domain=.freshcoastrf.com; Secure' : '');
    try { localStorage.setItem('theme', v); } catch (e) {}
  }

  var saved = read();
  if (saved) root.setAttribute('data-theme', saved);

  function current() {
    var t = root.getAttribute('data-theme');
    if (t) return t;
    return window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.getElementById('theme-toggle');
    if (!btn) return;
    function label() {
      var dark = current() === 'dark';
      btn.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
      btn.setAttribute('aria-pressed', dark ? 'true' : 'false');
    }
    label();
    btn.addEventListener('click', function () {
      var next = current() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      save(next);
      label();
    });
  });
})();
