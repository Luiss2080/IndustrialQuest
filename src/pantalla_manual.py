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
    Manual instructivo de alto contraste que explica los turnos y sus reglas.
    Equipado con tooltips flotantes bilingües de ayuda.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Colores
        self.color_fondo = (30, 22, 18)
        self.color_pergamino = (245, 235, 215)        # Crema claro (alto contraste)
        self.color_pergamino_borde = (160, 120, 80)
        self.color_texto = (35, 25, 15)               # Carbón oscuro legible
        self.color_titulo = (120, 30, 10)              # Rojo oscuro llamativo
        
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
            "  * Shift 4 (Dispatch): Mixed grammar review & questions."
        ]

        # Configurar rect del papel manual para colisión de tooltip
        self.rect_manual = pygame.Rect(40, 30, ANCHO_PANTALLA - 80, ALTO_PANTALLA - 100)
        
        # Tooltips bilingües
        self.tooltip_manual = BilingualTooltip(self.motor, "Review shift operating rules and guidelines.", "Revisa las reglas de turno y las directrices.")
        self.tooltip_volver = BilingualTooltip(self.motor, "Return to Main Menu.", "Volver al Menú Principal.")
        
        self.volver_hovered = False
        self.manual_hovered = False

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if self.boton_volver.collidepoint(evento.pos):
                        self.motor.reproducir_sonido("Correcta.wav")
                        from src.pantalla_menu import PantallaMenu
                        self.motor.cambiar_pantalla(PantallaMenu(self.motor))

    def actualizar(self, dt):
        pos_mouse = pygame.mouse.get_pos()
        self.volver_hovered = self.boton_volver.collidepoint(pos_mouse)
        self.manual_hovered = self.rect_manual.collidepoint(pos_mouse) and not self.volver_hovered

    def dibujar(self, superficie):
        # Rellenar fondo carbón
        superficie.fill(self.color_fondo)
        
        # Sombra del manual
        pygame.draw.rect(superficie, (10, 7, 5), (self.rect_manual.x + 5, self.rect_manual.y + 5, self.rect_manual.width, self.rect_manual.height), border_radius=8)
        # Relleno de papel pergamino
        pygame.draw.rect(superficie, self.color_pergamino, self.rect_manual, border_radius=8)
        # Bordes rústicos
        pygame.draw.rect(superficie, self.color_pergamino_borde, self.rect_manual, 6, border_radius=8)

        # Dibujar texto de las instrucciones
        y = 55
        for linea in self.instrucciones:
            if linea.endswith(":") or linea.startswith("OPERATING"):
                color = self.color_titulo
            else:
                color = self.color_texto
                
            texto_render = self.motor.fuente.render(linea, True, color)
            superficie.blit(texto_render, (70, y))
            y += 32

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
        elif self.manual_hovered:
            self.tooltip_manual.dibujar(superficie, mx, my)
