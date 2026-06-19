# -*- coding: utf-8 -*-
"""
Pantalla de Fin de Turno (Reporte de Producción / Game Over) para IndustrialQuest: Woodwork Edition.
"""
import pygame
from src.constantes import COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla
from src.tooltip import BilingualTooltip

class PantallaFin(Pantalla):
    """
    Renderea el reporte final de turno en un formato de hoja extendida de alta visibilidad,
    con alineación de dos columnas para prevenir encabalgamiento de texto.
    """
    def __init__(self, motor, victoria=False):
        super().__init__(motor)
        self.victoria = victoria
        
        # Reproducir sonido de fin de turno
        if self.victoria:
            sonido = self.motor.recursos.obtener_sonido("ganador.wav")
        else:
            sonido = self.motor.recursos.obtener_sonido("GameOver.wav")
        
        sonido.set_volume(self.motor.volumen_sfx)
        sonido.play()

        # Colores
        self.color_fondo = (30, 22, 18)
        self.color_reporte = (245, 240, 230)
        self.color_acero = (110, 115, 120)
        self.color_acero_borde = (60, 65, 70)
        self.color_texto = (30, 30, 30)

        # Botón continuar (Clock In)
        self.boton_img = self.motor.recursos.obtener_imagen("Boton.png")
        self.boton_img = pygame.transform.scale(self.boton_img, (200, 50))
        self.boton_continuar = self.boton_img.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA - 70))
        self.texto_continuar = self.motor.fuente.render("Return to Registry", True, COLOR_NEGRO)

        # Leer estadísticas
        if self.motor.historico_logs:
            self.ultimo_log = self.motor.historico_logs[-1]
        else:
            self.ultimo_log = {
                "nivel": self.motor.tema_actual or "Shift 1: Reception Area",
                "score": self.motor.puntuacion,
                "accuracy": 100.0,
                "time_taken": 0,
                "wpm": 0,
                "status": "COMPLETED" if self.victoria else "FAILED"
            }

        # Configurar rect del reporte para colisión de tooltip
        self.rect_reporte = pygame.Rect(100, 50, ANCHO_PANTALLA - 200, ALTO_PANTALLA - 160)

        # Tooltips bilingües
        self.tooltip_reporte = BilingualTooltip(self.motor, "Shift performance report sheet.", "Hoja de reporte de rendimiento del turno.")
        self.tooltip_volver = BilingualTooltip(self.motor, "Return to Shift Registry screen.", "Volver a la pantalla del Registro de Turnos.")

        self.continuar_hovered = False
        self.reporte_hovered = False

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if self.boton_continuar.collidepoint(evento.pos):
                        self.motor.reproducir_sonido("Correcta.wav")
                        self.motor.reiniciar_estadisticas()
                        from src.pantalla_niveles import PantallaNiveles
                        self.motor.cambiar_pantalla(PantallaNiveles(self.motor))
                        return

    def actualizar(self, dt):
        pos_mouse = pygame.mouse.get_pos()
        self.continuar_hovered = self.boton_continuar.collidepoint(pos_mouse)
        self.reporte_hovered = self.rect_reporte.collidepoint(pos_mouse) and not self.continuar_hovered

    def dibujar(self, superficie):
        superficie.fill(self.color_fondo)

        # Marco de acero
        grosor_marco = 15
        pygame.draw.rect(superficie, self.color_acero, (0, 0, ANCHO_PANTALLA, ALTO_PANTALLA), grosor_marco)
        pygame.draw.rect(superficie, self.color_acero_borde, (grosor_marco, grosor_marco, ANCHO_PANTALLA - 2*grosor_marco, ALTO_PANTALLA - 2*grosor_marco), 3)

        # Sombra del reporte
        pygame.draw.rect(superficie, (10, 7, 5), (self.rect_reporte.x + 6, self.rect_reporte.y + 6, self.rect_reporte.width, self.rect_reporte.height), border_radius=6)
        
        # Papel crema
        pygame.draw.rect(superficie, self.color_reporte, self.rect_reporte, border_radius=6)
        pygame.draw.rect(superficie, (180, 170, 150), self.rect_reporte, 4, border_radius=6)

        # Encabezado
        titulo_str = "SHIFT REPORT: COMPLETED" if self.victoria else "SHIFT REPORT: FAILED"
        color_titulo = (40, 140, 40) if self.victoria else (190, 40, 40)
        
        txt_titulo = self.motor.fuente.render(titulo_str, True, color_titulo)
        superficie.blit(txt_titulo, (self.rect_reporte.centerx - txt_titulo.get_width() // 2, self.rect_reporte.top + 25))

        # Línea divisoria roja
        pygame.draw.line(superficie, (190, 40, 40), (self.rect_reporte.left + 30, self.rect_reporte.top + 70), (self.rect_reporte.right - 30, self.rect_reporte.top + 70), 2)

        # Lista de estadísticas en formato de dos columnas de alta precisión
        stats = [
            ("Shift Zone:", f"{self.ultimo_log.get('nivel', 'Unknown')}".replace("Level ", "Shift ")),
            ("Work Status:", "SUCCESSFUL" if self.victoria else "ACCIDENT RECORDED"),
            ("Wood Planks Processed:", f"{self.ultimo_log.get('score', 0)} / 15 items"),
            ("Typing Accuracy:", f"{int(self.ultimo_log.get('accuracy', 0.0))}%"),
            ("Shift Duration:", f"{self.ultimo_log.get('time_taken', 0)} seconds"),
            ("Production Speed:", f"{self.ultimo_log.get('wpm', 0)} WPM")
        ]

        y_stat = self.rect_reporte.top + 95
        for etiqueta, valor in stats:
            # Columna izquierda (Etiqueta)
            txt_etiqueta = self.motor.fuente_sistemas.render(etiqueta, True, (80, 80, 95))
            superficie.blit(txt_etiqueta, (self.rect_reporte.left + 45, y_stat))
            
            # Columna derecha (Valor)
            color_val = (40, 130, 40) if (etiqueta == "Work Status:" and self.victoria) else (190, 40, 40) if etiqueta == "Work Status:" else self.color_texto
            txt_valor = self.motor.fuente_sistemas.render(valor, True, color_val)
            superficie.blit(txt_valor, (self.rect_reporte.right - 45 - txt_valor.get_width(), y_stat))
            
            y_stat += 38

        # Botón continuar (Clock In)
        offset = 2 if self.continuar_hovered else 0
        rect_cont_dibujo = self.boton_continuar.copy()
        rect_cont_dibujo.x += offset
        rect_cont_dibujo.y += offset
        
        superficie.blit(self.boton_img, rect_cont_dibujo)
        tx = rect_cont_dibujo.centerx - self.texto_continuar.get_width() // 2
        ty = rect_cont_dibujo.centery - self.texto_continuar.get_height() // 2
        superficie.blit(self.texto_continuar, (tx, ty))

        # Dibujar tooltips flotantes
        mx, my = pygame.mouse.get_pos()
        if self.continuar_hovered:
            self.tooltip_volver.dibujar(superficie, mx, my)
        elif self.reporte_hovered:
            self.tooltip_reporte.dibujar(superficie, mx, my)
