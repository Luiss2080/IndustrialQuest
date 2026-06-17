# Mecánicas del Juego

**IndustrialQuest** es un juego de acción gramatical en tiempo real. Este documento detalla el funcionamiento interno de las mecánicas que rigen el gameplay.

---

## 1. Sistema de Vidas (Salud)

- El jugador inicia cada partida con **3 vidas**, representadas en la interfaz de usuario mediante iconos de corazones pixel art en la parte superior derecha.
- Cada vez que una frase se desliza completamente y cruza el límite derecho de la pantalla (`x > 800`), el jugador pierde una vida y se reproduce un efecto de sonido de fallo (`equivocado.wav`).
- Si las vidas llegan a **0**, el juego se detiene inmediatamente. Ocurre una pausa dramática de 4 segundos antes de transicionar a la pantalla de **Game Over**.

---

## 2. Sistema de Marcador y Tiempo

- **Puntuación (Points):** Cada palabra escrita correctamente otorga **1 punto**. El marcador se actualiza en tiempo real en la esquina superior izquierda.
- **Temporizador (Time):** Muestra los segundos transcurridos desde que inició el nivel, ubicado en la parte superior central. Sirve para evaluar el desempeño y progreso del estudiante.

---

## 3. Dificultad Dinámica (Progresión Automática)

Para evitar la monotonía y entrenar la agilidad cognitiva, el juego implementa dos algoritmos de dificultad incremental basados en la puntuación actual:

### A. Velocidad Adaptativa de Desplazamiento
La velocidad con la que las frases se desplazan horizontalmente aumenta de acuerdo con la fórmula:
$$\text{velocidad} = 0.4 + \left(\frac{\text{puntuación}}{50}\right)$$

*Ejemplos:*
- Con `0` puntos: velocidad base de `0.4` píxeles por frame.
- Con `30` puntos: velocidad intermedia de `1.0` píxeles por frame.
- Con `80` puntos: velocidad rápida de `2.0` píxeles por frame.

### B. Densidad de Frases Simultáneas
La cantidad máxima de enunciados que pueden aparecer al mismo tiempo en pantalla se calcula mediante la fórmula:
$$\text{cantidad\_maxima} = \lfloor\frac{\text{puntuación}}{8}\rfloor + 1$$

*Ejemplos:*
- De `0` a `7` puntos: Máximo **1** frase en pantalla.
- De `8` a `15` puntos: Máximo **2** frases simultáneas.
- De `16` a `23` puntos: Máximo **3** frases simultáneas, y así sucesivamente.

---

## 4. Validación de Entrada y Reglas de Tipeo

- **Filtro de Entrada:** Solo se registran y muestran caracteres válidos e imprimibles. El uso de la tecla **Backspace** borra un carácter del búfer.
- **Sin Contracciones:** El juego educativo prohíbe el uso de abreviaciones. Para las frases de futuro negativo, por ejemplo, el jugador debe escribir la forma completa `"will not"` en lugar del coloquial `"won't"`.
- **Detección de Aciertos:** La validación no discrimina entre mayúsculas y minúsculas (Case Insensitive) y elimina los espacios en blanco iniciales o finales antes de comprobar la coincidencia, garantizando que un espacio extra al final no cause un error injusto.
