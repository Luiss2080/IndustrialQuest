# -*- coding: utf-8 -*-
"""
Archivo de lanzamiento principal para el juego IndustrialQuest.
Ejecuta esta clase para iniciar el videojuego educativo.
"""
import sys
import os

# Asegurar que el directorio del script esté en el path de búsqueda de módulos
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

from src.motor import MotorJuego

def main():
    """
    Función de arranque que inicializa el motor de IndustrialQuest y ejecuta el bucle de juego.
    """
    juego = MotorJuego()
    juego.ejecutar()

if __name__ == "__main__":
    main()
