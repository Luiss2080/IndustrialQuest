# -*- coding: utf-8 -*-
"""
Motor principal del juego IndustrialQuest. Gestiona las pantallas y el ciclo de vida del juego.
"""
import sys
import pygame
from src.constantes import ANCHO_PANTALLA, ALTO_PANTALLA, COLOR_AZUL, RUTA_FUENTE, TAMAÑO_FUENTE
from src.administrador_recursos import AdministradorRecursos

class MotorJuego:
    """
    Clase central que implementa el ciclo de vida completo del videojuego.
    Inicializa los subsistemas de Pygame, gestiona la máquina de estados de las pantallas
    y coordina las variables globales del progreso del jugador.
    """
    def __init__(self):
        # Inicializar los módulos de Pygame y el mezclador de sonidos
        pygame.init()
        pygame.mixer.init()

        # Configurar pantalla principal y el título oficial de la ventana
        self.pantalla_principal = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("IndustrialQuest")

        # Cargar la tipografía del juego
        try:
            self.fuente = pygame.font.Font(RUTA_FUENTE, TAMAÑO_FUENTE)
        except pygame.error as e:
            print(f"Error al cargar la fuente en {RUTA_FUENTE}. Usando fuente por defecto: {e}")
            self.fuente = pygame.font.SysFont("Arial", TAMAÑO_FUENTE)

        # Reloj de Pygame para controlar los fotogramas por segundo (FPS)
        self.reloj = pygame.time.Clock()

        # Inicializar el administrador de recursos (imágenes y sonidos en caché)
        self.recursos = AdministradorRecursos()

        # Inicialización del estado y estadísticas globales compartidas
        self.puntuacion = 0
        self.vidas = 3
        self.texto_ingresado = ""
        self.frases_en_pantalla = []
        self.tiempo_inicio = None
        self.tema_actual = None
        self.velocidad_palabra = 0.4
        self.frases_recientes = []

        # Pantalla activa y flag de control de bucle
        self.pantalla_activa = None
        self.corriendo = True

    def cambiar_pantalla(self, nueva_pantalla):
        """
        Transiciona el juego hacia una nueva pantalla.
        """
        self.pantalla_activa = nueva_pantalla

    def reiniciar_estadisticas(self):
        """
        Restablece todos los contadores de progreso del jugador a sus valores iniciales.
        """
        self.puntuacion = 0
        self.vidas = 3
        self.texto_ingresado = ""
        self.frases_en_pantalla = []
        self.tiempo_inicio = None
        self.frases_recientes = []
        self.velocidad_palabra = 0.4

    def salir(self):
        """
        Detiene la ejecución del juego y libera de forma segura los recursos del sistema.
        """
        self.corriendo = False
        pygame.quit()
        sys.exit()

    def ejecutar(self):
        """
        Ciclo principal de ejecución (Game Loop).
        Inicia reproduciendo la música de la pantalla de bienvenida y carga el menú principal.
        """
        # Reproducir sonido de título al inicio
        sonido_titulo = self.recursos.obtener_sonido("Title.wav")
        sonido_titulo.play()

        # Definir y mostrar la pantalla de menú inicial
        from src.pantalla_menu import PantallaMenu
        self.cambiar_pantalla(PantallaMenu(self))

        # Bucle principal de ejecución a 60 fotogramas por segundo
        while self.corriendo:
            dt = self.reloj.tick(60)

            # Capturar eventos generales del juego
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.salir()

            # Delegar el manejo de lógica, actualización y dibujo a la pantalla activa
            if self.pantalla_activa:
                self.pantalla_activa.manejar_eventos(eventos)
                self.pantalla_activa.actualizar(dt)
                self.pantalla_activa.dibujar(self.pantalla_principal)

            # Volcar el búfer de dibujo en pantalla
            pygame.display.flip()
