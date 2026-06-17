# -*- coding: utf-8 -*-
"""
Clase que representa una frase en la pantalla de juego.
"""
import random

class FraseJuego:
    """
    Representa una frase individual que se desplaza horizontalmente por la pantalla.
    Encapsula su texto, palabra correcta, coordenadas y color.
    
    Implementa soporte de acceso estilo diccionario para asegurar compatibilidad
    total con cualquier lógica de juego heredada.
    """
    def __init__(self, texto, palabra_correcta):
        self.texto = texto
        self.palabra_correcta = palabra_correcta
        self.x = 0
        self.y = random.randint(50, 500)
        
        # Generar un color aleatorio para pintar la frase en el juego
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

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
        raise KeyError(f"Clave inválida en FraseJuego: {clave}")

    def __setitem__(self, clave, valor):
        if clave == "x":
            self.x = valor
        elif clave == "y":
            self.y = valor
        else:
            raise KeyError(f"No se permite modificar la clave '{clave}' en FraseJuego")
            
    def __contains__(self, clave):
        return clave in ("frase", "palabra_correcta", "x", "y", "color")
