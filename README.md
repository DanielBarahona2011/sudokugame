# 🧩 Sudoku Game - Aplicación de Escritorio Completa

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://python.org)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![SQLite](https://img.shields.io/badge/Database-SQLite-orange.svg)](https://sqlite.org)
[![Release](https://img.shields.io/badge/Release-v1.0-brightgreen.svg)](https://github.com/usuario/sudoku-game/releases)

## 📖 Descripción

Aplicación completa de Sudoku desarrollada en Python con interfaz gráfica moderna, sistema de base de datos para persistencia, ranking competitivo y todas las funcionalidades esperadas en un juego profesional.

### ✨ Características Principales

- 🎯 **Juego Sudoku Completo** - Generación y validación matemáticamente correcta
- 🎨 **Interfaz Moderna** - Diseño responsivo con tema visual atractivo  
- 💾 **Base de Datos Integrada** - SQLite para guardar partidas, estadísticas y rankings
- 🏆 **Sistema de Ranking** - Competencia con nombres y mejores tiempos
- ⏱️ **Cronómetro y Puntuación** - Seguimiento preciso del rendimiento
- 🎮 **3 Niveles de Dificultad** - Fácil (30), Medio (40), Difícil (50 celdas vacías)
- 💡 **Sistema de Pistas** - Ayuda inteligente cuando la necesites
- ⏸️ **Pausar/Reanudar** - Botón dinámico que cambia según el estado

## 🚀 Descarga Rápida

### ⚡ Ejecutable para Windows
**[📥 Descargar Sudoku_Game.exe (19.4 MB)](./release/Sudoku_Game.exe)**

- ✅ **Sin instalación** - Ejecutar directamente
- ✅ **Portable** - Llevar en USB
- ✅ **Completo** - Incluye todas las dependencias

## 🛠️ Instalación desde Código Fuente

### Requisitos
- Python 3.14 o superior
- pip (gestor de paquetes)

### Pasos
```bash
# 1. Clonar o descargar código
git clone https://github.com/usuario/sudoku-game.git
cd sudoku-game

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar aplicación
python main.py
```

### Dependencias
```
ttkthemes==3.3.0
```

## 📁 Estructura del Proyecto

```
sudoku-game/
├── 📄 main.py                 # Punto de entrada principal
├── 📄 sudoku_gui.py           # Interfaz gráfica principal  
├── 📄 sudoku_game.py          # Lógica del juego
├── 📄 sudoku_generator.py     # Generador de puzzles
├── 📄 database.py             # Gestión de base de datos SQLite
├── 📄 style_manager.py        # Sistema de estilos CSS-like
├── 📄 styles.css              # Definiciones visuales
├── 📄 requirements.txt        # Dependencias del proyecto
├── 📁 release/                # Ejecutables compilados
│   ├── 📄 Sudoku_Game.exe     # Ejecutable para Windows
│   └── 📄 README_RELEASE.md   # Instrucciones de release
└── 📄 sudoku.db              # Base de datos (creada automáticamente)
```

## 🎮 Cómo Jugar

### Inicio Rápido
1. **Ejecuta** la aplicación
2. **Selecciona dificultad** (Fácil/Medio/Difícil)
3. **Haz clic** en celdas vacías del tablero 9x9
4. **Usa números** del panel lateral o teclado (1-9)
5. **Completa** el puzzle siguiendo reglas Sudoku

### Controles Avanzados
- **🎮 Nuevo Juego** - Iniciar nueva partida
- **⏸️ Pausar** - Pausar cronómetro (botón cambia a "▶️ Continuar")
- **💡 Pista** - Obtener ayuda inteligente
- **✓ Verificar** - Comprobar solución actual
- **💾 Guardar** - Guardar progreso en base de datos
- **📊 Rankings** - Ver mejores tiempos por dificultad

### Sistema de Ranking
Al completar un puzzle:
1. Se solicita **tu nombre**
2. Tu tiempo se **guarda en base de datos**
3. Se muestra **tu posición** en el ranking
4. **Celebración** con ventana de logro

## 🏗️ Arquitectura Técnica

### Patrón MVC
- **Model** (`sudoku_game.py`) - Lógica de negocio y reglas
- **View** (`sudoku_gui.py`) - Interfaz de usuario y eventos  
- **Controller** (`main.py`) - Coordinación y control de flujo

### Generación de Puzzles
```python
# Algoritmo garantizado matemáticamente correcto
1. Base válida conocida (matriz semilla)
2. Transformaciones: rotaciones, intercambios, permutaciones  
3. Eliminación inteligente de números según dificultad
4. Verificación de solución única
```

### Base de Datos (SQLite)
```sql
usuarios (id, nombre, fecha_registro, partidas_completadas, mejor_tiempo)
partidas (id, usuario_id, dificultad, tablero_estado, tiempo_jugado, fecha_guardado)  
estadisticas (id, usuario_id, dificultad, tiempo_total, fecha_completado)
```

## 🐛 Resolución de Problemas

### Windows Defender
Si Windows muestra advertencia de seguridad:
1. Clic en **"Más información"**
2. Seleccionar **"Ejecutar de todas formas"**
3. Es normal para ejecutables compilados con PyInstaller

### Problemas de Ejecución
```bash
# Si falla la instalación de dependencias
pip install --upgrade pip
pip install ttkthemes

# Si hay problemas con Tkinter
# En Ubuntu/Debian:
sudo apt-get install python3-tk

# En CentOS/RHEL:
sudo yum install tkinter
```

## 📊 Estadísticas de Desarrollo

- **🗃️ Líneas de código:** ~2,500
- **🧪 Funcionalidades:** 20+ características implementadas
- **🔧 Archivos Python:** 6 módulos principales
- **💾 Tamaño ejecutable:** 19.4 MB
- **⚡ Tiempo de startup:** <2 segundos
- **🎯 Cobertura funcional:** 100%

## 🎨 Capturas de Pantalla

### Pantalla Principal
- Tablero 9x9 con diseño moderno
- Panel lateral con números 1-9
- Cronómetro y puntuación en tiempo real

### Selección de Dificultad
- Interfaz limpia para elegir nivel
- Botones "Aceptar" y "Cancelar" claramente visibles

### Sistema de Ranking
- Lista de mejores tiempos por dificultad
- Solicitud de nombre al completar puzzle
- Posición en ranking mostrada al usuario

## 🤝 Desarrollo

### Tecnologías Utilizadas
- **Python 3.14** - Lenguaje principal
- **Tkinter/ThemedTk** - Interfaz gráfica
- **SQLite3** - Base de datos embebida
- **PyInstaller** - Compilación a ejecutable

### Características del Código
- **Arquitectura MVC** - Código organizado y mantenible
- **Comentarios extensivos** - Documentación inline
- **Manejo de errores** - Validación robusta
- **Estilo consistente** - Siguiendo PEP 8

## 📄 Licencia

Este proyecto es de uso educativo y académico.

## 👨‍💻 Autor

**Proyecto Académico - Sudoku Game**
- Desarrollado como aplicación de escritorio completa
- Implementa todas las funcionalidades de un juego profesional
- Base de datos integrada con sistema de ranking

---

⭐ **¡Disfruta jugando Sudoku!** 🧩

📦 **[Descargar Release v1.0](./release/)**