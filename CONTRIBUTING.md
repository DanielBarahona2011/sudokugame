# Sudoku Game - Contributing Guide

¡Gracias por tu interés en contribuir al proyecto Sudoku Game!

## 🤝 Cómo Contribuir

### Reportar Bugs
1. Busca en [Issues](../../issues) si ya fue reportado
2. Si no existe, crea un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Sistema operativo y versión de Python
   - Screenshots si es visual

### Sugerir Nuevas Funcionalidades
1. Abre un issue con la etiqueta "enhancement"
2. Describe claramente la funcionalidad propuesta
3. Explica por qué sería útil para otros usuarios

### Desarrollo de Código

#### Setup del Entorno
```bash
# 1. Fork del repositorio
git clone https://github.com/TU_USUARIO/sudoku-game.git
cd sudoku-game

# 2. Crear rama de desarrollo
git checkout -b feature/nueva-funcionalidad

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar pre-commit hooks (opcional pero recomendado)
pip install pre-commit
pre-commit install
```

#### Estándares de Código
- Seguir **PEP 8** para estilo de Python
- Comentarios en **español** para este proyecto
- Docstrings para todas las funciones públicas
- Nombres de variables descriptivos

#### Estructura de Commits
```
tipo(scope): descripción breve

Descripción más detallada si es necesaria.

Fixes #123
```

Tipos permitidos:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug  
- `docs`: Cambios en documentación
- `style`: Cambios de formato (no afectan funcionamiento)
- `refactor`: Refactoring de código
- `test`: Agregar o modificar tests

#### Testing
Antes de enviar tu Pull Request:
```bash
# Ejecutar la aplicación y verificar funcionalidad básica
python main.py

# Verificar que no hay errores de sintaxis
python -m py_compile *.py
```

### Pull Request Process

1. **Actualizar tu fork**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Crear Pull Request**
   - Título descriptivo
   - Descripción detallada de los cambios
   - Referencias a issues relacionados
   - Screenshots si hay cambios visuales

3. **Review Process**
   - Al menos un reviewer debe aprobar
   - Todos los checks de CI deben pasar
   - No conflictos con la rama main

## 🎯 Áreas que Necesitan Ayuda

### Alta Prioridad
- [ ] **Testing automatizado** - Implementar tests unitarios
- [ ] **Documentación** - Mejorar comentarios y docs
- [ ] **Internacionalización** - Soporte multi-idioma
- [ ] **Optimización** - Mejorar rendimiento del generador

### Media Prioridad  
- [ ] **Nuevos temas visuales** - Más opciones de personalización
- [ ] **Sonidos** - Efectos de audio opcionales
- [ ] **Exportar puzzles** - Guardar como PDF/imagen
- [ ] **Tutorial** - Guía interactiva para nuevos usuarios

### Baja Prioridad
- [ ] **Modo multijugador** - Competencia online
- [ ] **App móvil** - Versión para smartphones
- [ ] **Estadísticas avanzadas** - Gráficos y análisis
- [ ] **Integración social** - Compartir logros

## 🏗️ Arquitectura del Proyecto

### Módulos Principales
```
main.py              # Entry point y coordinación
sudoku_gui.py        # Interfaz gráfica (Vista)
sudoku_game.py       # Lógica del juego (Modelo)  
sudoku_generator.py  # Algoritmos de generación
database.py          # Persistencia de datos
style_manager.py     # Sistema de estilos
```

### Flujo de Datos
```
Usuario → GUI → Game → Database
         ↑ ← Style Manager ← CSS
```

### Patrones Utilizados
- **MVC** - Separación de responsabilidades
- **Observer** - Para eventos del juego
- **Strategy** - Diferentes niveles de dificultad
- **Singleton** - Para la base de datos

## 📝 Guidelines Específicos

### Nuevas Funcionalidades
1. Discutir en issue antes de implementar
2. Mantener compatibilidad con versiones anteriores
3. Agregar documentación y ejemplos
4. Considerar impacto en rendimiento

### Bug Fixes
1. Reproducir el bug antes de arreglar
2. Crear test que demuestre el fix
3. Verificar que no rompe funcionalidad existente
4. Documentar la solución en el commit

### UI/UX Changes
1. Mantener consistencia con diseño actual
2. Verificar en diferentes resoluciones
3. Considerar accesibilidad
4. Incluir screenshots en PR

## 🎮 Testing Manual

### Funcionalidades Críticas a Probar
- [ ] Generar nuevo juego en cada dificultad
- [ ] Guardar y cargar partidas
- [ ] Sistema de ranking con nombres
- [ ] Validación de reglas Sudoku
- [ ] Pausar/reanudar funcionamiento
- [ ] Cierre y apertura de aplicación

### Casos Edge a Considerar
- Tablero lleno vs vacío
- Múltiples usuarios concurrentes
- Nombres muy largos en ranking
- Partidas guardadas corruptas
- Cierre inesperado durante guardado

## 📬 Comunicación

### Canales Disponibles
- **GitHub Issues** - Para bugs y features
- **Pull Requests** - Para reviews de código
- **Discussions** - Para preguntas generales

### Tiempo de Respuesta Esperado
- Issues: 48-72 horas
- Pull Requests: 3-7 días  
- Discussions: 24-48 horas

## 🏆 Reconocimientos

Los contribuidores serán reconocidos en:
- README principal del proyecto
- Release notes de cada versión
- Sección "About" de la aplicación

### Tipos de Contribución Reconocidas
- 🐛 Bug fixes
- ✨ New features  
- 📖 Documentation
- 🎨 Design
- 🔧 Tools/Infrastructure
- 🌐 Translation

---

¡Gracias por ayudar a mejorar Sudoku Game! 🧩✨