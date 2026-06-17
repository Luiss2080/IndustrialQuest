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
        # Esto permite que la lógica interna del juego busque claves antiguas (ej: logo.png)
        # y devuelva el archivo físico correspondiente (ej: Logo.jpg), manteniendo
        # intacto el comportamiento original.
        self._mapeo_nombres = {
            "Will.jpg": "Will.jpg",
            "Comparativos.jpg": "Comparativos.jpg",
            "PresentPerfect.png": "PresentPerfect.png",
            "PastSimple.png": "PastSimple.jpg",         # Mapea clave png a archivo jpg físico
            "corazon.png": "corazon.png",
            "logo.png": "Logo.jpg",                     # Mapea clave png a archivo jpg físico
            "Signo.png": "Signo.png",
            "Boton.png": "Boton.png",
            "rule1.png": "rule1.png",
            "rule2.png": "rule2.png",
            "stage1_mascota.gif": "rule1.png"            # Mapea mascota gif a rule1.png físico
        }

    def obtener_ruta_recurso(self, nombre_archivo):
        """
        Resuelve y retorna la ruta absoluta o relativa correcta del archivo en el disco,
        aplicando los mapeos de compatibilidad si es necesario.
        """
        nombre_real = self._mapeo_nombres.get(nombre_archivo, nombre_archivo)
        return os.path.join(DIRECTORIO_RECURSOS, nombre_real)

    def obtener_imagen(self, nombre):
        """
        Carga una imagen desde el disco, la almacena en caché y la retorna.
        Si la imagen ya fue cargada anteriormente, la devuelve directamente de la caché.
        """
        if nombre not in self._imagenes:
            ruta = self.obtener_ruta_recurso(nombre)
            try:
                self._imagenes[nombre] = pygame.image.load(ruta)
            except pygame.error as e:
                print(f"Error crítico al cargar la imagen {ruta}: {e}")
                raise e
        return self._imagenes[nombre]

    def obtener_sonido(self, nombre):
        """
        Carga un archivo de audio (WAV) desde el disco, lo almacena en caché y retorna
        la instancia de pygame.mixer.Sound.
        """
        if nombre not in self._sonidos:
            ruta = self.obtener_ruta_recurso(nombre)
            try:
                self._sonidos[nombre] = pygame.mixer.Sound(ruta)
            except pygame.error as e:
                print(f"Error crítico al cargar el sonido {ruta}: {e}")
                raise e
        return self._sonidos[nombre]
