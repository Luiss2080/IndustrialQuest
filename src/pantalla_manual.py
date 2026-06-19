# -*- coding: utf-8 -*-
"""
Pantalla del Manual de Operaciones para IndustrialQuest: Woodwork Edition.
"""
import math
import pygame
from src.constantes import COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla
from src.tooltip import BilingualTooltip

class PantallaManual(Pantalla):
    """
    Manual instructivo con barra de desplazamiento (scroll) arrastrable, soporte de rueda de ratón,
    engranajes mecánicos decorativos y animaciones de deslizamiento.
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
        
        self.boton_img = self.motor.recursos.obtener_imagen("Boton.png")
        self.boton_img = pygame.transform.scale(self.boton_img, (160, 46))
        self.boton_volver = self.boton_img.get_rect(bottomright=(ANCHO_PANTALLA - 30, ALTO_PANTALLA - 30))
        self.texto_volver = self.motor.fuente.render("Clock In", True, COLOR_NEGRO)

        # Contenido instructivo
        self.instrucciones = [
            "OPERATING MANUAL: INDUSTRIALQUEST",
            "--------------------------------------------------",
            "1. INSTRUCTIONS:",
            "  * Wooden planks with sentences scroll on conveyor belts.",
            "  * Type the correct word/conjugation before the wood hits",
            "    the rotating saw blades at the right edge.",
            "  * Pressing keys carves/burns letters directly into the wood.",
            "  * Hitting the saw blades splinters the wood and costs 1 Life.",
            "  * Complete 15 planks correctly to successfully finish a shift.",
            "",
            "2. SHIFTS AND GRAMMAR RULES:",
            "  * Shift 1 (Reception): Verb To Be (am, is, are, was, were).",
            "  * Shift 2 (Production): Present Continuous (e.g., 'am checking').",
            "  * Shift 3 (Assembly): Present Simple action verbs (e.g., 'checks').",
            "  * Shift 4 (Dispatch): Mixed grammar review & questions.",
            "",
            "3. REGULATION & COMPLIANCE:",
            "  * Safety helmets are mandatory in all factory zones.",
            "  * Report machinery malfunction to supervisor immediately.",
            "  * Maintain workspace clean and free of sawdust.",
            "  * Happy woodworking! IndustrialQuest (c) 2026."
        ]

        # Configurar rect del manual
        self.rect_manual = pygame.Rect(60, 40, ANCHO_PANTALLA - 120, ALTO_PANTALLA - 120)
        
        # Animación de entrada (desliza desde la izquierda)
        self.offset_entrada = -600.0
        
        # Engranajes rotatorios
        self.angulo_cogs = 0.0

        # Sistema de Scroll
        self.scroll_y = 0
        self.alto_linea = 28
        self.alto_contenido = len(self.instrucciones) * self.alto_linea + 50
        self.alto_visible = self.rect_manual.height - 40
        self.max_scroll_y = max(0, self.alto_contenido - self.alto_visible)

        # Barra de desplazamiento (Scrollbar)
        self.rect_track = pygame.Rect(self.rect_manual.right - 20, self.rect_manual.top + 15, 10, self.rect_manual.height - 30)
        self.drag_scrollbar = False

        # Tooltips bilingües
        self.tooltip_manual = BilingualTooltip(self.motor, "Scroll down using mouse wheel or scrollbar.", "Desplázate hacia abajo usando la rueda o barra.")
        self.tooltip_volver = BilingualTooltip(self.motor, "Return to Main Menu.", "Volver al Menú Principal.")
        
        self.volver_hovered = False
        self.manual_hovered = False

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: # Clic izquierdo
                    # Verificar clic en volver
                    if self.boton_volver.collidepoint(evento.pos):
                        self.motor.reproducir_sonido("Correcta.wav")
                        from src.pantalla_menu import PantallaMenu
                        self.motor.cambiar_pantalla(PantallaMenu(self.motor))
                        return
                    
                    # Verificar clic en handle del scrollbar
                    handle_rect = self._obtener_handle_rect()
                    if handle_rect.collidepoint(evento.pos):
                        self.drag_scrollbar = True
                
                # Rueda del ratón
                elif evento.button == 4: # Scroll Up
                    self.scroll_y = max(0, self.scroll_y - 20)
                elif evento.button == 5: # Scroll Down
                    self.scroll_y = min(self.max_scroll_y, self.scroll_y + 20)
                    
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    self.drag_scrollbar = False
                    
            elif evento.type == pygame.MOUSEMOTION:
                if self.drag_scrollbar:
                    rel_y = evento.pos[1] - self.rect_track.top - 20
                    alto_rango = self.rect_track.height - 40
                    if alto_rango > 0:
                        porcentaje = max(0.0, min(1.0, rel_y / alto_rango))
                        self.scroll_y = porcentaje * self.max_scroll_y

    def _obtener_handle_rect(self):
        alto_rango = self.rect_track.height - 40
        if self.max_scroll_y > 0:
            porcentaje = self.scroll_y / self.max_scroll_y
            handle_y = self.rect_track.top + porcentaje * alto_rango
        else:
            handle_y = self.rect_track.top
        return pygame.Rect(self.rect_track.x - 2, handle_y, 14, 40)

    def actualizar(self, dt):
        # Deslizamiento de entrada
        self.offset_entrada += (0 - self.offset_entrada) * 0.15
        if abs(self.offset_entrada) < 1:
            self.offset_entrada = 0
            
        # Rotar engranajes
        self.angulo_cogs = (self.angulo_cogs + 0.08 * dt) % 360

        pos_mouse = pygame.mouse.get_pos()
        self.volver_hovered = self.boton_volver.collidepoint(pos_mouse)
        
        rect_actual = self.rect_manual.copy()
        rect_actual.x += int(self.offset_entrada)
        self.manual_hovered = rect_actual.collidepoint(pos_mouse) and not self.volver_hovered

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

        # Posición actual del manual (con offset)
        offset_x = int(self.offset_entrada)
        rect_manual_d = self.rect_manual.copy()
        rect_manual_d.x += offset_x

        # Sombra del manual
        pygame.draw.rect(superficie, (10, 7, 5), (rect_manual_d.x + 5, rect_manual_d.y + 5, rect_manual_d.width, rect_manual_d.height), border_radius=8)
        # Relleno de papel pergamino
        pygame.draw.rect(superficie, self.color_pergamino, rect_manual_d, border_radius=8)
        # Bordes rústicos
        pygame.draw.rect(superficie, self.color_pergamino_borde, rect_manual_d, 6, border_radius=8)

        # Dibujar textos usando fuente_sistemas para perfecta visualización y soporte de acentos
        sub_superficie_texto = pygame.Surface((self.rect_manual.width - 40, self.rect_manual.height - 40), pygame.SRCALPHA)
        
        y_dibujo = 15 - self.scroll_y
        for linea in self.instrucciones:
            if linea.endswith(":") or linea.startswith("OPERATING"):
                color = self.color_titulo
                fuente_render = self.motor.fuente_sistemas_grande
                # Centrar el título de cabecera
                if linea.startswith("OPERATING"):
                    txt_r = fuente_render.render(linea, True, color)
                    sub_superficie_texto.blit(txt_r, (sub_superficie_texto.get_width() // 2 - txt_r.get_width() // 2, y_dibujo))
                    y_dibujo += self.alto_linea + 5
                    continue
            else:
                color = self.color_texto
                fuente_render = self.motor.fuente_sistemas
                
            txt_r = fuente_render.render(linea, True, color)
            sub_superficie_texto.blit(txt_r, (20, y_dibujo))
            y_dibujo += self.alto_linea

        superficie.blit(sub_superficie_texto, (rect_manual_d.x + 15, rect_manual_d.y + 15))

        # Dibujar barra de desplazamiento (Scrollbar) si es necesario
        if self.max_scroll_y > 0:
            rect_track_d = self.rect_track.copy()
            rect_track_d.x += offset_x
            pygame.draw.rect(superficie, (200, 190, 175), rect_track_d, border_radius=3)
            pygame.draw.rect(superficie, (170, 160, 145), rect_track_d, 1, border_radius=3)
            
            handle_rect = self._obtener_handle_rect()
            handle_rect.x += offset_x
            pygame.draw.rect(superficie, (110, 115, 120), handle_rect, border_radius=4)
            pygame.draw.rect(superficie, (60, 65, 70), handle_rect, 2, border_radius=4)
            pygame.draw.line(superficie, (200, 200, 200), (handle_rect.centerx - 3, handle_rect.centery - 4), (handle_rect.centerx + 3, handle_rect.centery - 4), 2)
            pygame.draw.line(superficie, (200, 200, 200), (handle_rect.centerx - 3, handle_rect.centery), (handle_rect.centerx + 3, handle_rect.centery), 2)
            pygame.draw.line(superficie, (200, 200, 200), (handle_rect.centerx - 3, handle_rect.centery + 4), (handle_rect.centerx + 3, handle_rect.centery + 4), 2)

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
        elif self.manual_hovered and self.max_scroll_y > 0:
            self.tooltip_manual.dibujar(superficie, mx, my)
