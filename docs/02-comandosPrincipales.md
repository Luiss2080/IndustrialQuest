# Comandos Principales

Este documento lista y detalla los comandos de terminal útiles para la instalación, ejecución, validación y mantenimiento del videojuego **IndustrialQuest** en sistemas Windows y entornos compatibles.

## 1. Instalación de Dependencias

El juego solo requiere el paquete `pygame` para su ejecución. Instala la dependencia usando el instalador de paquetes de Python (`pip`):

```bash
pip install pygame
```

Si cuentas con múltiples versiones de Python, se recomienda usar:

```bash
python -m pip install pygame
```

## 2. Ejecución del Juego

Para iniciar el videojuego desde el directorio raíz del proyecto, ejecuta el script lanzador principal:

```bash
python IndustrialQuest.py
```

## 3. Verificación de Compilación y Sintaxis

Como desarrollador, puedes validar que todos los módulos de código Python compilen correctamente y no contengan errores de sintaxis mediante el compilador incorporado en Python:

### Para compilar todo el proyecto:
```bash
python -m py_compile IndustrialQuest.py src/*.py
```

### Para compilar un archivo en particular (ej: constantes):
```bash
python -m py_compile src/constantes.py
```

## 4. Limpieza de Caché y Archivos Temporales

Python genera automáticamente carpetas `__pycache__` al compilar los módulos para optimizar ejecuciones futuras. Si deseas limpiar el repositorio de archivos compilados `.pyc`, ejecuta el siguiente comando en PowerShell:

```powershell
Remove-Item -Path "**/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
```
