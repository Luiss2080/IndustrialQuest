# -*- coding: utf-8 -*-
"""
Pantalla que muestra las reglas del juego.
"""
import math
import pygame
from src.constantes import COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla
from src.tooltip import BilingualTooltip

class PantallaReglas(Pantalla):
    """
    Muestra las instrucciones del videojuego en inglés usando fuentes de sistemas
    e interactividad avanzada con engranajes giratorios.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Colores
        self.color_fondo = (30, 22, 18)
        self.color_pergamino = (245, 235, 215)
        self.color_pergamino_borde = (160, 120, 80)
        self.color_texto = (35, 25, 15)
        self.color_titulo = (120, 30, 10)
        self.color_acero = (110, 115, 120)
        self.color_acero_borde = (60, 65, 70)

        # Cargar la imagen del botón volver
        self.boton_img = self.motor.recursos.obtener_imagen("Boton.png")
        self.boton_img = pygame.transform.scale(self.boton_img, (160, 46))
        self.boton_volver = self.boton_img.get_rect(bottomright=(ANCHO_PANTALLA - 30, ALTO_PANTALLA - 30))
        self.texto_volver = self.motor.fuente.render("Clock In", True, COLOR_NEGRO)

        # Configurar rect del manual
        self.rect_manual = pygame.Rect(60, 40, ANCHO_PANTALLA - 120, ALTO_PANTALLA - 120)

        # Contenido de las reglas en inglés
        self.reglas = [
            "RULES OF THE GAME",
            "--------------------------------------------------",
            "1. A phrase with a missing word will appear on the screen.",
            "",
            "2. Type the correct word to score points.",
            "",
            "3. As your score goes up, more phrases will appear on screen.",
            "",
            "4. No contractions allowed.",
            "",
            "5. You lose one life for every phrase missed.",
            "",
            "6. The game ends when you run out of lives."
        ]

        # Animación de entrada (desliza desde la izquierda)
        self.offset_entrada = -600.0
        
        # Engranajes rotatorios
        self.angulo_cogs = 0.0

        # Tooltip
        self.tooltip_volver = BilingualTooltip(self.motor, "Return to Main Menu.", "Volver al Menú Principal.")
        self.volver_hovered = False

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if self.boton_volver.collidepoint(evento.pos):
                        self.motor.reproducir_sonido("Correcta.wav")
                        from src.pantalla_menu import PantallaMenu
                        self.motor.cambiar_pantalla(PantallaMenu(self.motor))
                        return

    def actualizar(self, dt):
        # Deslizamiento de entrada
        self.offset_entrada += (0 - self.offset_entrada) * 0.15
        if abs(self.offset_entrada) < 1:
            self.offset_entrada = 0
            
        # Rotar engranajes
        self.angulo_cogs = (self.angulo_cogs + 0.08 * dt) % 360

        pos_mouse = pygame.mouse.get_pos()
        self.volver_hovered = self.boton_volver.collidepoint(pos_mouse)

    def _dibujar_cog_engranaje(self, superficie, cx, cy, radio, dientes, angulo, color):
        pygame.draw.circle(superficie, color, (cx, cy), radio)
        pygame.draw.circle(superficie, (20, 20, 22), (cx, cy), radio // 3)
        pygame.draw.circle(superficie, color, (cx, cy), radio // 3, 2)
        for i in range(dientes):
            rad_base = math.radians(angulo + i * (360 / dientes))
            rad_desfase = math.radians(angulo + i * (360 / dientes) + (180 / dientes))
            bx = cx + radio * math.cos(rad_base)
            by = cy + radio * math.sin(rad_base)
            px = cx + (radio + 6) * math.cos(rad_desfase)
            py = cy + (radio + 6) * math.sin(rad_desfase)
            nx = cx + radio * math.cos(rad_siguiente := math.radians(angulo + (i + 1) * (360 / dientes)))
            ny = cy + radio * math.sin(rad_siguiente)
            pygame.draw.polygon(superficie, color, [(bx, by), (px, py), (nx, ny)])

    def dibujar(self, superficie):
        superficie.fill(self.color_fondo)
        
        # Marco de acero
        grosor_marco = 15
        pygame.draw.rect(superficie, self.color_acero, (0, 0, ANCHO_PANTALLA, ALTO_PANTALLA), grosor_marco)
        pygame.draw.rect(superficie, self.color_acero_borde, (grosor_marco, grosor_marco, ANCHO_PANTALLA - 2*grosor_marco, ALTO_PANTALLA - 2*grosor_marco), 3)

        # Engranajes en las esquinas
        self._dibujar_cog_engranaje(superficie, 45, 45, 24, 8, self.angulo_cogs, (85, 90, 95))
        self._dibujar_cog_engranaje(superficie, ANCHO_PANTALLA - 45, 45, 24, 8, -self.angulo_cogs, (85, 90, 95))
        self._dibujar_cog_engranaje(superficie, 45, ALTO_PANTALLA - 45, 24, 8, -self.angulo_cogs, (80, 85, 90))
        self._dibujar_cog_engranaje(superficie, ANCHO_PANTALLA - 45, ALTO_PANTALLA - 45, 24, 8, self.angulo_cogs, (80, 85, 90))

        # Posición actual del pergamino (con offset)
        offset_x = int(self.offset_entrada)
        rect_manual_d = self.rect_manual.copy()
        rect_manual_d.x += offset_x

        # Sombra del pergamino
        pygame.draw.rect(superficie, (10, 7, 5), (rect_manual_d.x + 5, rect_manual_d.y + 5, rect_manual_d.width, rect_manual_d.height), border_radius=8)
        # Relleno de papel pergamino
        pygame.draw.rect(superficie, self.color_pergamino, rect_manual_d, border_radius=8)
        # Bordes rústicos
        pygame.draw.rect(superficie, self.color_pergamino_borde, rect_manual_d, 6, border_radius=8)

        # Dibujar textos usando fuente_sistemas para perfecta visualización y soporte de acentos
        sub_superficie_texto = pygame.Surface((self.rect_manual.width - 40, self.rect_manual.height - 40), pygame.SRCALPHA)
        
        y_dibujo = 25
        for linea in self.reglas:
            if linea.startswith("RULES OF THE GAME"):
                color = self.color_titulo
                fuente_render = self.motor.fuente_sistemas_grande
                # Centrar el título de cabecera
                txt_r = fuente_render.render(linea, True, color)
                sub_superficie_texto.blit(txt_r, (sub_superficie_texto.get_width() // 2 - txt_r.get_width() // 2, y_dibujo))
                y_dibujo += 35
                continue
            else:
                color = self.color_texto
                fuente_render = self.motor.fuente_sistemas
                
            txt_r = fuente_render.render(linea, True, color)
            sub_superficie_texto.blit(txt_r, (25, y_dibujo))
            y_dibujo += 26

        superficie.blit(sub_superficie_texto, (rect_manual_d.x + 20, rect_manual_d.y + 20))

        # Dibujar botón volver (Clock In)
        offset = 2 if self.volver_hovered else 0
        rect_volver_dibujo = self.boton_volver.copy()
        rect_volver_dibujo.x += offset
        rect_volver_dibujo.y += offset
        
        superficie.blit(self.boton_img, rect_volver_dibujo)
        tx = rect_volver_dibujo.centerx - self.texto_volver.get_width() // 2
        ty = rect_volver_dibujo.centery - self.texto_volver.get_height() // 2
        superficie.blit(self.texto_volver, (tx, ty))

        # Dibujar tooltips flotantes
        mx, my = pygame.mouse.get_pos()
        if self.volver_hovered:
            self.tooltip_volver.dibujar(superficie, mx, my)
