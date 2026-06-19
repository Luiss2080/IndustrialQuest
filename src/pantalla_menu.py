# -*- coding: utf-8 -*-
"""
Pantalla de menú principal para IndustrialQuest: Woodwork Edition.
"""
import math
import pygame
from src.constantes import ANCHO_PANTALLA, ALTO_PANTALLA, COLOR_NEGRO
from src.pantalla import Pantalla
from src.tooltip import BilingualTooltip

class PantallaMenu(Pantalla):
    """
    Menú principal con estilo rústico-industrial, engranajes animados, reloj de fábrica,
    botones deslizantes y ayuda contextual flotante.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Cargar y configurar la imagen del logotipo
        self.logo = self.motor.recursos.obtener_imagen("logo.png")
        self.logo = pygame.transform.scale(self.logo, (300, 300))
        # Logo deslizante (entra por la izquierda)
        self.logo_rect = self.logo.get_rect(center=(-250, ALTO_PANTALLA // 2 - 30))
        self.destino_x = 200
        self.velocidad_deslizamiento = 15
        self.animacion_completada = False

        # Configurar botones
        self.nombres_botones = [
            "Start Shift",
            "Manual",
            "Production Logs",
            "Machinery Settings",
            "Clock Out"
        ]
        
        self.ancho_btn = 280
        self.alto_btn = 54
        self.x_btn = 470
        self.y_inicial_btn = 120
        self.espacio_btn = 75

        self.botones_rects = []
        for i in range(len(self.nombres_botones)):
            y = self.y_inicial_btn + i * self.espacio_btn
            rect = pygame.Rect(self.x_btn, y, self.ancho_btn, self.alto_btn)
            self.botones_rects.append(rect)

        # Animación de entrada de botones (se deslizan desde la derecha)
        self.offsets_botones = [500, 500, 500, 500, 500]

        # Engranajes rotatorios
        self.angulo_cogs = 0.0

        # Inicializar tooltips bilingües
        self.tooltips = [
            BilingualTooltip(self.motor, "Start your woodwork grammar shift.", "Comienza tu turno de gramática maderera."),
            BilingualTooltip(self.motor, "Open the operations manual and rules.", "Abre el manual de operaciones y reglas."),
            BilingualTooltip(self.motor, "View completed logs and high scores.", "Ver registros completados y récords."),
            BilingualTooltip(self.motor, "Configure audio volume and machine speed.", "Configurar volumen de audio y velocidad."),
            BilingualTooltip(self.motor, "Exit the factory and close game.", "Salir de la fábrica y cerrar el juego.")
        ]

        # Estado de interacción
        self.indice_hovered = -1
        
        # Paleta de colores rústica mejorada para alto contraste
        self.color_madera_oscuro = (60, 35, 15)
        self.color_madera_claro = (245, 230, 205)
        self.color_madera_hover = (255, 190, 80)
        self.color_acero = (110, 115, 120)
        self.color_acero_borde = (60, 65, 70)
        self.color_texto_normal = (30, 15, 5)
        self.color_texto_hover = (0, 0, 0)
        self.color_fondo = (30, 22, 18)
        self.color_bronce = (180, 140, 70)

    def manejar_eventos(self, eventos):
        if not self.animacion_completada:
            return

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clic izquierdo
                    for i, rect in enumerate(self.botones_rects):
                        rect_dibujo = rect.copy()
                        rect_dibujo.x += int(self.offsets_botones[i])
                        if rect_dibujo.collidepoint(evento.pos):
                            self.motor.reproducir_sonido("Correcta.wav")
                            self._ejecutar_accion(i)
                            return

    def _ejecutar_accion(self, indice):
        if indice == 0:
            from src.pantalla_niveles import PantallaNiveles
            self.motor.cambiar_pantalla(PantallaNiveles(self.motor))
        elif indice == 1:
            from src.pantalla_manual import PantallaManual
            self.motor.cambiar_pantalla(PantallaManual(self.motor))
        elif indice == 2:
            from src.pantalla_logs import PantallaLogs
            self.motor.cambiar_pantalla(PantallaLogs(self.motor))
        elif indice == 3:
            from src.pantalla_ajustes import PantallaAjustes
            self.motor.cambiar_pantalla(PantallaAjustes(self.motor))
        elif indice == 4:
            self.motor.salir()

    def actualizar(self, dt):
        # Animación de entrada de logotipo
        if not self.animacion_completada:
            if self.logo_rect.centerx < self.destino_x:
                self.logo_rect.x += self.velocidad_deslizamiento
                if self.logo_rect.centerx >= self.destino_x:
                    self.logo_rect.centerx = self.destino_x
                    self.animacion_completada = True
            else:
                self.animacion_completada = True

        # Animación de entrada de botones
        if self.animacion_completada:
            for i in range(len(self.offsets_botones)):
                self.offsets_botones[i] += (0 - self.offsets_botones[i]) * (0.15 - i * 0.01)
                if abs(self.offsets_botones[i]) < 1:
                    self.offsets_botones[i] = 0

        # Rotar engranajes
        self.angulo_cogs = (self.angulo_cogs + 0.08 * dt) % 360

        # Detección de hover en botones
        if self.animacion_completada:
            pos_mouse = pygame.mouse.get_pos()
            hover_actual = -1
            for i, rect in enumerate(self.botones_rects):
                rect_dibujo = rect.copy()
                rect_dibujo.x += int(self.offsets_botones[i])
                if rect_dibujo.collidepoint(pos_mouse):
                    hover_actual = i
                    break
            self.indice_hovered = hover_actual

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
            
            rad_siguiente = math.radians(angulo + (i + 1) * (360 / dientes))
            nx = cx + radio * math.cos(rad_siguiente)
            ny = cy + radio * math.sin(rad_siguiente)
            
            pygame.draw.polygon(superficie, color, [(bx, by), (px, py), (nx, ny)])

    def _dibujar_reloj_fabrica(self, superficie, cx, cy, radio):
        pygame.draw.circle(superficie, (10, 10, 12), (cx + 3, cy + 3), radio)
        pygame.draw.circle(superficie, self.color_bronce, (cx, cy), radio)
        pygame.draw.circle(superficie, (90, 70, 30), (cx, cy), radio, 3)
        pygame.draw.circle(superficie, (245, 240, 230), (cx, cy), radio - 5)
        
        for i in range(12):
            rad = math.radians(i * 30)
            x_b = cx + (radio - 9) * math.cos(rad)
            y_b = cy + (radio - 9) * math.sin(rad)
            x_e = cx + (radio - 5) * math.cos(rad)
            y_e = cy + (radio - 5) * math.sin(rad)
            pygame.draw.line(superficie, COLOR_NEGRO, (x_b, y_b), (x_e, y_e), 2)
            
        ticks = pygame.time.get_ticks()
        ang_min = (ticks * 0.05) % 360
        ang_hor = (ticks * 0.004) % 360
        
        mx = cx + (radio - 12) * math.cos(math.radians(ang_min - 90))
        my = cy + (radio - 12) * math.sin(math.radians(ang_min - 90))
        pygame.draw.line(superficie, (40, 40, 45), (cx, cy), (mx, my), 2)
        
        hx = cx + (radio - 18) * math.cos(math.radians(ang_hor - 90))
        hy = cy + (radio - 18) * math.sin(math.radians(ang_hor - 90))
        pygame.draw.line(superficie, COLOR_NEGRO, (cx, cy), (hx, hy), 3)
        pygame.draw.circle(superficie, (180, 40, 40), (cx, cy), 3)

    def dibujar(self, superficie):
        # Fondo oscuro
        superficie.fill(self.color_fondo)
        
        # Vigas decorativas de fondo
        for y in range(40, ALTO_PANTALLA, 80):
            pygame.draw.line(superficie, (20, 14, 11), (0, y), (ANCHO_PANTALLA, y), 8)

        # Marco de acero industrial
        grosor_marco = 15
        pygame.draw.rect(superficie, self.color_acero, (0, 0, ANCHO_PANTALLA, ALTO_PANTALLA), grosor_marco)
        pygame.draw.rect(superficie, self.color_acero_borde, (grosor_marco, grosor_marco, ANCHO_PANTALLA - 2*grosor_marco, ALTO_PANTALLA - 2*grosor_marco), 3)

        # Engranajes animados en las esquinas
        self._dibujar_cog_engranaje(superficie, 45, 45, 24, 8, self.angulo_cogs, (85, 90, 95))
        self._dibujar_cog_engranaje(superficie, ANCHO_PANTALLA - 45, 45, 24, 8, -self.angulo_cogs, (85, 90, 95))
        self._dibujar_cog_engranaje(superficie, 45, ALTO_PANTALLA - 45, 24, 8, -self.angulo_cogs, (80, 85, 90))
        self._dibujar_cog_engranaje(superficie, ANCHO_PANTALLA - 45, ALTO_PANTALLA - 45, 24, 8, self.angulo_cogs, (80, 85, 90))

        # Dibujar el logo
        superficie.blit(self.logo, self.logo_rect)

        # Reloj de fábrica a la derecha del logo
        if self.animacion_completada:
            self._dibujar_reloj_fabrica(superficie, 200, 390, 30)

        # Dibujar botones interactivos
        if self.animacion_completada:
            for i, rect in enumerate(self.botones_rects):
                is_hover = (self.indice_hovered == i)
                
                # Desplazamiento 3D y de entrada
                offset_entrada = int(self.offsets_botones[i])
                offset_x = 2 if is_hover else 0
                offset_y = 2 if is_hover else 0
                
                rect_dibujo = rect.copy()
                rect_dibujo.x += offset_entrada + offset_x
                rect_dibujo.y += offset_y

                # Sombra
                pygame.draw.rect(superficie, (10, 7, 5), (rect.x + offset_entrada + 4, rect.y + 4, rect.width, rect.height), border_radius=4)

                # Cuerpo del botón (Pine wood claro para alto contraste con texto oscuro)
                color_relleno = self.color_madera_hover if is_hover else self.color_madera_claro
                pygame.draw.rect(superficie, color_relleno, rect_dibujo, border_radius=4)
                
                # Bordes
                pygame.draw.rect(superficie, self.color_madera_oscuro, rect_dibujo, 3, border_radius=4)

                # Clavos decorativos en las esquinas del botón
                margen_clavo = 6
                pos_clavos = [
                    (rect_dibujo.left + margen_clavo, rect_dibujo.top + margen_clavo),
                    (rect_dibujo.right - margen_clavo, rect_dibujo.top + margen_clavo),
                    (rect_dibujo.left + margen_clavo, rect_dibujo.bottom - margen_clavo),
                    (rect_dibujo.right - margen_clavo, rect_dibujo.bottom - margen_clavo)
                ]
                for px, py in pos_clavos:
                    pygame.draw.circle(superficie, (80, 80, 80), (px, py), 3)

                # Dibujar texto centrado
                color_texto = self.color_texto_hover if is_hover else self.color_texto_normal
                texto_str = f"> {self.nombres_botones[i]} <" if is_hover else self.nombres_botones[i]
                
                texto_render = self.motor.fuente.render(texto_str, True, color_texto)
                tx = rect_dibujo.centerx - texto_render.get_width() // 2
                ty = rect_dibujo.centery - texto_render.get_height() // 2
                superficie.blit(texto_render, (tx, ty))

            # Dibujar el tooltip flotante al final si está hovered
            if self.indice_hovered != -1:
                mx, my = pygame.mouse.get_pos()
                self.tooltips[self.indice_hovered].dibujar(superficie, mx, my)
