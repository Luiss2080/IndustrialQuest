# Arquitectura del Motor y Clases

Este documento detalla la arquitectura de software de **IndustrialQuest**, la cual implementa un diseño orientado a objetos basado en la modularidad y el desacoplamiento de responsabilidades.

---

## 1. El Ciclo de Juego (Game Loop) y la Máquina de Estados

El videojuego está gobernado por la clase `MotorJuego` (`src/motor.py`). Su método principal `ejecutar()` implementa el **Game Loop** clásico, limitando el frame rate a **60 FPS** e integrando un **Gestor de Pantallas (Screen Manager)** basado en el **Patrón de Estados**.

```text
[Bucle Principal en MotorJuego]
      │
      ├── 1. capturar eventos globales (ej. Cerrar ventana)
      ├── 2. delegar eventos locales a la pantalla activa -> pantalla_activa.manejar_eventos()
      ├── 3. actualizar lógica de la pantalla activa -> pantalla_activa.actualizar(dt)
      ├── 4. renderizar elementos de la pantalla activa -> pantalla_activa.dibujar(pantalla)
      │
      └── Limitar fotogramas (Tick a 60 FPS)
```

---

## 2. Diagrama y Responsabilidades de las Clases

### A. Motor del Juego (`src/motor.py`)
- **Clase:** `MotorJuego`
- **Función:** Inicializa los subsistemas de Pygame y el mezclador de sonido. Contiene el estado global de la partida (`puntuacion`, `vidas`, `texto_ingresado`, `frases_en_pantalla`, `tiempo_inicio`). Administra la transición de pantallas a través del método `cambiar_pantalla(nueva_pantalla)`.

### B. Plantilla de Escena (`src/pantalla.py`)
- **Clase:** `Pantalla`
- **Función:** Es la clase base abstracta de la que heredan todas las vistas del juego. Declara los métodos abstractos:
  - `manejar_eventos(self, eventos)`: Captura clics del ratón o entradas del teclado particulares de la pantalla.
  - `actualizar(self, dt)`: Ejecuta actualizaciones físicas, de temporizadores o de animaciones.
  - `dibujar(self, superficie)`: Blitea texturas y textos en la ventana.

### C. Administrador de Recursos (`src/administrador_recursos.py`)
- **Clase:** `AdministradorRecursos`
- **Función:** Carga bajo demanda y retiene en memoria (caché) las imágenes y efectos sonoros del directorio `recursos/`. Implementa mapeos para redirigir claves antiguas (ej: `.gif` o nombres incorrectos) a los archivos físicos correctos en `recursos/imagenes` o `recursos/sonidos`.

### D. Entidad Frase (`src/frase.py`)
- **Clase:** `FraseJuego`
- **Función:** Modela cada frase que se desliza por la pantalla de juego. Guarda su posición `(x, y)`, su color aleatorio y el texto de la pregunta. Para asegurar retrocompatibilidad con la lógica original, implementa accesibilidad híbrida (soporta accesos tradicionales por propiedad como `frase.x` y por claves tipo diccionario como `frase["x"]`).

### E. Los Estados de Pantalla (`src/pantalla_*.py`)
- **`PantallaMenu`**: Controla el menú inicial y desliza el logotipo de entrada de forma progresiva.
- **`PantallaReglas`**: Dibuja el panel informativo de las directrices de juego.
- **`PantallaNiveles`**: Lee dinámicamente las llaves de la base de datos de preguntas y dibuja los botones de selección.
- **`PantallaJuego`**: Ejecuta el bucle de juego activo, actualizando coordenadas de frases, verificando respuestas correctas, descontando vidas y reproduciendo audios.
- **`PantallaFin`**: Dibuja el mensaje de término de juego, detiene la música e introduce un delay de 6 segundos antes de regresar al selector de niveles.
