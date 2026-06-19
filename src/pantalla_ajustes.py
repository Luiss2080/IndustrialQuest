# -*- coding: utf-8 -*-
"""
Pantalla de Ajustes de Maquinaria (Machinery Settings) para IndustrialQuest: Woodwork Edition.
"""
import pygame
from src.constantes import COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla
from src.tooltip import BilingualTooltip

class PantallaAjustes(Pantalla):
    """
    Control de audio y velocidad de cinta con tooltips y alineación de alta precisión.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Colores
        self.color_fondo = (30, 22, 18)
        self.color_panel = (95, 100, 105)
        self.color_panel_borde = (50, 55, 60)
        self.color_luces = (50, 210, 50)
        self.color_texto = (245, 245, 245)
        self.color_texto_valor = (255, 210, 80)

        # Botón volver
        self.boton_img = self.motor.recursos.obtener_imagen("Boton.png")
        self.boton_img = pygame.transform.scale(self.boton_img, (160, 46))
        self.boton_volver = self.boton_img.get_rect(bottomright=(ANCHO_PANTALLA - 30, ALTO_PANTALLA - 30))
        self.texto_volver = self.motor.fuente.render("Clock In", True, COLOR_NEGRO)

        # Botones de ajuste
        self.btn_musica_menos = pygame.Rect(430, 145, 40, 40)
        self.btn_musica_mas = pygame.Rect(570, 145, 40, 40)
        
        self.btn_sfx_menos = pygame.Rect(430, 225, 40, 40)
        self.btn_sfx_mas = pygame.Rect(570, 225, 40, 40)
        
        self.btn_speed_menos = pygame.Rect(430, 305, 40, 40)
        self.btn_speed_mas = pygame.Rect(570, 305, 40, 40)
        
        self.btn_clear_logs = pygame.Rect(290, 395, 240, 45)

        # Tooltips bilingües
        self.tooltip_musica = BilingualTooltip(self.motor, "Adjust background music volume.", "Ajustar volumen de música de fondo.")
        self.tooltip_sfx = BilingualTooltip(self.motor, "Adjust mechanical sound effects volume.", "Ajustar volumen de efectos de sonido mecánicos.")
        self.tooltip_speed = BilingualTooltip(self.motor, "Adjust the speed multiplier of conveyor planks.", "Ajustar el multiplicador de velocidad de los tablones.")
        self.tooltip_clear = BilingualTooltip(self.motor, "Clear all saved logs, completion stamps and high scores.", "Borrar registros, marcas de completado y récords.")
        self.tooltip_volver = BilingualTooltip(self.motor, "Save settings and return to main menu.", "Guardar ajustes y volver al menú principal.")

        self.mensaje_logs = ""
        self.temporizador_mensaje = 0
        self.hover_volver = False

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    clic_valido = False
                    
                    if self.btn_musica_menos.collidepoint(evento.pos):
                        self.motor.volumen_musica = max(0.0, self.motor.volumen_musica - 0.1)
                        clic_valido = True
                    elif self.btn_musica_mas.collidepoint(evento.pos):
                        self.motor.volumen_musica = min(1.0, self.motor.volumen_musica + 0.1)
                        clic_valido = True
                        
                    elif self.btn_sfx_menos.collidepoint(evento.pos):
                        self.motor.volumen_sfx = max(0.0, self.motor.volumen_sfx - 0.1)
                        clic_valido = True
                    elif self.btn_sfx_mas.collidepoint(evento.pos):
                        self.motor.volumen_sfx = min(1.0, self.motor.volumen_sfx + 0.1)
                        clic_valido = True
                        
                    elif self.btn_speed_menos.collidepoint(evento.pos):
                        self.motor.velocidad_ajustada = max(0.6, self.motor.velocidad_ajustada - 0.1)
                        clic_valido = True
                    elif self.btn_speed_mas.collidepoint(evento.pos):
                        self.motor.velocidad_ajustada = min(2.0, self.motor.velocidad_ajustada + 0.1)
                        clic_valido = True
                        
                    elif self.btn_clear_logs.collidepoint(evento.pos):
                        self.motor.historico_logs = []
                        self.motor.niveles_completados = []
                        self.mensaje_logs = "LOGS WIPED CLEAN!"
                        self.temporizador_mensaje = 120
                        clic_valido = True
                        
                    elif self.boton_volver.collidepoint(evento.pos):
                        self.motor.reproducir_sonido("Correcta.wav")
                        self.motor.guardar_datos()
                        from src.pantalla_menu import PantallaMenu
                        self.motor.cambiar_pantalla(PantallaMenu(self.motor))
                        return
                    
                    if clic_valido:
                        self.motor.reproducir_sonido("Correcta.wav")

    def actualizar(self, dt):
        if self.temporizador_mensaje > 0:
            self.temporizador_mensaje -= 1
            if self.temporizador_mensaje == 0:
                self.mensaje_logs = ""
        
        pos_mouse = pygame.mouse.get_pos()
        self.hover_volver = self.boton_volver.collidepoint(pos_mouse)

    def dibujar(self, superficie):
        superficie.fill(self.color_fondo)

        # Panel de acero central
        rect_panel = pygame.Rect(100, 50, ANCHO_PANTALLA - 200, ALTO_PANTALLA - 150)
        pygame.draw.rect(superficie, (15, 15, 18), (rect_panel.x + 5, rect_panel.y + 5, rect_panel.width, rect_panel.height), border_radius=10)
        pygame.draw.rect(superficie, self.color_panel, rect_panel, border_radius=10)
        pygame.draw.rect(superficie, self.color_panel_borde, rect_panel, 5, border_radius=10)

        # Título
        pygame.draw.line(superficie, (60, 65, 70), (rect_panel.left, rect_panel.top + 60), (rect_panel.right, rect_panel.top + 60), 3)
        titulo_render = self.motor.fuente.render("MACHINERY DIAGNOSTICS", True, (255, 220, 80))
        superficie.blit(titulo_render, (rect_panel.x + 40, rect_panel.y + 18))

        # Luz piloto
        pygame.draw.circle(superficie, (30, 30, 30), (rect_panel.right - 40, rect_panel.top + 30), 12)
        pygame.draw.circle(superficie, self.color_luces, (rect_panel.right - 40, rect_panel.top + 30), 8)
        pygame.draw.circle(superficie, (200, 255, 200), (rect_panel.right - 42, rect_panel.top + 28), 3)

        # Filas de configuración
        ajustes_lista = [
            ("Music Volume", f"{int(self.motor.volumen_musica * 100)}%", self.btn_musica_menos, self.btn_musica_mas, 150),
            ("SFX Volume", f"{int(self.motor.volumen_sfx * 100)}%", self.btn_sfx_menos, self.btn_sfx_mas, 230),
            ("Belt Speed", f"{self.motor.velocidad_ajustada:.1f}x", self.btn_speed_menos, self.btn_speed_mas, 310)
        ]

        for nombre, valor, btn_menos, btn_mas, y in ajustes_lista:
            txt_nombre = self.motor.fuente.render(nombre, True, self.color_texto)
            superficie.blit(txt_nombre, (rect_panel.x + 40, y + 5))
            
            # [-]
            pygame.draw.rect(superficie, (40, 45, 50), btn_menos, border_radius=4)
            pygame.draw.rect(superficie, (200, 200, 200), btn_menos, 2, border_radius=4)
            txt_menos = self.motor.fuente.render("-", True, (255, 255, 255))
            superficie.blit(txt_menos, (btn_menos.centerx - txt_menos.get_width() // 2, btn_menos.centery - txt_menos.get_height() // 2))

            # Valor
            pygame.draw.rect(superficie, (20, 20, 20), (480, y, 80, 40), border_radius=4)
            txt_valor = self.motor.fuente.render(valor, True, self.color_texto_valor)
            superficie.blit(txt_valor, (520 - txt_valor.get_width() // 2, y + 20 - txt_valor.get_height() // 2))

            # [+]
            pygame.draw.rect(superficie, (40, 45, 50), btn_mas, border_radius=4)
            pygame.draw.rect(superficie, (200, 200, 200), btn_mas, 2, border_radius=4)
            txt_mas = self.motor.fuente.render("+", True, (255, 255, 255))
            superficie.blit(txt_mas, (btn_mas.centerx - txt_mas.get_width() // 2, btn_mas.centery - txt_mas.get_height() // 2))

        # Wipe logs
        pygame.draw.rect(superficie, (180, 50, 50), self.btn_clear_logs, border_radius=4)
        pygame.draw.rect(superficie, (90, 20, 20), self.btn_clear_logs, 3, border_radius=4)
        txt_clear = self.motor.fuente.render("Wipe Production Logs", True, (255, 255, 255))
        superficie.blit(txt_clear, (self.btn_clear_logs.centerx - txt_clear.get_width() // 2, self.btn_clear_logs.centery - txt_clear.get_height() // 2))

        if self.mensaje_logs:
            txt_msg = self.motor.fuente.render(self.mensaje_logs, True, (255, 100, 100))
            superficie.blit(txt_msg, (self.btn_clear_logs.right + 15, self.btn_clear_logs.y + 10))

        # Volver
        offset = 2 if self.hover_volver else 0
        rect_volver_dibujo = self.boton_volver.copy()
        rect_volver_dibujo.x += offset
        rect_volver_dibujo.y += offset
        
        superficie.blit(self.boton_img, rect_volver_dibujo)
        tx = rect_volver_dibujo.centerx - self.texto_volver.get_width() // 2
        ty = rect_volver_dibujo.centery - self.texto_volver.get_height() // 2
        superficie.blit(self.texto_volver, (tx, ty))

        # Dibujar tooltips flotantes
        mx, my = pygame.mouse.get_pos()
        if self.btn_musica_menos.collidepoint(mx, my) or self.btn_musica_mas.collidepoint(mx, my):
            self.tooltip_musica.dibujar(superficie, mx, my)
        elif self.btn_sfx_menos.collidepoint(mx, my) or self.btn_sfx_mas.collidepoint(mx, my):
            self.tooltip_sfx.dibujar(superficie, mx, my)
        elif self.btn_speed_menos.collidepoint(mx, my) or self.btn_speed_mas.collidepoint(mx, my):
            self.tooltip_speed.dibujar(superficie, mx, my)
        elif self.btn_clear_logs.collidepoint(mx, my):
            self.tooltip_clear.dibujar(superficie, mx, my)
        elif self.hover_volver:
            self.tooltip_volver.dibujar(superficie, mx, my)
