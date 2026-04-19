const CACHE='paris-food-v1';
const PRECACHE=[
  './paris-food-map.html',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
  'https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css',
  'https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css',
  'https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js',
];

self.addEventListener('install',e=>{
  e.waitUntil(
    caches.open(CACHE).then(c=>c.addAll(PRECACHE)).then(()=>self.skipWaiting())
  );
});

self.addEventListener('activate',e=>{
  e.waitUntil(
    caches.keys()
      .then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k))))
      .then(()=>self.clients.claim())
  );
});

self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  e.respondWith(
    caches.match(e.request).then(cached=>{
      if(cached)return cached;
      return fetch(e.request).then(res=>{
        if(!res||res.status!==200||res.type==='opaque')return res;
        const clone=res.clone();
        caches.open(CACHE).then(c=>c.put(e.request,clone));
        return res;
      });
    }).catch(()=>caches.match('./paris-food-map.html'))
  );
});
