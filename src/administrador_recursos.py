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
                if nombre == "corazon.png":
                    # Generar dinámicamente un corazón pixel-art rojo de 32x32 con canal Alfa
                    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
                    # Dibujar corazón pixel-art
                    pygame.draw.circle(surf, (220, 35, 35), (10, 11), 8)
                    pygame.draw.circle(surf, (220, 35, 35), (22, 11), 8)
                    pygame.draw.polygon(surf, (220, 35, 35), [(2, 13), (30, 13), (16, 27)])
                    # Sombra interior del corazón (profundidad)
                    pygame.draw.circle(surf, (160, 20, 20), (10, 13), 6)
                    pygame.draw.circle(surf, (160, 20, 20), (22, 13), 6)
                    pygame.draw.polygon(surf, (160, 20, 20), [(4, 14), (28, 14), (16, 25)])
                    # Brillo pixel-art blanco
                    pygame.draw.rect(surf, (255, 255, 255), (7, 7, 4, 4), border_radius=1)
                    pygame.draw.rect(surf, (255, 255, 255), (19, 7, 4, 4), border_radius=1)
                    self._imagenes[nombre] = surf
                elif nombre == "estrella.png":
                    # Generar una estrella dorada pixel-art de 32x32 con canal Alfa
                    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
                    puntos = [
                        (16, 2), (20, 11), (30, 11), (22, 18),
                        (25, 28), (16, 22), (7, 28), (10, 18),
                        (2, 11), (12, 11)
                    ]
                    pygame.draw.polygon(surf, (255, 215, 0), puntos) # Dorado
                    pygame.draw.polygon(surf, (180, 140, 10), puntos, 2) # Borde bronce
                    # Brillo interior
                    pygame.draw.circle(surf, (255, 255, 200), (16, 14), 4)
                    self._imagenes[nombre] = surf
                elif nombre == "Boton.png":
                    surf = pygame.Surface((200, 50))
                    surf.fill((160, 110, 65))
                    pygame.draw.rect(surf, (90, 55, 30), (0, 0, 200, 50), 3)
                    pygame.draw.circle(surf, (80, 80, 80), (8, 8), 3)
                    pygame.draw.circle(surf, (80, 80, 80), (192, 8), 3)
                    pygame.draw.circle(surf, (80, 80, 80), (8, 42), 3)
                    pygame.draw.circle(surf, (80, 80, 80), (192, 42), 3)
                    self._imagenes[nombre] = surf
                elif nombre == "logo.png" or nombre == "Logo.jpg":
                    surf = pygame.Surface((320, 320))
                    surf.fill((90, 55, 30))
                    pygame.draw.rect(surf, (160, 110, 65), (10, 10, 300, 300), 5)
                    self._imagenes[nombre] = surf
                else:
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
