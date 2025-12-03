@echo off
REM Script para generar ejecutable de Sudoku Game en Windows

echo 🧩 Generador de Ejecutable - Sudoku Game
echo ========================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "main.py" (
    echo ❌ Error: No se encontro main.py. Ejecuta este script desde la carpeta raiz del proyecto.
    pause
    exit /b 1
)

echo 📋 Verificando dependencias...

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no esta instalado
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

REM Instalar PyInstaller si no está instalado
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando PyInstaller...
    pip install pyinstaller
)

echo ✅ PyInstaller disponible

REM Limpiar builds anteriores
echo 🧹 Limpiando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"

REM Crear ejecutable
echo 🔨 Generando ejecutable...
echo    Esto puede tomar unos minutos...

pyinstaller --onefile --windowed --name "Sudoku_Game" --add-data "styles.css;." main.py

REM Verificar si se generó correctamente
if exist "dist\Sudoku_Game.exe" (
    echo.
    echo ✅ ¡Ejecutable generado exitosamente!
    
    REM Crear/actualizar carpeta release
    if not exist "release" mkdir "release"
    copy "dist\Sudoku_Game.exe" "release\" >nul
    
    echo 📦 Ubicacion: .\release\Sudoku_Game.exe
    echo 📏 Tamaño: ~20 MB
    echo.
    echo 🎯 El ejecutable esta listo para distribuir!
    echo    Comparte la carpeta 'release/' o solo el archivo .exe
    
) else (
    echo.
    echo ❌ Error al generar el ejecutable
    echo    Revisa los mensajes de error anteriores
    pause
    exit /b 1
)

echo.
echo 🚀 Proceso completado!
pause