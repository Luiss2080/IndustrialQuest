# -*- coding: utf-8 -*-
"""
Clase que representa una frase en la pantalla de juego de IndustrialQuest: Woodwork Edition.
"""
import random

# Alturas fijas para las tres cintas transportadoras (carriles)
LANES_Y = [165, 285, 405]

class FraseJuego:
    """
    Representa una frase individual (tabla de madera) que se desplaza horizontalmente.
    Está asignada a una cinta transportadora específica (carril 0, 1 o 2).
    Soporta acceso estilo diccionario por retrocompatibilidad.
    """
    def __init__(self, texto, palabra_correcta, lane=0):
        self.texto = texto
        self.palabra_correcta = palabra_correcta
        self.lane = lane
        self.x = -350  # Iniciar fuera de la pantalla a la izquierda para un scroll suave
        self.y = LANES_Y[self.lane]
        
        # Color del texto por si se requiere renderizado simple
        self.color = (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))

    # Métodos mágicos para permitir el acceso por claves dict (compatibilidad heredada)
    def __getitem__(self, clave):
        if clave == "frase":
            return self.texto
        elif clave == "palabra_correcta":
            return self.palabra_correcta
        elif clave == "x":
            return self.x
        elif clave == "y":
            return self.y
        elif clave == "color":
            return self.color
        elif clave == "lane":
            return self.lane
        raise KeyError(f"Clave inválida en FraseJuego: {clave}")

    def __setitem__(self, clave, valor):
        if clave == "x":
            self.x = valor
        elif clave == "y":
            self.y = valor
        else:
            raise KeyError(f"No se permite modificar la clave '{clave}' en FraseJuego")
            
    def __contains__(self, clave):
        return clave in ("frase", "palabra_correcta", "x", "y", "color", "lane")
