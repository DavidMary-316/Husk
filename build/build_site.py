# Builds the website folder (site/) from husk.html. Icons and og-image.png are pre-made and not regenerated. Run after build_standalone.py.
import re, os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL='https://husk.fragmentsofsilent.workers.dev'
SRC=os.path.join(ROOT,'husk.html'); OUT=os.path.join(ROOT,'site')
os.makedirs(OUT, exist_ok=True)
s=open(SRC,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1,(s.count(old),old[:60]); s=s.replace(old,new)
CSP_SITE="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src 'self' blob: data:; media-src blob:; connect-src 'none'; object-src 'none'; frame-src 'none'; worker-src 'self'; manifest-src 'self'; form-action 'none'; base-uri 'none'"
s=re.sub(r'<meta http-equiv="Content-Security-Policy" content="[^"]*">', '<meta http-equiv="Content-Security-Policy" content="%s">'%CSP_SITE, s, count=1)
s=re.sub(r'<link rel="icon" href="data:[^"]*">', '''<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#f5f6f8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b0f14" media="(prefers-color-scheme: dark)">
<meta name="description" content="Husk removes hidden location, device and time data from your photos and videos. Free, no ads, and it runs entirely on your device.">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Husk">
<link rel="canonical" href="%(u)s/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Husk">
<meta property="og:title" content="Husk: remove hidden data from your photos and videos">
<meta property="og:description" content="Free, no ads, and it runs on your device. Removes hidden location, phone and time data before you post.">
<meta property="og:url" content="%(u)s/">
<meta property="og:image" content="%(u)s/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Husk: remove hidden data from your photos and videos">
<meta name="twitter:description" content="Free, no ads, and it runs on your device.">
<meta name="twitter:image" content="%(u)s/og-image.png">''' % {'u': SITE_URL}, s, count=1)
import hashlib
SHA = hashlib.sha256(open(SRC,'rb').read()).hexdigest()
rep('<li>Social apps often strip metadata', '<li>Offline copy checksum (SHA-256): <code>%s</code>. After downloading <code>husk.html</code> you can check that your copy matches: on Windows run <code>certutil -hashfile husk.html SHA256</code>, on Mac or Linux run <code>shasum -a 256 husk.html</code>. This catches a damaged download, and the same number is the one to compare if a copy ever comes from somewhere else.</li>\n        <li>Social apps often strip metadata' % SHA)
rep('</style>', """.get { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px 20px; border: 1px solid var(--line-strong); border-radius: 14px; padding: 16px 18px; }
.get p { margin: 2px 0 0; font-size: 0.86rem; color: var(--muted); }
.get b { font-size: 0.95rem; }
.get .getbtns { display: flex; flex-wrap: wrap; gap: 8px; }
.get a.btn { text-decoration: none; }
.know code { font: 0.8rem/1.5 var(--font-mono); overflow-wrap: anywhere; word-break: break-all; }
</style>""")
rep('<aside class="support" id="support" hidden>', """<aside class="get" id="get">
    <div><b>Take Husk with you</b><p>Install it like an app, or download one file that works with no internet.</p><p id="iosHint" hidden>On iPhone or iPad: tap the Share button, then &ldquo;Add to Home Screen&rdquo;.</p></div>
    <div class="getbtns"><button type="button" class="btn" id="installBtn" hidden>Install app</button><a class="btn ghost" id="dlLink" href="husk.html" download="husk.html">Download offline copy</a></div>
  </aside>

  <aside class="support" id="support" hidden>""")
rep('</body>','<script>\n/* Install button and offline download. Hidden when they do not apply. */\n(function () {\n  var card = document.getElementById("get"), btn = document.getElementById("installBtn"), dl = document.getElementById("dlLink"), hint = document.getElementById("iosHint");\n  var ev = null;\n  var installed = (window.matchMedia && matchMedia("(display-mode: standalone)").matches) || navigator.standalone === true;\n  if (installed) { card.hidden = true; return; }\n  var ios = /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);\n  if (ios) { hint.hidden = false; dl.hidden = true; }\n  window.addEventListener("beforeinstallprompt", function (e) { e.preventDefault(); ev = e; btn.hidden = false; });\n  btn.addEventListener("click", function () { if (!ev) return; ev.prompt(); ev.userChoice.then(function () { ev = null; btn.hidden = true; }, function () {}); });\n  window.addEventListener("appinstalled", function () { card.hidden = true; });\n})();\n</script>\n</body>')
rep('</body>','''<script>
/* Lets the page be installed and work offline. Only runs on https (or localhost). */
if ('serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === 'localhost')) {
  navigator.serviceWorker.register('sw.js').catch(function () {});
}
</script>
</body>''')
open(OUT+'/index.html','w',encoding='utf-8').write(s)
import shutil; shutil.copyfile(SRC, OUT+'/husk.html')

open(OUT+'/sw.js','w').write('''/* Husk service worker: keeps a copy of the page so it opens offline. Network first, so updates show up as soon as you are online. */
var V = 'husk-v2';
var FILES = ['./', 'index.html', 'favicon.svg', 'icon-192.png', 'icon-512.png', 'manifest.webmanifest', 'husk.html'];
self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(V).then(function (c) { return c.addAll(FILES); }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (ks) {
    return Promise.all(ks.filter(function (k) { return k !== V; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener('fetch', function (e) {
  var r = e.request;
  if (r.method !== 'GET') return;
  var u = new URL(r.url);
  if (u.origin !== self.location.origin) return;
  e.respondWith(
    fetch(r).then(function (res) {
      if (res.ok) { var copy = res.clone(); caches.open(V).then(function (c) { c.put(r, copy); }); }
      return res;
    }).catch(function () {
      return caches.match(r).then(function (hit) { return hit || caches.match('index.html'); });
    })
  );
});
''')
json.dump({"name":"Husk","short_name":"Husk","description":"Remove hidden location, device and time data from photos and videos. Free and private.","start_url":"./","scope":"./","display":"standalone","background_color":"#f5f6f8","theme_color":"#0e7a5a","icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},{"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"},{"src":"icon-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]}, open(OUT+'/manifest.webmanifest','w'), indent=2)
open(OUT+'/favicon.svg','w').write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path d="M20 4H38L60 26V44C60 53.4 53.4 60 44 60H20C10.6 60 4 53.4 4 44V20C4 10.6 10.6 4 20 4Z" fill="#0E7A5A"/><path d="M38 4V18C38 22.4 41.6 26 46 26H60Z" fill="#7FD9B6"/><circle cx="22" cy="26" r="5" fill="#fff"/><path d="M12 50L26 33L35 43L41 37L52 50Z" fill="#fff"/></svg>
''')
open(OUT+'/robots.txt','w').write('User-agent: *\nAllow: /\n')
csp_hdr=CSP_SITE.replace("connect-src 'none'","connect-src 'self'")+"; frame-ancestors 'none'"
open(OUT+'/_headers','w').write('''# Real HTTP security headers (Cloudflare Pages and Netlify read this file).
/*
  Content-Security-Policy: %s
  X-Content-Type-Options: nosniff
  Referrer-Policy: no-referrer
  X-Frame-Options: DENY
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()
  Cross-Origin-Opener-Policy: same-origin
  Strict-Transport-Security: max-age=31536000

/sw.js
  Cache-Control: no-cache

/index.html
  Cache-Control: no-cache
''' % csp_hdr)
print('built', os.listdir(OUT))
