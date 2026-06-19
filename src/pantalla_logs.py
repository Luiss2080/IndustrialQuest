# -*- coding: utf-8 -*-
"""
Pantalla de Registros de Producción (Production Logs) para IndustrialQuest: Woodwork Edition.
"""
import pygame
from src.constantes import COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla

class PantallaLogs(Pantalla):
    """
    Renderea los registros históricos de turnos de trabajo completados (puntuación, precisión, WPM).
    Presenta la información sobre una tabla rústica tipo Clipboard (Portapapeles de fábrica).
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Colores
        self.color_fondo = (35, 25, 20)
        self.color_tablon = (120, 85, 50)
        self.color_papel = (235, 230, 220)
        self.color_metal = (180, 180, 180)
        self.color_metal_sombra = (90, 90, 90)
        self.color_texto = (30, 30, 30)
        self.color_cabecera = (90, 45, 10)
        
        self.boton_img = self.motor.recursos.obtener_imagen("Boton.png")
        self.boton_img = pygame.transform.scale(self.boton_img, (160, 46))
        self.boton_volver = self.boton_img.get_rect(bottomright=(ANCHO_PANTALLA - 30, ALTO_PANTALLA - 30))
        self.texto_volver = self.motor.fuente.render("Clock In", True, COLOR_NEGRO)

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if self.boton_volver.collidepoint(evento.pos):
                        self.motor.reproducir_sonido("Correcta.wav")
                        from src.pantalla_menu import PantallaMenu
                        self.motor.cambiar_pantalla(PantallaMenu(self.motor))

    def actualizar(self, dt):
        pass

    def dibujar(self, superficie):
        # Fondo carbón oscuro
        superficie.fill(self.color_fondo)

        # 1. Dibujar el Clipboard de madera (Fondo del portapapeles)
        rect_clip = pygame.Rect(80, 40, ANCHO_PANTALLA - 160, ALTO_PANTALLA - 120)
        pygame.draw.rect(superficie, (20, 15, 10), (rect_clip.x + 6, rect_clip.y + 6, rect_clip.width, rect_clip.height), border_radius=6)
        pygame.draw.rect(superficie, self.color_tablon, rect_clip, border_radius=6)
        pygame.draw.rect(superficie, (60, 40, 20), rect_clip, 4, border_radius=6)

        # 2. Dibujar la pinza metálica superior del portapapeles
        rect_pinza = pygame.Rect(ANCHO_PANTALLA // 2 - 80, 25, 160, 35)
        pygame.draw.rect(superficie, self.color_metal_sombra, (rect_pinza.x + 3, rect_pinza.y + 3, rect_pinza.width, rect_pinza.height), border_radius=4)
        pygame.draw.rect(superficie, self.color_metal, rect_pinza, border_radius=4)
        pygame.draw.rect(superficie, (100, 100, 100), rect_pinza, 2, border_radius=4)
        # Remaches metálicos en la pinza
        pygame.draw.circle(superficie, (50, 50, 50), (rect_pinza.left + 20, rect_pinza.centery), 5)
        pygame.draw.circle(superficie, (50, 50, 50), (rect_pinza.right - 20, rect_pinza.centery), 5)

        # 3. Dibujar la hoja de papel blanca sobre el Clipboard
        rect_papel = pygame.Rect(110, 75, ANCHO_PANTALLA - 220, ALTO_PANTALLA - 170)
        pygame.draw.rect(superficie, self.color_papel, rect_papel)
        pygame.draw.rect(superficie, (200, 195, 180), rect_papel, 2)

        # 4. Título de la hoja
        titulo_render = self.motor.fuente.render("PRODUCTION LOGS - RECENT SHIFTS", True, self.color_cabecera)
        superficie.blit(titulo_render, (rect_papel.x + 25, rect_papel.y + 20))

        # Línea divisoria roja (estilo cuaderno)
        pygame.draw.line(superficie, (220, 80, 80), (rect_papel.left + 20, rect_papel.y + 55), (rect_papel.right - 20, rect_papel.y + 55), 2)

        # 5. Listar los logs históricos (máximo los últimos 6 registros)
        registros = self.motor.historico_logs[-6:]
        registros.reverse() # Mostrar primero los más recientes

        y_item = rect_papel.y + 70
        
        # Dibujar cabeceras de columnas
        texto_cabeceras = self.motor.fuente.render("Shift Name          Pts    Acc     Time     Status", True, (80, 80, 80))
        superficie.blit(texto_cabeceras, (rect_papel.x + 20, y_item))
        y_item += 35
        
        if not registros:
            # Mensaje si no hay registros
            texto_vacio = self.motor.fuente.render("No completed shifts found in logs.", True, (130, 130, 130))
            superficie.blit(texto_vacio, (rect_papel.x + 40, rect_papel.centery - 10))
            texto_subvacio = self.motor.fuente.render("Start a shift to record production data!", True, (130, 130, 130))
            superficie.blit(texto_subvacio, (rect_papel.x + 20, rect_papel.centery + 25))
        else:
            for log in registros:
                nivel_nombre = log.get("nivel", "Unknown Level")
                # Recortar nombre si es muy largo
                if len(nivel_nombre) > 18:
                    nivel_nombre = nivel_nombre[:16] + ".."
                    
                score = log.get("score", 0)
                acc = log.get("accuracy", 0.0)
                time_taken = log.get("time_taken", 0)
                status = log.get("status", "COMPLETED")
                
                # Renderizar datos en columnas alineadas
                linea_str = f"{nivel_nombre:<18}   {score:>2}   {int(acc):>3}%   {time_taken:>3}s     {status}"
                
                color_status = (50, 120, 40) if status == "COMPLETED" else (160, 40, 40)
                texto_log = self.motor.fuente.render(linea_str, True, self.color_texto)
                superficie.blit(texto_log, (rect_papel.x + 20, y_item))
                y_item += 32

        # 6. Dibujar botón volver (Clock In)
        mouse_pos = pygame.mouse.get_pos()
        offset = 2 if self.boton_volver.collidepoint(mouse_pos) else 0
        
        rect_volver_dibujo = self.boton_volver.copy()
        rect_volver_dibujo.x += offset
        rect_volver_dibujo.y += offset
        
        superficie.blit(self.boton_img, rect_volver_dibujo)
        tx = rect_volver_dibujo.centerx - self.texto_volver.get_width() // 2
        ty = rect_volver_dibujo.centery - self.texto_volver.get_height() // 2
        superficie.blit(self.texto_volver, (tx, ty))
