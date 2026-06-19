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

        # Configurar pantalla principal en Pantalla Completa con escalado automático (FULLSCREEN | SCALED)
        self.pantalla_principal = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.FULLSCREEN | pygame.SCALED)
        pygame.display.set_caption("IndustrialQuest")

        # Cargar la tipografía del juego
        try:
            self.fuente = pygame.font.Font(RUTA_FUENTE, TAMAÑO_FUENTE)
        except pygame.error as e:
            print(f"Error al cargar la fuente en {RUTA_FUENTE}. Usando fuente por defecto: {e}")
            self.fuente = pygame.font.SysFont("Arial", TAMAÑO_FUENTE)

        # Fuentes del sistema para soportar acentos y símbolos sin errores de renderizado
        self.fuente_sistemas = pygame.font.SysFont("Calibri", 20, bold=True)
        self.fuente_sistemas_grande = pygame.font.SysFont("Calibri", 26, bold=True)

        # Reloj de Pygame para controlar los fotogramas por segundo (FPS)
        self.reloj = pygame.time.Clock()

        # Inicializar el administrador de recursos (imágenes y sonidos en caché)
        self.recursos = AdministradorRecursos()

        # Configuración persistente y logs
        self.historico_logs = []
        self.volumen_musica = 0.5
        self.volumen_sfx = 0.7
        self.velocidad_ajustada = 1.0
        self.niveles_completados = []
        self.cargar_datos()

        # Inicialización del estado y estadísticas globales compartidas
        self.puntuacion = 0
        self.vidas = 3
        self.texto_ingresado = ""
        self.frases_en_pantalla = []
        self.tiempo_inicio = None
        self.tema_actual = None
        self.velocidad_palabra = 0.4
        self.frases_recientes = []

        # Estadísticas de tecleo detalladas
        self.pulsaciones_correctas = 0
        self.pulsaciones_incorrectas = 0

        # Pantalla activa y flag de control de bucle
        self.pantalla_activa = None
        self.corriendo = True

    def cargar_datos(self):
        import json
        import os
        self.ruta_datos = "production_logs.json"
        if os.path.exists(self.ruta_datos):
            try:
                with open(self.ruta_datos, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    self.historico_logs = datos.get("logs", [])
                    self.volumen_musica = datos.get("volumen_musica", 0.5)
                    self.volumen_sfx = datos.get("volumen_sfx", 0.7)
                    self.velocidad_ajustada = datos.get("velocidad_ajustada", 1.0)
                    self.niveles_completados = datos.get("niveles_completados", [])
            except Exception as e:
                print(f"Error al cargar logs: {e}")

    def guardar_datos(self):
        import json
        datos = {
            "logs": self.historico_logs,
            "volumen_musica": self.volumen_musica,
            "volumen_sfx": self.volumen_sfx,
            "velocidad_ajustada": self.velocidad_ajustada,
            "niveles_completados": self.niveles_completados
        }
        try:
            with open("production_logs.json", "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar logs: {e}")

    def reproducir_sonido(self, nombre):
        sonido = self.recursos.obtener_sonido(nombre)
        sonido.set_volume(self.volumen_sfx)
        sonido.play()
        return sonido

    def reproducir_musica(self, nombre, loops=-1):
        musica = self.recursos.obtener_sonido(nombre)
        musica.set_volume(self.volumen_musica)
        musica.play(loops)
        return musica

    def obtener_records(self):
        """
        Retorna los 5 mejores turnos de trabajo completados exitosamente,
        ordenados por puntuación, precisión y menor tiempo.
        """
        exitosos = [log for log in self.historico_logs if log.get("status") == "COMPLETED"]
        exitosos.sort(key=lambda x: (-x.get("score", 0), -x.get("accuracy", 0.0), x.get("time_taken", 9999)))
        return exitosos[:5]

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
        self.pulsaciones_correctas = 0
        self.pulsaciones_incorrectas = 0

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
        self.reproducir_sonido("Title.wav")

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
