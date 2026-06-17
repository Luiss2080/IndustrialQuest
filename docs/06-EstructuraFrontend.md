# Estructura del Frontend y Renderizado Gráfico

El frontend de **IndustrialQuest** está construido sobre la biblioteca multimedia **Pygame**, utilizando superficies 2D e interfaces del sistema para la gestión del HUD, renderizado de textos y animaciones.

---

## 1. Superficie Principal y Bucle de Dibujo

La visualización del juego se maneja mediante una única superficie de visualización principal (`superficie` o `pantalla_principal`), obtenida mediante la inicialización del motor en `src/motor.py`:

```python
self.pantalla_principal = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
```

El dibujado de fotogramas sigue un flujo síncrono de tres fases:
1. **Limpieza/Fondo:** Se rellena la pantalla con el fondo correspondiente o color sólido.
2. **Dibujado (Blitting):** Cada elemento visual (imágenes de fondo, cajas de texto, corazones, entrada de texto y letreros) se dibuja mediante llamadas a `.blit()`.
3. **Volcado (Flip):** Se invoca a `pygame.display.flip()` para intercambiar el búfer de dibujo y hacerlo visible en el monitor del jugador.

---

## 2. Tipografía y Renderizado de Texto

El juego implementa una fuente pixel art retro cargada a partir de un archivo TrueType (`.ttf`):
- Archivo fuente: `fonts/Pixellettersfull-BnJ5.ttf`.
- Los textos se renderizan dinámicamente en tiempo de ejecución utilizando `fuente.render(texto, antialias, color_texto, color_fondo)`.
- Las frases flotantes del gameplay se renderizan con un fondo blanco sólido para asegurar su legibilidad frente a los fondos ilustrados de cada nivel:
  ```python
  texto_frase = self.motor.fuente.render(frase.texto, True, COLOR_NEGRO, COLOR_BLANCO)
  ```

---

## 3. Animaciones No Bloqueantes

El menú de inicio presenta una animación en la que el logotipo de *IndustrialQuest* se desliza desde fuera de la pantalla (coordenada `x = -400`) hacia el centro de la pantalla (`x = 200`).
A diferencia del código original, esta animación se realiza de forma **no bloqueante** dentro del bucle de eventos general, lo que permite que el sistema operativo mantenga la ventana responsiva al usuario (por ejemplo, al intentar cerrar la aplicación durante la entrada).

---

## 4. Captura de Entrada (Typing System)

El control principal se realiza a través del teclado físico:
- Se procesan los eventos de tipo `pygame.KEYDOWN`.
- La tecla **Backspace** elimina el último carácter ingresado.
- La tecla **Escape** detiene el juego y abre la pantalla final de Game Over.
- Los demás caracteres se filtran mediante `evento.unicode.isprintable()` para descartar teclas de control (como Shift, Alt, etc.) e ir armando dinámicamente el string `self.motor.texto_ingresado`.
- La pantalla de juego dibuja este búfer de texto centrado en la parte inferior sobre el letrero de madera decorativo.
