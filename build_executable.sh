#!/bin/bash
# Script para generar ejecutable de Sudoku Game

echo "🧩 Generador de Ejecutable - Sudoku Game"
echo "========================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "❌ Error: No se encontró main.py. Ejecuta este script desde la carpeta raíz del proyecto."
    exit 1
fi

echo "📋 Verificando dependencias..."

# Verificar Python
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python no está instalado"
    exit 1
fi

echo "✅ Python encontrado: $(python --version)"

# Instalar PyInstaller si no está instalado
if ! pip show pyinstaller &> /dev/null; then
    echo "📦 Instalando PyInstaller..."
    pip install pyinstaller
fi

echo "✅ PyInstaller disponible"

# Limpiar builds anteriores
echo "🧹 Limpiando builds anteriores..."
rm -rf build/ dist/ *.spec

# Crear ejecutable
echo "🔨 Generando ejecutable..."
echo "   Esto puede tomar unos minutos..."

pyinstaller \
    --onefile \
    --windowed \
    --name "Sudoku_Game" \
    --add-data "styles.css;." \
    main.py

# Verificar si se generó correctamente
if [ -f "dist/Sudoku_Game.exe" ]; then
    echo ""
    echo "✅ ¡Ejecutable generado exitosamente!"
    
    # Crear/actualizar carpeta release
    mkdir -p release
    cp "dist/Sudoku_Game.exe" "release/"
    
    # Calcular tamaño
    SIZE=$(du -h "release/Sudoku_Game.exe" | cut -f1)
    echo "📦 Ubicación: ./release/Sudoku_Game.exe"
    echo "📏 Tamaño: $SIZE"
    echo ""
    echo "🎯 El ejecutable está listo para distribuir!"
    echo "   Comparte la carpeta 'release/' o solo el archivo .exe"
    
else
    echo ""
    echo "❌ Error al generar el ejecutable"
    echo "   Revisa los mensajes de error anteriores"
    exit 1
fi

echo ""
echo "🚀 Proceso completado!"