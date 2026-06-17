# Guía de Inicio Rápido

Este documento guía a los nuevos desarrolladores a través del proceso de configuración inicial de su entorno local para ejecutar e iterar sobre el videojuego **IndustrialQuest**.

---

## Paso 1: Clonar o Descargar el Proyecto

Asegúrate de tener todos los archivos en tu máquina local dentro del directorio de trabajo deseado:

```bash
cd c:\laragon\www\IndustrialQuest
```

## Paso 2: Verificar la Instalación de Python

El proyecto requiere **Python 3.8 o superior**. Verifica tu versión instalada:

```bash
python --version
```

*Si no tienes Python instalado, descárgalo desde el [sitio web oficial](https://www.python.org/downloads/).*

## Paso 3: Configurar un Entorno Virtual (Recomendado)

Es una buena práctica de ingeniería de software aislar las dependencias del proyecto utilizando un entorno virtual de Python (`venv`):

### En Windows (PowerShell):
```powershell
# Crear el entorno virtual en la carpeta .venv
python -m venv .venv

# Activar el entorno virtual
.venv\Scripts\Activate.ps1
```

### En macOS / Linux:
```bash
# Crear el entorno virtual
python3 -m venv .venv

# Activar el entorno virtual
source .venv/bin/activate
```

## Paso 4: Instalar las Dependencias

Con el entorno virtual activo, instala la dependencia principal de Pygame:

```bash
pip install pygame
```

## Paso 5: Lanzar el Videojuego

Inicia la aplicación ejecutando el archivo lanzador en el directorio raíz:

```bash
python IndustrialQuest.py
```

Esto abrirá la ventana del juego con la animación de inicio. ¡Ya estás listo para jugar y comenzar a desarrollar nuevas funciones!
