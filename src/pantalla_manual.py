# -*- coding: utf-8 -*-
"""
Pantalla del Manual de Operaciones para IndustrialQuest: Woodwork Edition.
"""
import pygame
from src.constantes import COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla

class PantallaManual(Pantalla):
    """
    Muestra las instrucciones detalladas del juego y las reglas gramaticales de cada nivel.
    Renderea un manual estilo papel antiguo/madera con botones de navegación.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Colores
        self.color_fondo = (35, 25, 20)
        self.color_pergamino = (240, 220, 180)
        self.color_pergamino_borde = (190, 160, 110)
        self.color_texto = (40, 30, 20)
        self.color_titulo = (120, 40, 10)
        
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

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if self.boton_volver.collidepoint(evento.pos):
                        self.motor.reproducir_sonido("Correcta.wav")
                        from src.pantalla_menu import PantallaMenu
                        self.motor.cambiar_pantalla(PantallaMenu(self.motor))

    def actualizar(self, dt):
        pass

    def dibujar(self, superficie):
        # Rellenar fondo carbón
        superficie.fill(self.color_fondo)
        
        # Dibujar marco de pergamino/madera rústica central
        ancho_manual = ANCHO_PANTALLA - 80
        alto_manual = ALTO_PANTALLA - 100
        rect_manual = pygame.Rect(40, 30, ancho_manual, alto_manual)
        
        # Sombra del manual
        pygame.draw.rect(superficie, (15, 10, 5), (45, 35, ancho_manual, alto_manual), border_radius=8)
        # Relleno de papel pergamino
        pygame.draw.rect(superficie, self.color_pergamino, rect_manual, border_radius=8)
        # Bordes rústicos
        pygame.draw.rect(superficie, self.color_pergamino_borde, rect_manual, 6, border_radius=8)

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
        # Hover check
        mouse_pos = pygame.mouse.get_pos()
        offset = 2 if self.boton_volver.collidepoint(mouse_pos) else 0
        
        rect_volver_dibujo = self.boton_volver.copy()
        rect_volver_dibujo.x += offset
        rect_volver_dibujo.y += offset
        
        superficie.blit(self.boton_img, rect_volver_dibujo)
        tx = rect_volver_dibujo.centerx - self.texto_volver.get_width() // 2
        ty = rect_volver_dibujo.centery - self.texto_volver.get_height() // 2
        superficie.blit(self.texto_volver, (tx, ty))
