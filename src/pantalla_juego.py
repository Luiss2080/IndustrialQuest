# -*- coding: utf-8 -*-
"""
Pantalla principal de juego (gameplay) para IndustrialQuest: Woodwork Edition.
"""
import random
import pygame
import datetime
from src.constantes import COLOR_BLANCO, COLOR_ROJO, COLOR_NEGRO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.pantalla import Pantalla
from src.datos_juego import TEMAS
from src.frase import LANES_Y, FraseJuego
from src.tooltip import BilingualTooltip

class Particula:
    """
    Representa una pequeña partícula física (aserrín, chispas o astillas)
    con movimiento, gravedad y encogimiento progresivo por tiempo de vida.
    """
    def __init__(self, x, y, vx, vy, color, vida, gravedad=0.15, tamaño=5):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.vida = vida
        self.vida_max = vida
        self.gravedad = gravedad
        self.tamaño = tamaño

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravedad
        self.vida -= 1

    def dibujar(self, superficie):
        if self.vida > 0:
            tam = max(1, int(self.tamaño * (self.vida / self.vida_max)))
            pygame.draw.rect(superficie, self.color, (int(self.x), int(self.y), tam, tam))

class PantallaJuego(Pantalla):
    """
    Clase central del gameplay de IndustrialQuest: Woodwork Edition.
    Visuales estáticos, sin sonidos en tipeo, alto contraste de lectura y menú de pausa.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Reiniciar estadísticas de juego
        self.motor.reiniciar_estadisticas()
        self.tema_info = TEMAS[self.motor.tema_actual]
        
        # Cargar imágenes base
        self.fondo = self.motor.recursos.obtener_imagen(self.tema_info["imagen_fondo"])
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
        
        self.sierra_vida = self.motor.recursos.obtener_imagen("corazon.png")
        self.sierra_vida = pygame.transform.scale(self.sierra_vida, (36, 36))
        
        self.estrella_icon = self.motor.recursos.obtener_imagen("estrella.png")
        self.estrella_icon = pygame.transform.scale(self.estrella_icon, (24, 24))

        self.boton_img = self.motor.recursos.obtener_imagen("Boton.png")
        self.boton_img = pygame.transform.scale(self.boton_img, (180, 42))

        # Inicializar música de fondo del nivel en bucle
        self.sonido_nivel = self.motor.recursos.obtener_sonido(self.tema_info["audio_fondo"])
        self.sonido_nivel.set_volume(self.motor.volumen_musica)
        self.sonido_nivel.play(-1)
        
        # Rotación automática de música
        self.tiempo_cambio_musica = 90.0 * 1000  # 90 segundos
        self.tiempo_ultima_musica = pygame.time.get_ticks()
        try:
            self.indice_musica_actual = int(self.motor.tema_actual.split(" ")[1].split(":")[0]) - 1
        except Exception:
            self.indice_musica_actual = 0
        
        # Captura de tiempo inicial
        self.motor.tiempo_inicio = pygame.time.get_ticks()
        self.tiempo_pausado_acumulado = 0
        self.momento_pausa = 0

        # Configuración del juego
        self.objetivo_shift = 15
        self.particulas = []
        self.plank_activo = None
        self.shake_duracion = 0
        self.pausado = False
        
        # Paleta de colores rústica mejorada para alto contraste
        self.color_madera = (245, 235, 215)          # Madera de abedul claro (máximo contraste para texto negro)
        self.color_madera_veta = (215, 195, 175)     # Vetado suave
        self.color_madera_borde = (60, 35, 15)       # Borde oscuro
        self.color_madera_active_borde = (255, 120, 0) # Resaltado naranja de actividad
        self.color_acero = (90, 95, 100)
        
        self.x_sierras = 730
        self.cogs_x = [40, 200, 360, 520, 680]

        # Definir áreas de rectángulos del HUD para mostrar Tooltips
        self.rect_hud_progreso = pygame.Rect(15, 14, 260, 44)
        self.rect_hud_tiempo = pygame.Rect(ANCHO_PANTALLA // 2 - 80, 14, 180, 44)
        self.rect_btn_pausa = pygame.Rect(ANCHO_PANTALLA - 280, 14, 70, 44)
        self.rect_hud_vidas = pygame.Rect(ANCHO_PANTALLA - 195, 14, 180, 44)
        self.rect_input_box = pygame.Rect(ANCHO_PANTALLA // 2 - 180, ALTO_PANTALLA - 80, 360, 50)

        # Botones del Menú de Pausa
        self.rect_pausa_panel = pygame.Rect(180, 80, 440, 440)
        self.btn_pausa_resume = pygame.Rect(210, 140, 380, 44)
        self.btn_pausa_restart = pygame.Rect(210, 200, 380, 44)
        self.btn_pausa_music_menos = pygame.Rect(440, 265, 36, 36)
        self.btn_pausa_music_mas = pygame.Rect(540, 265, 36, 36)
        self.btn_pausa_sfx_menos = pygame.Rect(440, 320, 36, 36)
        self.btn_pausa_sfx_mas = pygame.Rect(540, 320, 36, 36)
        self.btn_pausa_abandon = pygame.Rect(210, 395, 380, 44)

        # Tooltips de juego
        self.tooltip_progreso = BilingualTooltip(self.motor, "Current completed planks / target.", "Tablones completados en este turno / objetivo.")
        self.tooltip_tiempo = BilingualTooltip(self.motor, "Total elapsed shift time.", "Tiempo total de turno transcurrido.")
        self.tooltip_pausa = BilingualTooltip(self.motor, "Pause the current shift.", "Pausar el turno de trabajo actual.")
        self.tooltip_vidas = BilingualTooltip(self.motor, "Remaining lives before shift failure.", "Vidas restantes antes de fallar el turno.")
        self.tooltip_input = BilingualTooltip(self.motor, "Type the missing English word here.", "Escribe la palabra faltante en inglés aquí.")

        self.hover_progreso = False
        self.hover_tiempo = False
        self.hover_pausa = False
        self.hover_vidas = False
        self.hover_input = False

    def generar_nueva_frase(self):
        tema = self.motor.tema_actual
        if not tema:
            return None

        # Evitar solapamientos (carril libre en la entrada)
        lanes_ocupados = {0: False, 1: False, 2: False}
        for frase in self.motor.frases_en_pantalla:
            if frase.x < 180:
                lanes_ocupados[frase.lane] = True
        
        lanes_libres = [lane for lane, ocupado in lanes_ocupados.items() if not ocupado]
        if not lanes_libres:
            return None
            
        lane_seleccionado = random.choice(lanes_libres)
        frases_disponibles = TEMAS[tema]["frases"]
        
        nueva_frase_instancia = None
        intentos = 0
        while nueva_frase_instancia is None and intentos < 100:
            intentos += 1
            indice = random.randint(0, len(frases_disponibles) - 1)
            texto, palabra_correcta = frases_disponibles[indice]
            
            if texto not in self.motor.frases_recientes:
                nueva_frase_instancia = FraseJuego(texto, palabra_correcta, lane=lane_seleccionado)

        if nueva_frase_instancia is None:
            indice = random.randint(0, len(frases_disponibles) - 1)
            texto, palabra_correcta = frases_disponibles[indice]
            nueva_frase_instancia = FraseJuego(texto, palabra_correcta, lane=lane_seleccionado)

        self.motor.frases_recientes.append(nueva_frase_instancia.texto)
        if len(self.motor.frases_recientes) > 10:
            self.motor.frases_recientes.pop(0)

        return nueva_frase_instancia

    def obtener_rect_tablon(self, frase):
        texto = frase.texto
        underscores = "______" if "______" in texto else "___" if "___" in texto else ""
        if underscores:
            partes = texto.split(underscores, 1)
            before = partes[0]
            after = partes[1]
        else:
            before = texto
            after = ""
            
        w_before, _ = self.motor.fuente.size(before)
        w_after, _ = self.motor.fuente.size(after)
        
        is_active = (self.plank_activo == frase)
        if is_active:
            typed = self.motor.texto_ingresado
            ans_str = frase.palabra_correcta[0] if isinstance(frase.palabra_correcta, list) else frase.palabra_correcta
            remaining_len = max(0, len(ans_str) - len(typed))
            blank_content = typed + ("_" * remaining_len)
        else:
            blank_content = underscores
            
        w_blank, _ = self.motor.fuente.size(blank_content)
        total_text_width = w_before + w_blank + w_after
        plank_width = total_text_width + 40
        plank_height = 48
        return pygame.Rect(frase.x, frase.y - plank_height // 2, plank_width, plank_height)

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if self.pausado:
                        self._reanudar_juego()
                    else:
                        self._pausar_juego()
                elif not self.pausado:
                    if evento.key == pygame.K_BACKSPACE:
                        self.motor.texto_ingresado = self.motor.texto_ingresado[:-1]
                    else:
                        char = evento.unicode
                        if len(char) > 0 and (char.isprintable() or char == " "):
                            nuevo_buffer = self.motor.texto_ingresado + char
                            coincidencia = False
                            for frase in self.motor.frases_en_pantalla:
                                respuestas = frase.palabra_correcta
                                if isinstance(respuestas, list):
                                    coincide_pref = any(r.lower().startswith(nuevo_buffer.lower()) for r in respuestas)
                                else:
                                    coincide_pref = respuestas.lower().startswith(nuevo_buffer.lower())
                                
                                if coincide_pref:
                                    coincidencia = True
                                    break
                            
                            self.motor.texto_ingresado = nuevo_buffer
                            if coincidencia:
                                self.motor.pulsaciones_correctas += 1
                                if self.plank_activo:
                                    self._crear_chispas_tallado(self.plank_activo)
                            else:
                                self.motor.pulsaciones_incorrectas += 1

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: # Clic izquierdo
                    # Si está pausado, manejar interfaz del menú de pausa
                    if self.pausado:
                        if self.btn_pausa_resume.collidepoint(evento.pos):
                            self.motor.reproducir_sonido("Correcta.wav")
                            self._reanudar_juego()
                        elif self.btn_pausa_restart.collidepoint(evento.pos):
                            self.sonido_nivel.stop()
                            self.motor.reproducir_sonido("Correcta.wav")
                            # Reiniciar la pantalla de juego
                            self.__init__(self.motor)
                        elif self.btn_pausa_music_menos.collidepoint(evento.pos):
                            self.motor.volumen_musica = max(0.0, self.motor.volumen_musica - 0.1)
                            self.sonido_nivel.set_volume(self.motor.volumen_musica)
                            self.motor.reproducir_sonido("Correcta.wav")
                        elif self.btn_pausa_music_mas.collidepoint(evento.pos):
                            self.motor.volumen_musica = min(1.0, self.motor.volumen_musica + 0.1)
                            self.sonido_nivel.set_volume(self.motor.volumen_musica)
                            self.motor.reproducir_sonido("Correcta.wav")
                        elif self.btn_pausa_sfx_menos.collidepoint(evento.pos):
                            self.motor.volumen_sfx = max(0.0, self.motor.volumen_sfx - 0.1)
                            self.motor.reproducir_sonido("Correcta.wav")
                        elif self.btn_pausa_sfx_mas.collidepoint(evento.pos):
                            self.motor.volumen_sfx = min(1.0, self.motor.volumen_sfx + 0.1)
                            self.motor.reproducir_sonido("Correcta.wav")
                        elif self.btn_pausa_abandon.collidepoint(evento.pos):
                            self.sonido_nivel.stop()
                            self.motor.reproducir_sonido("Correcta.wav")
                            self._registrar_log(completado=False)
                            from src.pantalla_niveles import PantallaNiveles
                            self.motor.cambiar_pantalla(PantallaNiveles(self.motor))
                    else:
                        # Si no está pausado, comprobar clic en botón Pausa
                        if self.rect_btn_pausa.collidepoint(evento.pos):
                            self.motor.reproducir_sonido("Correcta.wav")
                            self._pausar_juego()

    def _pausar_juego(self):
        self.pausado = True
        self.momento_pausa = pygame.time.get_ticks()

    def _reanudar_juego(self):
        self.pausado = False
        self.tiempo_pausado_acumulado += pygame.time.get_ticks() - self.momento_pausa

    def _crear_chispas_tallado(self, frase):
        x_plank = frase.x + 120
        y_plank = frase.y
        for _ in range(2):
            vx = random.uniform(-0.8, 0.8)
            vy = random.uniform(-1.5, -0.5)
            color = random.choice([(255, 130, 0), (255, 210, 40)])
            self.particulas.append(Particula(x_plank, y_plank, vx, vy, color, vida=20, gravedad=-0.01, tamaño=3))

    def _crear_astillas_destruccion(self, frase):
        x = 730
        y = frase.y
        for _ in range(25):
            vx = random.uniform(-4, -1)
            vy = random.uniform(-2, 2)
            color = random.choice([(141, 82, 36), (181, 122, 66), (225, 200, 160)])
            self.particulas.append(Particula(x, y, vx, vy, color, vida=45, gravedad=0.18, tamaño=5))

    def _crear_chispas_exito(self, frase):
        x = frase.x + 180
        y = frase.y
        for _ in range(30):
            vx = random.uniform(-3, 3)
            vy = random.uniform(-3, 3)
            color = random.choice([(100, 255, 100), (255, 220, 50), (255, 255, 255)])
            self.particulas.append(Particula(x, y, vx, vy, color, vida=35, gravedad=0.08, tamaño=4))

    def _registrar_log(self, completado=True):
        total_ticks = pygame.time.get_ticks() - self.motor.tiempo_inicio - self.tiempo_pausado_acumulado
        tiempo_total = max(1.0, total_ticks / 1000)
        minutos = tiempo_total / 60
        wpm = int(self.motor.puntuacion / minutos) if minutos > 0 else 0
        
        pulsaciones_totales = self.motor.pulsaciones_correctas + self.motor.pulsaciones_incorrectas
        precision = (self.motor.pulsaciones_correctas / pulsaciones_totales * 100) if pulsaciones_totales > 0 else 100.0
        
        log_entry = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "nivel": self.motor.tema_actual,
            "score": self.motor.puntuacion,
            "accuracy": precision,
            "time_taken": int(tiempo_total),
            "wpm": wpm,
            "status": "COMPLETED" if completado else "FAILED"
        }
        self.motor.historico_logs.append(log_entry)
        
        if completado and self.motor.tema_actual not in self.motor.niveles_completados:
            self.motor.niveles_completados.append(self.motor.tema_actual)
            
        self.motor.guardar_datos()

    def actualizar(self, dt):
        if self.pausado:
            return

        for p in self.particulas[:]:
            p.actualizar()
            if p.vida <= 0:
                self.particulas.remove(p)

        # Generar tablones
        cantidad_maxima_frases = min(3, (self.motor.puntuacion // 6) + 1)
        if len(self.motor.frases_en_pantalla) < cantidad_maxima_frases:
            nueva = self.generar_nueva_frase()
            if nueva:
                self.motor.frases_en_pantalla.append(nueva)

        self.motor.velocidad_palabra = (0.5 + (self.motor.puntuacion / 80)) * self.motor.velocidad_ajustada

        # Plank activo
        self.plank_activo = None
        if self.motor.texto_ingresado:
            candidatos = []
            for frase in self.motor.frases_en_pantalla:
                respuestas = frase.palabra_correcta
                if isinstance(respuestas, list):
                    coincide = any(r.lower().startswith(self.motor.texto_ingresado.lower()) for r in respuestas)
                else:
                    coincide = respuestas.lower().startswith(self.motor.texto_ingresado.lower())
                
                if coincide:
                    candidatos.append(frase)
            if candidatos:
                self.plank_activo = max(candidatos, key=lambda f: f.x)

        # Desplazamiento
        for frase in self.motor.frases_en_pantalla[:]:
            frase.x += self.motor.velocidad_palabra

            # Colisión con sierra
            if frase.x + 350 > self.x_sierras + 20:
                self.motor.frases_en_pantalla.remove(frase)
                self.motor.vidas -= 1
                
                self.shake_duracion = 15
                self._crear_astillas_destruccion(frase)
                
                self.motor.reproducir_sonido("equivocado.wav")

                if self.motor.vidas <= 0:
                    self.sonido_nivel.stop()
                    self._registrar_log(completado=False)
                    from src.pantalla_fin import PantallaFin
                    self.motor.cambiar_pantalla(PantallaFin(self.motor, victoria=False))
                    return

            # Coincidencia completa
            coincidio_completo = False
            respuestas = frase.palabra_correcta
            if isinstance(respuestas, list):
                for resp in respuestas:
                    if self.motor.texto_ingresado.strip().lower() == resp.lower():
                        coincidio_completo = True
                        break
            else:
                if self.motor.texto_ingresado.strip().lower() == respuestas.lower():
                    coincidio_completo = True
                    
            if coincidio_completo:
                self.motor.puntuacion += 1
                
                self._crear_chispas_exito(frase)
                self.motor.reproducir_sonido("Correcta.wav")
                
                self.motor.frases_en_pantalla.remove(frase)
                self.motor.texto_ingresado = ""
                
                if self.motor.puntuacion >= self.objetivo_shift:
                    self.sonido_nivel.stop()
                    self._registrar_log(completado=True)
                    from src.pantalla_fin import PantallaFin
                    self.motor.cambiar_pantalla(PantallaFin(self.motor, victoria=True))
                    return

        # Rotar música automáticamente cada 90 segundos
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultima_musica > self.tiempo_cambio_musica:
            self.tiempo_ultima_musica = ahora
            self.sonido_nivel.stop()
            self.indice_musica_actual = (self.indice_musica_actual + 1) % 4
            nombre_audio = f"Stage{self.indice_musica_actual + 1}.wav"
            self.sonido_nivel = self.motor.recursos.obtener_sonido(nombre_audio)
            self.sonido_nivel.set_volume(self.motor.volumen_musica)
            self.sonido_nivel.play(-1)
            self.motor.reproducir_sonido("Correcta.wav")

        # Detección de hovers en HUD y tablones de frases
        pos_mouse = pygame.mouse.get_pos()
        self.hover_progreso = self.rect_hud_progreso.collidepoint(pos_mouse)
        self.hover_tiempo = self.rect_hud_tiempo.collidepoint(pos_mouse)
        self.hover_pausa = self.rect_btn_pausa.collidepoint(pos_mouse)
        self.hover_vidas = self.rect_hud_vidas.collidepoint(pos_mouse)
        self.hover_input = self.rect_input_box.collidepoint(pos_mouse)

        self.plank_hovered = None
        for frase in self.motor.frases_en_pantalla:
            r_tablon = self.obtener_rect_tablon(frase)
            if r_tablon.collidepoint(pos_mouse):
                self.plank_hovered = frase
                break

    def dibujar(self, superficie):
        # Calcular sacudida
        offset_shake_x = 0
        offset_shake_y = 0
        if self.shake_duracion > 0 and not self.pausado:
            self.shake_duracion -= 1
            offset_shake_x = random.randint(-4, 4)
            offset_shake_y = random.randint(-4, 4)

        superficie_juego = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
        superficie_juego.blit(self.fondo, (0, 0))
        self._dibujar_decoraciones_fabrica(superficie_juego)

        # Cintas transportadoras estáticas
        for lane_y in LANES_Y:
            pygame.draw.rect(superficie_juego, (50, 50, 50), (0, lane_y + 16, ANCHO_PANTALLA, 14))
            pygame.draw.rect(superficie_juego, self.color_acero, (0, lane_y + 18, ANCHO_PANTALLA, 10))
            
            # Cogs estáticos
            for cx in self.cogs_x:
                pygame.draw.circle(superficie_juego, (75, 80, 85), (cx, lane_y + 23), 10)
                import math
                for i in range(4):
                    rad = math.radians(i * 90)
                    rx = int(cx + 8 * math.cos(rad))
                    ry = int(lane_y + 23 + 8 * math.sin(rad))
                    pygame.draw.line(superficie_juego, (30, 35, 40), (cx, lane_y + 23), (rx, ry), 2)
            
            # Sierras estáticas
            self._dibujar_sierra_giratoria(superficie_juego, self.x_sierras, lane_y + 23, 0)

        # Dibujar tablones
        for frase in self.motor.frases_en_pantalla:
            self._dibujar_tablon_frase(superficie_juego, frase)

        # Partículas
        for p in self.particulas:
            p.dibujar(superficie_juego)

        # --- HUD Superior ---
        # 1. Caja de Progreso (Con estrella dorada y checklist al inicio)
        pygame.draw.rect(superficie_juego, (20, 15, 10), (self.rect_hud_progreso.x, self.rect_hud_progreso.y, self.rect_hud_progreso.width, self.rect_hud_progreso.height), border_radius=4)
        pygame.draw.rect(superficie_juego, self.color_madera_borde, (self.rect_hud_progreso.x, self.rect_hud_progreso.y, self.rect_hud_progreso.width, self.rect_hud_progreso.height), 2, border_radius=4)
        
        # Checklist icon next to PROGRESS
        # Clipboard backing
        pygame.draw.rect(superficie_juego, (150, 100, 60), (self.rect_hud_progreso.x + 10, self.rect_hud_progreso.y + 11, 14, 18), border_radius=1)
        # Steel clip
        pygame.draw.rect(superficie_juego, (180, 180, 180), (self.rect_hud_progreso.x + 13, self.rect_hud_progreso.y + 8, 8, 4))
        # Paper sheet
        pygame.draw.rect(superficie_juego, (245, 240, 230), (self.rect_hud_progreso.x + 12, self.rect_hud_progreso.y + 13, 10, 14))
        # Lines on paper
        pygame.draw.line(superficie_juego, (100, 100, 100), (self.rect_hud_progreso.x + 14, self.rect_hud_progreso.y + 16), (self.rect_hud_progreso.x + 20, self.rect_hud_progreso.y + 16), 1)
        pygame.draw.line(superficie_juego, (100, 100, 100), (self.rect_hud_progreso.x + 14, self.rect_hud_progreso.y + 20), (self.rect_hud_progreso.x + 20, self.rect_hud_progreso.y + 20), 1)

        texto_pts = self.motor.fuente.render(f"PROGRESS: {self.motor.puntuacion}/{self.objetivo_shift}", True, (255, 220, 80))
        superficie_juego.blit(texto_pts, (self.rect_hud_progreso.x + 36, self.rect_hud_progreso.y + 6))

        # 2. Caja de Tiempo
        total_ticks = pygame.time.get_ticks() - self.motor.tiempo_inicio - self.tiempo_pausado_acumulado
        if self.pausado:
            total_ticks = self.momento_pausa - self.motor.tiempo_inicio - self.tiempo_pausado_acumulado
        tiempo_transcurrido = int(max(0, total_ticks) / 1000)
        
        pygame.draw.rect(superficie_juego, (20, 15, 10), (self.rect_hud_tiempo.x, self.rect_hud_tiempo.y, self.rect_hud_tiempo.width, self.rect_hud_tiempo.height), border_radius=4)
        
        # Reloj analógico procedimental
        cx_reloj = self.rect_hud_tiempo.x + 20
        cy_reloj = self.rect_hud_tiempo.y + 22
        pygame.draw.circle(superficie_juego, (245, 240, 230), (cx_reloj, cy_reloj), 9)
        pygame.draw.circle(superficie_juego, (110, 115, 120), (cx_reloj, cy_reloj), 9, 2)
        pygame.draw.line(superficie_juego, COLOR_NEGRO, (cx_reloj, cy_reloj), (cx_reloj, cy_reloj - 6), 2)
        pygame.draw.line(superficie_juego, COLOR_NEGRO, (cx_reloj, cy_reloj), (cx_reloj + 4, cy_reloj), 2)

        texto_tiempo = self.motor.fuente.render(f"TIME: {tiempo_transcurrido}s", True, (255, 255, 255))
        superficie_juego.blit(texto_tiempo, (self.rect_hud_tiempo.x + 36, self.rect_hud_tiempo.y + 6))

        # 3. Botón de Pausa
        color_btn_pausa = (60, 65, 70) if self.hover_pausa else (40, 45, 50)
        pygame.draw.rect(superficie_juego, color_btn_pausa, self.rect_btn_pausa, border_radius=4)
        pygame.draw.rect(superficie_juego, (180, 140, 70), self.rect_btn_pausa, 2, border_radius=4)
        texto_pausa = self.motor.fuente.render("||", True, (255, 255, 255))
        superficie_juego.blit(texto_pausa, (self.rect_btn_pausa.centerx - texto_pausa.get_width() // 2, self.rect_btn_pausa.centery - texto_pausa.get_height() // 2))

        # 4. Vidas (Estáticas en el HUD)
        pygame.draw.rect(superficie_juego, (20, 15, 10), (self.rect_hud_vidas.x, self.rect_hud_vidas.y, self.rect_hud_vidas.width, self.rect_hud_vidas.height), border_radius=4)
        for i in range(self.motor.vidas):
            x_vida = self.rect_hud_vidas.right - 40 - i * 40
            y_vida = self.rect_hud_vidas.y + 4
            superficie_juego.blit(self.sierra_vida, (x_vida, y_vida))

        # --- Caja de entrada metálica moderna ---
        pygame.draw.rect(superficie_juego, (20, 20, 22), (self.rect_input_box.x + 4, self.rect_input_box.y + 4, self.rect_input_box.width, self.rect_input_box.height), border_radius=6)
        pygame.draw.rect(superficie_juego, (45, 45, 50), self.rect_input_box, border_radius=6)
        pygame.draw.rect(superficie_juego, (180, 140, 70), self.rect_input_box, 3, border_radius=6)
        
        texto_usr_render = self.motor.fuente.render(self.motor.texto_ingresado, True, (255, 255, 255))
        pos_x_usr = self.rect_input_box.centerx - texto_usr_render.get_width() // 2
        pos_y_usr = self.rect_input_box.centery - texto_usr_render.get_height() // 2
        superficie_juego.blit(texto_usr_render, (pos_x_usr, pos_y_usr))

        # 5. Dibujar Menú de Pausa si está activo
        if self.pausado:
            self._dibujar_menu_pausa(superficie_juego)

        # Volcar superficie
        superficie.fill((0, 0, 0))
        superficie.blit(superficie_juego, (offset_shake_x, offset_shake_y))

        # Tooltips flotantes (sobre la superficie final)
        mx, my = pygame.mouse.get_pos()
        if not self.pausado:
            if self.plank_hovered:
                texto_en = self.plank_hovered.texto
                from src.traductor import TRADUCCIONES
                texto_es = TRADUCCIONES.get(texto_en, "Traducción no disponible.")
                
                # Mostrar traducción de la frase con la fuente de sistemas limpia
                tip_frase = BilingualTooltip(self.motor, f"Sentence: {texto_en}", f"Traducción: {texto_es}")
                tip_frase.dibujar(superficie, mx, my)
            elif self.hover_progreso:
                self.tooltip_progreso.dibujar(superficie, mx, my)
            elif self.hover_tiempo:
                self.tooltip_tiempo.dibujar(superficie, mx, my)
            elif self.hover_pausa:
                self.tooltip_pausa.dibujar(superficie, mx, my)
            elif self.hover_vidas:
                self.tooltip_vidas.dibujar(superficie, mx, my)
            elif self.hover_input:
                self.tooltip_input.dibujar(superficie, mx, my)

    def _dibujar_menu_pausa(self, superficie):
        """Dibuja el panel superpuesto de pausa con opciones y ajustes de sonido."""
        # Capa translúcida oscura sobre el juego
        overlay = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
        overlay.fill((10, 10, 15, 180))
        superficie.blit(overlay, (0, 0))

        # Panel de Pausa
        pygame.draw.rect(superficie, (15, 15, 18), (self.rect_pausa_panel.x + 5, self.rect_pausa_panel.y + 5, self.rect_pausa_panel.width, self.rect_pausa_panel.height), border_radius=8)
        pygame.draw.rect(superficie, self.color_acero, self.rect_pausa_panel, border_radius=8)
        pygame.draw.rect(superficie, (180, 140, 70), self.rect_pausa_panel, 3, border_radius=8)

        # Encabezado Pausa
        txt_pausa_title = self.motor.fuente.render("SHIFT PAUSED", True, (255, 210, 50))
        superficie.blit(txt_pausa_title, (self.rect_pausa_panel.centerx - txt_pausa_title.get_width() // 2, self.rect_pausa_panel.top + 15))
        pygame.draw.line(superficie, (180, 140, 70), (self.rect_pausa_panel.left + 20, self.rect_pausa_panel.top + 55), (self.rect_pausa_panel.right - 20, self.rect_pausa_panel.top + 55), 2)

        # Botones
        pos_mouse = pygame.mouse.get_pos()
        
        # 1. Resume
        is_hover_res = self.btn_pausa_resume.collidepoint(pos_mouse)
        offset_res = 2 if is_hover_res else 0
        rect_res_d = self.btn_pausa_resume.copy()
        rect_res_d.x += offset_res
        rect_res_d.y += offset_res
        superficie.blit(self.boton_img, rect_res_d)
        txt_res = self.motor.fuente.render("Resume Shift", True, COLOR_NEGRO)
        superficie.blit(txt_res, (rect_res_d.centerx - txt_res.get_width() // 2, rect_res_d.centery - txt_res.get_height() // 2))

        # 2. Restart
        is_hover_rest = self.btn_pausa_restart.collidepoint(pos_mouse)
        offset_rest = 2 if is_hover_rest else 0
        rect_rest_d = self.btn_pausa_restart.copy()
        rect_rest_d.x += offset_rest
        rect_rest_d.y += offset_rest
        superficie.blit(self.boton_img, rect_rest_d)
        txt_rest = self.motor.fuente.render("Restart Shift", True, COLOR_NEGRO)
        superficie.blit(txt_rest, (rect_rest_d.centerx - txt_rest.get_width() // 2, rect_rest_d.centery - txt_rest.get_height() // 2))

        # 3. Control Música
        txt_mus = self.motor.fuente.render("Music", True, (245, 245, 245))
        superficie.blit(txt_mus, (self.rect_pausa_panel.left + 35, 270))
        
        pygame.draw.rect(superficie, (40, 45, 50), self.btn_pausa_music_menos, border_radius=4)
        pygame.draw.rect(superficie, (200, 200, 200), self.btn_pausa_music_menos, 2, border_radius=4)
        txt_menos = self.motor.fuente.render("-", True, (255, 255, 255))
        superficie.blit(txt_menos, (self.btn_pausa_music_menos.centerx - txt_menos.get_width() // 2, self.btn_pausa_music_menos.centery - txt_menos.get_height() // 2))

        pygame.draw.rect(superficie, (20, 20, 20), (480, 265, 55, 36), border_radius=4)
        txt_val_m = self.motor.fuente.render(f"{int(self.motor.volumen_musica*100)}%", True, (255, 210, 80))
        superficie.blit(txt_val_m, (507 - txt_val_m.get_width() // 2, 283 - txt_val_m.get_height() // 2))

        pygame.draw.rect(superficie, (40, 45, 50), self.btn_pausa_music_mas, border_radius=4)
        pygame.draw.rect(superficie, (200, 200, 200), self.btn_pausa_music_mas, 2, border_radius=4)
        txt_mas = self.motor.fuente.render("+", True, (255, 255, 255))
        superficie.blit(txt_mas, (self.btn_pausa_music_mas.centerx - txt_mas.get_width() // 2, self.btn_pausa_music_mas.centery - txt_mas.get_height() // 2))

        # 4. Control SFX
        txt_sfx = self.motor.fuente.render("SFX Volume", True, (245, 245, 245))
        superficie.blit(txt_sfx, (self.rect_pausa_panel.left + 35, 325))
        
        pygame.draw.rect(superficie, (40, 45, 50), self.btn_pausa_sfx_menos, border_radius=4)
        pygame.draw.rect(superficie, (200, 200, 200), self.btn_pausa_sfx_menos, 2, border_radius=4)
        superficie.blit(txt_menos, (self.btn_pausa_sfx_menos.centerx - txt_menos.get_width() // 2, self.btn_pausa_sfx_menos.centery - txt_menos.get_height() // 2))

        pygame.draw.rect(superficie, (20, 20, 20), (480, 320, 55, 36), border_radius=4)
        txt_val_s = self.motor.fuente.render(f"{int(self.motor.volumen_sfx*100)}%", True, (255, 210, 80))
        superficie.blit(txt_val_s, (507 - txt_val_s.get_width() // 2, 338 - txt_val_s.get_height() // 2))

        pygame.draw.rect(superficie, (40, 45, 50), self.btn_pausa_sfx_mas, border_radius=4)
        pygame.draw.rect(superficie, (200, 200, 200), self.btn_pausa_sfx_mas, 2, border_radius=4)
        superficie.blit(txt_mas, (self.btn_pausa_sfx_mas.centerx - txt_mas.get_width() // 2, self.btn_pausa_sfx_mas.centery - txt_mas.get_height() // 2))

        # 5. Abandonar Shift
        is_hover_ab = self.btn_pausa_abandon.collidepoint(pos_mouse)
        offset_ab = 2 if is_hover_ab else 0
        rect_ab_d = self.btn_pausa_abandon.copy()
        rect_ab_d.x += offset_ab
        rect_ab_d.y += offset_ab
        superficie.blit(self.boton_img, rect_ab_d)
        txt_ab = self.motor.fuente.render("Abandon Shift", True, COLOR_NEGRO)
        superficie.blit(txt_ab, (rect_ab_d.centerx - txt_ab.get_width() // 2, rect_ab_d.centery - txt_ab.get_height() // 2))

    def _dibujar_sierra_giratoria(self, superficie, cx, cy, angulo):
        import math
        pygame.draw.circle(superficie, (100, 105, 110), (cx, cy), 32)
        pygame.draw.circle(superficie, (200, 205, 210), (cx, cy), 32, 3)
        pygame.draw.circle(superficie, (50, 50, 50), (cx, cy), 8)
        
        for i in range(12):
            rad_base = math.radians(angulo + i * 30)
            rad_punta = math.radians(angulo + i * 30 + 15)
            
            bx = cx + 32 * math.cos(rad_base)
            by = cy + 32 * math.sin(rad_base)
            
            px = cx + 42 * math.cos(rad_punta)
            py = cy + 42 * math.sin(rad_punta)
            
            rad_siguiente = math.radians(angulo + (i + 1) * 30)
            nx = cx + 32 * math.cos(rad_siguiente)
            ny = cy + 32 * math.sin(rad_siguiente)
            
            pygame.draw.polygon(superficie, (200, 205, 210), [(bx, by), (px, py), (nx, ny)])

    def _dibujar_tablon_frase(self, superficie, frase):
        is_active = (self.plank_activo == frase)

        texto = frase.texto
        underscores = ""
        if "______" in texto:
            underscores = "______"
        elif "___" in texto:
            underscores = "___"

        if underscores:
            partes = texto.split(underscores, 1)
            before = partes[0]
            after = partes[1]
        else:
            before = texto
            after = ""

        w_before, _ = self.motor.fuente.size(before)
        w_after, _ = self.motor.fuente.size(after)
        
        if is_active:
            typed = self.motor.texto_ingresado
            ans_str = frase.palabra_correcta[0] if isinstance(frase.palabra_correcta, list) else frase.palabra_correcta
            remaining_len = max(0, len(ans_str) - len(typed))
            blank_content = typed + ("_" * remaining_len)
        else:
            blank_content = underscores

        w_blank, h_text = self.motor.fuente.size(blank_content)
        
        total_text_width = w_before + w_blank + w_after
        plank_width = total_text_width + 40
        plank_height = 48
        
        plank_x = frase.x
        plank_y = frase.y - plank_height // 2

        # Sombra
        pygame.draw.rect(superficie, (10, 7, 5), (plank_x + 4, plank_y + 4, plank_width, plank_height), border_radius=4)
        
        # Abedul claro
        pygame.draw.rect(superficie, self.color_madera, (plank_x, plank_y, plank_width, plank_height), border_radius=4)
        
        # Vetado
        pygame.draw.line(superficie, self.color_madera_veta, (plank_x + 5, plank_y + 12), (plank_x + plank_width - 5, plank_y + 12), 2)
        pygame.draw.line(superficie, self.color_madera_veta, (plank_x + 5, plank_y + 36), (plank_x + plank_width - 5, plank_y + 36), 2)

        # Borde
        color_borde = self.color_madera_active_borde if is_active else self.color_madera_borde
        grosor_borde = 3 if is_active else 2
        pygame.draw.rect(superficie, color_borde, (plank_x, plank_y, plank_width, plank_height), grosor_borde, border_radius=4)

        # Clavos
        clavos_pos = [
            (plank_x + 6, plank_y + 6),
            (plank_x + plank_width - 6, plank_y + 6),
            (plank_x + 6, plank_y + plank_height - 6),
            (plank_x + plank_width - 6, plank_y + plank_height - 6)
        ]
        for px, py in clavos_pos:
            pygame.draw.circle(superficie, (90, 90, 90), (px, py), 3)

        # Textos
        curr_x = plank_x + 20
        curr_y = plank_y + (plank_height - h_text) // 2
        
        # Before
        r_before = self.motor.fuente.render(before, True, COLOR_NEGRO)
        superficie.blit(r_before, (curr_x, curr_y))
        curr_x += w_before
        
        # Blank
        if is_active:
            typed_part = blank_content[:len(self.motor.texto_ingresado)]
            guide_part = blank_content[len(self.motor.texto_ingresado):]
            
            # Letras en rojo de alto contraste
            r_typed = self.motor.fuente.render(typed_part, True, (220, 30, 0))
            superficie.blit(r_typed, (curr_x, curr_y))
            curr_x += self.motor.fuente.size(typed_part)[0]
            
            # Guías en gris
            r_guide = self.motor.fuente.render(guide_part, True, (110, 110, 110))
            superficie.blit(r_guide, (curr_x, curr_y))
            curr_x += self.motor.fuente.size(guide_part)[0]
        else:
            r_blank = self.motor.fuente.render(blank_content, True, (60, 60, 60))
            superficie.blit(r_blank, (curr_x, curr_y))
            curr_x += w_blank
            
        # After
        r_after = self.motor.fuente.render(after, True, COLOR_NEGRO)
        superficie.blit(r_after, (curr_x, curr_y))
