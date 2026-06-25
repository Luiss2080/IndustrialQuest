# -*- coding: utf-8 -*-
"""
Constantes de configuración para el juego IndustrialQuest.
"""
import os

# Dimensiones de la pantalla de juego
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 610

# Definición de colores principales (formato RGB)
COLOR_BLANCO = (255, 255, 255)
COLOR_ROJO = (255, 0, 0)
COLOR_NEGRO = (0, 0, 0)
COLOR_AZUL = (27, 19, 66)

# Configuración del motor de texto (fuente)
TAMAÑO_FUENTE = 35
RUTA_FUENTE = os.path.join("fonts", "Pixellettersfull-BnJ5.ttf")

# Directorio donde se almacenan los recursos multimedia
DIRECTORIO_RECURSOS = "recursos"

# Posiciones fijas para renderizar los corazones en pantalla (3 vidas)
POSICIONES_CORAZONES = [(ANCHO_PANTALLA - 60 - i * 60, 0) for i in range(3)]
