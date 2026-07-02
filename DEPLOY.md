# 🚀 Guía de Deploy a Netlify

## Preparación Previa

Tu proyecto **IndustrialQuest** ha sido adaptado para funcionar como una aplicación web usando **Pygame4Web** (pygbag). Esto permite que cualquier persona pueda jugar directamente desde un navegador.

### ✅ Lo que se ha configurado:

1. **Capa de persistencia adaptada** (`src/almacenamiento.py`)
   - Usa localStorage en navegador
   - Usa JSON en escritorio
   - Totalmente transparente para el resto del código

2. **Entrada compatible con Pygame4Web** (`main.py`)
   - Punto de entrada único para la conversión

3. **Configuración de pygbag** (`pyproject.toml`)
   - Especifica qué archivos incluir

4. **HTML wrapper** (`index.html`)
   - Interfaz cargada en navegador
   - Pantalla de carga profesional
   - Manejo de errores

5. **Configuración de Netlify** (`netlify.toml`)
   - Instrucciones de build automático via GitHub Actions
   - Headers de caché y seguridad
   - Compresión de recursos

6. **GitHub Actions Workflow** (`.github/workflows/build-deploy.yml`)
   - Compilación automática con pygbag cuando haces push
   - Deploy automático a Netlify

---

## 📋 Pasos para Desplegar a Netlify (MÉTODO RECOMENDADO)

### 1. Preparar Git

```bash
cd c:\laragon\www\IndustrialQuest
git init
git add .
git commit -m "Initial commit: IndustrialQuest web version"
```

### 2. Subir a GitHub

```bash
git remote add origin https://github.com/TU_USUARIO/IndustrialQuest.git
git branch -M main
git push -u origin main
```

### 3. Conectar Netlify con GitHub (Automático)

#### Opción A: Usar Netlify CLI

```bash
npm install -g netlify-cli
netlify login
netlify init
```

Selecciona:
- Conectar con GitHub
- Selecciona el repositorio
- Build command: (déjalo vacío, ya está en netlify.toml)
- Publish directory: `build/web`

#### Opción B: Via GitHub App (Recomendado)

1. Ve a https://app.netlify.com
2. Click en "Add new site" → "Import an existing project"
3. Selecciona GitHub
4. Autoriza a Netlify
5. Selecciona el repositorio `IndustrialQuest`
6. Click en "Deploy site"

**¡Eso es todo!** Netlify se configurará automáticamente.

### 4. Configurar Variables de Entorno en Netlify (IMPORTANTE)

Ve a tu sitio en Netlify → Site settings → Build & deploy → Environment

No necesitas variables especiales, pero puedes verificar que no haya conflictos.

### 5. Primer Deploy

GitHub Actions compilará automáticamente cuando hagas push:

```bash
git add .
git commit -m "Deploy to Netlify"
git push origin main
```

Monitorea el build en:
- GitHub: Actions tab de tu repositorio
- Netlify: Deployments de tu sitio

---

## 🧪 Probar Localmente Antes de Subir

### Opción 1: Usar el script de build

```bash
# Windows
build.bat

# Linux/Mac
chmod +x build.sh
./build.sh
```

Luego prueba:

```bash
python -m http.server 8000 --directory build\web
```

Abre: `http://localhost:8000`

### Opción 2: Build directo (más lento)

```bash
python -m pygbag --build main.py
python -m http.server 8000 --directory build/web
```

---

## ⚙️ Troubleshooting

### Problema: "GitHub Action falla" en el build

**Solución:**
- Verifica que `main.py` está en la raíz
- Verifica que `pyproject.toml` existe
- Ve a tu repo → Actions para ver detalles del error

### Problema: "TypeError: 'GameRuntime' object is not subscriptable"

**Solución:** 
- Asegúrate que `almacenamiento.py` está en `src/`
- Ejecuta `python -c "import src.almacenamiento"` para verificar
- Si falla, revisa que el archivo no tenga errores de sintaxis

### Problema: "ModuleNotFoundError"

**Solución:** Revisa que todos los imports en `motor.py` sean correctos.

### Problema: Imágenes o sonidos no aparecen

**Solución:** Verifica que `recursos/imagenes/` y `recursos/sonidos/` existen con los archivos.

### Problema: El juego no guarda datos en navegador

**Solución:** 
- Verifica la consola del navegador (F12 → Console)
- Busca errores de localStorage
- Prueba en otro navegador para descartar problemas de privacidad

### Problema: El build tarda muchísimo o timeout

**Solución:**
- Pygbag puede tardar 10-20 minutos la primera vez
- En GitHub Actions, el timeout es de 30 minutos (suficiente)
- Haz el build localmente con `build.bat` y commitealo si es urgente

---

## 📦 Estructura Final del Deploy

Lo que sube Netlify a `build/web/`:

```
build/web/
├── index.html           ← Punto de entrada
├── pygame_runner.js     ← Runtime de Pygame4Web
├── industrialquest.js   ← Tu código compilado
├── industrialquest.wasm ← WebAssembly compilado
├── recursos/            ← Tus imágenes y sonidos
├── fonts/               ← Tus fuentes
└── [otros archivos generados]
```

---

## 🎮 Características Garantizadas ✅

✅ Funciona en todos los navegadores modernos (Chrome, Firefox, Safari, Edge)
✅ Totalmente offline después de cargar (no necesita conexión después)
✅ Los datos del jugador se guardan en localStorage automáticamente
✅ Rendimiento optimizado para escritorio y móvil
✅ Sin servidor backend necesario (host estático puro = ¡GRATIS!)

---

## 🔗 URLs Útiles

- **Tu sitio Netlify:** https://[tu-nombre].netlify.app
- **Netlify Dashboard:** https://app.netlify.com
- **GitHub:** https://github.com/tu-usuario/IndustrialQuest
- **pygbag Docs:** https://github.com/pygame-web/pygbag
- **Pygame CE:** https://pyga.me/

---

## ❓ Preguntas Frecuentes

**¿Cuánto cuesta Netlify?**
→ GRATIS para hosting estático ilimitado (tu caso)

**¿Cuánto tarda el build?**
→ Primera vez: 10-20 minutos (emscripten compila)
→ Siguientes: 2-5 minutos (caché de build)

**¿Puedo jugar sin internet?**
→ SÍ, después de la primera carga se cachea todo localmente

**¿Dónde se guardan los datos del jugador?**
→ En localStorage del navegador (local de cada usuario)

**¿Puedo usar mi propio dominio?**
→ SÍ, en Netlify → Site settings → Domain management

---

## 🎉 ¡Tu juego es ahora global!

Cualquier persona en el mundo puede jugar IndustrialQuest sin instalaciones.

**Comparte tu enlace:** `https://[tu-nombre].netlify.app`

¡Buen luck! 🚀🎮

