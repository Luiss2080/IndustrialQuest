# Estructura de la Base de Datos de Preguntas

Las frases y categorías de estudio en **IndustrialQuest** se definen de manera estática y centralizada en el archivo `src/datos_juego.py`. Esto permite editar o expandir fácilmente los contenidos lingüísticos sin alterar la lógica de renderizado del gameplay.

## Diccionario de Temas

El diccionario global `TEMAS` mapea los nombres de las categorías gramaticales con sus respectivos recursos gráficos, efectos de audio y la lista de tuplas con las preguntas/respuestas.

### Estructura de un Tema

Cada entrada en `TEMAS` contiene la siguiente estructura de datos:

```python
"Nombre del Tema": {
    "audio_fondo": "ArchivoAudioNivel.wav",    # Música de fondo para el gameplay
    "audio_clic": "ArchivoAudioExito.wav",     # Sonido reproducido al responder correctamente
    "audio_exito": "ganador.wav",              # Sonido de victoria (reservado)
    "audio_fracaso": "equivocado.wav",          # Sonido reproducido al perder una vida
    "imagen_fondo": "FondoNivel.png",          # Textura de fondo del nivel
    "imagen_corazon": "corazon.png",           # Icono de vidas (corazones)
    "frases": [                                # Colección de preguntas
        ("Enunciado de la frase con '_' (pista)", "palabra_correcta"),
        ...
    ]
}
```

*Nota: La frase debe contener obligatoriamente el carácter guion bajo (`_`), el cual sirve para identificar visualmente el espacio en blanco y calcular la posición del tipeo en pantalla.*

---

## Cómo Añadir un Nuevo Capítulo

Para añadir una nueva lección al juego, sigue estos pasos:

1. Agrega tus imágenes y sonidos correspondientes en las subcarpetas `recursos/imagenes/` y `recursos/sonidos/`.
2. Abre el archivo `src/datos_juego.py`.
3. Añade una nueva clave al diccionario `TEMAS` con la configuración de recursos y las tuplas de preguntas.

### Ejemplo de código para añadir un tema:

```python
    "Modal Verbs": {
        "audio_fondo": "Stage2.wav",
        "audio_clic": "Correcta.wav",
        "audio_exito": "ganador.wav",
        "audio_fracaso": "equivocado.wav",
        "imagen_fondo": "Comparativos.jpg", # Puedes reutilizar fondos existentes
        "imagen_corazon": "corazon.png",
        "frases": [
            ("You _ study for the test (must)", "must"),
            ("She _ speak French fluently (can)", "can"),
            ("We _ go to the park tomorrow (might)", "might")
        ]
    }
```

Al reiniciar el juego, la pantalla de selección de capítulos (`PantallaNiveles`) detectará automáticamente la nueva clave y generará el botón interactivo de forma dinámica.
