# Catálogo de Recursos Multimedia (Gráficos, Audio y Fuentes)

**IndustrialQuest** utiliza una estética pixel art retro que se complementa con efectos de sonido de estilo 8-bit y música de sintetizadores (CHIPTUNE). Este documento cataloga los activos multimedia empleados por el motor y su organización física.

---

## 1. Organización del Espacio de Trabajo

Los recursos están separados de los scripts de código fuente y se dividen en dos carpetas raíz:

- **`fonts/`**: Almacena las tipografías vectoriales TTF del juego.
- **`recursos/`**: Contiene dos subcarpetas específicas para dividir los archivos por tipo de media:
  - **`recursos/imagenes/`**: Gráficos, sprites y fondos.
  - **`recursos/sonidos/`**: Audio digital en formato WAVE.

---

## 2. Tipografías (`fonts/`)

- **`Pixelletters-RLm3.ttf`**: Tipografía pixel art secundaria (conservada).
- **`Pixellettersfull-BnJ5.ttf`**: Fuente principal del juego. Utilizada para renderizar los textos del menú, diálogos de reglas, puntuación, temporizador y la entrada del jugador. Cargada a tamaño de `35` puntos.

---

## 3. Catálogo de Imágenes (`recursos/imagenes/`)

- **Fondos de Nivel:**
  - `PastSimple.jpg`: Ilustración del primer capítulo (Pasado Simple).
  - `Comparativos.jpg`: Ilustración del segundo capítulo.
  - `PresentPerfect.png`: Ilustración del tercer capítulo.
  - `Will.jpg`: Ilustración del cuarto capítulo.
- **Interfaz y HUD:**
  - `Logo.jpg`: Logo principal de *IndustrialQuest* que se desliza al inicio.
  - `corazon.png`: Icono del indicador de vidas.
  - `Signo.png`: Letrero de madera inferior donde se escribe el texto tipeado.
  - `Boton.png`: Botón base para el menú principal y selección de temas.
  - `rule1.png` y `rule2.png`: Paneles decorativos empleados en la pantalla de reglas.

---

## 4. Catálogo de Audios (`recursos/sonidos/`)

- **Música de Fondo (Banda Sonora):**
  - `Title.wav`: Chiptune de bienvenida que suena en el menú principal.
  - `Stage1.wav` a `Stage4.wav`: Canciones en bucle que ambientan el gameplay de los capítulos 1 al 4 respectivamente.
- **Efectos de Sonido (SFX):**
  - `Correcta.wav`: Sonido corto al tipear una palabra correcta (+1 punto).
  - `equivocado.wav`: Sonido áspero al perder una vida por escapar una palabra.
  - `ganador.wav`: Sonido triunfal (reservado).
  - `GameOver.wav`: Tonada triste reproducida en la pantalla de derrota.

---

## 5. Optimización del Motor de Recursos (Caché en RAM)

En el diseño original del software, las imágenes y sonidos se cargaban constantemente desde el disco duro en cada transición de pantalla o durante la pulsación de botones. 

En la versión refactorizada, la clase `AdministradorRecursos` implementa un **mapa en caché (RAM)**:
- Cuando una pantalla solicita un recurso (por ejemplo, `recursos.obtener_imagen("logo.png")`), el administrador comprueba si la textura ya reside en memoria.
- Si no está cargada, la lee desde el disco de forma síncrona y la almacena en el diccionario interno.
- En solicitudes futuras, la devuelve instantáneamente sin acceder al almacenamiento secundario, reduciendo el retardo (latencia) y eliminando el uso innecesario de CPU y de memoria.
