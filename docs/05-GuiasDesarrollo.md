# Guía de Desarrollo y Mantenimiento

Este documento sirve como manual técnico para los desarrolladores que deseen configurar, probar o expandir el código de **IndustrialQuest**.

---

## 1. Configuración del Entorno de Desarrollo

### Prerrequisitos
- **Python 3.8 o superior** instalado en el sistema.
- El gestor de dependencias **pip**.

### Instalación
1. Ubícate en el directorio raíz del proyecto:
   ```bash
   cd c:\laragon\www\IndustrialQuest
   ```
2. Instala la dependencia Pygame de forma global o en tu entorno virtual:
   ```bash
   pip install pygame
   ```

---

## 2. Ejecución y Validación del Código

### Lanzamiento del juego
Para iniciar el videojuego, ejecuta el script lanzador principal desde la raíz:
```bash
python IndustrialQuest.py
```

### Comprobación de sintaxis y compilación
Antes de subir cambios al repositorio o enviarlos a producción, asegúrate de compilar los archivos Python para comprobar que no existan errores de tipeado o sintaxis:
```bash
python -m py_compile IndustrialQuest.py src/*.py
```
Si el comando no retorna salida alguna, significa que todos los archivos están listos para ejecutarse de forma segura.

---

## 3. Mantenimiento del Contenido (Preguntas y Temas)

Todo el contenido gramatical se encuentra en `src/datos_juego.py` dentro de un diccionario estructurado llamado `TEMAS`.

### A. Modificar o añadir preguntas a un tema existente:
1. Abre `src/datos_juego.py`.
2. Busca la categoría a modificar (ej: `"Simple Past"`).
3. Añade una nueva tupla en el formato `("Enunciado con _ (Pista)", "PalabraCorrecta")` dentro de la lista `"frases"`.
   ```python
   # Ejemplo:
   ("I _ a good movie last night (watch)", "watched")
   ```

### B. Crear un nuevo tema en el juego:
1. Añade los recursos de audio a la carpeta `recursos/sonidos/` y los fondos de imagen a `recursos/imagenes/`.
2. Define una nueva clave en el diccionario `TEMAS` en `src/datos_juego.py`:
   ```python
   "Passive Voice": {
       "audio_fondo": "Stage3.wav",           # Archivo en recursos/sonidos/
       "audio_clic": "Correcta.wav",
       "audio_exito": "ganador.wav",
       "audio_fracaso": "equivocado.wav",
       "imagen_fondo": "PresentPerfect.png",  # Archivo en recursos/imagenes/
       "imagen_corazon": "corazon.png",
       "frases": [
           ("The letter _ written yesterday (was)", "was"),
           ("Active sentences _ changed to passive (are)", "are")
       ]
   }
   ```
3. Guarda el archivo y ejecuta el juego. El menú de selección de niveles agregará automáticamente el nuevo botón interactivo con el nombre `"Passive Voice"`.
