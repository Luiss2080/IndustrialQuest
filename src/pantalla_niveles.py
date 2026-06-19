# -*- coding: utf-8 -*-
"""
Pantalla de selección de turnos (niveles) para IndustrialQuest: Woodwork Edition.
"""
import pygame
from src.constantes import COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla
from src.datos_juego import TEMAS
from src.tooltip import BilingualTooltip

class PantallaNiveles(Pantalla):
    """
    Panel de selección de turnos con tarjetas de madera de alto contraste, locks secuenciales
    y tooltips descriptivos para guiar al estudiante.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Colores
        self.color_fondo = (30, 22, 18)
        self.color_acero = (110, 115, 120)
        self.color_acero_borde = (60, 65, 70)
        
        # Tarjetas de nivel desbloqueadas (Pine wood claro para alto contraste)
        self.color_tarjeta = (245, 230, 205)
        self.color_tarjeta_hover = (255, 190, 80)
        self.color_tarjeta_borde = (60, 35, 15)
        
        # Tarjetas bloqueadas (Gris oscuro moderno y legible)
        self.color_tarjeta_bloqueada = (95, 100, 105)
        self.color_tarjeta_bloqueada_borde = (55, 60, 65)
        
        self.color_texto_oscuro = (25, 15, 5)          # Texto para tarjetas activas
        self.color_texto_claro = (240, 240, 240)       # Texto para tarjetas bloqueadas
        self.color_texto_desc = (65, 50, 40)

        # Botón volver
        self.boton_img = self.motor.recursos.obtener_imagen("Boton.png")
        self.boton_img = pygame.transform.scale(self.boton_img, (160, 46))
        self.boton_volver = self.boton_img.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA - 40))
        self.texto_volver = self.motor.fuente.render("Clock In", True, COLOR_NEGRO)

        # Configurar tarjetas de nivel
        self.nombres_niveles = list(TEMAS.keys())
        self.rects_tarjetas = [
            pygame.Rect(80, 110, 300, 170),
            pygame.Rect(420, 110, 300, 170),
            pygame.Rect(80, 305, 300, 170),
            pygame.Rect(420, 305, 300, 170)
        ]
        
        # Versiones ultra cortas de las reglas gramaticales para evitar overflow
        self.reglas_cortas = {
            "Level 1: Reception Area": "Verb To Be (am, is, are...)",
            "Level 2: Production Area": "Present Continuous (verb-ing)",
            "Level 3: Assembly Area": "Present Simple (base or -s)",
            "Level 4: Quality Control & Dispatch": "Mixed Review & Questions"
        }

        # Inicializar tooltips de niveles
        self.tooltips_niveles = [
            BilingualTooltip(self.motor, "Reception Area: Practice verb To Be past and present.", "Área de Recepción: Practica el verbo To Be pasado y presente."),
            BilingualTooltip(self.motor, "Production Line: Practice present continuous conjugations.", "Línea de Producción: Practica conjugaciones del presente continuo."),
            BilingualTooltip(self.motor, "Assembly Zone: Practice present simple subject agreement.", "Zona de Ensamblaje: Practica concordancia del presente simple."),
            BilingualTooltip(self.motor, "Dispatch Center: Mixed review of all grammar rules.", "Centro de Despacho: Repaso mixto de todas las reglas gramaticales.")
        ]
        
        self.tooltip_volver = BilingualTooltip(self.motor, "Return to Main Menu.", "Volver al Menú Principal.")

        # Estado de hover
        self.indice_hovered = -1
        self.volver_hovered = False

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    # Clic en volver
                    if self.boton_volver.collidepoint(evento.pos):
                        self.motor.reproducir_sonido("Correcta.wav")
                        from src.pantalla_menu import PantallaMenu
                        self.motor.cambiar_pantalla(PantallaMenu(self.motor))
                        return
                    
                    # Clic en tarjetas
                    for i, rect in enumerate(self.rects_tarjetas):
                        if rect.collidepoint(evento.pos):
                            if self._esta_desbloqueado(i):
                                self.motor.reproducir_sonido("Correcta.wav")
                                self.motor.tema_actual = self.nombres_niveles[i]
                                from src.pantalla_juego import PantallaJuego
                                self.motor.cambiar_pantalla(PantallaJuego(self.motor))
                            else:
                                self.motor.reproducir_sonido("equivocado.wav")
                            return

    def _esta_desbloqueado(self, indice):
        if indice == 0:
            return True
        nivel_previo = self.nombres_niveles[indice - 1]
        return nivel_previo in self.motor.niveles_completados

    def actualizar(self, dt):
        pos_mouse = pygame.mouse.get_pos()
        
        # Hover tarjetas
        hover_actual = -1
        for i, rect in enumerate(self.rects_tarjetas):
            if rect.collidepoint(pos_mouse):
                hover_actual = i
                break
        self.indice_hovered = hover_actual

        # Hover volver
        self.volver_hovered = self.boton_volver.collidepoint(pos_mouse)

    def dibujar(self, superficie):
        # Fondo oscuro
        superficie.fill(self.color_fondo)

        # Marco de acero
        grosor_marco = 15
        pygame.draw.rect(superficie, self.color_acero, (0, 0, ANCHO_PANTALLA, ALTO_PANTALLA), grosor_marco)
        pygame.draw.rect(superficie, self.color_acero_borde, (grosor_marco, grosor_marco, ANCHO_PANTALLA - 2*grosor_marco, ALTO_PANTALLA - 2*grosor_marco), 3)

        # Título
        titulo_render = self.motor.fuente.render("FACTORY SHIFT REGISTRY", True, (255, 220, 80))
        superficie.blit(titulo_render, (ANCHO_PANTALLA // 2 - titulo_render.get_width() // 2, 35))

        # Dibujar las 4 tarjetas
        for i, rect in enumerate(self.rects_tarjetas):
            desbloqueado = self._esta_desbloqueado(i)
            completado = self.nombres_niveles[i] in self.motor.niveles_completados
            is_hover = (self.indice_hovered == i)
            
            # Desplazamiento 3D sutil en hover si está activo
            offset = 2 if (is_hover and desbloqueado) else 0
            rect_dibujo = rect.copy()
            rect_dibujo.x += offset
            rect_dibujo.y += offset

            # Sombra
            pygame.draw.rect(superficie, (10, 7, 5), (rect.x + 5, rect.y + 5, rect.width, rect.height), border_radius=6)

            # Color del tablón de nivel
            if not desbloqueado:
                color_relleno = self.color_tarjeta_bloqueada
                color_borde = self.color_tarjeta_bloqueada_borde
            elif is_hover:
                color_relleno = self.color_tarjeta_hover
                color_borde = self.color_tarjeta_borde
            else:
                color_relleno = self.color_tarjeta
                color_borde = self.color_tarjeta_borde
                
            pygame.draw.rect(superficie, color_relleno, rect_dibujo, border_radius=6)
            pygame.draw.rect(superficie, color_borde, rect_dibujo, 3, border_radius=6)

            # Clavitos esquineros
            margen_clavo = 6
            pos_clavos = [
                (rect_dibujo.left + margen_clavo, rect_dibujo.top + margen_clavo),
                (rect_dibujo.right - margen_clavo, rect_dibujo.top + margen_clavo),
                (rect_dibujo.left + margen_clavo, rect_dibujo.bottom - margen_clavo),
                (rect_dibujo.right - margen_clavo, rect_dibujo.bottom - margen_clavo)
            ]
            for px, py in pos_clavos:
                color_clavo = (60, 60, 65) if not desbloqueado else (90, 50, 20)
                pygame.draw.circle(superficie, color_clavo, (px, py), 3)

            # Textos legibles de alta visibilidad
            # 1. Nombre de Shift
            nombre_corto = self.nombres_niveles[i].replace("Level ", "Shift ")
            color_titulo = self.color_texto_oscuro if desbloqueado else self.color_texto_claro
            txt_titulo = self.motor.fuente.render(nombre_corto, True, color_titulo)
            superficie.blit(txt_titulo, (rect_dibujo.x + 18, rect_dibujo.y + 18))

            # 2. Regla gramatical (Cortada)
            regla_str = self.reglas_cortas[self.nombres_niveles[i]]
            color_regla = self.color_texto_desc if desbloqueado else (190, 190, 195)
            txt_regla = self.motor.fuente.render(regla_str, True, color_regla)
            superficie.blit(txt_regla, (rect_dibujo.x + 18, rect_dibujo.y + 58))

            # 3. Estado de progreso
            tarea_str = "Status: "
            if not desbloqueado:
                tarea_str += "LOCKED"
                color_estado = (240, 100, 100) # Rojo claro visible
            elif completado:
                tarea_str += "COMPLETED ⚙️"
                color_estado = (50, 160, 40)   # Verde legible
            else:
                tarea_str += "READY"
                color_estado = (190, 100, 0)   # Naranja-marrón legible
                
            txt_estado = self.motor.fuente.render(tarea_str, True, color_estado)
            superficie.blit(txt_estado, (rect_dibujo.x + 18, rect_dibujo.y + 105))

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
        if self.indice_hovered != -1:
            self.tooltips_niveles[self.indice_hovered].dibujar(superficie, mx, my)
        elif self.volver_hovered:
            self.tooltip_volver.dibujar(superficie, mx, my)
