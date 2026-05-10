# Guía para generar el APK de MARY'S GYM

## ✅ Lo que YA está hecho

He configurado tu app para que sea una PWA instalable. Los archivos preparados son:

- `app.py` — actualizado con meta tags PWA y enlace al manifest
- `.streamlit/config.toml` — configurado para servir archivos estáticos
- `static/manifest.json` — manifest PWA con tu URL pública
- `static/icon-192.png` ... `static/icon-512.png` — íconos en distintos tamaños generados desde tu Logo GYM
- `static/icon-maskable-192.png` y `static/icon-maskable-512.png` — íconos para Android (con padding)

## 📤 PASO 1: Subir los cambios a GitHub

Streamlit Cloud usa tu repositorio de GitHub. Para que los cambios se vean en tu URL pública necesitas:

1. Abre la carpeta `MARY'S GYM` en GitHub Desktop o con `git` en la terminal
2. Haz commit de TODOS los archivos nuevos (la carpeta `static/`, `.streamlit/config.toml`, y el `app.py` actualizado)
3. Push al repositorio
4. Streamlit Cloud detectará los cambios y redesplegará automáticamente (toma ~1-2 minutos)

Si nunca has usado git: descarga **GitHub Desktop**, abre tu carpeta del proyecto, vas a ver todos los cambios listados, le das **Commit to main** y luego **Push origin**.

## ✔️ PASO 2: Verificar que funcione la PWA

1. Espera 1-2 minutos a que Streamlit Cloud termine de redesplegar
2. Abre desde tu celular: https://marys-gym-lbjrnkbifnax46gxclzm8u.streamlit.app/
3. En **Chrome** debería aparecer un mensaje "Instalar app" o ícono de instalación en la barra de direcciones
4. También puedes ir a **Menú (3 puntos) → "Instalar aplicación"** o **"Agregar a pantalla de inicio"**
5. Si funciona ahí, el APK también funcionará

Si NO aparece la opción de instalar, puede que necesite refrescar (Ctrl+F5 o limpiar caché). Espera a que el redespliegue de Streamlit termine.

## 📱 PASO 3: Generar el APK con PWABuilder

1. Abre desde un computador: **https://www.pwabuilder.com/**
2. En la caja de texto pega tu URL: `https://marys-gym-lbjrnkbifnax46gxclzm8u.streamlit.app/`
3. Click en **"Start"**
4. PWABuilder analizará tu app y te dará una puntuación. Si todo está bien, verás luces verdes en "Manifest" e "Icons"
5. Click en **"Package For Stores"**
6. Selecciona la opción **"Android"**
7. Click en **"Generate Package"**
8. En las opciones del APK:
   - **Package ID**: `app.marysgym.gym` (o el que quieras, debe ser único)
   - **App name**: `MARY'S GYM`
   - **Launcher name**: `MARY'S GYM`
   - **App version**: `1.0.0`
   - El resto déjalo como está
9. Click **"Download"**
10. Te descargará un ZIP con varios archivos
11. Dentro del ZIP encontrarás un archivo `.apk` (firmado para test) o instrucciones para firmarlo

## 📲 PASO 4: Instalar el APK en el celular

1. Pasa el archivo `.apk` al celular (por WhatsApp, Bluetooth, USB, etc.)
2. En el celular Android, abre el `.apk`
3. Posible que diga "Instalación de orígenes desconocidos bloqueada" → Habilita en Configuración → Seguridad
4. Instala
5. Ya tienes la app de MARY'S GYM en el celular

## 🔄 ¿Cómo se actualiza?

¡Esto es lo bueno! El APK no contiene la app, solo es un "envoltorio" que abre tu URL pública. Eso significa:

- Cuando hagas cambios al código y los subas a GitHub, **la app se actualiza automáticamente**
- NO necesitas regenerar el APK ni reinstalarlo
- Los empleados solo necesitan conexión a internet

## ⚠️ Limitaciones a tener en cuenta

- **Necesita internet** siempre. Si Streamlit Cloud está caído o no hay WiFi/datos, no funciona.
- **Streamlit Cloud gratis tiene límite**: las apps se "duermen" después de unos días sin uso. La primera persona que entre tendrá que esperar ~30 segundos a que despierte.
- **Para cargar fotos o usar cámara directa** se necesitarían cambios extra en el código.

## 🆘 Si algo no funciona

- **PWABuilder dice que no encuentra el manifest**: Asegúrate de haber subido los archivos a GitHub y que Streamlit Cloud haya redesplegado. Verifica en navegador que `https://marys-gym-lbjrnkbifnax46gxclzm8u.streamlit.app/app/static/manifest.json` muestre el JSON.
- **Los íconos no se ven**: Igual, verifica que `https://marys-gym-lbjrnkbifnax46gxclzm8u.streamlit.app/app/static/icon-192.png` muestre la imagen.
- **El APK no instala**: Necesitas habilitar "Fuentes desconocidas" en Android (Configuración → Seguridad).

## 📋 Archivos a subir a GitHub

```
MARY'S GYM/
├── app.py                    ← actualizado con meta tags PWA
├── requirements.txt          ← (ya existente)
├── Logo GYM.png              ← (ya existente)
├── icon_*.png                ← (ya existentes)
├── .streamlit/
│   └── config.toml           ← NUEVO
└── static/                   ← NUEVA CARPETA
    ├── manifest.json
    ├── icon-192.png
    ├── icon-256.png
    ├── icon-384.png
    ├── icon-512.png
    ├── icon-maskable-192.png
    └── icon-maskable-512.png
```
