# -*- coding: utf-8 -*-
"""
Clase base para representar una pantalla o estado del juego.
"""

class Pantalla:
    """
    Clase base (interfaz) para representar los diferentes estados/pantallas del videojuego.
    Todas las pantallas del juego (menú, reglas, gameplay, etc.) deben heredar de esta.
    """
    def __init__(self, motor):
        self.motor = motor

    def manejar_eventos(self, eventos):
        """
        Procesa la lista de eventos de pygame para esta pantalla específica.
        Debe ser sobreescrito en las clases hijas.
        """
        pass

    def actualizar(self, dt):
        """
        Actualiza la lógica interna del estado de esta pantalla.
        Recibe dt (delta time en milisegundos desde el último frame).
        Debe ser sobreescrito en las clases hijas.
        """
        pass

    def dibujar(self, superficie):
        """
        Dibuja los elementos visuales de la pantalla sobre la superficie principal.
        Debe ser sobreescrito en las clases hijas.
        """
        pass
