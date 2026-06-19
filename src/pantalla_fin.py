# -*- coding: utf-8 -*-
"""
Pantalla de Fin de Turno (Reporte de Producción / Game Over) para IndustrialQuest: Woodwork Edition.
"""
import pygame
from src.constantes import COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla

class PantallaFin(Pantalla):
    """
    Renderea la pantalla final del turno. Muestra un reporte detallado del desempeño del jugador
    (puntos, precisión, tiempo, WPM) tanto para turnos completados con éxito (Victoria) como
    para accidentes en la línea (Derrota).
    """
    def __init__(self, motor, victoria=False):
        super().__init__(motor)
        self.victoria = victoria
        
        # Detener sonidos previos y reproducir sonido correspondiente
        if self.victoria:
            sonido = self.motor.recursos.obtener_sonido("ganador.wav")
        else:
            sonido = self.motor.recursos.obtener_sonido("GameOver.wav")
        
        sonido.set_volume(self.motor.volumen_sfx)
        sonido.play()

        # Colores
        self.color_fondo = (35, 25, 20)
        self.color_reporte = (235, 230, 220) # Papel crema
        self.color_acero = (110, 115, 120)
        self.color_acero_borde = (60, 65, 70)
        self.color_texto = (30, 30, 30)

        # Configurar botón volver
        self.boton_img = self.motor.recursos.obtener_imagen("Boton.png")
        self.boton_img = pygame.transform.scale(self.boton_img, (200, 50))
        self.boton_continuar = self.boton_img.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA - 70))
        self.texto_continuar = self.motor.fuente.render("Return to Registry", True, COLOR_NEGRO)

        # Leer estadísticas del último registro del log
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
        pass

    def dibujar(self, superficie):
        # Fondo carbón oscuro
        superficie.fill(self.color_fondo)

        # Dibujar marco de acero industrial
        grosor_marco = 15
        pygame.draw.rect(superficie, self.color_acero, (0, 0, ANCHO_PANTALLA, ALTO_PANTALLA), grosor_marco)
        pygame.draw.rect(superficie, self.color_acero_borde, (grosor_marco, grosor_marco, ANCHO_PANTALLA - 2*grosor_marco, ALTO_PANTALLA - 2*grosor_marco), 3)

        # 1. Dibujar el Reporte de Turno (papel de fábrica)
        rect_reporte = pygame.Rect(180, 50, ANCHO_PANTALLA - 360, ALTO_PANTALLA - 160)
        
        # Sombra
        pygame.draw.rect(superficie, (15, 10, 5), (rect_reporte.x + 6, rect_reporte.y + 6, rect_reporte.width, rect_reporte.height), border_radius=6)
        # Papel crema
        pygame.draw.rect(superficie, self.color_reporte, rect_reporte, border_radius=6)
        pygame.draw.rect(superficie, (180, 170, 150), rect_reporte, 4, border_radius=6)

        # 2. Dibujar Encabezado del reporte
        titulo_str = "SHIFT REPORT: COMPLETED" if self.victoria else "SHIFT REPORT: FAILED"
        color_titulo = (45, 135, 45) if self.victoria else (180, 45, 45)
        
        txt_titulo = self.motor.fuente.render(titulo_str, True, color_titulo)
        superficie.blit(txt_titulo, (rect_reporte.centerx - txt_titulo.get_width() // 2, rect_reporte.top + 25))

        # Línea divisoria
        pygame.draw.line(superficie, (180, 40, 40), (rect_reporte.left + 30, rect_reporte.top + 70), (rect_reporte.right - 30, rect_reporte.top + 70), 2)

        # 3. Listar estadísticas de producción
        stats = [
            ("Shift Zone:", f"{self.ultimo_log.get('nivel', 'Unknown')}".replace("Level ", "Shift ")),
            ("Work Status:", "SUCCESSFUL" if self.victoria else "ACCIDENT RECORDED"),
            ("Wood Planks Processed:", f"{self.ultimo_log.get('score', 0)} items"),
            ("Typing Accuracy:", f"{int(self.ultimo_log.get('accuracy', 0.0))}%"),
            ("Shift Duration:", f"{self.ultimo_log.get('time_taken', 0)} seconds"),
            ("Production Speed:", f"{self.ultimo_log.get('wpm', 0)} WPM")
        ]

        y_stat = rect_reporte.top + 95
        for etiqueta, valor in stats:
            # Etiqueta
            txt_etiqueta = self.motor.fuente.render(etiqueta, True, (80, 80, 80))
            superficie.blit(txt_etiqueta, (rect_reporte.left + 30, y_stat))
            
            # Valor
            color_val = (40, 100, 40) if etiqueta == "Work Status:" and self.victoria else (160, 40, 40) if etiqueta == "Work Status:" else self.color_texto
            txt_valor = self.motor.fuente.render(valor, True, color_val)
            superficie.blit(txt_valor, (rect_reporte.right - 30 - txt_valor.get_width(), y_stat))
            
            y_stat += 38

        # 4. Dibujar botón Continuar (Clock In)
        mouse_pos = pygame.mouse.get_pos()
        offset = 2 if self.boton_continuar.collidepoint(mouse_pos) else 0
        
        rect_cont_dibujo = self.boton_continuar.copy()
        rect_cont_dibujo.x += offset
        rect_cont_dibujo.y += offset
        
        superficie.blit(self.boton_img, rect_cont_dibujo)
        tx = rect_cont_dibujo.centerx - self.texto_continuar.get_width() // 2
        ty = rect_cont_dibujo.centery - self.texto_continuar.get_height() // 2
        superficie.blit(self.texto_continuar, (tx, ty))
