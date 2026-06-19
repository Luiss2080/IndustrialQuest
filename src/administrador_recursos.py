# -*- coding: utf-8 -*-
"""
Administrador de recursos para cargar y gestionar imágenes, sonidos y fuentes.
"""
import os
import pygame
from src.constantes import DIRECTORIO_RECURSOS

class AdministradorRecursos:
    """
    Clase para cargar de forma segura y almacenar en caché imágenes y sonidos,
    evitando accesos repetitivos a disco y optimizando el consumo de memoria.
    """
    def __init__(self):
        self._imagenes = {}
        self._sonidos = {}
        
        # Mapeos especiales de compatibilidad con las claves originales de assets.
        self._mapeo_nombres = {
            "Will.jpg": "Will.jpg",
            "Comparativos.jpg": "Comparativos.jpg",
            "PresentPerfect.png": "PresentPerfect.png",
            "PastSimple.png": "PastSimple.jpg",
            "corazon.png": "corazon.png",
            "logo.png": "IndustrialQuestLogoFinal.png",  # Corregido para usar el logo oficial existente
            "Signo.png": "Signo.png",
            "Boton.png": "Boton.png",
            "rule1.png": "rule1.png",
            "rule2.png": "rule2.png",
            "stage1_mascota.gif": "rule1.png"
        }

    def obtener_ruta_recurso(self, nombre_archivo):
        """
        Resuelve y retorna la ruta del archivo en el disco.
        """
        nombre_real = self._mapeo_nombres.get(nombre_archivo, nombre_archivo)
        extension = os.path.splitext(nombre_real)[1].lower()
        
        if extension in (".wav", ".mp3", ".ogg"):
            subcarpeta = "sonidos"
        else:
            subcarpeta = "imagenes"
            
        return os.path.join(DIRECTORIO_RECURSOS, subcarpeta, nombre_real)

    def obtener_imagen(self, nombre):
        """
        Carga una imagen desde el disco, la almacena en caché y la retorna.
        Genera dinámicamente recursos de reemplazo temáticos si no se encuentran en disco.
        """
        if nombre not in self._imagenes:
            ruta = self.obtener_ruta_recurso(nombre)
            try:
                self._imagenes[nombre] = pygame.image.load(ruta)
            except (pygame.error, FileNotFoundError) as e:
                print(f"Advertencia: No se pudo cargar {ruta}. Generando recurso dinámico para '{nombre}'...")
                if nombre == "Boton.png":
                    # Generar dinámicamente un tablón de madera de 200x50 para botones
                    surf = pygame.Surface((200, 50))
                    # Color madera
                    surf.fill((160, 110, 65))
                    # Borde madera oscura
                    pygame.draw.rect(surf, (90, 55, 30), (0, 0, 200, 50), 3)
                    # Remaches metálicos en las esquinas
                    pygame.draw.circle(surf, (80, 80, 80), (8, 8), 3)
                    pygame.draw.circle(surf, (80, 80, 80), (192, 8), 3)
                    pygame.draw.circle(surf, (80, 80, 80), (8, 42), 3)
                    pygame.draw.circle(surf, (80, 80, 80), (192, 42), 3)
                    self._imagenes[nombre] = surf
                elif nombre == "logo.png" or nombre == "Logo.jpg":
                    # Logo de repuesto rústico
                    surf = pygame.Surface((320, 320))
                    surf.fill((90, 55, 30))
                    pygame.draw.rect(surf, (160, 110, 65), (10, 10, 300, 300), 5)
                    self._imagenes[nombre] = surf
                else:
                    # Superficie vacía genérica de color fucsia
                    surf = pygame.Surface((64, 64))
                    surf.fill((255, 0, 255))
                    self._imagenes[nombre] = surf
        return self._imagenes[nombre]

    def obtener_sonido(self, nombre):
        """
        Carga un archivo de audio (WAV) desde el disco, lo almacena en caché y retorna
        la instancia de pygame.mixer.Sound. Genera un objeto silencioso de respaldo si falla.
        """
        if nombre not in self._sonidos:
            ruta = self.obtener_ruta_recurso(nombre)
            try:
                self._sonidos[nombre] = pygame.mixer.Sound(ruta)
            except Exception as e:
                print(f"Advertencia: No se pudo cargar el sonido {ruta}: {e}. Generando audio silencioso de respaldo...")
                try:
                    # Intentar crear un buffer de silencio de 1 segundo (44100 Hz, 16-bit, mono = 88200 bytes)
                    self._sonidos[nombre] = pygame.mixer.Sound(buffer=bytes(88200))
                except Exception:
                    # Fallback final: Mock completo con interfaz idéntica
                    class MockSound:
                        def play(self, loops=0): pass
                        def stop(self): pass
                        def set_volume(self, volume): pass
                    self._sonidos[nombre] = MockSound()
        return self._sonidos[nombre]
