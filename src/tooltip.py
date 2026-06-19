# -*- coding: utf-8 -*-
"""
Clase BilingualTooltip para mostrar ayuda contextual bilingüe (Inglés/Español)
al pasar el cursor sobre botones, tarjetas o elementos del juego.
"""
import pygame
from src.constantes import RUTA_FUENTE

class BilingualTooltip:
    """
    Renderea un cuadro flotante bilingüe con traducción y guía contextual.
    Se adapta automáticamente a los límites de la pantalla para evitar desbordes.
    """
    def __init__(self, motor, texto_en, texto_es):
        self.motor = motor
        self.texto_en = texto_en
        self.texto_es = texto_es
        
        # Inicializar fuente para el tooltip (tamaño más pequeño y legible)
        try:
            self.fuente = pygame.font.Font(RUTA_FUENTE, 20)
        except Exception:
            self.fuente = pygame.font.SysFont("Arial", 16)

    def dibujar(self, superficie, x, y):
        """
        Dibuja el tooltip flotante sobre la superficie dada, en las coordenadas especificadas.
        """
        # Renderizar ambos textos
        render_en = self.fuente.render(self.texto_en, True, (255, 255, 255))      # Blanco
        render_es = self.fuente.render(self.texto_es, True, (200, 200, 200))      # Gris claro para menor jerarquía visual
        
        # Calcular dimensiones del cuadro
        ancho = max(render_en.get_width(), render_es.get_width()) + 20
        alto = render_en.get_height() + render_es.get_height() + 14
        
        # Ajustar coordenadas para mantener el tooltip dentro de la ventana de juego
        tx = x + 15
        ty = y + 15
        
        if tx + ancho > superficie.get_width():
            tx = x - ancho - 5
        if ty + alto > superficie.get_height():
            ty = y - alto - 5
            
        tx = max(5, tx)
        ty = max(5, ty)

        # Dibujar sombra
        pygame.draw.rect(superficie, (10, 10, 12), (tx + 3, ty + 3, ancho, alto), border_radius=4)
        
        # Dibujar cuadro principal
        pygame.draw.rect(superficie, (25, 25, 30), (tx, ty, ancho, alto), border_radius=4)
        # Borde dorado rústico de alta visibilidad
        pygame.draw.rect(superficie, (180, 140, 70), (tx, ty, ancho, alto), 2, border_radius=4)
        
        # Dibujar textos
        superficie.blit(render_en, (tx + 10, ty + 5))
        # Línea divisoria muy delgada y sutil
        y_div = ty + 5 + render_en.get_height() + 3
        pygame.draw.line(superficie, (75, 75, 85), (tx + 8, y_div), (tx + ancho - 8, y_div), 1)
        superficie.blit(render_es, (tx + 10, y_div + 3))
