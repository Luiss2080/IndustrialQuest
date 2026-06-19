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
    Tablero del Registro de Turnos con todos los niveles desbloqueados desde el inicio,
    mostrando claramente el tema, la dificultad y el estado de completado.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Colores
        self.color_fondo = (30, 22, 18)
        self.color_acero = (110, 115, 120)
        self.color_acero_borde = (60, 65, 70)
        
        # Tarjetas de nivel (Pine wood claro para alto contraste)
        self.color_tarjeta = (245, 230, 205)
        self.color_tarjeta_hover = (255, 190, 80)
        self.color_tarjeta_borde = (60, 35, 15)
        
        self.color_texto_oscuro = (25, 15, 5)
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
        
        # Información específica de temática y dificultad de cada nivel
        self.detalles_niveles = {
            "Level 1: Reception Area": {
                "title": "Shift 1: Reception",
                "theme": "Cargo Audit",
                "diff": "Easy",
                "diff_color": (50, 150, 40) # Verde
            },
            "Level 2: Production Area": {
                "title": "Shift 2: Production",
                "theme": "Wood Sawmill",
                "diff": "Medium",
                "diff_color": (180, 120, 20) # Dorado
            },
            "Level 3: Assembly Area": {
                "title": "Shift 3: Assembly",
                "theme": "Furniture Build",
                "diff": "Hard",
                "diff_color": (190, 80, 20) # Naranja
            },
            "Level 4: Quality Control & Dispatch": {
                "title": "Shift 4: Dispatch",
                "theme": "Final Shipment Audit",
                "diff": "Expert",
                "diff_color": (210, 30, 30) # Rojo
            }
        }

        # Inicializar tooltips de niveles
        self.tooltips_niveles = [
            BilingualTooltip(self.motor, "Practice Verb To Be past and present conjugations.", "Practica conjugaciones del verbo To Be pasado y presente."),
            BilingualTooltip(self.motor, "Practice present continuous (be + verb-ing) forms.", "Practica conjugaciones del presente continuo."),
            BilingualTooltip(self.motor, "Practice present simple third person and agreement.", "Practica concordancia del presente simple."),
            BilingualTooltip(self.motor, "Mixed grammar review including question formation.", "Repaso mixto de gramática y estructura de preguntas.")
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
                    
                    # Clic en tarjetas (todos desbloqueados)
                    for i, rect in enumerate(self.rects_tarjetas):
                        if rect.collidepoint(evento.pos):
                            self.motor.reproducir_sonido("Correcta.wav")
                            self.motor.tema_actual = self.nombres_niveles[i]
                            from src.pantalla_juego import PantallaJuego
                            self.motor.cambiar_pantalla(PantallaJuego(self.motor))
                            return

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

        # Dibujar las 4 tarjetas (Todas desbloqueadas por defecto)
        for i, rect in enumerate(self.rects_tarjetas):
            nombre_real = self.nombres_niveles[i]
            detalles = self.detalles_niveles[nombre_real]
            completado = nombre_real in self.motor.niveles_completados
            is_hover = (self.indice_hovered == i)
            
            # Desplazamiento 3D sutil en hover
            offset = 2 if is_hover else 0
            rect_dibujo = rect.copy()
            rect_dibujo.x += offset
            rect_dibujo.y += offset

            # Sombra
            pygame.draw.rect(superficie, (10, 7, 5), (rect.x + 5, rect.y + 5, rect.width, rect.height), border_radius=6)

            # Relleno madera clara
            color_relleno = self.color_tarjeta_hover if is_hover else self.color_tarjeta
            pygame.draw.rect(superficie, color_relleno, rect_dibujo, border_radius=6)
            pygame.draw.rect(superficie, self.color_tarjeta_borde, rect_dibujo, 3, border_radius=6)

            # Clavitos esquineros
            margen_clavo = 6
            pos_clavos = [
                (rect_dibujo.left + margen_clavo, rect_dibujo.top + margen_clavo),
                (rect_dibujo.right - margen_clavo, rect_dibujo.top + margen_clavo),
                (rect_dibujo.left + margen_clavo, rect_dibujo.bottom - margen_clavo),
                (rect_dibujo.right - margen_clavo, rect_dibujo.bottom - margen_clavo)
            ]
            for px, py in pos_clavos:
                pygame.draw.circle(superficie, (90, 50, 20), (px, py), 3)

            # 1. Nombre de Shift
            txt_titulo = self.motor.fuente.render(detalles["title"], True, self.color_texto_oscuro)
            superficie.blit(txt_titulo, (rect_dibujo.x + 18, rect_dibujo.y + 12))

            # 2. Temática del turno
            txt_tematica = self.motor.fuente.render(f"Theme: {detalles['theme']}", True, self.color_texto_desc)
            superficie.blit(txt_tematica, (rect_dibujo.x + 18, rect_dibujo.y + 50))

            # 3. Dificultad (con color diferenciado)
            txt_dificultad_lbl = self.motor.fuente.render("Diff: ", True, self.color_texto_desc)
            superficie.blit(txt_dificultad_lbl, (rect_dibujo.x + 18, rect_dibujo.y + 88))
            
            txt_dificultad_val = self.motor.fuente.render(detalles["diff"], True, detalles["diff_color"])
            superficie.blit(txt_dificultad_val, (rect_dibujo.x + 18 + txt_dificultad_lbl.get_width(), rect_dibujo.y + 88))

            # 4. Estado de completado
            tarea_str = "Status: "
            if completado:
                tarea_str += "COMPLETED ⚙"
                color_estado = (50, 160, 40) # Verde
            else:
                tarea_str += "READY"
                color_estado = (190, 100, 0) # Dorado
                
            txt_estado = self.motor.fuente.render(tarea_str, True, color_estado)
            superficie.blit(txt_estado, (rect_dibujo.x + 18, rect_dibujo.y + 126))

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
