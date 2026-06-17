# -*- coding: utf-8 -*-
"""
Pantalla de menú principal para IndustrialQuest.
"""
import pygame
from src.constantes import COLOR_AZUL, COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla

class PantallaMenu(Pantalla):
    """
    Representa el menú principal del videojuego.
    Maneja una animación fluida de entrada del logotipo y los botones de interacción
    para acceder a las reglas del juego o iniciar la partida.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Cargar y configurar la imagen del logotipo
        self.logo = self.motor.recursos.obtener_imagen("logo.png")
        self.logo = pygame.transform.scale(self.logo, (400, 400))
        # El logo comienza fuera de la pantalla (a la izquierda)
        self.logo_rect = self.logo.get_rect(center=(-200, ALTO_PANTALLA // 3))
        
        # Destino horizontal para centrar el logo
        self.destino_x = ANCHO_PANTALLA // 2 - 200
        self.velocidad_deslizamiento = 5
        self.animacion_completada = False

        # Cargar imágenes de los botones del menú
        self.boton_img = self.motor.recursos.obtener_imagen("Boton.png")
        self.boton_img = pygame.transform.scale(self.boton_img, (200, 50))

        # Configurar la posición física de los rectángulos de botones
        self.boton_reglas = self.boton_img.get_rect(
            topleft=(ANCHO_PANTALLA // 4 - 100, ALTO_PANTALLA // 2 + 100)
        )
        self.boton_niveles = self.boton_img.get_rect(
            topleft=(ANCHO_PANTALLA // 4 * 3 - 100, ALTO_PANTALLA // 2 + 100)
        )

        # Renderizar los textos descriptivos en inglés para los botones
        self.texto_reglas = self.motor.fuente.render("Rules", True, COLOR_NEGRO)
        self.texto_niveles = self.motor.fuente.render("Play the Game", True, COLOR_NEGRO)

    def manejar_eventos(self, eventos):
        # Evitar interacción si la animación del logo de entrada está en curso
        if not self.animacion_completada:
            return

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_reglas.collidepoint(evento.pos):
                    from src.pantalla_reglas import PantallaReglas
                    self.motor.cambiar_pantalla(PantallaReglas(self.motor))
                elif self.boton_niveles.collidepoint(evento.pos):
                    from src.pantalla_niveles import PantallaNiveles
                    self.motor.cambiar_pantalla(PantallaNiveles(self.motor))

    def actualizar(self, dt):
        # Animación de deslizamiento de entrada del logotipo
        if not self.animacion_completada:
            if self.logo_rect.x < self.destino_x:
                self.logo_rect.x += self.velocidad_deslizamiento
                if self.logo_rect.x >= self.destino_x:
                    self.logo_rect.x = self.destino_x
                    self.animacion_completada = True
            else:
                self.animacion_completada = True

    def dibujar(self, superficie):
        # Rellenar el fondo
        superficie.fill(COLOR_AZUL)
        
        # Dibujar el logo
        superficie.blit(self.logo, self.logo_rect)

        # Si la animación terminó, dibujar botones y sus textos correspondientes
        if self.animacion_completada:
            superficie.blit(self.boton_img, self.boton_reglas)
            superficie.blit(self.boton_img, self.boton_niveles)

            # Dibujar el texto centrado del botón "Rules"
            superficie.blit(self.texto_reglas, (self.boton_reglas.x + 60, self.boton_reglas.y + 10))
            # Dibujar el texto centrado del botón "Play the Game"
            superficie.blit(self.texto_niveles, (self.boton_niveles.x + 12, self.boton_niveles.y + 10))

