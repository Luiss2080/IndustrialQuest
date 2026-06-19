# -*- coding: utf-8 -*-
"""
Pantalla de Registros de Producción (Production Logs) para IndustrialQuest: Woodwork Edition.
"""
import pygame
from src.constantes import COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA, RUTA_FUENTE
from src.pantalla import Pantalla
from src.tooltip import BilingualTooltip

class PantallaLogs(Pantalla):
    """
    Renderea el historial de turnos y la tabla de récords (High Scores) en un portapapeles bilingüe.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Colores
        self.color_fondo = (30, 22, 18)
        self.color_tablon = (120, 85, 50)
        self.color_papel = (245, 240, 230)
        self.color_metal = (180, 180, 180)
        self.color_metal_sombra = (90, 90, 90)
        self.color_texto = (30, 30, 30)
        self.color_texto_tabla = (50, 50, 50)
        self.color_cabecera = (120, 40, 10)
        
        self.boton_img = self.motor.recursos.obtener_imagen("Boton.png")
        self.boton_img = pygame.transform.scale(self.boton_img, (160, 46))
        self.boton_volver = self.boton_img.get_rect(bottomright=(ANCHO_PANTALLA - 30, ALTO_PANTALLA - 30))
        self.texto_volver = self.motor.fuente.render("Clock In", True, COLOR_NEGRO)

        # Cargar fuente de tabla pequeña para evitar overflow
        try:
            self.fuente_tabla = pygame.font.Font(RUTA_FUENTE, 20)
        except Exception:
            self.fuente_tabla = pygame.font.SysFont("Arial", 16)

        # Rect del papel para tooltip
        self.rect_papel = pygame.Rect(70, 75, ANCHO_PANTALLA - 140, ALTO_PANTALLA - 170)
        
        # Tooltips bilingües
        self.tooltip_logs = BilingualTooltip(self.motor, "Review shift history and factory top performance.", "Revisa el historial de turnos y el récord de rendimiento.")
        self.tooltip_volver = BilingualTooltip(self.motor, "Return to Main Menu.", "Volver al Menú Principal.")
        
        self.volver_hovered = False
        self.logs_hovered = False

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if self.boton_volver.collidepoint(evento.pos):
                        self.motor.reproducir_sonido("Correcta.wav")
                        from src.pantalla_menu import PantallaMenu
                        self.motor.cambiar_pantalla(PantallaMenu(self.motor))

    def actualizar(self, dt):
        pos_mouse = pygame.mouse.get_pos()
        self.volver_hovered = self.boton_volver.collidepoint(pos_mouse)
        self.logs_hovered = self.rect_papel.collidepoint(pos_mouse) and not self.volver_hovered

    def dibujar(self, superficie):
        # Fondo carbón oscuro
        superficie.fill(self.color_fondo)

        # 1. Dibujar Clipboard de madera
        rect_clip = pygame.Rect(50, 40, ANCHO_PANTALLA - 100, ALTO_PANTALLA - 120)
        pygame.draw.rect(superficie, (10, 7, 5), (rect_clip.x + 6, rect_clip.y + 6, rect_clip.width, rect_clip.height), border_radius=6)
        pygame.draw.rect(superficie, self.color_tablon, rect_clip, border_radius=6)
        pygame.draw.rect(superficie, (60, 40, 20), rect_clip, 4, border_radius=6)

        # 2. Pinza metálica superior
        rect_pinza = pygame.Rect(ANCHO_PANTALLA // 2 - 80, 25, 160, 35)
        pygame.draw.rect(superficie, self.color_metal_sombra, (rect_pinza.x + 3, rect_pinza.y + 3, rect_pinza.width, rect_pinza.height), border_radius=4)
        pygame.draw.rect(superficie, self.color_metal, rect_pinza, border_radius=4)
        pygame.draw.rect(superficie, (100, 100, 100), rect_pinza, 2, border_radius=4)
        pygame.draw.circle(superficie, (50, 50, 50), (rect_pinza.left + 20, rect_pinza.centery), 5)
        pygame.draw.circle(superficie, (50, 50, 50), (rect_pinza.right - 20, rect_pinza.centery), 5)

        # 3. Hoja de papel crema
        pygame.draw.rect(superficie, self.color_papel, self.rect_papel)
        pygame.draw.rect(superficie, (200, 195, 185), self.rect_papel, 2)

        # Título de la hoja
        titulo_render = self.motor.fuente.render("FACTORY PRODUCTION LEDGER", True, self.color_cabecera)
        superficie.blit(titulo_render, (self.rect_papel.x + 25, self.rect_papel.y + 15))
        pygame.draw.line(superficie, (200, 50, 50), (self.rect_papel.left + 20, self.rect_papel.y + 50), (self.rect_papel.right - 20, self.rect_papel.y + 50), 2)

        # Línea divisoria central vertical
        x_divisor = self.rect_papel.centerx
        pygame.draw.line(superficie, (180, 175, 160), (x_divisor, self.rect_papel.top + 65), (x_divisor, self.rect_papel.bottom - 20), 2)

        # === SECCIÓN IZQUIERDA: RECIENTES ===
        x_izq = self.rect_papel.left + 20
        y_item = self.rect_papel.top + 65
        
        lbl_recientes = self.motor.fuente.render("RECENT SHIFTS", True, (120, 80, 30))
        superficie.blit(lbl_recientes, (x_izq, y_item))
        y_item += 35
        
        cabeceras_izq = self.fuente_tabla.render("Shift Name            Score  Status", True, (100, 100, 100))
        superficie.blit(cabeceras_izq, (x_izq, y_item))
        y_item += 25
        
        recientes = self.motor.historico_logs[-5:]
        recientes.reverse()
        
        if not recientes:
            txt_vacio = self.fuente_tabla.render("No shifts completed yet.", True, (140, 140, 140))
            superficie.blit(txt_vacio, (x_izq + 10, y_item + 40))
        else:
            for log in recientes:
                nombre = log.get("nivel", "Unknown").replace("Level ", "Shift ")
                if len(nombre) > 16:
                    nombre = nombre[:14] + ".."
                score = log.get("score", 0)
                status = log.get("status", "COMPLETED")
                
                linea_str = f"{nombre:<16}   {score:>2}/15   {status}"
                color_linea = (40, 120, 30) if status == "COMPLETED" else (160, 40, 40)
                
                txt_linea = self.fuente_tabla.render(linea_str, True, color_linea)
                superficie.blit(txt_linea, (x_izq, y_item))
                y_item += 28

        # === SECCIÓN DERECHA: RÉCORDS / HIGH SCORES ===
        x_der = x_divisor + 20
        y_item_der = self.rect_papel.top + 65
        
        lbl_records = self.motor.fuente.render("HIGH SCORES 🏆", True, (170, 110, 20))
        superficie.blit(lbl_records, (x_der, y_item_der))
        y_item_der += 35
        
        cabeceras_der = self.fuente_tabla.render("Rank  Shift Name        Score  Acc", True, (100, 100, 100))
        superficie.blit(cabeceras_der, (x_der, y_item_der))
        y_item_der += 25
        
        records = self.motor.obtener_records()
        
        if not records:
            txt_vacio = self.fuente_tabla.render("No successful shifts recorded.", True, (140, 140, 140))
            superficie.blit(txt_vacio, (x_der + 10, y_item_der + 40))
        else:
            for idx, log in enumerate(records):
                nombre = log.get("nivel", "Unknown").replace("Level ", "Shift ")
                if len(nombre) > 15:
                    nombre = nombre[:13] + ".."
                score = log.get("score", 0)
                acc = int(log.get("accuracy", 0.0))
                
                linea_str = f" #{idx+1}   {nombre:<15}   {score:>2}/15   {acc:>3}%"
                
                # Resaltar primer lugar
                color_linea = (180, 120, 20) if idx == 0 else self.color_texto_tabla
                
                txt_linea = self.fuente_tabla.render(linea_str, True, color_linea)
                superficie.blit(txt_linea, (x_der, y_item_der))
                y_item_der += 28

        # 4. Dibujar botón volver (Clock In)
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
        if self.volver_hovered:
            self.tooltip_volver.dibujar(superficie, mx, my)
        elif self.logs_hovered:
            self.tooltip_logs.dibujar(superficie, mx, my)
