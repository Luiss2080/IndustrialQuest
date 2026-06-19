# -*- coding: utf-8 -*-
"""
Pantalla de selección de turnos (niveles) para IndustrialQuest: Woodwork Edition.
"""
import pygame
from src.constantes import COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla
from src.datos_juego import TEMAS

class PantallaNiveles(Pantalla):
    """
    Renderea el tablero de turnos de la fábrica. Presenta los 4 niveles en un formato
    de tarjetas de madera de 2x2, controlando el desbloqueo secuencial de cada turno
    y registrando sellos de completado.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Colores
        self.color_fondo = (35, 25, 20)
        self.color_acero = (110, 115, 120)
        self.color_acero_borde = (60, 65, 70)
        
        self.color_tarjeta = (150, 105, 60)
        self.color_tarjeta_hover = (195, 140, 85)
        self.color_tarjeta_bloqueada = (70, 55, 45)
        self.color_tarjeta_borde = (80, 50, 20)
        
        self.color_texto_titulo = (255, 240, 200)
        self.color_texto_desc = (230, 220, 210)
        self.color_texto_estado = (255, 220, 100)

        # Botón volver
        self.boton_img = self.motor.recursos.obtener_imagen("Boton.png")
        self.boton_img = pygame.transform.scale(self.boton_img, (160, 46))
        self.boton_volver = self.boton_img.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA - 40))
        self.texto_volver = self.motor.fuente.render("Clock In", True, COLOR_NEGRO)

        # Configurar tarjetas de nivel
        self.nombres_niveles = list(TEMAS.keys())
        self.rects_tarjetas = [
            pygame.Rect(80, 110, 300, 170),  # Nivel 1
            pygame.Rect(420, 110, 300, 170), # Nivel 2
            pygame.Rect(80, 305, 300, 170),  # Nivel 3
            pygame.Rect(420, 305, 300, 170)  # Nivel 4
        ]
        
        # Estado de hover
        self.indice_hovered = -1

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    # Verificar clic en volver
                    if self.boton_volver.collidepoint(evento.pos):
                        self.motor.reproducir_sonido("Correcta.wav")
                        from src.pantalla_menu import PantallaMenu
                        self.motor.cambiar_pantalla(PantallaMenu(self.motor))
                        return
                    
                    # Verificar clic en tarjetas
                    for i, rect in enumerate(self.rects_tarjetas):
                        if rect.collidepoint(evento.pos):
                            if self._esta_desbloqueado(i):
                                self.motor.reproducir_sonido("Correcta.wav")
                                self.motor.tema_actual = self.nombres_niveles[i]
                                from src.pantalla_juego import PantallaJuego
                                self.motor.cambiar_pantalla(PantallaJuego(self.motor))
                            else:
                                # Sonido de fracaso/error sutil (bloqueado)
                                self.motor.reproducir_sonido("equivocado.wav")
                            return

    def _esta_desbloqueado(self, indice):
        if indice == 0:
            return True
        # El nivel actual está desbloqueado si el nivel anterior está en la lista de completados
        nivel_previo = self.nombres_niveles[indice - 1]
        return nivel_previo in self.motor.niveles_completados

    def actualizar(self, dt):
        # Detección de hover
        pos_mouse = pygame.mouse.get_pos()
        hover_actual = -1
        for i, rect in enumerate(self.rects_tarjetas):
            if rect.collidepoint(pos_mouse) and self._esta_desbloqueado(i):
                hover_actual = i
                break
        
        if hover_actual != self.indice_hovered:
            if hover_actual != -1:
                self.motor.reproducir_sonido("Correcta.wav")
            self.indice_hovered = hover_actual

    def dibujar(self, superficie):
        # Fondo carbón oscuro
        superficie.fill(self.color_fondo)

        # Dibujar marco de acero exterior
        grosor_marco = 15
        pygame.draw.rect(superficie, self.color_acero, (0, 0, ANCHO_PANTALLA, ALTO_PANTALLA), grosor_marco)
        pygame.draw.rect(superficie, self.color_acero_borde, (grosor_marco, grosor_marco, ANCHO_PANTALLA - 2*grosor_marco, ALTO_PANTALLA - 2*grosor_marco), 3)

        # Dibujar título de la pantalla
        titulo_render = self.motor.fuente.render("FACTORY SHIFT REGISTRY", True, (255, 230, 100))
        superficie.blit(titulo_render, (ANCHO_PANTALLA // 2 - titulo_render.get_width() // 2, 35))

        # Dibujar las 4 tarjetas de nivel
        for i, rect in enumerate(self.rects_tarjetas):
            desbloqueado = self._esta_desbloqueado(i)
            completado = self.nombres_niveles[i] in self.motor.niveles_completados
            is_hover = (self.indice_hovered == i)
            
            # Animación de hover (desplazamiento 3D)
            offset = 2 if (is_hover and desbloqueado) else 0
            rect_dibujo = rect.copy()
            rect_dibujo.x += offset
            rect_dibujo.y += offset

            # Sombra de la tarjeta
            pygame.draw.rect(superficie, (15, 10, 5), (rect.x + 5, rect.y + 5, rect.width, rect.height), border_radius=6)

            # Determinar color de fondo de la tarjeta
            if not desbloqueado:
                color_relleno = self.color_tarjeta_bloqueada
            elif is_hover:
                color_relleno = self.color_tarjeta_hover
            else:
                color_relleno = self.color_tarjeta
                
            pygame.draw.rect(superficie, color_relleno, rect_dibujo, border_radius=6)
            pygame.draw.rect(superficie, self.color_tarjeta_borde, rect_dibujo, 3, border_radius=6)

            # Clavos decorativos en las esquinas de cada tarjeta
            margen_clavo = 6
            pos_clavos = [
                (rect_dibujo.left + margen_clavo, rect_dibujo.top + margen_clavo),
                (rect_dibujo.right - margen_clavo, rect_dibujo.top + margen_clavo),
                (rect_dibujo.left + margen_clavo, rect_dibujo.bottom - margen_clavo),
                (rect_dibujo.right - margen_clavo, rect_dibujo.bottom - margen_clavo)
            ]
            for px, py in pos_clavos:
                color_clavo = (40, 30, 20) if not desbloqueado else (90, 90, 90)
                pygame.draw.circle(superficie, color_clavo, (px, py), 3)

            # Dibujar textos dentro de la tarjeta
            # Título de Nivel (Shift)
            nombre_corto = self.nombres_niveles[i].replace("Level ", "Shift ")
            txt_titulo = self.motor.fuente.render(nombre_corto, True, self.color_texto_titulo if desbloqueado else (100, 90, 80))
            superficie.blit(txt_titulo, (rect_dibujo.x + 15, rect_dibujo.y + 15))

            # Regla gramatical
            regla_str = TEMAS[self.nombres_niveles[i]]["regla"]
            # Acortar texto si es muy largo
            if len(regla_str) > 28:
                regla_str = regla_str[:26] + ".."
            txt_regla = self.motor.fuente.render(regla_str, True, self.color_texto_desc if desbloqueado else (90, 80, 70))
            superficie.blit(txt_regla, (rect_dibujo.x + 15, rect_dibujo.y + 55))

            # Subtítulo historia/tarea corto
            tarea_str = "Status: "
            if not desbloqueado:
                tarea_str += "[LOCKED]"
                color_estado = (170, 70, 70)
            elif completado:
                tarea_str += "[COMPLETED ⚙️]"
                color_estado = (80, 220, 80)
            else:
                tarea_str += "[READY TO WORK]"
                color_estado = (255, 230, 100)
                
            txt_estado = self.motor.fuente.render(tarea_str, True, color_estado)
            superficie.blit(txt_estado, (rect_dibujo.x + 15, rect_dibujo.y + 105))

        # Dibujar botón volver (Clock In)
        mouse_pos = pygame.mouse.get_pos()
        offset = 2 if self.boton_volver.collidepoint(mouse_pos) else 0
        
        rect_volver_dibujo = self.boton_volver.copy()
        rect_volver_dibujo.x += offset
        rect_volver_dibujo.y += offset
        
        superficie.blit(self.boton_img, rect_volver_dibujo)
        tx = rect_volver_dibujo.centerx - self.texto_volver.get_width() // 2
        ty = rect_volver_dibujo.centery - self.texto_volver.get_height() // 2
        superficie.blit(self.texto_volver, (tx, ty))
