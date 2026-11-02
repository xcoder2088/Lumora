/* Lumora : service worker. Garde la page, les icônes, les polices, toutes les illustrations et tous les sons
   (liste dans precache.json, produite par tools/build_site.py) pour utiliser l'application sans réseau.
   Changer le numéro de version ci-dessous à chaque version ou révision pour que les appareils se mettent à jour. */
const VERSION = '5.19';
const CACHE = 'lumora-' + VERSION;
const COQUILLE = ['./', './index.html', './manifest.webmanifest?v=2', './favicon.ico?v=2', './icons/icon.svg?v=2', './icons/favicon-32.png?v=2', './icons/icon-192.png?v=2', './icons/icon-512.png?v=2', './icons/icon-maskable-512.png?v=2', './icons/apple-touch-icon.png?v=2'];

const FLAG = './__hors-ligne';   // présent seulement quand TOUT a été gardé

async function toutGarder() {
  const c = await caches.open(CACHE);
  if (await c.match(FLAG)) return true;
  let liste = [];
  try { liste = await (await fetch('./precache.json', { cache: 'reload' })).json(); } catch (e) { return false; }
  let ok = true;
  const file = liste.filter(u => !COQUILLE.includes(u));
  for (let i = 0; i < file.length; i += 6) {          // par petits lots : ne bloque pas l'écran
    await Promise.all(file.slice(i, i + 6).map(async u => {
      if (await c.match(u)) return;
      try { const r = await fetch(u); if (r.ok) await c.put(u, r); else ok = false; } catch (e) { ok = false; }
    }));
  }
  if (ok) await c.put(FLAG, new Response('ok'));
  return ok;
}
async function dire(ok) { for (const cl of await self.clients.matchAll()) cl.postMessage({ type: 'offline', ok }); }
self.addEventListener('message', e => { if (e.data === 'status') e.waitUntil(toutGarder().then(dire)); });

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(COQUILLE.map(url => new Request(url, { cache: 'reload' })))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('lumora-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()).then(() => toutGarder()).then(dire));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;                // polices, PayPal : jamais gardés ici
  if (req.mode === 'navigate') {                                  // la page : le réseau d'abord, la copie gardée si hors ligne
    e.respondWith(fetch(req).then(r => { const copie = r.clone(); caches.open(CACHE).then(c => c.put('./index.html', copie)); return r; })
      .catch(() => caches.match('./index.html')));
    return;
  }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => {
    if (r.ok && r.status === 200) { const copie = r.clone(); caches.open(CACHE).then(c => c.put(req, copie)); }
    return r;
  })));
});

