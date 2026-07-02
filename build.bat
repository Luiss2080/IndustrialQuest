@echo off
REM Script de build para IndustrialQuest usando pygbag
REM Compatible con Windows, compilará el proyecto a WebAssembly

echo ================================
echo  IndustrialQuest Build Script
echo ================================
echo.

REM Verificar si estamos en el directorio correcto
if not exist "main.py" (
    echo Error: main.py no encontrado. Ejecuta este script desde la raíz del proyecto.
    exit /b 1
)

REM Activar venv si existe
if exist ".venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call .venv\Scripts\activate.bat
)

REM Verificar que pygbag está instalado
echo Verificando pygbag...
python -c "import pygbag" >nul 2>&1
if errorlevel 1 (
    echo Instalando pygbag...
    pip install pygbag
)

REM Limpiar build anterior
echo.
echo Limpiando build anterior...
if exist "build" (
    rmdir /s /q build
)

REM Compilar con pygbag
echo.
echo Compilando con pygbag (esto puede tardar varios minutos)...
echo.
python -m pygbag --build main.py

if errorlevel 1 (
    echo.
    echo ERROR: Falló la compilación con pygbag
    exit /b 1
)

REM Verificar que el build fue exitoso
if not exist "build\web" (
    echo.
    echo ERROR: El directorio build\web no fue creado
    exit /b 1
)

echo.
echo ================================
echo  ¡Build completado exitosamente!
echo ================================
echo.
echo El juego está en: build\web
echo.
echo Para probar localmente, ejecuta:
echo   python -m http.server 8000 --directory build\web
echo.
echo Luego abre en tu navegador:
echo   http://localhost:8000
echo.

exit /b 0
