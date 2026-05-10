// MAR'S GYM Service Worker
// Versión 1.0 - Cache-first strategy con network fallback

const CACHE_NAME = 'marys-gym-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/static/manifest.json',
  '/static/icon-192.png',
  '/static/icon-256.png',
  '/static/icon-384.png',
  '/static/icon-512.png',
  '/static/icon-maskable-192.png',
  '/static/icon-maskable-512.png'
];

// Instalar el Service Worker y hacer cache de los assets
self.addEventListener('install', (event) => {
  console.log('Service Worker: Instalando...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('Service Worker: Cacheando assets');
      return cache.addAll(ASSETS_TO_CACHE);
    }).catch((error) => {
      console.log('Service Worker: Error al cachear', error);
    })
  );
  self.skipWaiting();
});

// Activar el Service Worker y limpiar caches antiguos
self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activando...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('Service Worker: Eliminando cache antiguo:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Manejar las solicitudes - Strategy: Network first, fallback to cache
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Para solicitudes GET
  if (request.method === 'GET') {
    // Para APIs (solicitudes fetch)
    if (url.pathname.startsWith('/api/') || url.pathname.includes('_stcore')) {
      event.respondWith(
        fetch(request)
          .then((response) => {
            // Cachear respuestas exitosas
            if (response.status === 200) {
              const cache = caches.open(CACHE_NAME);
              cache.then((c) => c.put(request, response.clone()));
            }
            return response;
          })
          .catch(() => {
            // Si falla la red, usar cache
            return caches.match(request).then((response) => {
              return response || new Response('Offline - Contenido no disponible', {
                status: 503,
                statusText: 'Service Unavailable'
              });
            });
          })
      );
    } else {
      // Para archivos estáticos, usar cache-first
      event.respondWith(
        caches.match(request).then((response) => {
          return response || fetch(request).then((fetchResponse) => {
            // Cachear respuestas exitosas
            if (fetchResponse.status === 200) {
              const cache = caches.open(CACHE_NAME);
              cache.then((c) => c.put(request, fetchResponse.clone()));
            }
            return fetchResponse;
          }).catch(() => {
            // Respuesta fallback
            return new Response('Offline - Contenido no disponible', {
              status: 503,
              statusText: 'Service Unavailable'
            });
          });
        })
      );
    }
  }
});

// Manejar mensajes desde el cliente
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

console.log('Service Worker cargado correctamente');
