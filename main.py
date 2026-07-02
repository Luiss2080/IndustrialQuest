# -*- coding: utf-8 -*-
"""
Archivo de entrada principal compatible con Pygame4Web (pygbag).
Se ejecuta como punto de entrada único para la conversión a WebAssembly.
"""
import sys
import os

# Configurar rutas para importar módulos del proyecto
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
os.chdir(ruta_raiz)
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

from src.motor import MotorJuego

async def main():
    """
    Función asincrónica de arranque (requerida para Pygame4Web).
    Inicializa el motor de IndustrialQuest y ejecuta el bucle de juego.
    """
    juego = MotorJuego()
    juego.ejecutar()

if __name__ == "__main__":
    # Para Pygame4Web/pygbag, se ejecuta como async
    try:
        import asyncio
        asyncio.run(main())
    except:
        # Fallback para ejecución normal en escritorio
        juego = MotorJuego()
        juego.ejecutar()
