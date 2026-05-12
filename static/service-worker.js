// service-worker.js - PWA offline support
const CACHE_NAME = 'apartman-v1';
const URLS_TO_CACHE = [
    '/',
    '/static/manifest.json',
];

// Instalacija
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(URLS_TO_CACHE))
    );
    self.skipWaiting();
});

// Aktivacija - obriši stare cache-ove
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(names => Promise.all(
            names.filter(n => n !== CACHE_NAME).map(n => caches.delete(n))
        ))
    );
    self.clients.claim();
});

// Network-first strategija (uvijek probaj s mreže prvo)
self.addEventListener('fetch', event => {
    if (event.request.method !== 'GET') return;
    if (event.request.url.includes('/admin/')) return;
    if (event.request.url.includes('/chatbot/')) return;
    if (event.request.url.includes('/api/')) return;

    event.respondWith(
        fetch(event.request)
            .then(response => {
                // Spremi u cache za offline
                if (response && response.status === 200) {
                    const klon = response.clone();
                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, klon);
                    });
                }
                return response;
            })
            .catch(() => {
                // Offline - vrati iz cache-a
                return caches.match(event.request).then(cached => {
                    return cached || caches.match('/');
                });
            })
    );
});
