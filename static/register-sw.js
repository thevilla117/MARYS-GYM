// Registrar el Service Worker en MAR'S GYM
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/service-worker.js')
      .then((registration) => {
        console.log('Service Worker registrado correctamente:', registration);

        // Verificar actualizaciones periódicamente
        setInterval(() => {
          registration.update();
        }, 60000); // Cada 60 segundos
      })
      .catch((error) => {
        console.error('Error al registrar Service Worker:', error);
      });

    // Manejar actualizaciones del Service Worker
    let refreshing;
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      if (refreshing) return;
      refreshing = true;
      window.location.reload();
    });
  });
} else {
  console.warn('Este navegador no soporta Service Workers');
}
