# Integración con Backend e Interacciones de Red

Este documento describe el estado actual de las comunicaciones de red del videojuego **IndustrialQuest** y proporciona guías de diseño en caso de que un desarrollador decida conectar el juego a un backend web en el futuro.

---

## 1. Estado Actual: Sin Interacciones de Red (Offline)

Actualmente, **IndustrialQuest** es una aplicación 100 % local (offline). 

- **Sin AJAX/Fetch:** Al ser un ejecutable de escritorio escrito en Python y Pygame, no utiliza tecnologías web tradicionales como llamadas AJAX o Fetch API.
- **Carga de Datos Local:** Las lecciones, oraciones y respuestas se cargan directamente desde la memoria desde el archivo `src/datos_juego.py`.
- **Activos Locales:** Los archivos de audio y las imágenes están almacenados en el disco local y el `AdministradorRecursos` los lee localmente.

---

## 2. Propuesta de Arquitectura para una Futura Conexión a un Backend (API REST)

Si en el futuro se desea centralizar el progreso de los alumnos, agregar tablas de clasificación competitiva (leaderboards) o cargar dinámicamente nuevas preguntas desde un panel escolar en la web, se recomienda seguir el siguiente esquema de integración:

### Componentes de Red Recomendados

1. **Cliente de Red (`src/cliente_api.py`):**
   - Implementar una clase que utilice la biblioteca estándar de Python `urllib` o la popular librería externa `requests`.
   - Métodos recomendados:
     - `obtener_frases_por_nivel(nivel_id)`: Para consultar preguntas en formato JSON desde un endpoint web.
     - `guardar_puntuacion(alumno_id, score, time)`: Envía una petición `POST` al servidor al finalizar una partida.

2. **Asincronía (Hilos o Threading):**
   - *Importante:* Las llamadas a red son bloqueantes. Si realizas una petición HTTP directa en el bucle principal de Pygame, la ventana se congelará hasta que el servidor responda.
   - Se deben ejecutar las peticiones en un hilo secundario utilizando el módulo estándar `threading` de Python o técnicas de programación asíncrona (`asyncio`).

---

## 3. Ejemplo Teórico de Obtención de Preguntas

A continuación se muestra un bosquejo de cómo se podría implementar la consulta de frases dinámicas desde una API REST en Python:

```python
import threading
import requests

def cargar_datos_asincronos(tema, callback):
    def tarea():
        try:
            # Consultar base de datos web
            respuesta = requests.get(f"https://api.industrialquest.com/v1/temas/{tema}")
            if respuesta.status_code == 200:
                datos = respuesta.json()
                # Invocar callback con las nuevas frases
                callback(datos["frases"])
        except Exception as e:
            print(f"Error consultando el backend: {e}")
            
    # Lanzar la petición en un hilo separado para evitar congelar el juego
    hilo = threading.Thread(target=tarea)
    hilo.start()
```
