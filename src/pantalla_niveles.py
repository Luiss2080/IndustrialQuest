# -*- coding: utf-8 -*-
"""
Pantalla de selección de turnos (niveles) para IndustrialQuest: Woodwork Edition.
"""
import math
import pygame
from src.constantes import COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla
from src.datos_juego import TEMAS
from src.tooltip import BilingualTooltip

class PantallaNiveles(Pantalla):
    """
    Tablero interactivo del Registro de Turnos. Cuenta con animaciones de deslizamiento,
    resalte de selección, engranajes giratorios y un reloj de fábrica temático.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Colores rústicos y metálicos
        self.color_fondo = (30, 22, 18)
        self.color_acero = (110, 115, 120)
        self.color_acero_borde = (60, 65, 70)
        self.color_bronce = (180, 140, 70)
        
        # Madera clara para las tarjetas
        self.color_tarjeta = (245, 230, 205)
        self.color_tarjeta_hover = (255, 200, 100)
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
        
        # Animación de entrada (desplazamiento horizontal inicial)
        # Las tarjetas izquierdas (0, 2) vienen de la izquierda (-450), las derechas de la derecha (+450)
        self.offsets_entrada = [-450, 450, -450, 450]
        
        # Ángulo para la animación de rotación de engranajes
        self.angulo_cogs = 0.0

        # Detalles para la visualización de tarjetas
        self.detalles_niveles = {
            "Level 1: Reception Area": {
                "title": "Shift 1: Reception",
                "theme": "Cargo Audit",
                "Verb To Be": "(Present & Past)",
                "diff_color": (35, 140, 30)
            },
            "Level 2: Production Area": {
                "title": "Shift 2: Production",
                "theme": "Wood Sawmill",
                "Present": "Continuous",
                "diff_color": (160, 105, 15)
            },
            "Level 3: Assembly Area": {
                "title": "Shift 3: Assembly",
                "theme": "Furniture Build",
                "Present": "Simple",
                "diff_color": (190, 75, 15)
            },
            "Level 4: Quality Control & Dispatch": {
                "title": "Shift 4: Dispatch",
                "theme": "Final Shipment Audit",
                "diff": "Expert",
                "diff_color": (210, 25, 25)
            }
        }

        # Inicializar tooltips bilingües
        self.tooltips_niveles = [
            BilingualTooltip(self.motor, "Practice Verb To Be past and present conjugations.", "Practica conjugaciones del verbo To Be pasado y presente."),
            BilingualTooltip(self.motor, "Practice present continuous (be + verb-ing) forms.", "Practica conjugaciones del presente continuo."),
            BilingualTooltip(self.motor, "Practice present simple third person and agreement.", "Practica concordancia del presente simple."),
            BilingualTooltip(self.motor, "Mixed grammar review including question formation.", "Repaso mixto de gramática y estructura de preguntas.")
        ]
        self.tooltip_volver = BilingualTooltip(self.motor, "Return to Main Menu.", "Volver al Menú Principal.")

        # Estado de hover e interacción
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
                    
                    # Clic en una tarjeta de nivel
                    for i, rect in enumerate(self.rects_tarjetas):
                        # Solo permitir clic si ya ha terminado casi de deslizarse
                        if abs(self.offsets_entrada[i]) < 10:
                            # Calcular posición actual con offset
                            rect_actual = rect.copy()
                            rect_actual.x += int(self.offsets_entrada[i])
                            if rect_actual.collidepoint(evento.pos):
                                self.motor.reproducir_sonido("Correcta.wav")
                                self.motor.tema_actual = self.nombres_niveles[i]
                                from src.pantalla_juego import PantallaJuego
                                self.motor.cambiar_pantalla(PantallaJuego(self.motor))
                                return

    def actualizar(self, dt):
        # Actualizar animaciones de entrada (interpolación suave)
        for i in range(4):
            self.offsets_entrada[i] += (0 - self.offsets_entrada[i]) * 0.15
            if abs(self.offsets_entrada[i]) < 1:
                self.offsets_entrada[i] = 0
        
        # Rotar engranajes decorativos
        self.angulo_cogs = (self.angulo_cogs + 0.08 * dt) % 360

        # Hover de ratón
        pos_mouse = pygame.mouse.get_pos()
        
        hover_actual = -1
        for i, rect in enumerate(self.rects_tarjetas):
            rect_actual = rect.copy()
            rect_actual.x += int(self.offsets_entrada[i])
            if rect_actual.collidepoint(pos_mouse):
                hover_actual = i
                break
        self.indice_hovered = hover_actual
        self.volver_hovered = self.boton_volver.collidepoint(pos_mouse)

    def _dibujar_cog_engranaje(self, superficie, cx, cy, radio, dientes, angulo, color):
        """Dibuja un engranaje metálico animado en la pantalla."""
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
            
            rad_siguiente = math.radians(angulo + (i + 1) * (360 / dientes))
            nx = cx + radio * math.cos(rad_siguiente)
            ny = cy + radio * math.sin(rad_siguiente)
            
            pygame.draw.polygon(superficie, color, [(bx, by), (px, py), (nx, ny)])

    def _dibujar_reloj_fabrica(self, superficie, cx, cy, radio):
        """Dibuja un reloj de pared industrial animado en la parte superior."""
        # Sombra
        pygame.draw.circle(superficie, (10, 10, 12), (cx + 3, cy + 3), radio)
        # Marco de bronce
        pygame.draw.circle(superficie, self.color_bronce, (cx, cy), radio)
        pygame.draw.circle(superficie, (90, 70, 30), (cx, cy), radio, 3)
        # Esfera blanca
        pygame.draw.circle(superficie, (245, 240, 230), (cx, cy), radio - 5)
        
        # Ticks del reloj (12 marcas)
        for i in range(12):
            rad = math.radians(i * 30)
            x_b = cx + (radio - 9) * math.cos(rad)
            y_b = cy + (radio - 9) * math.sin(rad)
            x_e = cx + (radio - 5) * math.cos(rad)
            y_e = cy + (radio - 5) * math.sin(rad)
            pygame.draw.line(superficie, COLOR_NEGRO, (x_b, y_b), (x_e, y_e), 2)
            
        # Manecillas animadas (simuladas por tiempo)
        ticks = pygame.time.get_ticks()
        ang_min = (ticks * 0.05) % 360
        ang_hor = (ticks * 0.004) % 360
        
        # Minutero
        mx = cx + (radio - 12) * math.cos(math.radians(ang_min - 90))
        my = cy + (radio - 12) * math.sin(math.radians(ang_min - 90))
        pygame.draw.line(superficie, (40, 40, 45), (cx, cy), (mx, my), 2)
        
        # Horero
        hx = cx + (radio - 18) * math.cos(math.radians(ang_hor - 90))
        hy = cy + (radio - 18) * math.sin(math.radians(ang_hor - 90))
        pygame.draw.line(superficie, COLOR_NEGRO, (cx, cy), (hx, hy), 3)
        
        # Remache central
        pygame.draw.circle(superficie, (180, 40, 40), (cx, cy), 3)

    def dibujar(self, superficie):
        # Fondo oscuro de madera/fábrica
        superficie.fill(self.color_fondo)

        # Marco de acero
        grosor_marco = 15
        pygame.draw.rect(superficie, self.color_acero, (0, 0, ANCHO_PANTALLA, ALTO_PANTALLA), grosor_marco)
        pygame.draw.rect(superficie, self.color_acero_borde, (grosor_marco, grosor_marco, ANCHO_PANTALLA - 2*grosor_marco, ALTO_PANTALLA - 2*grosor_marco), 3)

        # Engranajes animados en las esquinas
        self._dibujar_cog_engranaje(superficie, 45, 45, 24, 8, self.angulo_cogs, (85, 90, 95))
        self._dibujar_cog_engranaje(superficie, ANCHO_PANTALLA - 45, 45, 24, 8, -self.angulo_cogs, (85, 90, 95))
        self._dibujar_cog_engranaje(superficie, 45, ALTO_PANTALLA - 45, 24, 8, -self.angulo_cogs, (80, 85, 90))
        self._dibujar_cog_engranaje(superficie, ANCHO_PANTALLA - 45, ALTO_PANTALLA - 45, 24, 8, self.angulo_cogs, (80, 85, 90))

        # Título centrado
        titulo_render = self.motor.fuente.render("FACTORY SHIFT REGISTRY", True, (255, 220, 80))
        superficie.blit(titulo_render, (ANCHO_PANTALLA // 2 - titulo_render.get_width() // 2 - 30, 35))

        # Reloj de fábrica a la derecha del título
        self._dibujar_reloj_fabrica(superficie, ANCHO_PANTALLA // 2 + titulo_render.get_width() // 2 + 15, 48, 22)

        # Dibujar las 4 tarjetas con animaciones
        for i, rect in enumerate(self.rects_tarjetas):
            nombre_real = self.nombres_niveles[i]
            detalles = self.detalles_niveles[nombre_real]
            completado = nombre_real in self.motor.niveles_completados
            is_hover = (self.indice_hovered == i)
            
            # Aplicar offset de entrada
            offset_x = int(self.offsets_entrada[i])
            rect_dibujo = rect.copy()
            rect_dibujo.x += offset_x
            
            # Sutil escalado o desplazamiento en hover
            if is_hover:
                rect_dibujo.inflate_ip(6, 6) # Crece 6px
            
            # Dibujar Sombra
            pygame.draw.rect(superficie, (10, 7, 5), (rect_dibujo.x + 5, rect_dibujo.y + 5, rect_dibujo.width, rect_dibujo.height), border_radius=6)

            # Relleno de madera
            color_relleno = self.color_tarjeta_hover if is_hover else self.color_tarjeta
            pygame.draw.rect(superficie, color_relleno, rect_dibujo, border_radius=6)
            
            # Borde (Dorado en hover, oscuro normal)
            color_borde = self.color_bronce if is_hover else self.color_tarjeta_borde
            grosor_borde = 4 if is_hover else 2
            pygame.draw.rect(superficie, color_borde, rect_dibujo, grosor_borde, border_radius=6)

            # Clavitos decorativos en esquinas de tarjetas
            margen_clavo = 8
            pos_clavos = [
                (rect_dibujo.left + margen_clavo, rect_dibujo.top + margen_clavo),
                (rect_dibujo.right - margen_clavo, rect_dibujo.top + margen_clavo),
                (rect_dibujo.left + margen_clavo, rect_dibujo.bottom - margen_clavo),
                (rect_dibujo.right - margen_clavo, rect_dibujo.bottom - margen_clavo)
            ]
            for px, py in pos_clavos:
                pygame.draw.circle(superficie, (90, 50, 20), (px, py), 3)

            # --- Textos Centrados usando fuente_sistemas de alta legibilidad ---
            cx = rect_dibujo.centerx
            
            # 1. Nombre de Shift (Negrita destacado)
            txt_titulo = self.motor.fuente_sistemas_grande.render(detalles["title"], True, self.color_texto_oscuro)
            superficie.blit(txt_titulo, (cx - txt_titulo.get_width() // 2, rect_dibujo.y + 15))

            # Línea decorativa divisoria en el tablón
            pygame.draw.line(superficie, (160, 120, 80), (rect_dibujo.left + 25, rect_dibujo.y + 52), (rect_dibujo.right - 25, rect_dibujo.y + 52), 1)

            # 2. Temática del turno
            txt_tematica = self.motor.fuente_sistemas.render(f"Zone: {detalles['theme']}", True, self.color_texto_desc)
            superficie.blit(txt_tematica, (cx - txt_tematica.get_width() // 2, rect_dibujo.y + 60))

            # 3. Dificultad
            diff_label = "Difficulty: "
            w_lbl = self.motor.fuente_sistemas.size(diff_label)[0]
            txt_diff_lbl = self.motor.fuente_sistemas.render(diff_label, True, self.color_texto_desc)
            txt_diff_val = self.motor.fuente_sistemas.render(detalles["diff"], True, detalles["diff_color"])
            
            total_diff_w = w_lbl + txt_diff_val.get_width()
            pos_x_lbl = cx - total_diff_w // 2
            superficie.blit(txt_diff_lbl, (pos_x_lbl, rect_dibujo.y + 92))
            superficie.blit(txt_diff_val, (pos_x_lbl + w_lbl, rect_dibujo.y + 92))

            # 4. Estado de completado
            if completado:
                tarea_str = "Status: COMPLETED ⚙"
                color_estado = (35, 140, 30)
            else:
                tarea_str = "Status: READY TO WORK"
                color_estado = (170, 95, 10)
                
            txt_estado = self.motor.fuente_sistemas.render(tarea_str, True, color_estado)
            superficie.blit(txt_estado, (cx - txt_estado.get_width() // 2, rect_dibujo.y + 128))

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
