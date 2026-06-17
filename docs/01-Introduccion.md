# Introducción a IndustrialQuest

**IndustrialQuest** es un videojuego educativo interactivo desarrollado con Python y Pygame. El software está diseñado como una herramienta didáctica para reforzar la adquisición y práctica de la gramática del idioma inglés en estudiantes de diversos niveles.

## Propósito Educativo

El juego combina el concepto de **typing game** (juego de mecanografía) con la resolución de ejercicios de gramática. Al requerir que el jugador complete frases en tiempo real escribiendo la palabra faltante, el videojuego promueve:
- **Agilidad Mental:** Asociación rápida de estructuras gramaticales bajo presión de tiempo.
- **Mecanografía Dinámica:** Práctica de la escritura correcta (ortografía) de palabras y verbos en inglés.
- **Feedback Inmediato:** Refuerzo auditivo y visual tras cada acierto o error, lo que consolida el aprendizaje por condicionamiento positivo.

## El Concepto del Juego

El jugador se enfrenta a frases en inglés que se desplazan horizontalmente de izquierda a derecha. Cada frase tiene un espacio en blanco (`_`) donde falta una palabra clave. La pista sobre qué palabra colocar está escrita al final de la oración entre paréntesis. 

Para salvar la frase antes de que cruce el borde derecho de la pantalla, el jugador debe escribir correctamente la respuesta por teclado.

---

## Flujo de Pantallas del Usuario

El software se compone de las siguientes interfaces visuales para el jugador (todas presentadas enteramente en inglés para preservar la inmersión didáctica):

1. **Menú de Inicio (Main Menu):** Presenta el logotipo del juego con una animación retro y da acceso a la pantalla de reglas y a la de selección de niveles.
2. **Reglas del Juego (Rules):** Muestra de forma numerada las instrucciones básicas y el sistema de vidas.
3. **Selección de Nivel (Select a Chapter):** Permite elegir entre cuatro categorías gramaticales diferentes (capítulos).
4. **Área de Juego (Gameplay):** Contiene el HUD superior con las vidas y el marcador, el fondo ilustrado del nivel, las frases cayendo y la zona inferior de tipeo.
5. **Pantalla de Fin (Game Over):** Informa al jugador de la conclusión de la partida al perder las vidas y regresa automáticamente al menú de niveles.
