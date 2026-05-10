// ════════════════════════════════════════
// MARY'S GYM — Service Worker
// Estrategia: Cache-First para app shell,
//             Network-First para Supabase API
// ════════════════════════════════════════

const CACHE = 'marysgym-v2';

const SHELL = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
];

// ── INSTALL: Pre-cache app shell ──
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

// ── ACTIVATE: Clean old caches ──
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// ── FETCH: Smart routing ──
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // Supabase API → Network-First (offline returns empty array)
  if (url.hostname.includes('supabase.co')) {
    e.respondWith(
      fetch(e.request.clone()).catch(() =>
        new Response(JSON.stringify([]), { headers: { 'Content-Type': 'application/json' } })
      )
    );
    return;
  }

  // Google Fonts / CDN → Cache-First
  if (url.hostname.includes('fonts.') || url.hostname.includes('cdnjs.cloudflare.com')) {
    e.respondWith(
      caches.match(e.request).then(cached => {
        if (cached) return cached;
        return fetch(e.request).then(res => {
          if (res.ok) {
            const clone = res.clone();
            caches.open(CACHE).then(c => c.put(e.request, clone));
          }
          return res;
        });
      })
    );
    return;
  }

  // App Shell → Cache-First, fallback to index.html
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(res => {
        if (res.ok && e.request.method === 'GET') {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      }).catch(() => {
        // Navigation fallback → serve index.html
        if (e.request.mode === 'navigate') {
          return caches.match('./index.html');
        }
      });
    })
  );
});
