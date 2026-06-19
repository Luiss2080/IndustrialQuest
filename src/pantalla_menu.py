# -*- coding: utf-8 -*-
"""
Pantalla de menú principal para IndustrialQuest: Woodwork Edition.
"""
import pygame
import sys
from src.constantes import COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla

class PantallaMenu(Pantalla):
    """
    Representa el menú principal de IndustrialQuest: Woodwork Edition.
    Cuenta con estética rústico-industrial, logotipo deslizante, y 5 botones de madera
    interactivos con sonido y animaciones tridimensionales de pulsación y resalte.
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

        # Estado de interacción
        self.indice_hovered = -1
        
        # Colores de la paleta rústico-industrial
        self.color_madera_oscuro = (90, 55, 30)
        self.color_madera_claro = (160, 110, 65)
        self.color_madera_hover = (210, 150, 90)
        self.color_acero = (110, 115, 120)
        self.color_acero_borde = (60, 65, 70)
        self.color_texto_normal = (50, 30, 10)
        self.color_texto_hover = (255, 230, 150)
        self.color_fondo = (35, 25, 20)  # Tono carbón oscuro

    def manejar_eventos(self, eventos):
        if not self.animacion_completada:
            return

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clic izquierdo
                    for i, rect in enumerate(self.botones_rects):
                        if rect.collidepoint(evento.pos):
                            self.motor.reproducir_sonido("Correcta.wav")
                            self._ejecutar_accion(i)
                            return

    def _ejecutar_accion(self, indice):
        if indice == 0:
            # Start Shift
            from src.pantalla_niveles import PantallaNiveles
            self.motor.cambiar_pantalla(PantallaNiveles(self.motor))
        elif indice == 1:
            # Manual
            from src.pantalla_manual import PantallaManual
            self.motor.cambiar_pantalla(PantallaManual(self.motor))
        elif indice == 2:
            # Production Logs
            from src.pantalla_logs import PantallaLogs
            self.motor.cambiar_pantalla(PantallaLogs(self.motor))
        elif indice == 3:
            # Machinery Settings
            from src.pantalla_ajustes import PantallaAjustes
            self.motor.cambiar_pantalla(PantallaAjustes(self.motor))
        elif indice == 4:
            # Clock Out
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

        # Detección de hover en botones
        if self.animacion_completada:
            pos_mouse = pygame.mouse.get_pos()
            hover_actual = -1
            for i, rect in enumerate(self.botones_rects):
                if rect.collidepoint(pos_mouse):
                    hover_actual = i
                    break
            
            if hover_actual != self.indice_hovered:
                if hover_actual != -1:
                    # Sonido de clic sutil de madera/chisel al pasar el ratón
                    self.motor.reproducir_sonido("Correcta.wav")
                self.indice_hovered = hover_actual

    def dibujar(self, superficie):
        # 1. Dibujar el fondo rústico de madera oscura
        superficie.fill(self.color_fondo)
        
        # Dibujar vigas decorativas de madera en el fondo (2 lineas horizontales texturizadas)
        for y in range(40, ALTO_PANTALLA, 80):
            pygame.draw.line(superficie, (45, 33, 27), (0, y), (ANCHO_PANTALLA, y), 8)
            pygame.draw.line(superficie, (25, 17, 13), (0, y + 4), (ANCHO_PANTALLA, y + 4), 4)

        # Dibujar marco de acero industrial alrededor de toda la pantalla
        grosor_marco = 15
        pygame.draw.rect(superficie, self.color_acero, (0, 0, ANCHO_PANTALLA, ALTO_PANTALLA), grosor_marco)
        pygame.draw.rect(superficie, self.color_acero_borde, (grosor_marco, grosor_marco, ANCHO_PANTALLA - 2*grosor_marco, ALTO_PANTALLA - 2*grosor_marco), 3)

        # Dibujar remaches/clavos en las esquinas del marco de acero
        esquinas = [
            (30, 30), (ANCHO_PANTALLA - 30, 30),
            (30, ALTO_PANTALLA - 30), (ANCHO_PANTALLA - 30, ALTO_PANTALLA - 30),
            (ANCHO_PANTALLA // 2, 30), (ANCHO_PANTALLA // 2, ALTO_PANTALLA - 30)
        ]
        for cx, cy in esquinas:
            pygame.draw.circle(superficie, (50, 55, 60), (cx, cy), 8)
            pygame.draw.circle(superficie, (180, 185, 190), (cx - 2, cy - 2), 3)  # Brillo

        # 2. Dibujar el logo
        superficie.blit(self.logo, self.logo_rect)

        # 3. Dibujar botones interactivos en forma de tablones
        if self.animacion_completada:
            for i, rect in enumerate(self.botones_rects):
                is_hover = (self.indice_hovered == i)
                
                # Desplazar ligeramente hacia abajo/derecha si está en hover para efecto 3D
                offset_x = 2 if is_hover else 0
                offset_y = 2 if is_hover else 0
                
                rect_dibujo = rect.copy()
                rect_dibujo.x += offset_x
                rect_dibujo.y += offset_y

                # Sombra del tablón
                pygame.draw.rect(superficie, (15, 10, 5), (rect.x + 4, rect.y + 4, rect.width, rect.height), border_radius=4)

                # Relleno del tablón (color madera claro, o resaltado en hover)
                color_relleno = self.color_madera_hover if is_hover else self.color_madera_claro
                pygame.draw.rect(superficie, color_relleno, rect_dibujo, border_radius=4)
                
                # Bordes del tablón (madera oscura tallada)
                pygame.draw.rect(superficie, self.color_madera_oscuro, rect_dibujo, 3, border_radius=4)

                # Clavos decorativos en las esquinas del tablón
                diametro_clavo = 4
                margen_clavo = 6
                posiciones_clavos = [
                    (rect_dibujo.left + margen_clavo, rect_dibujo.top + margen_clavo),
                    (rect_dibujo.right - margen_clavo, rect_dibujo.top + margen_clavo),
                    (rect_dibujo.left + margen_clavo, rect_dibujo.bottom - margen_clavo),
                    (rect_dibujo.right - margen_clavo, rect_dibujo.bottom - margen_clavo)
                ]
                for px, py in posiciones_clavos:
                    pygame.draw.circle(superficie, (80, 80, 80), (px, py), diametro_clavo)
                    pygame.draw.circle(superficie, (30, 30, 30), (px, py), diametro_clavo, 1)

                # Dibujar texto centrado
                color_texto = self.color_texto_hover if is_hover else self.color_texto_normal
                
                # Si está hovered, agregar un prefijo de sierra decorativo o indicador
                texto_str = f"> {self.nombres_botones[i]} <" if is_hover else self.nombres_botones[i]
                
                texto_render = self.motor.fuente.render(texto_str, True, color_texto)
                tx = rect_dibujo.centerx - texto_render.get_width() // 2
                ty = rect_dibujo.centery - texto_render.get_height() // 2
                superficie.blit(texto_render, (tx, ty))
