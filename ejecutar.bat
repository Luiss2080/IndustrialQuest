@echo off
setlocal EnableExtensions EnableDelayedExpansion

title Lanzador de IndustrialQuest
cd /d "%~dp0"

echo ===================================================
echo             INICIANDO INDUSTRIALQUEST
echo ===================================================
echo.

set "PYTHON_CMD="

where py >nul 2>&1
if not errorlevel 1 (
    py -3 --version >nul 2>&1
    if not errorlevel 1 set "PYTHON_CMD=py -3"
)

if not defined PYTHON_CMD (
    where python >nul 2>&1
    if not errorlevel 1 (
        python --version >nul 2>&1
        if not errorlevel 1 set "PYTHON_CMD=python"
    )
)

if not defined PYTHON_CMD (
    echo [AVISO] No se encontro Python en esta PC.
    where winget >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Tampoco se encontro winget para instalar Python automaticamente.
        echo Instala Python 3.8 o superior desde https://www.python.org/downloads/ y vuelve a ejecutar este archivo.
        echo.
        pause
        exit /b 1
    )

    echo [INFO] Intentando instalar Python 3.12 con winget...
    winget install --id Python.Python.3.12 -e --source winget --silent --accept-package-agreements --accept-source-agreements
    if errorlevel 1 (
        echo [ERROR] No se pudo instalar Python automaticamente.
        echo Instala Python manualmente y vuelve a ejecutar este archivo.
        echo.
        pause
        exit /b 1
    )

    where py >nul 2>&1
    if not errorlevel 1 (
        py -3 --version >nul 2>&1
        if not errorlevel 1 set "PYTHON_CMD=py -3"
    )

    if not defined PYTHON_CMD (
        where python >nul 2>&1
        if not errorlevel 1 (
            python --version >nul 2>&1
            if not errorlevel 1 set "PYTHON_CMD=python"
        )
    )

    if not defined PYTHON_CMD (
        echo [ERROR] Python se instalo, pero no quedo disponible en esta consola.
        echo Cierra y abre una nueva terminal, luego vuelve a ejecutar este archivo.
        echo.
        pause
        exit /b 1
    )
)

if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Creando entorno virtual...
    %PYTHON_CMD% -m venv ".venv"
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual.
        echo.
        pause
        exit /b 1
    )
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual.
    echo.
    pause
    exit /b 1
)

echo [INFO] Actualizando pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [ERROR] No se pudo actualizar pip.
    echo.
    pause
    exit /b 1
)

echo [INFO] Instalando dependencias...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] No se pudieron instalar las dependencias.
    echo.
    pause
    exit /b 1
)

echo [INFO] Iniciando el juego...
python IndustrialQuest.py
if errorlevel 1 (
    echo.
    echo [ERROR] El juego no pudo iniciarse correctamente.
    echo Revisa el mensaje anterior para identificar la causa.
    echo.
    pause
    exit /b 1
)

endlocal