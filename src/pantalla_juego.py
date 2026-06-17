# -*- coding: utf-8 -*-
"""
Pantalla principal de juego (gameplay) para IndustrialQuest.
"""
import random
import pygame
from src.constantes import COLOR_BLANCO, COLOR_ROJO, COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla
from src.datos_juego import TEMAS
from src.frase import FraseJuego

class PantallaJuego(Pantalla):
    """
    Gestiona la lógica interactiva del juego activo:
    - Movimiento y dibujado de las frases en pantalla.
    - Cómputo de la puntuación y las vidas restantes.
    - Captura de la entrada de teclado (typing game).
    - Progresión dinámica de la dificultad (velocidad y cantidad de frases).
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Reiniciar estadísticas de juego para iniciar limpia la partida
        self.motor.reiniciar_estadisticas()
        
        # Obtener los datos y recursos específicos del capítulo seleccionado
        self.tema_info = TEMAS[self.motor.tema_actual]
        
        # Cargar imágenes
        self.fondo = self.motor.recursos.obtener_imagen(self.tema_info["imagen_fondo"])
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
        
        self.signo = self.motor.recursos.obtener_imagen("Signo.png")
        self.signo = pygame.transform.scale(self.signo, (350, 158))
        
        self.imagen_corazon = self.motor.recursos.obtener_imagen("corazon.png")
        self.imagen_corazon = pygame.transform.scale(self.imagen_corazon, (70, 70))
        
        # Inicializar música de fondo del nivel en bucle
        self.sonido_nivel = self.motor.recursos.obtener_sonido(self.tema_info["audio_fondo"])
        self.sonido_nivel.play(-1)
        
        # Captura de tiempo inicial
        self.motor.tiempo_inicio = pygame.time.get_ticks()
        
        # Posiciones de los corazones (vidas)
        from src.constantes import POSICIONES_CORAZONES
        self.posiciones_corazones = POSICIONES_CORAZONES

        # Inicialización de variables locales del juego original (conservadas para total fidelidad)
        self.temporizador_puntuacion = 0
        self.duracion_puntuacion = 60
        self.posicion_puntuacion = None

    def generar_nueva_frase(self):
        """
        Retorna una nueva instancia de FraseJuego asociada al tema seleccionado,
        evitando repetir frases recientes (historial de hasta 10 frases).
        """
        tema = self.motor.tema_actual
        if not tema:
            return None

        nueva_frase_instancia = None
        frases_disponibles = TEMAS[tema]["frases"]
        
        # Control de intentos para evitar bucles infinitos
        intentos = 0
        while nueva_frase_instancia is None and intentos < 100:
            intentos += 1
            indice = random.randint(0, len(frases_disponibles) - 1)
            texto, palabra_correcta = frases_disponibles[indice]
            
            if texto not in self.motor.frases_recientes:
                nueva_frase_instancia = FraseJuego(texto, palabra_correcta)

        # Si todas las frases están en la cola reciente, tomar una aleatoria por seguridad
        if nueva_frase_instancia is None:
            indice = random.randint(0, len(frases_disponibles) - 1)
            texto, palabra_correcta = frases_disponibles[indice]
            nueva_frase_instancia = FraseJuego(texto, palabra_correcta)

        # Añadir al historial reciente
        self.motor.frases_recientes.append(nueva_frase_instancia.texto)
        if len(self.motor.frases_recientes) > 10:
            self.motor.frases_recientes.pop(0)

        return nueva_frase_instancia

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.sonido_nivel.stop()
                    from src.pantalla_fin import PantallaFin
                    self.motor.cambiar_pantalla(PantallaFin(self.motor))
                elif evento.key == pygame.K_BACKSPACE:
                    self.motor.texto_ingresado = self.motor.texto_ingresado[:-1]
                else:
                    # Permitir solo caracteres imprimibles (letras, espacios) en el búfer de entrada
                    if len(evento.unicode) > 0 and (evento.unicode.isprintable() or evento.unicode == " "):
                        self.motor.texto_ingresado += evento.unicode

    def actualizar(self, dt):
        # Aumentar la cantidad de frases en pantalla progresivamente según la puntuación
        cantidad_maxima_frases = (self.motor.puntuacion // 8) + 1
        while len(self.motor.frases_en_pantalla) < cantidad_maxima_frases:
            nueva = self.generar_nueva_frase()
            if nueva:
                self.motor.frases_en_pantalla.append(nueva)
            else:
                break

        # Aumentar la velocidad de desplazamiento de las palabras
        self.motor.velocidad_palabra = 0.4 + (self.motor.puntuacion / 50)

        # Disminuir el temporizador de puntuación si es mayor que cero
        if self.temporizador_puntuacion > 0:
            self.temporizador_puntuacion -= 1

        # Actualizar la posición de cada frase
        for frase in self.motor.frases_en_pantalla[:]:
            frase.x += self.motor.velocidad_palabra

            # Colisión con el borde derecho de la pantalla (pérdida de vida)
            if frase.x > ANCHO_PANTALLA:
                self.motor.frases_en_pantalla.remove(frase)
                self.motor.vidas -= 1
                
                # Efecto de audio de error
                sonido_error = self.motor.recursos.obtener_sonido(self.tema_info["audio_fracaso"])
                sonido_error.play()

                # Fin de la partida al agotar vidas
                if self.motor.vidas <= 0:
                    pygame.time.delay(4000)  # Espera de 4 segundos del juego original
                    self.sonido_nivel.stop()
                    from src.pantalla_fin import PantallaFin
                    self.motor.cambiar_pantalla(PantallaFin(self.motor))
                    return

            # Verificar si la palabra escrita del jugador coincide con la palabra correcta de la frase
            if self.motor.texto_ingresado.strip().lower() == frase.palabra_correcta.lower():
                self.motor.puntuacion += 1
                
                # Efecto de audio de éxito
                sonido_correcto = self.motor.recursos.obtener_sonido(self.tema_info["audio_clic"])
                sonido_correcto.play()

                # Eliminar la frase completada
                for p in self.motor.frases_en_pantalla:
                    if p.palabra_correcta.lower() == frase.palabra_correcta.lower():
                        self.motor.frases_en_pantalla.remove(p)
                        if not self.posicion_puntuacion:
                            self.posicion_puntuacion = p.x
                        break
                
                # Resetear el campo de entrada
                self.motor.texto_ingresado = ""
                self.temporizador_puntuacion = self.duracion_puntuacion

    def dibujar(self, superficie):
        # Dibujar fondo del capítulo
        superficie.blit(self.fondo, (0, 0))

        # Dibujar el cuadro y texto de puntuación inicial
        texto_pts = self.motor.fuente.render(f"Points: {self.motor.puntuacion}", True, COLOR_ROJO)
        rect_pts = texto_pts.get_rect(topleft=(10, 10))
        pygame.draw.rect(superficie, COLOR_BLANCO, rect_pts)
        superficie.blit(texto_pts, (10, 10))

        # Dibujar las vidas restantes (corazones)
        for i, (x, y) in enumerate(self.posiciones_corazones[:self.motor.vidas]):
            superficie.blit(self.imagen_corazon, (x, y))

        # Dibujar el letrero inferior decorativo
        superficie.blit(self.signo, (230, 518))

        # Dibujar las frases que caen con fondo blanco
        for frase in self.motor.frases_en_pantalla:
            texto_frase = self.motor.fuente.render(frase.texto, True, COLOR_NEGRO, COLOR_BLANCO)
            rect_fondo = texto_frase.get_rect(topleft=(frase.x, frase.y))
            pygame.draw.rect(superficie, COLOR_BLANCO, rect_fondo)
            superficie.blit(texto_frase, rect_fondo)

        # Calcular el tiempo transcurrido
        tiempo_transcurrido = 0
        if self.motor.tiempo_inicio is not None:
            tiempo_transcurrido = (pygame.time.get_ticks() - self.motor.tiempo_inicio) / 1000

        # Dibujar el tiempo transcurrido centrado en la parte superior
        texto_tiempo = self.motor.fuente.render(f"Time: {int(tiempo_transcurrido)}s", True, COLOR_ROJO)
        rect_tiempo = texto_tiempo.get_rect(midtop=(ANCHO_PANTALLA // 2, 10))
        pygame.draw.rect(superficie, COLOR_BLANCO, rect_tiempo)
        superficie.blit(texto_tiempo, rect_tiempo)

        # Dibujar la puntuación actual superpuesta (comportamiento original)
        texto_puntuacion_doble = self.motor.fuente.render(f"Points: {self.motor.puntuacion}", True, COLOR_ROJO)
        superficie.blit(texto_puntuacion_doble, (10, 10))

        # Dibujar la entrada de texto del jugador en la parte inferior
        texto_usr_render = self.motor.fuente.render(self.motor.texto_ingresado, True, COLOR_NEGRO)
        pos_x_usr = ANCHO_PANTALLA // 2 - texto_usr_render.get_width() // 2
        superficie.blit(texto_usr_render, (pos_x_usr, ALTO_PANTALLA - 50))
