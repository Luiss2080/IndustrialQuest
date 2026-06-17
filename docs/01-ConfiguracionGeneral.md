# Configuración General

Este documento describe la configuración global del proyecto **IndustrialQuest**. Toda la configuración técnica se centraliza en el archivo `src/constantes.py` para garantizar la modularidad y facilidad de mantenimiento.

## Parámetros de la Pantalla

El juego se renderiza en una ventana con las siguientes dimensiones predeterminadas:

- **Ancho de Pantalla:** `800` píxeles.
- **Alto de Pantalla:** `600` píxeles.

## Paleta de Colores

Se utiliza un conjunto limitado de colores en formato RGB para mantener la estética pixel art retro del juego:

- **Blanco:** `(255, 255, 255)` — Utilizado para fondos de texto de las preguntas y cajas decorativas.
- **Rojo:** `(255, 0, 0)` — Color para textos de advertencia y marcadores (como el tiempo transcurrido o la puntuación).
- **Negro:** `(0, 0, 0)` — Utilizado para el texto tipeado por el usuario y los enunciados.
- **Azul Oscuro:** `(27, 19, 66)` — Color de fondo sólido para menús principales, reglas y pantallas de fin de juego.

## Rutas de Recursos y Tipografías

La organización física del proyecto define dos carpetas principales en la raíz para la carga de archivos multimedia y tipográficos:

1. **Tipografía (`fonts/`):**
   - Archivo fuente principal: `fonts/Pixellettersfull-BnJ5.ttf`.
   - Tamaño de fuente por defecto: `35` puntos.
2. **Multimedia (`recursos/`):**
   - Las imágenes y sprites se almacenan y cargan desde la subcarpeta `recursos/imagenes/`.
   - Los efectos de sonido y la música de fondo se almacenan y cargan desde la subcarpeta `recursos/sonidos/`.

## Vidas y Posicionamiento de Corazones

El sistema de juego otorga al usuario un total de `3` vidas representadas por corazones. Estos corazones se dibujan en la esquina superior derecha del HUD y sus coordenadas se calculan dinámicamente utilizando una lista por comprensión:

```python
POSICIONES_CORAZONES = [(ANCHO_PANTALLA - 60 - i * 60, 0) for i in range(3)]
```
Esto genera las coordenadas fijas `(740, 0)`, `(680, 0)` y `(620, 0)`.
