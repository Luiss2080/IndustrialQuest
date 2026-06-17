# -*- coding: utf-8 -*-
"""
Pantalla de fin de juego (Game Over) para IndustrialQuest.
"""
import pygame
from src.constantes import COLOR_AZUL, COLOR_BLANCO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla

class PantallaFin(Pantalla):
    """
    Representa la pantalla final cuando el jugador pierde todas las vidas.
    Muestra el texto 'Game Over!', reproduce un efecto de sonido dramático
    y espera 6 segundos antes de reiniciar y volver a la selección de nivel.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Detener cualquier sonido o música anterior y reproducir el audio de fin de juego
        sonido_game_over = self.motor.recursos.obtener_sonido("GameOver.wav")
        sonido_game_over.play()
        
        # Configurar y centrar el texto final
        self.texto_game_over = self.motor.fuente.render("Game Over!", True, COLOR_BLANCO)
        self.pos_x = ANCHO_PANTALLA // 2 - self.texto_game_over.get_width() // 2
        self.pos_y = ALTO_PANTALLA // 2

    def manejar_eventos(self, eventos):
        pass

    def actualizar(self, dt):
        pass

    def dibujar(self, superficie):
        # Fondo azul
        superficie.fill(COLOR_AZUL)
        # Pintar el texto central
        superficie.blit(self.texto_game_over, (self.pos_x, self.pos_y))
        
        # Forzar la actualización visual en la pantalla
        pygame.display.flip()
        
        # Esperar 6 segundos como en el juego original
        pygame.time.delay(6000)
        
        # Reiniciar estadísticas de juego e ir al menú de selección de nivel
        self.motor.reiniciar_estadisticas()
        from src.pantalla_niveles import PantallaNiveles
        self.motor.cambiar_pantalla(PantallaNiveles(self.motor))
