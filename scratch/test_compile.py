# -*- coding: utf-8 -*-
import sys
import os
import pygame

# Set CWD and sys path
ruta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ruta_raiz)
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

print("Initializing Pygame headless...")
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.display.set_mode((800, 600))

print("Testing imports...")
try:
    from src.motor import MotorJuego
    from src.pantalla_juego import PantallaJuego
    print("Imports successful!")
    
    print("Initializing engine...")
    motor = MotorJuego()
    print("Engine initialization successful!")
    
    print("Initializing PantallaJuego...")
    motor.tema_actual = "Level 1: Reception Area"
    pantalla = PantallaJuego(motor)
    print("PantallaJuego initialization successful!")
    
    print("Compiling all other screens...")
    from src.pantalla_menu import PantallaMenu
    from src.pantalla_manual import PantallaManual
    from src.pantalla_reglas import PantallaReglas
    from src.pantalla_niveles import PantallaNiveles
    from src.pantalla_logs import PantallaLogs
    from src.pantalla_ajustes import PantallaAjustes
    from src.pantalla_fin import PantallaFin
    print("All screen imports compile successfully!")
    
except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)

print("SUCCESS")
sys.exit(0)
