/* Lumora : service worker. Garde la page et les icônes pour ouvrir l'application sans réseau ;
   les sons et illustrations sont gardés au fur et à mesure qu'ils sont utilisés.
   Changer le numéro de version ci-dessous à chaque version ou révision pour que les appareils se mettent à jour. */
const VERSION = '5.13';
const CACHE = 'lumora-' + VERSION;
const COQUILLE = ['./', './index.html', './manifest.webmanifest?v=2', './favicon.ico?v=2', './icons/icon.svg?v=2', './icons/favicon-32.png?v=2', './icons/icon-192.png?v=2', './icons/icon-512.png?v=2', './icons/icon-maskable-512.png?v=2', './icons/apple-touch-icon.png?v=2'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(COQUILLE.map(url => new Request(url, { cache: 'reload' })))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('lumora-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
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

