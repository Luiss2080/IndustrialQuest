# -*- coding: utf-8 -*-
"""
Pantalla de selección de niveles/capítulos del juego.
"""
import pygame
from src.constantes import COLOR_AZUL, COLOR_BLANCO, COLOR_NEGRO, ANCHO_PANTALLA
from src.pantalla import Pantalla
from src.datos_juego import TEMAS

class PantallaNiveles(Pantalla):
    """
    Administra la pantalla que permite al jugador seleccionar qué capítulo
    (tema de gramática) desea jugar.
    Los botones se generan de forma dinámica según la base de datos de datos_juego.py.
    """
    def __init__(self, motor):
        super().__init__(motor)

        # Cargar y configurar imagen base de botones (escalada)
        self.boton_img = self.motor.recursos.obtener_imagen("Boton.png")
        self.boton_img = pygame.transform.scale(self.boton_img, (400, 50))

        # Texto del encabezado
        self.texto_titulo = self.motor.fuente.render("Select a Chapter:", True, COLOR_BLANCO)

        # Generación de botones para cada categoría gramatical disponible
        self.botones = []
        self.textos_botones = []
        self.nombres_temas = list(TEMAS.keys())

        y = 100
        for tema in self.nombres_temas:
            # Rectángulo interactivo
            rect_boton = pygame.Rect(ANCHO_PANTALLA // 2 - 200, y, 400, 50)
            self.botones.append(rect_boton)

            # Renderizar el nombre del tema
            texto_renderizado = self.motor.fuente.render(tema, True, COLOR_NEGRO)
            
            # Centrar el texto dentro del botón
            x_texto = rect_boton.x + (rect_boton.width - texto_renderizado.get_width()) // 2
            y_texto = rect_boton.y + (rect_boton.height - texto_renderizado.get_height()) // 2
            
            self.textos_botones.append((texto_renderizado, (x_texto, y_texto)))
            y += 100

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if event_action := self._verificar_click_botones(evento):
                return event_action

    def _verificar_click_botones(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for i, boton in enumerate(self.botones):
                if boton.collidepoint(evento.pos):
                    # Asignar tema seleccionado al motor y comenzar el juego
                    self.motor.tema_actual = self.nombres_temas[i]
                    from src.pantalla_juego import PantallaJuego
                    self.motor.cambiar_pantalla(PantallaJuego(self.motor))
                    return True
        return False

    def actualizar(self, dt):
        pass

    def dibujar(self, superficie):
        # Fondo azul
        superficie.fill(COLOR_AZUL)

        # Dibujar título principal
        superficie.blit(self.texto_titulo, (ANCHO_PANTALLA // 2 - 100, 50))

        # Dibujar cada botón con su respectivo texto centrado
        for i, boton in enumerate(self.botones):
            superficie.blit(self.boton_img, boton)
            
            texto, posicion = self.textos_botones[i]
            superficie.blit(texto, posicion)
