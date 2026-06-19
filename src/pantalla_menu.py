# -*- coding: utf-8 -*-
"""
Pantalla de menú principal para IndustrialQuest: Woodwork Edition.
"""
import pygame
from src.constantes import ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla
from src.tooltip import BilingualTooltip

class PantallaMenu(Pantalla):
    """
    Menú principal con estilo rústico-industrial de alto contraste y ayuda contextual flotante.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Cargar y configurar la imagen del logotipo
        self.logo = self.motor.recursos.obtener_imagen("logo.png")
        self.logo = pygame.transform.scale(self.logo, (320, 320))
        # Logo deslizante (entra por la izquierda)
        self.logo_rect = self.logo.get_rect(center=(-200, ALTO_PANTALLA // 2))
        self.destino_x = 220
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
        self.color_madera_oscuro = (60, 35, 15)       # Tablón bordes oscuros
        self.color_madera_claro = (245, 230, 205)      # Madera de pino clara (alto contraste para texto negro)
        self.color_madera_hover = (255, 180, 70)       # Resalte dorado en hover
        self.color_acero = (110, 115, 120)
        self.color_acero_borde = (60, 65, 70)
        self.color_texto_normal = (30, 15, 5)          # Marrón casi negro (máximo contraste)
        self.color_texto_hover = (0, 0, 0)             # Negro absoluto en hover
        self.color_fondo = (30, 22, 18)                # Tono madera de fondo oscura

    def manejar_eventos(self, eventos):
        if not self.animacion_completada:
            return

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clic izquierdo
                    for i, rect in enumerate(self.botones_rects):
                        if rect.collidepoint(evento.pos):
                            # Play click sound
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

        # Detección de hover en botones (sin reproducir sonidos)
        if self.animacion_completada:
            pos_mouse = pygame.mouse.get_pos()
            hover_actual = -1
            for i, rect in enumerate(self.botones_rects):
                if rect.collidepoint(pos_mouse):
                    hover_actual = i
                    break
            self.indice_hovered = hover_actual

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

        # Remaches metálicos en el marco
        esquinas = [
            (30, 30), (ANCHO_PANTALLA - 30, 30),
            (30, ALTO_PANTALLA - 30), (ANCHO_PANTALLA - 30, ALTO_PANTALLA - 30),
            (ANCHO_PANTALLA // 2, 30), (ANCHO_PANTALLA // 2, ALTO_PANTALLA - 30)
        ]
        for cx, cy in esquinas:
            pygame.draw.circle(superficie, (50, 55, 60), (cx, cy), 8)
            pygame.draw.circle(superficie, (180, 185, 190), (cx - 2, cy - 2), 3)

        # Dibujar el logo
        superficie.blit(self.logo, self.logo_rect)

        # Dibujar botones interactivos (Tablones con alto contraste)
        if self.animacion_completada:
            for i, rect in enumerate(self.botones_rects):
                is_hover = (self.indice_hovered == i)
                
                # Desplazamiento 3D sutil
                offset_x = 2 if is_hover else 0
                offset_y = 2 if is_hover else 0
                
                rect_dibujo = rect.copy()
                rect_dibujo.x += offset_x
                rect_dibujo.y += offset_y

                # Sombra
                pygame.draw.rect(superficie, (10, 7, 5), (rect.x + 4, rect.y + 4, rect.width, rect.height), border_radius=4)

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

                # Dibujar texto
                color_texto = self.color_texto_hover if is_hover else self.color_texto_normal
                texto_str = f"> {self.nombres_botones[i]} <" if is_hover else self.nombres_botones[i]
                
                texto_render = self.motor.fuente.render(texto_str, True, color_texto)
                tx = rect_dibujo.centerx - texto_render.get_width() // 2
                ty = rect_dibujo.centery - texto_render.get_height() // 2
                superficie.blit(texto_render, (tx, ty))

            # Dibujar el tooltip flotante al final (sobre todo lo demás) si está hovered
            if self.indice_hovered != -1:
                mx, my = pygame.mouse.get_pos()
                self.tooltips[self.indice_hovered].dibujar(superficie, mx, my)
