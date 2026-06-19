# -*- coding: utf-8 -*-
"""
Pantalla de Ajustes de Maquinaria (Machinery Settings) para IndustrialQuest: Woodwork Edition.
"""
import pygame
from src.constantes import COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla

class PantallaAjustes(Pantalla):
    """
    Controla la configuración de audio (música, efectos) y velocidad de la maquinaria.
    Presenta controles interactivos estilo panel de control de acero con luces e indicadores.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Colores
        self.color_fondo = (35, 25, 20)
        self.color_panel = (90, 95, 100) # Acero gris
        self.color_panel_borde = (50, 55, 60)
        self.color_luces = (30, 200, 40) # Verde indicador
        self.color_texto = (240, 240, 240)
        self.color_texto_valor = (255, 200, 50) # Amarillo digital

        # Botón volver
        self.boton_img = self.motor.recursos.obtener_imagen("Boton.png")
        self.boton_img = pygame.transform.scale(self.boton_img, (160, 46))
        self.boton_volver = self.boton_img.get_rect(bottomright=(ANCHO_PANTALLA - 30, ALTO_PANTALLA - 30))
        self.texto_volver = self.motor.fuente.render("Clock In", True, COLOR_NEGRO)

        # Botones interactivos (Rectángulos de colisión)
        self.btn_musica_menos = pygame.Rect(420, 145, 40, 40)
        self.btn_musica_mas = pygame.Rect(560, 145, 40, 40)
        
        self.btn_sfx_menos = pygame.Rect(420, 225, 40, 40)
        self.btn_sfx_mas = pygame.Rect(560, 225, 40, 40)
        
        self.btn_speed_menos = pygame.Rect(420, 305, 40, 40)
        self.btn_speed_mas = pygame.Rect(560, 305, 40, 40)
        
        self.btn_clear_logs = pygame.Rect(300, 395, 220, 45)

        # Mensaje temporal de confirmación
        self.mensaje_logs = ""
        self.temporizador_mensaje = 0

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: # Clic izquierdo
                    clic_valido = False
                    
                    # Música
                    if self.btn_musica_menos.collidepoint(evento.pos):
                        self.motor.volumen_musica = max(0.0, self.motor.volumen_musica - 0.1)
                        clic_valido = True
                    elif self.btn_musica_mas.collidepoint(evento.pos):
                        self.motor.volumen_musica = min(1.0, self.motor.volumen_musica + 0.1)
                        clic_valido = True
                        
                    # SFX
                    elif self.btn_sfx_menos.collidepoint(evento.pos):
                        self.motor.volumen_sfx = max(0.0, self.motor.volumen_sfx - 0.1)
                        clic_valido = True
                    elif self.btn_sfx_mas.collidepoint(evento.pos):
                        self.motor.volumen_sfx = min(1.0, self.motor.volumen_sfx + 0.1)
                        clic_valido = True
                        
                    # Velocidad
                    elif self.btn_speed_menos.collidepoint(evento.pos):
                        self.motor.velocidad_ajustada = max(0.6, self.motor.velocidad_ajustada - 0.1)
                        clic_valido = True
                    elif self.btn_speed_mas.collidepoint(evento.pos):
                        self.motor.velocidad_ajustada = min(2.0, self.motor.velocidad_ajustada + 0.1)
                        clic_valido = True
                        
                    # Reset logs
                    elif self.btn_clear_logs.collidepoint(evento.pos):
                        self.motor.historico_logs = []
                        self.motor.niveles_completados = []
                        self.mensaje_logs = "LOGS WIPED CLEAN!"
                        self.temporizador_mensaje = 120
                        clic_valido = True
                        
                    # Volver
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

    def dibujar(self, superficie):
        # Fondo carbón oscuro
        superficie.fill(self.color_fondo)

        # 1. Dibujar el Panel de Acero
        rect_panel = pygame.Rect(100, 50, ANCHO_PANTALLA - 200, ALTO_PANTALLA - 150)
        pygame.draw.rect(superficie, (20, 20, 25), (rect_panel.x + 6, rect_panel.y + 6, rect_panel.width, rect_panel.height), border_radius=10)
        pygame.draw.rect(superficie, self.color_panel, rect_panel, border_radius=10)
        pygame.draw.rect(superficie, self.color_panel_borde, rect_panel, 5, border_radius=10)

        # Líneas horizontales de unión de metal
        pygame.draw.line(superficie, (60, 65, 70), (rect_panel.left, rect_panel.top + 60), (rect_panel.right, rect_panel.top + 60), 3)

        # Título del panel
        titulo_render = self.motor.fuente.render("MACHINERY CONTROLS & DIAGNOSTICS", True, (255, 230, 100))
        superficie.blit(titulo_render, (rect_panel.x + 40, rect_panel.y + 15))

        # Dibujar bombillas indicadoras (luces LED de estado)
        pygame.draw.circle(superficie, (30, 30, 30), (rect_panel.right - 40, rect_panel.top + 30), 12)
        pygame.draw.circle(superficie, self.color_luces, (rect_panel.right - 40, rect_panel.top + 30), 8)
        pygame.draw.circle(superficie, (200, 255, 200), (rect_panel.right - 42, rect_panel.top + 28), 3) # Brillo de luz

        # 2. Dibujar las filas de ajustes
        ajustes_lista = [
            ("Music Volume", f"{int(self.motor.volumen_musica * 100)}%", self.btn_musica_menos, self.btn_musica_mas, 150),
            ("SFX Volume", f"{int(self.motor.volumen_sfx * 100)}%", self.btn_sfx_menos, self.btn_sfx_mas, 230),
            ("Belt Speed", f"{self.motor.velocidad_ajustada:.1f}x", self.btn_speed_menos, self.btn_speed_mas, 310)
        ]

        for nombre, valor, btn_menos, btn_mas, y in ajustes_lista:
            # Nombre del ajuste
            txt_nombre = self.motor.fuente.render(nombre, True, self.color_texto)
            superficie.blit(txt_nombre, (rect_panel.x + 40, y + 5))
            
            # Botón Menos [-]
            pygame.draw.rect(superficie, (40, 45, 50), btn_menos, border_radius=4)
            pygame.draw.rect(superficie, (200, 200, 200), btn_menos, 2, border_radius=4)
            txt_menos = self.motor.fuente.render("-", True, (255, 255, 255))
            superficie.blit(txt_menos, (btn_menos.centerx - txt_menos.get_width() // 2, btn_menos.centery - txt_menos.get_height() // 2))

            # Indicador de Valor
            pygame.draw.rect(superficie, (20, 20, 20), (470, y, 80, 40), border_radius=4)
            txt_valor = self.motor.fuente.render(valor, True, self.color_texto_valor)
            superficie.blit(txt_valor, (510 - txt_valor.get_width() // 2, y + 20 - txt_valor.get_height() // 2))

            # Botón Más [+]
            pygame.draw.rect(superficie, (40, 45, 50), btn_mas, border_radius=4)
            pygame.draw.rect(superficie, (200, 200, 200), btn_mas, 2, border_radius=4)
            txt_mas = self.motor.fuente.render("+", True, (255, 255, 255))
            superficie.blit(txt_mas, (btn_mas.centerx - txt_mas.get_width() // 2, btn_mas.centery - txt_mas.get_height() // 2))

        # 3. Fila de Borrado de logs
        pygame.draw.rect(superficie, (180, 50, 50), self.btn_clear_logs, border_radius=4)
        pygame.draw.rect(superficie, (90, 20, 20), self.btn_clear_logs, 3, border_radius=4)
        txt_clear = self.motor.fuente.render("Wipe Production Logs", True, (255, 255, 255))
        superficie.blit(txt_clear, (self.btn_clear_logs.centerx - txt_clear.get_width() // 2, self.btn_clear_logs.centery - txt_clear.get_height() // 2))

        # Mensaje de confirmación de logs borrados
        if self.mensaje_logs:
            txt_msg = self.motor.fuente.render(self.mensaje_logs, True, (255, 100, 100))
            superficie.blit(txt_msg, (self.btn_clear_logs.right + 15, self.btn_clear_logs.y + 10))

        # 4. Dibujar botón volver (Clock In)
        mouse_pos = pygame.mouse.get_pos()
        offset = 2 if self.boton_volver.collidepoint(mouse_pos) else 0
        
        rect_volver_dibujo = self.boton_volver.copy()
        rect_volver_dibujo.x += offset
        rect_volver_dibujo.y += offset
        
        superficie.blit(self.boton_img, rect_volver_dibujo)
        tx = rect_volver_dibujo.centerx - self.texto_volver.get_width() // 2
        ty = rect_volver_dibujo.centery - self.texto_volver.get_height() // 2
        superficie.blit(self.texto_volver, (tx, ty))
