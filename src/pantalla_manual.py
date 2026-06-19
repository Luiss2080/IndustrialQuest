# -*- coding: utf-8 -*-
"""
Pantalla del Manual de Operaciones para IndustrialQuest: Woodwork Edition.
"""
import pygame
from src.constantes import COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla
from src.tooltip import BilingualTooltip

class PantallaManual(Pantalla):
    """
    Manual instructivo de alto contraste que incorpora barra de desplazamiento (scroll)
    arrastrable y soporte de rueda del ratón para facilitar la lectura.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Colores
        self.color_fondo = (30, 22, 18)
        self.color_pergamino = (245, 235, 215)
        self.color_pergamino_borde = (160, 120, 80)
        self.color_texto = (35, 25, 15)
        self.color_titulo = (120, 30, 10)
        
        self.boton_img = self.motor.recursos.obtener_imagen("Boton.png")
        self.boton_img = pygame.transform.scale(self.boton_img, (160, 46))
        self.boton_volver = self.boton_img.get_rect(bottomright=(ANCHO_PANTALLA - 30, ALTO_PANTALLA - 30))
        self.texto_volver = self.motor.fuente.render("Clock In", True, COLOR_NEGRO)

        # Contenido instructivo extendido (con más líneas para probar el scroll)
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
        self.rect_manual = pygame.Rect(40, 30, ANCHO_PANTALLA - 80, ALTO_PANTALLA - 100)
        
        # Sistema de Scroll (Desplazamiento)
        self.scroll_y = 0
        self.alto_linea = 32
        self.margen_y_texto = 30
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
            # Control de arrastre del scrollbar
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
                
                # Rueda del ratón (Mouse wheel scroll)
                elif evento.button == 4: # Scroll Up
                    self.scroll_y = max(0, self.scroll_y - 25)
                elif evento.button == 5: # Scroll Down
                    self.scroll_y = min(self.max_scroll_y, self.scroll_y + 25)
                    
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    self.drag_scrollbar = False
                    
            elif evento.type == pygame.MOUSEMOTION:
                if self.drag_scrollbar:
                    # Calcular posición del scroll según arrastre del cursor
                    rel_y = evento.pos[1] - self.rect_track.top - 20
                    alto_rango = self.rect_track.height - 40
                    if alto_rango > 0:
                        porcentaje = max(0.0, min(1.0, rel_y / alto_rango))
                        self.scroll_y = porcentaje * self.max_scroll_y

    def _obtener_handle_rect(self):
        """Calcula las coordenadas de la barra deslizante (thumb/handle) del scrollbar."""
        alto_rango = self.rect_track.height - 40
        if self.max_scroll_y > 0:
            porcentaje = self.scroll_y / self.max_scroll_y
            handle_y = self.rect_track.top + porcentaje * alto_rango
        else:
            handle_y = self.rect_track.top
        return pygame.Rect(self.rect_track.x - 2, handle_y, 14, 40)

    def actualizar(self, dt):
        pos_mouse = pygame.mouse.get_pos()
        self.volver_hovered = self.boton_volver.collidepoint(pos_mouse)
        self.manual_hovered = self.rect_manual.collidepoint(pos_mouse) and not self.volver_hovered

    def dibujar(self, superficie):
        # Fondo carbón oscuro
        superficie.fill(self.color_fondo)
        
        # Sombra del manual
        pygame.draw.rect(superficie, (10, 7, 5), (self.rect_manual.x + 5, self.rect_manual.y + 5, self.rect_manual.width, self.rect_manual.height), border_radius=8)
        # Relleno de papel pergamino
        pygame.draw.rect(superficie, self.color_pergamino, self.rect_manual, border_radius=8)
        # Bordes rústicos
        pygame.draw.rect(superficie, self.color_pergamino_borde, self.rect_manual, 6, border_radius=8)

        # Dibujar textos recortados por el área visible (usar clip rect para no salirse de la caja)
        sub_superficie_texto = pygame.Surface((self.rect_manual.width - 40, self.rect_manual.height - 40), pygame.SRCALPHA)
        
        y_dibujo = 15 - self.scroll_y
        for linea in self.instrucciones:
            if linea.endswith(":") or linea.startswith("OPERATING"):
                color = self.color_titulo
            else:
                color = self.color_texto
                
            texto_render = self.motor.fuente.render(linea, True, color)
            sub_superficie_texto.blit(texto_render, (15, y_dibujo))
            y_dibujo += self.alto_linea

        superficie.blit(sub_superficie_texto, (self.rect_manual.x + 10, self.rect_manual.y + 15))

        # Dibujar barra de desplazamiento (Scrollbar) si el contenido supera el área visible
        if self.max_scroll_y > 0:
            # Canal del scrollbar (track)
            pygame.draw.rect(superficie, (200, 190, 175), self.rect_track, border_radius=3)
            pygame.draw.rect(superficie, (170, 160, 145), self.rect_track, 1, border_radius=3)
            
            # Manija del scrollbar (handle/thumb)
            handle_rect = self._obtener_handle_rect()
            pygame.draw.rect(superficie, (110, 115, 120), handle_rect, border_radius=4)
            pygame.draw.rect(superficie, (60, 65, 70), handle_rect, 2, border_radius=4)
            # Líneas del grip
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
