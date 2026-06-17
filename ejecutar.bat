@echo off
title Lanzador de IndustrialQuest
echo ===================================================
echo             INICIANDO INDUSTRIALQUEST              
echo ===================================================
echo.

:: Comprobar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado o no se encuentra en el PATH del sistema.
    echo Por favor, descarga e instala Python desde: https://www.python.org/
    echo.
    pause
    exit /b 1
)

:: Intentar ejecutar el videojuego
python IndustrialQuest.py
if %errorlevel% neq 0 (
    echo.
    echo [AVISO] Hubo un problema al arrancar el juego.
    echo Intentando instalar o actualizar la dependencia Pygame-CE mediante pip...
    echo.
    python -m pip install pygame-ce
    if "%errorlevel%"=="0" (
        echo.
        echo [INFO] Pygame se ha instalado con exito. Iniciando el juego de nuevo...
        echo.
        python IndustrialQuest.py
    ) else (
        echo [ERROR] No se pudo instalar Pygame de forma automatica.
        echo Por favor, ejecuta en consola: pip install pygame
        echo.
        pause
    )
)





