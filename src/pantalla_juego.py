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
            # Achicar partícula según su vida restante
            tam = max(1, int(self.tamaño * (self.vida / self.vida_max)))
            pygame.draw.rect(superficie, self.color, (int(self.x), int(self.y), tam, tam))

class PantallaJuego(Pantalla):
    """
    Clase central del gameplay de IndustrialQuest: Woodwork Edition.
    Dibuja cintas transportadoras, sierras giratorias, partículas de colisión/tallado,
    e implementa el validador gramatical interactivo para 3 carriles.
    """
    def __init__(self, motor):
        super().__init__(motor)
        
        # Reiniciar estadísticas de juego para iniciar limpia la partida
        self.motor.reiniciar_estadisticas()
        
        # Obtener los datos y recursos específicos del capítulo seleccionado
        self.tema_info = TEMAS[self.motor.tema_actual]
        
        # Cargar imágenes base
        self.fondo = self.motor.recursos.obtener_imagen(self.tema_info["imagen_fondo"])
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
        
        # Reutilizar el signo inferior
        self.signo = self.motor.recursos.obtener_imagen("Signo.png")
        self.signo = pygame.transform.scale(self.signo, (350, 100))
        
        # Cargar sierra como reemplazo de corazón (vida)
        self.sierra_vida = self.motor.recursos.obtener_imagen("corazon.png")
        self.sierra_vida = pygame.transform.scale(self.sierra_vida, (50, 50))
        
        # Inicializar música de fondo del nivel en bucle
        self.sonido_nivel = self.motor.recursos.obtener_sonido(self.tema_info["audio_fondo"])
        self.sonido_nivel.set_volume(self.motor.volumen_musica)
        self.sonido_nivel.play(-1)
        
        # Captura de tiempo inicial
        self.motor.tiempo_inicio = pygame.time.get_ticks()

        # Configuración del juego
        self.objetivo_shift = 15 # 15 aciertos para completar el turno
        self.particulas = []
        self.plank_activo = None
        self.shake_duracion = 0
        
        # Paleta de colores rústica
        self.color_madera = (181, 122, 66)
        self.color_madera_veta = (141, 82, 36)
        self.color_madera_borde = (90, 55, 30)
        self.color_madera_active_borde = (255, 140, 0) # Brillo naranja
        self.color_acero = (90, 95, 100)
        
        # Posiciones de los remaches de las sierras al final de las cintas
        self.x_sierras = 730
        
        # Coordenadas de los cogs decorativos de las cintas
        self.cogs_x = [40, 200, 360, 520, 680]

    def generar_nueva_frase(self):
        """
        Genera una frase en un carril libre, evitando solapamientos y frases repetidas.
        """
        tema = self.motor.tema_actual
        if not tema:
            return None

        # Detectar qué carriles (lanes) están libres en la zona de inicio (X < 180)
        lanes_ocupados = {0: False, 1: False, 2: False}
        for frase in self.motor.frases_en_pantalla:
            if frase.x < 180:
                lanes_ocupados[frase.lane] = True
        
        lanes_libres = [lane for lane, ocupado in lanes_ocupados.items() if not ocupado]
        if not lanes_libres:
            return None # Esperar a que se despeje espacio
            
        lane_seleccionado = random.choice(lanes_libres)
        frases_disponibles = TEMAS[tema]["frases"]
        
        # Seleccionar frase del dataset sin repetir recientes
        nueva_frase_instancia = None
        intentos = 0
        while nueva_frase_instancia is None and intentos < 100:
            intentos += 1
            indice = random.randint(0, len(frases_disponibles) - 1)
            texto, palabra_correcta = frases_disponibles[indice]
            
            if texto not in self.motor.frases_recientes:
                nueva_frase_instancia = FraseJuego(texto, palabra_correcta, lane=lane_seleccionado)

        # Respaldo si todo está en el historial
        if nueva_frase_instancia is None:
            indice = random.randint(0, len(frases_disponibles) - 1)
            texto, palabra_correcta = frases_disponibles[indice]
            nueva_frase_instancia = FraseJuego(texto, palabra_correcta, lane=lane_seleccionado)

        self.motor.frases_recientes.append(nueva_frase_instancia.texto)
        if len(self.motor.frases_recientes) > 10:
            self.motor.frases_recientes.pop(0)

        return nueva_frase_instancia

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.sonido_nivel.stop()
                    self._registrar_log(completado=False)
                    from src.pantalla_fin import PantallaFin
                    self.motor.cambiar_pantalla(PantallaFin(self.motor, victoria=False))
                elif evento.key == pygame.K_BACKSPACE:
                    self.motor.texto_ingresado = self.motor.texto_ingresado[:-1]
                else:
                    char = evento.unicode
                    if len(char) > 0 and (char.isprintable() or char == " "):
                        # Intentar añadir carácter
                        nuevo_buffer = self.motor.texto_ingresado + char
                        
                        # Validar si este nuevo buffer coincide con algún prefijo
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
                            # Sonido de cincel/teclado de madera
                            self.motor.reproducir_sonido("Correcta.wav")
                            self.motor.pulsaciones_correctas += 1
                            
                            # Si hay tablón activo, soltar chispas de tallado
                            if self.plank_activo:
                                self._crear_chispas_tallado(self.plank_activo)
                        else:
                            # Typo
                            self.motor.pulsaciones_incorrectas += 1
                            # Efecto sonoro apagado
                            self.motor.reproducir_sonido("equivocado.wav")

    def _crear_chispas_tallado(self, frase):
        """Genera pequeñas chispas de fuego al tallar la madera en tiempo real."""
        x_plank = frase.x + 100  # Posición aproximada del blank
        y_plank = frase.y
        for _ in range(3):
            vx = random.uniform(-1, 1)
            vy = random.uniform(-2, -0.5)
            color = random.choice([(255, 120, 0), (255, 200, 30), (100, 100, 100)]) # Chispas y humo
            self.particulas.append(Particula(x_plank, y_plank, vx, vy, color, vida=30, gravedad=-0.02, tamaño=3))

    def _crear_astillas_destruccion(self, frase):
        """Genera astillas de madera voladoras cuando la sierra corta el tablón."""
        x = 730
        y = frase.y
        for _ in range(35):
            vx = random.uniform(-5, -1)
            vy = random.uniform(-3, 3)
            color = random.choice([(141, 82, 36), (181, 122, 66), (220, 180, 130)]) # Tonos madera
            self.particulas.append(Particula(x, y, vx, vy, color, vida=60, gravedad=0.2, tamaño=6))

    def _crear_chispas_exito(self, frase):
        """Genera chispas doradas/verdes brillantes cuando se completa con éxito el tablón."""
        x = frase.x + 200
        y = frase.y
        for _ in range(40):
            vx = random.uniform(-4, 4)
            vy = random.uniform(-4, 4)
            color = random.choice([(80, 255, 80), (255, 215, 0), (255, 255, 255)]) # Chispas de éxito
            self.particulas.append(Particula(x, y, vx, vy, color, vida=45, gravedad=0.1, tamaño=5))

    def _registrar_log(self, completado=True):
        """Registra la sesión actual en el historial de logs de producción."""
        tiempo_total = (pygame.time.get_ticks() - self.motor.tiempo_inicio) / 1000
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
        # 1. Gestionar partículas físicas
        for p in self.particulas[:]:
            p.actualizar()
            if p.vida <= 0:
                self.particulas.remove(p)

        # 2. Generar frases progresivamente hasta el límite del nivel
        cantidad_maxima_frases = min(3, (self.motor.puntuacion // 6) + 1)
        if len(self.motor.frases_en_pantalla) < cantidad_maxima_frases:
            # Intentar generar frase (solo si hay carril libre)
            nueva = self.generar_nueva_frase()
            if nueva:
                self.motor.frases_en_pantalla.append(nueva)

        # 3. Ajustar velocidad según la velocidad base y la configuración de maquinaria
        self.motor.velocidad_palabra = (0.5 + (self.motor.puntuacion / 80)) * self.motor.velocidad_ajustada

        # 4. Actualizar tablón activo
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
                # El candidato más a la derecha (mayor X) es el activo
                self.plank_activo = max(candidatos, key=lambda f: f.x)

        # 5. Desplazar tablones de madera
        for frase in self.motor.frases_en_pantalla[:]:
            frase.x += self.motor.velocidad_palabra

            # Colisión con la sierra giratoria al final de la cinta transportadora
            if frase.x + 350 > self.x_sierras + 20: # 350 es el ancho estimado
                self.motor.frases_en_pantalla.remove(frase)
                self.motor.vidas -= 1
                
                # Activar vibración de cámara y partículas de astillado
                self.shake_duracion = 18
                self._crear_astillas_destruccion(frase)
                
                # Sonido de madera astillándose
                self.motor.reproducir_sonido("equivocado.wav")

                # Derrota: vidas agotadas
                if self.motor.vidas <= 0:
                    self.sonido_nivel.stop()
                    self._registrar_log(completado=False)
                    from src.pantalla_fin import PantallaFin
                    self.motor.cambiar_pantalla(PantallaFin(self.motor, victoria=False))
                    return

            # Verificar si coincide de forma completa el input del jugador
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
                
                # Chispas doradas e impacto sonoro
                self._crear_chispas_exito(frase)
                self.motor.reproducir_sonido("Correcta.wav")
                
                # Eliminar frase completada
                self.motor.frases_en_pantalla.remove(frase)
                
                # Resetear entrada
                self.motor.texto_ingresado = ""
                
                # Victoria: alcanzar el objetivo del turno
                if self.motor.puntuacion >= self.objetivo_shift:
                    self.sonido_nivel.stop()
                    self._registrar_log(completado=True)
                    from src.pantalla_fin import PantallaFin
                    self.motor.cambiar_pantalla(PantallaFin(self.motor, victoria=True))
                    return

    def dibujar(self, superficie):
        # Aplicar sacudida de pantalla (camera shake) al perder vida
        offset_shake_x = 0
        offset_shake_y = 0
        if self.shake_duracion > 0:
            self.shake_duracion -= 1
            offset_shake_x = random.randint(-6, 6)
            offset_shake_y = random.randint(-6, 6)

        # Crear una superficie intermedia para aplicar el shake fácilmente
        superficie_juego = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))

        # 1. Dibujar el fondo del nivel
        superficie_juego.blit(self.fondo, (0, 0))

        # 2. Dibujar las Cintas Transportadoras (carriles)
        cog_angulo = (pygame.time.get_ticks() // 8) % 360
        sierra_angulo = (pygame.time.get_ticks() // 3) % 360
        
        for lane_y in LANES_Y:
            # Dibujar la base metálica de la cinta
            pygame.draw.rect(superficie_juego, (50, 50, 50), (0, lane_y + 16, ANCHO_PANTALLA, 14))
            pygame.draw.rect(superficie_juego, self.color_acero, (0, lane_y + 18, ANCHO_PANTALLA, 10))
            
            # Dibujar los cogs decorativos giratorios a lo largo de la cinta
            for cx in self.cogs_x:
                pygame.draw.circle(superficie_juego, (80, 85, 90), (cx, lane_y + 23), 10)
                # Radios del cog
                import math
                for i in range(4):
                    rad = math.radians(cog_angulo + i * 90)
                    rx = int(cx + 8 * math.cos(rad))
                    ry = int(lane_y + 23 + 8 * math.sin(rad))
                    pygame.draw.line(superficie_juego, (30, 35, 40), (cx, lane_y + 23), (rx, ry), 2)
            
            # Dibujar sierra giratoria peligrosa (Hoja de Sierra) al final de cada cinta
            self._dibujar_sierra_giratoria(superficie_juego, self.x_sierras, lane_y + 23, sierra_angulo)

        # 3. Dibujar los Tablones de Madera (frases)
        for frase in self.motor.frases_en_pantalla:
            self._dibujar_tablon_frase(superficie_juego, frase)

        # 4. Dibujar todas las partículas activas
        for p in self.particulas:
            p.dibujar(superficie_juego)

        # 5. Dibujar HUD Superior (Score y Vidas)
        # Score Box
        texto_pts = self.motor.fuente.render(f"SHIFT PROGRESS: {self.motor.puntuacion}/{self.objetivo_shift}", True, (255, 230, 100))
        rect_pts = texto_pts.get_rect(topleft=(25, 20))
        pygame.draw.rect(superficie_juego, (20, 15, 10), (rect_pts.x - 10, rect_pts.y - 6, rect_pts.width + 20, rect_pts.height + 12), border_radius=4)
        pygame.draw.rect(superficie_juego, self.color_madera_borde, (rect_pts.x - 10, rect_pts.y - 6, rect_pts.width + 20, rect_pts.height + 12), 2, border_radius=4)
        superficie_juego.blit(texto_pts, rect_pts)

        # Vidas (Sierras girando lentamente)
        for i in range(self.motor.vidas):
            x_vida = ANCHO_PANTALLA - 60 - i * 50
            y_vida = 15
            # Rotar sierra del HUD
            sierra_rotada = pygame.transform.rotate(self.sierra_vida, cog_angulo)
            rect_rot = sierra_rotada.get_rect(center=(x_vida + 25, y_vida + 25))
            superficie_juego.blit(sierra_rotada, rect_rot.topleft)

        # Dibujar tiempo transcurrido
        tiempo_transcurrido = int((pygame.time.get_ticks() - self.motor.tiempo_inicio) / 1000)
        texto_tiempo = self.motor.fuente.render(f"SHIFT TIME: {tiempo_transcurrido}s", True, (255, 255, 255))
        rect_t = texto_tiempo.get_rect(midtop=(ANCHO_PANTALLA // 2, 20))
        pygame.draw.rect(superficie_juego, (20, 15, 10), (rect_t.x - 10, rect_t.y - 6, rect_t.width + 20, rect_t.height + 12), border_radius=4)
        superficie_juego.blit(texto_tiempo, rect_t)

        # 6. Dibujar la Caja de Entrada de Texto en la parte inferior
        superficie_juego.blit(self.signo, (ANCHO_PANTALLA // 2 - 175, ALTO_PANTALLA - 110))
        
        # Texto ingresado dentro del letrero inferior
        texto_usr_render = self.motor.fuente.render(self.motor.texto_ingresado, True, (255, 220, 80))
        pos_x_usr = ANCHO_PANTALLA // 2 - texto_usr_render.get_width() // 2
        superficie_juego.blit(texto_usr_render, (pos_x_usr, ALTO_PANTALLA - 80))

        # Volcar superficie de juego en la superficie principal con el shake offset
        superficie.fill((0, 0, 0))
        superficie.blit(superficie_juego, (offset_shake_x, offset_shake_y))

    def _dibujar_sierra_giratoria(self, superficie, cx, cy, angulo):
        """Dibuja una hoja de sierra circular de acero con dientes que rotan."""
        import math
        # Cuerpo de la sierra
        pygame.draw.circle(superficie, (100, 105, 110), (cx, cy), 32)
        pygame.draw.circle(superficie, (200, 205, 210), (cx, cy), 32, 3)
        pygame.draw.circle(superficie, (50, 50, 50), (cx, cy), 8) # Eje central
        
        # Dibujar 12 dientes triangulares
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
        """Renderea una frase formateada dentro de un tablón de madera con clavos."""
        is_active = (self.plank_activo == frase)

        # Dividir texto en antes y después del blank
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

        # Calcular tamaños de texto
        w_before, _ = self.motor.fuente.size(before)
        w_after, _ = self.motor.fuente.size(after)
        
        # Determinar contenido del blank
        if is_active:
            typed = self.motor.texto_ingresado
            
            # Dibujar caracteres restantes como guiones bajos para guía visual
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

        # 1. Dibujar tablón de madera rústico
        # Sombra
        pygame.draw.rect(superficie, (15, 10, 5), (plank_x + 4, plank_y + 4, plank_width, plank_height), border_radius=4)
        
        # Madera cuerpo
        pygame.draw.rect(superficie, self.color_madera, (plank_x, plank_y, plank_width, plank_height), border_radius=4)
        
        # Vetar líneas horizontales decorativas en la madera
        pygame.draw.line(superficie, self.color_madera_veta, (plank_x + 5, plank_y + 12), (plank_x + plank_width - 5, plank_y + 12), 2)
        pygame.draw.line(superficie, self.color_madera_veta, (plank_x + 5, plank_y + 24), (plank_x + plank_width - 5, plank_y + 24), 1)
        pygame.draw.line(superficie, self.color_madera_veta, (plank_x + 5, plank_y + 36), (plank_x + plank_width - 5, plank_y + 36), 2)

        # Borde de madera tallado (Naranja brillante si está activo, marrón oscuro si no)
        color_borde = self.color_madera_active_borde if is_active else self.color_madera_borde
        grosor_borde = 3 if is_active else 2
        pygame.draw.rect(superficie, color_borde, (plank_x, plank_y, plank_width, plank_height), grosor_borde, border_radius=4)

        # Clavos en las esquinas del tablón
        clavos_pos = [
            (plank_x + 6, plank_y + 6),
            (plank_x + plank_width - 6, plank_y + 6),
            (plank_x + 6, plank_y + plank_height - 6),
            (plank_x + plank_width - 6, plank_y + plank_height - 6)
        ]
        for px, py in clavos_pos:
            pygame.draw.circle(superficie, (90, 90, 90), (px, py), 3)

        # 2. Dibujar partes del texto
        curr_x = plank_x + 20
        curr_y = plank_y + (plank_height - h_text) // 2
        
        # Renderizar parte 1: Before
        r_before = self.motor.fuente.render(before, True, COLOR_NEGRO)
        superficie.blit(r_before, (curr_x, curr_y))
        curr_x += w_before
        
        # Renderizar parte 2: Blank
        if is_active:
            # Las letras ya tecleadas se queman/tallan en color carbón quemado con resplandor naranja
            # Para simular quemado, podemos dibujarlo en rojo oscuro/glowing
            # Separar lo escrito del resto de la guía visual
            typed_part = blank_content[:len(self.motor.texto_ingresado)]
            guide_part = blank_content[len(self.motor.texto_ingresado):]
            
            # Dibujar texto quemado (carbón oscuro brillante)
            r_typed = self.motor.fuente.render(typed_part, True, (255, 69, 0)) # Glowing red-orange
            superficie.blit(r_typed, (curr_x, curr_y))
            curr_x += self.motor.fuente.size(typed_part)[0]
            
            # Dibujar guías restantes en gris
            r_guide = self.motor.fuente.render(guide_part, True, (130, 130, 130))
            superficie.blit(r_guide, (curr_x, curr_y))
            curr_x += self.motor.fuente.size(guide_part)[0]
        else:
            # Inactivo: Dibujar guías normales en gris oscuro
            r_blank = self.motor.fuente.render(blank_content, True, (70, 70, 70))
            superficie.blit(r_blank, (curr_x, curr_y))
            curr_x += w_blank
            
        # Renderizar parte 3: After
        r_after = self.motor.fuente.render(after, True, COLOR_NEGRO)
        superficie.blit(r_after, (curr_x, curr_y))
