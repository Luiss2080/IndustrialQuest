# -*- coding: utf-8 -*-
"""
Pantalla que muestra las reglas del juego.
"""
import pygame
from src.constantes import COLOR_AZUL, COLOR_BLANCO, COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla

class PantallaReglas(Pantalla):
    """
    Muestra las instrucciones del videojuego en inglés.
    Mantiene la compatibilidad del posicionamiento y tamaño de las cajas de reglas
    del juego original (incluido el detalle del uso de rule1.get_rect para rule2).
    """
    def __init__(self, motor):
        super().__init__(motor)

        # Cargar e inicializar la imagen de regla 1
        self.imagen_regla1 = self.motor.recursos.obtener_imagen("rule1.png")
        self.imagen_regla1 = pygame.transform.scale(self.imagen_regla1, (490, 80))
        self.rect_regla1 = self.imagen_regla1.get_rect(center=(300, 190))

        # Cargar e inicializar la imagen de regla 2
        self.imagen_regla2 = self.motor.recursos.obtener_imagen("rule2.png")
        self.imagen_regla2 = pygame.transform.scale(self.imagen_regla2, (180, 70))
        # Quirk de diseño del juego original: se usa el rect de regla1 para calcular regla2
        self.rect_regla2 = self.imagen_regla1.get_rect(center=(400, 340))

        # Cargar la imagen del botón volver
        self.boton_img = self.motor.recursos.obtener_imagen("Boton.png")
        self.boton_img = pygame.transform.scale(self.boton_img, (150, 50))
        self.boton_volver = self.boton_img.get_rect(bottomright=(ANCHO_PANTALLA - 20, ALTO_PANTALLA - 20))

        # Configurar textos de la pantalla
        self.texto_titulo = self.motor.fuente.render("RULES OF THE GAME:", True, COLOR_BLANCO)
        self.texto_volver = self.motor.fuente.render("Volver", True, COLOR_NEGRO)

        # Contenido de las reglas en inglés
        # Nota: Del "3." pasa al "5.", omitiendo el número 4 para respetar el contenido exacto del original.
        self.reglas = [
            "1. A phrase with a missing word will appear on the screen.",
            "",
            "",
            "2. Type the correct word to score points.",
            "",
            "",
            "3. As your score goes up, more phrases will appear on screen.",
            "5. No contractions allowed.",
            "6. You lose one life for every phrase missed.",
            "7. The game ends when you run out of lives."
        ]

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_volver.collidepoint(evento.pos):
                    from src.pantalla_menu import PantallaMenu
                    self.motor.cambiar_pantalla(PantallaMenu(self.motor))

    def dibujar(self, superficie):
        superficie.fill(COLOR_AZUL)
        
        # Dibujar título
        superficie.blit(self.texto_titulo, (20, 20))

        # Dibujar las imágenes decorativas traseras
        superficie.blit(self.imagen_regla1, self.rect_regla1)
        superficie.blit(self.imagen_regla2, self.rect_regla2)

        # Dibujar los enunciados de las reglas
        y = 100
        for regla in self.reglas:
            texto_regla = self.motor.fuente.render(regla, True, COLOR_BLANCO)
            superficie.blit(texto_regla, (20, y))
            y += 50

        # Dibujar botón volver
        superficie.blit(self.boton_img, self.boton_volver)
        superficie.blit(self.texto_volver, (self.boton_volver.x + 35, self.boton_volver.y + 10))
