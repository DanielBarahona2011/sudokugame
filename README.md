# Sudoku Game

Juego de Sudoku de escritorio en Python con interfaz Tkinter, base de datos SQLite y ranking de tiempos.

## Ejecutable (Windows)

Descarga y ejecuta sin instalar:

[release/Sudoku_Game.exe](release/Sudoku_Game.exe)

Si Windows muestra advertencia de seguridad, usa "Más información" y "Ejecutar de todas formas". Es normal en ejecutables hechos con PyInstaller.

## Desde código fuente

Requisitos: Python 3.10+

```bash
git clone https://github.com/DanielBarahona2011/sudokugame.git
cd sudokugame
pip install -r requirements.txt
python main.py
```

## Qué incluye

- Tres niveles de dificultad (fácil, medio, difícil)
- Cronómetro y puntuación
- Pistas y verificación de tablero
- Guardado de partidas en SQLite
- Ranking por nombre y tiempo

## Estructura

```
main.py              # Entrada
sudoku_gui.py        # Interfaz
sudoku_game.py       # Lógica del juego
sudoku_generator.py  # Generación de puzzles
database.py          # SQLite
style_manager.py     # Estilos
release/             # Ejecutable Windows
```

## Dependencias

- `ttkthemes` — temas para la interfaz
- `pyinstaller` — solo si quieres compilar el .exe

## Licencia

MIT. Ver [LICENSE](LICENSE).
