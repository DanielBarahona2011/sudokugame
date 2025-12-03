"""
Interfaz gráfica principal del juego Sudoku
Implementa la ventana principal, grid de juego y controles usando Tkinter y ThemedTk
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ttkthemes import ThemedTk
import time
import threading
from sudoku_game import SudokuGame
from database import SudokuDatabase
from style_manager import StyleManager


class SudokuGUI:
    def __init__(self):
        """Inicializa la interfaz gráfica de Sudoku"""
        # Crear ventana principal con tema
        self.root = ThemedTk(theme="arc")
        self.root.title("🧩 Sudoku - Juego de Lógica")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        
        # Inicializar gestor de estilos
        self.style_manager = StyleManager(self.root)
        
        # Centrar ventana
        self.center_window()
        
        # Variables de estado
        self.selected_cell = None
        self.cell_entries = {}
        self.cell_frames = {}
        self.number_buttons = {}
        self.pause_button = None  # Referencia al botón de pausa
        
        # Inicializar juego y base de datos
        self.game = SudokuGame()
        self.database = SudokuDatabase()
        self.current_user = None
        
        # Variables para cronómetro
        self.time_var = tk.StringVar(value="00:00")
        self.timer_running = False
        self.timer_thread = None
        
        # Variables para estadísticas y funcionalidades adicionales
        self.score_var = tk.StringVar(value="Puntuación: 0")
        self.hints_var = tk.StringVar(value="Pistas: 0")
        self.mistakes_var = tk.StringVar(value="Errores: 0/3")
        self.difficulty_var = tk.StringVar(value="Dificultad: Medio")
        self.validation_enabled = tk.BooleanVar(value=True)
        self.auto_check = tk.BooleanVar(value=False)
        self.show_conflicts = tk.BooleanVar(value=True)
        
        # Sistema de puntuación mejorado
        self.score_multiplier = 1.0
        self.combo_count = 0
        self.perfect_moves = 0
        
        # Configurar callbacks del juego
        self.game.on_cell_change = self.on_cell_change
        self.game.on_game_complete = self.on_game_complete
        self.game.on_mistake = self.on_mistake
        
        # Crear interfaz con funcionalidades mejoradas
        self.create_menu()
        self.create_header()
        self.create_game_board()
        self.create_controls()
        self.create_advanced_features()
        self.create_status_bar()
        
        # Aplicar estilos mejorados
        self.apply_enhanced_styles()
        
        # Inicializar un juego por defecto
        self.initialize_default_game()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (650 // 2)
        self.root.geometry(f"900x650+{x}+{y}")
    
    def create_menu(self):
        """Crea la barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo Juego", command=self.new_game_dialog)
        file_menu.add_command(label="Cargar Partida", command=self.load_game_dialog)
        file_menu.add_command(label="Guardar Partida", command=self.save_game)
        file_menu.add_separator()
        file_menu.add_command(label="Cambiar Usuario", command=self.change_user_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.on_closing)
        
        # Menú Juego
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Juego", menu=game_menu)
        game_menu.add_command(label="Pausar/Reanudar", command=self.toggle_pause)
        game_menu.add_command(label="Obtener Pista", command=self.get_hint)
        game_menu.add_command(label="Verificar Solución", command=self.check_solution)
        game_menu.add_command(label="Mostrar Solución", command=self.show_solution)
        
        # Menú Estadísticas
        stats_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Estadísticas", menu=stats_menu)
        stats_menu.add_command(label="Estadísticas del Jugador", command=self.show_player_stats)
        stats_menu.add_command(label="Mejores Tiempos", command=self.show_best_times)
        stats_menu.add_command(label="Ranking", command=self.show_ranking)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Cómo Jugar", command=self.show_instructions)
        help_menu.add_command(label="Acerca de", command=self.show_about)
    
    def create_header(self):
        """Crea la sección del encabezado con información del juego"""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=10, padx=20, fill="x")
        
        # Frame izquierdo - información del juego
        left_frame = ttk.Frame(header_frame)
        left_frame.pack(side="left", fill="x", expand=True)
        
        info_frame1 = ttk.Frame(left_frame)
        info_frame1.pack(fill="x")
        
        ttk.Label(info_frame1, textvariable=self.difficulty_var, 
                 style="Header.TLabel").pack(side="left")
        ttk.Label(info_frame1, textvariable=self.score_var, 
                 style="Header.TLabel").pack(side="right")
        
        info_frame2 = ttk.Frame(left_frame)
        info_frame2.pack(fill="x", pady=(5, 0))
        
        ttk.Label(info_frame2, textvariable=self.hints_var, 
                 style="Info.TLabel").pack(side="left")
        ttk.Label(info_frame2, textvariable=self.mistakes_var, 
                 style="Info.TLabel").pack(side="right")
        
        # Frame derecho - cronómetro
        right_frame = ttk.Frame(header_frame)
        right_frame.pack(side="right")
        
        ttk.Label(right_frame, text="Tiempo:", 
                 style="Info.TLabel").pack()
        ttk.Label(right_frame, textvariable=self.time_var, 
                 style="Timer.TLabel").pack()
    
    def create_game_board(self):
        """Crea el tablero de juego 9x9"""
        # Frame principal horizontal
        main_game_frame = ttk.Frame(self.root)
        main_game_frame.pack(pady=15, padx=20, fill="both", expand=True)
        
        # Frame izquierdo para el tablero
        board_frame = ttk.Frame(main_game_frame)
        board_frame.pack(side="left", padx=(0, 20))
        
        # Frame principal del tablero
        main_board = ttk.Frame(board_frame, relief="solid", borderwidth=3)
        main_board.pack()
        
        # Crear grid 3x3 de subcuadrículas
        for block_row in range(3):
            for block_col in range(3):
                # Frame para cada subcuadrícula 3x3
                block_frame = ttk.Frame(main_board, relief="solid", borderwidth=2)
                block_frame.grid(row=block_row, column=block_col, padx=1, pady=1)
                
                # Crear celdas dentro de cada subcuadrícula
                for cell_row in range(3):
                    for cell_col in range(3):
                        # Calcular posición absoluta
                        abs_row = block_row * 3 + cell_row
                        abs_col = block_col * 3 + cell_col
                        
                        # Crear frame para la celda con tamaño fijo
                        cell_frame = tk.Frame(block_frame, 
                                            width=45, height=45,
                                            relief="solid", borderwidth=1,
                                            bg="white")
                        cell_frame.grid(row=cell_row, column=cell_col, padx=1, pady=1)
                        cell_frame.grid_propagate(False)  # Evitar que se redimensione
                        cell_frame.pack_propagate(False)  # Evitar que se redimensione
                        
                        # Crear entrada de texto con configuración estable
                        entry = tk.Entry(cell_frame, 
                                       width=2, 
                                       font=("Arial", 14, "bold"),
                                       justify="center",
                                       relief="flat",
                                       bd=0,
                                       highlightthickness=0,
                                       insertwidth=0)  # Ocultar cursor
                        entry.pack(fill="both", expand=True, padx=2, pady=2)
                        
                        # Configurar eventos
                        entry.bind("<FocusIn>", 
                                 lambda e, r=abs_row, c=abs_col: self.on_cell_focus(r, c))
                        entry.bind("<KeyPress>", 
                                 lambda e, r=abs_row, c=abs_col: self.on_key_press(e, r, c))
                        entry.bind("<Button-1>", 
                                 lambda e, r=abs_row, c=abs_col: self.on_cell_click(r, c))
                        
                        # Guardar referencias
                        self.cell_entries[(abs_row, abs_col)] = entry
                        self.cell_frames[(abs_row, abs_col)] = cell_frame
        
        # Frame derecho para botones numéricos
        numbers_frame = ttk.LabelFrame(main_game_frame, text="📱 Números", padding=15)
        numbers_frame.pack(side="left", fill="y", padx=(10, 0))
        
        # Grid de botones numéricos 3x3
        for i in range(1, 10):
            row = (i - 1) // 3
            col = (i - 1) % 3
            
            btn = tk.Button(numbers_frame, text=str(i), 
                           width=4, height=2,
                           font=("Arial", 14, "bold"),
                           bg="#3498db", fg="white",
                           activebackground="#2980b9",
                           relief="raised", borderwidth=2,
                           command=lambda n=i: self.insert_number(n))
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
            self.number_buttons[i] = btn
        
        # Botón para borrar
        clear_btn = tk.Button(numbers_frame, text="❌", 
                             width=4, height=2,
                             font=("Arial", 12, "bold"),
                             bg="#e74c3c", fg="white",
                             activebackground="#c0392b",
                             relief="raised", borderwidth=2,
                             command=lambda: self.insert_number(0))
        clear_btn.grid(row=3, column=1, padx=3, pady=3, sticky="nsew")
        
        # Configurar grid para que se expanda
        for i in range(3):
            numbers_frame.grid_columnconfigure(i, weight=1)
        for i in range(4):
            numbers_frame.grid_rowconfigure(i, weight=1)
    
    def create_controls(self):
        """Crea los controles del juego"""
        controls_frame = ttk.Frame(self.root)
        controls_frame.pack(pady=15, padx=20, fill="x")
        
        # Botones principales en una sola fila
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.pack()
        
        ttk.Button(buttons_frame, text="🎮 Nuevo Juego", 
                  command=self.new_game_dialog, 
                  style="Action.TButton").pack(side="left", padx=8)
        
        self.pause_button = ttk.Button(buttons_frame, text="⏸️ Pausar", 
                  command=self.toggle_pause, 
                  style="Action.TButton")
        self.pause_button.pack(side="left", padx=8)
        
        ttk.Button(buttons_frame, text="💡 Pista", 
                  command=self.get_hint, 
                  style="Hint.TButton").pack(side="left", padx=8)
        
        ttk.Button(buttons_frame, text="✓ Verificar", 
                  command=self.check_solution, 
                  style="Check.TButton").pack(side="left", padx=8)
        
        # Instrucciones de uso
        instructions_frame = ttk.Frame(controls_frame)
        instructions_frame.pack(pady=(15, 0))
        
        instructions_text = "💡 Cómo jugar: Haz clic en una celda y escribe un número del 1-9, o usa Backspace para borrar"
        ttk.Label(instructions_frame, text=instructions_text, 
                 style="Info.TLabel", font=("Segoe UI", 9)).pack()
    
    def create_advanced_features(self):
        """Crea las funcionalidades avanzadas"""
        features_frame = ttk.LabelFrame(self.root, text="⚙️ Opciones", 
                                       padding=10, style="Custom.TLabelframe")
        features_frame.pack(pady=10, padx=20, fill="x")
        
        # Frame para opciones en una sola línea
        options_frame = ttk.Frame(features_frame)
        options_frame.pack(fill="x")
        
        # Checkboxes de opciones más compactas
        ttk.Checkbutton(options_frame, text="✓ Validación en tiempo real", 
                       variable=self.validation_enabled,
                       style="Custom.TCheckbutton",
                       command=self.toggle_validation).pack(side="left", padx=15)
        
        ttk.Checkbutton(options_frame, text="🔍 Mostrar conflictos", 
                       variable=self.show_conflicts,
                       style="Custom.TCheckbutton",
                       command=self.update_board_display).pack(side="left", padx=15)
        
        # Botones de herramientas en el lado derecho
        tools_frame = ttk.Frame(options_frame)
        tools_frame.pack(side="right")
        
        ttk.Button(tools_frame, text="📊 Estadísticas", 
                  command=self.show_detailed_stats,
                  style="Info.TButton").pack(side="left", padx=5)
        
        ttk.Button(tools_frame, text="🔄 Resolver", 
                  command=self.auto_solve,
                  style="Danger.TButton").pack(side="left", padx=5)
    
    def toggle_validation(self):
        """Activa/desactiva la validación en tiempo real"""
        if self.validation_enabled.get():
            self.status_text.set("✓ Validación en tiempo real activada")
        else:
            self.status_text.set("❌ Validación en tiempo real desactivada")
        self.update_board_display()
    
    def toggle_notes_mode(self):
        """Activa/desactiva el modo de notas"""
        # Implementar modo de notas (para futuras versiones)
        messagebox.showinfo("Modo Notas", "🚧 Función de notas en desarrollo.\n"
                           "Próximamente podrás agregar notas en las celdas.")
    
    def undo_move(self):
        """Deshace el último movimiento"""
        # Implementar sistema de deshacer (para futuras versiones)
        messagebox.showinfo("Deshacer", "🚧 Función de deshacer en desarrollo.\n"
                           "Próximamente podrás deshacer movimientos.")
    
    def auto_solve(self):
        """Resuelve automáticamente el puzzle"""
        if not self.game or not self.game.current_puzzle:
            return
        
        response = messagebox.askyesno("Resolver Automáticamente", 
                                     "⚠️ ¿Estás seguro de que quieres resolver automáticamente?\n"
                                     "Esto terminará el juego actual y no obtendrás puntos.")
        if response:
            # Resolver paso a paso con animación
            self.solve_with_animation()
    
    def solve_with_animation(self):
        """Resuelve el puzzle con animación paso a paso"""
        empty_cells = [(i, j) for i in range(9) for j in range(9) 
                       if self.game.current_puzzle[i][j] == 0]
        
        if not empty_cells:
            return
        
        def solve_step(index=0):
            if index >= len(empty_cells):
                self.status_text.set("🎉 Puzzle resuelto automáticamente")
                self.game.end_game(False)
                return
            
            row, col = empty_cells[index]
            correct_number = self.game.solution[row][col]
            
            # Aplicar número con efecto visual
            self.game.current_puzzle[row][col] = correct_number
            entry = self.cell_entries[(row, col)]
            entry.delete(0, tk.END)
            entry.insert(0, str(correct_number))
            entry.configure(bg=self.style_manager.colors['success_bg'])
            
            # Continuar con el siguiente paso
            self.root.after(100, lambda: solve_step(index + 1))
        
        solve_step()
    
    def show_detailed_stats(self):
        """Muestra estadísticas detalladas de la partida actual"""
        if not self.game:
            messagebox.showwarning("Sin Partida", "No hay partida activa.")
            return
        
        stats = self.game.get_statistics()
        
        # Crear ventana de estadísticas
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Estadísticas Detalladas")
        stats_window.geometry("500x600")
        stats_window.resizable(False, False)
        stats_window.transient(self.root)
        stats_window.grab_set()
        
        # Centrar ventana
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 250
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 300
        stats_window.geometry(f"500x600+{x}+{y}")
        
        # Crear contenido
        main_frame = ttk.Frame(stats_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, text="📊 Estadísticas de la Partida Actual", 
                               font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Información básica
        basic_frame = ttk.LabelFrame(main_frame, text="📈 Información Básica", padding=15)
        basic_frame.pack(fill="x", pady=(0, 10))
        
        basic_stats = [
            ("🎯 Dificultad:", stats['difficulty']),
            ("📊 Progreso:", f"{stats['progress_percentage']:.1f}%"),
            ("🔢 Celdas llenas:", f"{stats['filled_cells']}/{stats['total_cells']}"),
            ("⏱️ Tiempo jugado:", f"{stats['elapsed_time']//60:02d}:{stats['elapsed_time']%60:02d}"),
            ("🏆 Puntuación:", str(stats['score'])),
            ("💡 Pistas usadas:", str(stats['hints_used'])),
            ("❌ Errores:", f"{stats['mistakes']}/3")
        ]
        
        for label, value in basic_stats:
            row_frame = ttk.Frame(basic_frame)
            row_frame.pack(fill="x", pady=2)
            ttk.Label(row_frame, text=label, font=("Segoe UI", 10, "bold")).pack(side="left")
            ttk.Label(row_frame, text=value, font=("Segoe UI", 10)).pack(side="right")
        
        # Información avanzada
        advanced_frame = ttk.LabelFrame(main_frame, text="🎯 Análisis Avanzado", padding=15)
        advanced_frame.pack(fill="x", pady=(10, 10))
        
        # Calcular estadísticas adicionales
        completion_rate = (stats['filled_cells'] - sum(1 for i in range(9) for j in range(9) 
                                                       if self.game.initial_puzzle[i][j] != 0)) / (81 - sum(1 for i in range(9) for j in range(9) if self.game.initial_puzzle[i][j] != 0)) * 100 if self.game else 0
        
        moves_per_minute = (stats['filled_cells'] / max(1, stats['elapsed_time'] / 60)) if stats['elapsed_time'] > 0 else 0
        accuracy = ((self.perfect_moves / max(1, self.perfect_moves + stats['mistakes'])) * 100) if hasattr(self, 'perfect_moves') else 95
        
        advanced_stats = [
            ("📈 Tasa de completado:", f"{completion_rate:.1f}%"),
            ("⚡ Movimientos por minuto:", f"{moves_per_minute:.1f}"),
            ("🎯 Precisión:", f"{accuracy:.1f}%"),
            ("🔥 Combo actual:", str(getattr(self, 'combo_count', 0))),
            ("⭐ Multiplicador:", f"x{getattr(self, 'score_multiplier', 1.0):.1f}")
        ]
        
        for label, value in advanced_stats:
            row_frame = ttk.Frame(advanced_frame)
            row_frame.pack(fill="x", pady=2)
            ttk.Label(row_frame, text=label, font=("Segoe UI", 10, "bold")).pack(side="left")
            ttk.Label(row_frame, text=value, font=("Segoe UI", 10)).pack(side="right")
        
        # Gráfico de progreso simple
        progress_frame = ttk.LabelFrame(main_frame, text="📊 Progreso Visual", padding=15)
        progress_frame.pack(fill="x", pady=(10, 0))
        
        # Barra de progreso
        progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate', 
                                      style="Custom.Horizontal.TProgressbar")
        progress_bar.pack(pady=10)
        progress_bar['value'] = stats['progress_percentage']
        
        # Etiqueta de progreso
        ttk.Label(progress_frame, text=f"Progreso: {stats['progress_percentage']:.1f}%",
                 font=("Segoe UI", 12, "bold")).pack()
        
        # Botón de cerrar
        ttk.Button(main_frame, text="Cerrar", command=stats_window.destroy,
                  style="Action.TButton").pack(pady=20)
    
    def create_status_bar(self):
        """Crea la barra de estado"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side="bottom", fill="x", padx=5, pady=5)
        
        self.status_text = tk.StringVar(value="Listo para jugar")
        ttk.Label(status_frame, textvariable=self.status_text, 
                 style="Status.TLabel").pack(side="left")
        
        # Progreso del juego
        self.progress_var = tk.StringVar(value="Progreso: 0%")
        ttk.Label(status_frame, textvariable=self.progress_var, 
                 style="Status.TLabel").pack(side="right")
    
    def apply_enhanced_styles(self):
        """Aplica estilos mejorados usando el StyleManager"""
        # Los estilos ya están aplicados por el StyleManager
        
        # Configurar estilos adicionales para checkbuttons
        self.style_manager.style.configure("Custom.TCheckbutton",
                                          background=self.style_manager.colors['background'],
                                          foreground=self.style_manager.colors['text'],
                                          font=('Segoe UI', 9),
                                          focuscolor="none")
        
        self.style_manager.style.map("Custom.TCheckbutton",
                                    background=[('active', self.style_manager.colors['hover'])])
        
        # Configurar colores para diferentes estados de celdas
        self.cell_styles = self.style_manager.create_cell_styles()
        self.frame_styles = self.style_manager.create_frame_styles()
    
    def update_board_display(self):
        """Actualiza la visualización del tablero con estilos mejorados"""
        # Si no hay juego, solo limpiar
        if not self.game or not hasattr(self.game, 'current_puzzle') or not self.game.current_puzzle:
            for row in range(9):
                for col in range(9):
                    if (row, col) in self.cell_entries:
                        entry = self.cell_entries[(row, col)]
                        frame = self.cell_frames[(row, col)]
                        entry.delete(0, tk.END)
                        entry.configure(state='normal')
                        self.apply_cell_style(entry, frame, 'normal')
            return
        
        # Actualizar cada celda con el nuevo puzzle
        for row in range(9):
            for col in range(9):
                entry = self.cell_entries[(row, col)]
                frame = self.cell_frames[(row, col)]
                value = self.game.current_puzzle[row][col]
                
                # Limpiar entrada primero
                entry.configure(state='normal')
                entry.delete(0, tk.END)
                
                # Insertar valor si no está vacío
                if value != 0:
                    entry.insert(0, str(value))
                
                # Aplicar estilos según el tipo de celda
                if (row, col) in self.game.locked_cells:
                    # Celdas iniciales (no modificables)
                    self.apply_cell_style(entry, frame, 'locked')
                    entry.configure(state='readonly')
                else:
                    # Celdas editables
                    self.apply_cell_style(entry, frame, 'normal')
                    entry.configure(state='normal')
                
                # Verificar conflictos si está habilitado
                if self.show_conflicts.get() and value != 0:
                    conflicts = self.game.get_cell_conflicts(row, col)
                    if conflicts:
                        self.apply_cell_style(entry, frame, 'error')
    
    def apply_cell_style(self, entry, frame, style_type):
        """
        Aplica un estilo específico a una celda sin causar redimensionamiento
        
        Args:
            entry: Widget Entry de la celda
            frame: Frame contenedor de la celda
            style_type (str): Tipo de estilo ('normal', 'locked', 'selected', etc.)
        """
        if style_type in self.cell_styles:
            cell_style = self.cell_styles[style_type]
            frame_style = self.frame_styles.get(f'cell_frame_{style_type}', 
                                               self.frame_styles['cell_frame'])
            
            # Aplicar estilos al entry sin redimensionar
            for key, value in cell_style.items():
                if hasattr(entry, 'configure'):
                    try:
                        if key == 'state' and style_type == 'locked':
                            entry.configure(state='readonly')
                        elif key not in ['state', 'width', 'height']:  # Evitar cambios de tamaño
                            entry.configure(**{key: value})
                    except tk.TclError:
                        pass  # Ignorar propiedades no válidas
            
            # Aplicar estilos al frame sin redimensionar
            for key, value in frame_style.items():
                if hasattr(frame, 'configure'):
                    try:
                        if key not in ['width', 'height']:  # Evitar cambios de tamaño
                            frame.configure(**{key: value})
                    except tk.TclError:
                        pass
    
    def update_game_info(self):
        """Actualiza la información del juego"""
        if self.game and hasattr(self.game, 'current_puzzle') and self.game.current_puzzle:
            stats = self.game.get_statistics()
            self.score_var.set(f"Puntuación: {self.game.score}")
            self.hints_var.set(f"Pistas: {self.game.hints_used}")
            self.mistakes_var.set(f"Errores: {self.game.mistakes}/{self.game.max_mistakes}")
            self.difficulty_var.set(f"Dificultad: {self.game.difficulty.capitalize()}")
            self.progress_var.set(f"Progreso: {stats['progress_percentage']:.1f}%")
        else:
            # Valores por defecto cuando no hay juego
            self.score_var.set("Puntuación: 0")
            self.hints_var.set("Pistas: 0")
            self.mistakes_var.set("Errores: 0/3")
            self.difficulty_var.set("Dificultad: ---")
            self.progress_var.set("Progreso: 0.0%")
    
    def start_timer(self):
        """Inicia el cronómetro"""
        self.timer_running = True
        self.timer_thread = threading.Thread(target=self.update_timer, daemon=True)
        self.timer_thread.start()
    
    def stop_timer(self):
        """Detiene el cronómetro"""
        self.timer_running = False
    
    def update_timer(self):
        """Actualiza el cronómetro cada segundo"""
        while self.timer_running:
            if self.game and not self.game.is_paused and not self.game.is_completed:
                elapsed = self.game.get_elapsed_time()
                minutes = elapsed // 60
                seconds = elapsed % 60
                time_str = f"{minutes:02d}:{seconds:02d}"
                self.time_var.set(time_str)
            time.sleep(1)
    
    def on_cell_focus(self, row, col):
        """Maneja el foco en una celda"""
        self.selected_cell = (row, col)
        self.highlight_related_cells(row, col)
    
    def on_cell_click(self, row, col):
        """Maneja el clic en una celda"""
        self.selected_cell = (row, col)
        self.highlight_related_cells(row, col)
    
    def highlight_related_cells(self, row, col):
        """Resalta las celdas relacionadas de forma más suave"""
        # Solo cambiar colores de fondo, no tamaños
        for r in range(9):
            for c in range(9):
                frame = self.cell_frames[(r, c)]
                entry = self.cell_entries[(r, c)]
                
                # Restaurar color base sin cambiar tamaño
                if (r, c) in self.game.locked_cells:
                    frame.configure(bg=self.style_manager.colors['border'])
                    entry.configure(readonlybackground=self.style_manager.colors['light'])
                else:
                    frame.configure(bg="white")
                    entry.configure(bg="white")
        
        # Resaltar celda seleccionada
        selected_frame = self.cell_frames[(row, col)]
        selected_frame.configure(bg=self.style_manager.colors['selected'])
        
        # Resaltar fila, columna y subcuadrícula con color más suave
        highlight_color = self.style_manager.colors['hover']
        
        for i in range(9):
            # Fila
            if i != col:
                self.cell_frames[(row, i)].configure(bg=highlight_color)
            # Columna
            if i != row:
                self.cell_frames[(i, col)].configure(bg=highlight_color)
        
        # Subcuadrícula 3x3
        start_row = row - row % 3
        start_col = col - col % 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if (r, c) != (row, col):
                    self.cell_frames[(r, c)].configure(bg=highlight_color)
    
    def on_key_press(self, event, row, col):
        """Maneja las teclas presionadas en una celda"""
        key = event.char
        entry = self.cell_entries[(row, col)]
        
        # Prevenir entrada si es celda bloqueada
        if (row, col) in self.game.locked_cells:
            return "break"
        
        # Solo permitir números del 1-9 y teclas especiales
        if key.isdigit() and key != "0":
            # Limpiar la celda primero y luego insertar el nuevo número
            entry.delete(0, tk.END)
            number = int(key)
            self.make_move(row, col, number)
            return "break"
        elif key in ['\b', '\x7f']:  # Backspace o Delete
            entry.delete(0, tk.END)
            self.make_move(row, col, 0)
            return "break"
        elif key == ' ':  # Espacio para borrar
            entry.delete(0, tk.END)
            self.make_move(row, col, 0)
            return "break"
        else:
            return "break"  # Bloquear otras teclas
    
    def insert_number(self, number):
        """Inserta un número en la celda seleccionada"""
        if self.selected_cell:
            row, col = self.selected_cell
            self.make_move(row, col, number)
    
    def make_move(self, row, col, number):
        """Realiza un movimiento en el juego"""
        if not self.game:
            return
        
        result = self.game.make_move(row, col, number)
        cell_entry = self.cell_entries[(row, col)]
        
        # Actualizar visualización
        self.update_board_display()
        self.update_game_info()
        
        # Aplicar efecto visual simple para errores
        if not result['success'] or not result['is_valid']:
            if number != 0:  # Solo para números, no para borrar
                # Marcar momentáneamente en rojo sin animación de movimiento
                self._flash_error_simple(cell_entry)
        
        # Mostrar resultado en la barra de estado
        if result['success'] and result['is_valid']:
            if number != 0:
                self.status_text.set("✅ Movimiento correcto")
                # Verificar áreas completadas
                completion_info = self.game.check_area_completion(row, col)
                if completion_info['row']:
                    self.status_text.set("🎊 ¡Fila completada!")
                    self.game.score += 50
                elif completion_info['column']:
                    self.status_text.set("🎊 ¡Columna completada!")
                    self.game.score += 50
                elif completion_info['box']:
                    self.status_text.set("🎊 ¡Cuadro completado!")
                    self.game.score += 50
            else:
                self.status_text.set("🗑️ Celda borrada")
        else:
            self.status_text.set(result.get('message', '❌ Número incorrecto'))
        
        # Verificar finalización del juego
        if result.get('completed'):
            self.on_game_complete_enhanced(True, self.game.score, self.game.get_elapsed_time())
        elif result.get('game_over'):
            self.stop_timer()
            messagebox.showerror("Juego Terminado", result['message'])
    
    def _flash_error_simple(self, widget):
        """Efecto visual simple para errores - solo cambio de color temporal"""
        try:
            original_bg = widget.cget('bg')
            original_fg = widget.cget('fg')
            
            # Cambiar a rojo temporalmente
            widget.configure(bg='#ffebee', fg='#d32f2f')
            
            # Restaurar colores originales después de 500ms
            widget.after(500, lambda: widget.configure(bg=original_bg, fg=original_fg))
        except:
            pass  # Ignorar errores
    
    def on_game_complete_enhanced(self, completed, score, time_elapsed):
        """Manejo mejorado de finalización de juego con celebración"""
        self.stop_timer()
        
        if completed:
            # Verificar si es un nuevo récord de tiempo
            is_new_record = False
            if self.current_user:
                is_new_record = self.database.actualizar_mejor_tiempo(
                    self.current_user['id'], time_elapsed
                )
            
            # Solicitar nombre para el ranking (especialmente si es récord)
            ranking_name = self.solicitar_nombre_ranking(is_new_record, time_elapsed)
            
            # Si se proporcionó un nombre, actualizar en la base de datos
            if ranking_name and ranking_name.strip():
                # Actualizar el nombre del usuario actual para el ranking
                self.current_user['nombre'] = ranking_name.strip()
                # Actualizar en la base de datos para persistir el cambio
                if self.current_user.get('id'):
                    self.database.actualizar_nombre_usuario_ranking(
                        self.current_user['id'], ranking_name.strip()
                    )
            
            # Crear ventana de celebración
            celebration_window = tk.Toplevel(self.root)
            celebration_window.title("🎉 ¡Felicitaciones!")
            celebration_window.geometry("500x450")
            celebration_window.resizable(False, False)
            celebration_window.transient(self.root)
            celebration_window.grab_set()
            celebration_window.configure(bg=self.style_manager.colors['success'])
            
            # Centrar ventana
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 250
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 225
            celebration_window.geometry(f"500x450+{x}+{y}")
            
            # Contenido de celebración
            main_frame = tk.Frame(celebration_window, bg=self.style_manager.colors['success'])
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Título de celebración con récord si aplica
            if is_new_record:
                title_text = "🏆 ¡NUEVO RÉCORD PERSONAL! 🏆"
                title_color = "#FFD700"  # Dorado
            else:
                title_text = "🎉 ¡SUDOKU COMPLETADO! 🎉"
                title_color = "white"
            
            tk.Label(main_frame, text=title_text,
                    font=("Segoe UI", 18, "bold"),
                    fg=title_color, bg=self.style_manager.colors['success']).pack(pady=15)
            
            # Mostrar el nombre del jugador
            if ranking_name and ranking_name.strip():
                tk.Label(main_frame, text=f"🎮 Jugador: {ranking_name}",
                        font=("Segoe UI", 14, "bold"),
                        fg="#FFE4B5", bg=self.style_manager.colors['success']).pack(pady=5)
            
            # Estadísticas finales
            stats_text = f"""🏆 Puntuación Final: {score:,}
⏱️ Tiempo: {time_elapsed//60:02d}:{time_elapsed%60:02d}
🎯 Dificultad: {self.game.difficulty.capitalize()}
💡 Pistas Usadas: {self.game.hints_used}
❌ Errores: {self.game.mistakes}
🔥 Combo Máximo: {self.combo_count}
⭐ Multiplicador Final: x{self.score_multiplier:.1f}"""
            
            if is_new_record:
                stats_text += f"\n\n🌟 ¡NUEVO MEJOR TIEMPO!\n⚡ Récord anterior superado"
            
            # Agregar información sobre posición en ranking
            posicion_ranking = self.obtener_posicion_en_ranking(time_elapsed, self.game.difficulty)
            if posicion_ranking:
                stats_text += f"\n\n📊 Posición en ranking: #{posicion_ranking}"
            
            # Crear ventana de celebración
            celebration_window = tk.Toplevel(self.root)
            celebration_window.title("🎉 ¡Felicitaciones!")
            celebration_window.geometry("450x400")
            celebration_window.resizable(False, False)
            celebration_window.transient(self.root)
            celebration_window.grab_set()
            celebration_window.configure(bg=self.style_manager.colors['success'])
            
            # Centrar ventana
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 225
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 200
            celebration_window.geometry(f"450x400+{x}+{y}")
            
            # Contenido de celebración
            main_frame = tk.Frame(celebration_window, bg=self.style_manager.colors['success'])
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Título de celebración con récord si aplica
            if is_new_record:
                title_text = "🏆 ¡NUEVO RÉCORD PERSONAL! 🏆"
                title_color = "#FFD700"  # Dorado
            else:
                title_text = "🎉 ¡SUDOKU COMPLETADO! 🎉"
                title_color = "white"
            
            tk.Label(main_frame, text=title_text,
                    font=("Segoe UI", 16, "bold"),
                    fg=title_color, bg=self.style_manager.colors['success']).pack(pady=15)
            
            # Estadísticas finales
            stats_text = f"""🏆 Puntuación Final: {score:,}
⏱️ Tiempo: {time_elapsed//60:02d}:{time_elapsed%60:02d}
🎯 Dificultad: {self.game.difficulty.capitalize()}
💡 Pistas Usadas: {self.game.hints_used}
❌ Errores: {self.game.mistakes}
🔥 Combo Máximo: {self.combo_count}
⭐ Multiplicador Final: x{self.score_multiplier:.1f}"""
            
            if is_new_record:
                stats_text += f"\n\n🌟 ¡NUEVO MEJOR TIEMPO!\n⚡ Récord anterior superado"
            
            tk.Label(main_frame, text=stats_text,
                    font=("Segoe UI", 11),
                    fg="white", bg=self.style_manager.colors['success'],
                    justify="left").pack(pady=10)
            
            # Botones de acción
            button_frame = tk.Frame(main_frame, bg=self.style_manager.colors['success'])
            button_frame.pack(pady=20)
            
            tk.Button(button_frame, text="🎮 Nuevo Juego",
                     command=lambda: [celebration_window.destroy(), self.new_game_dialog()],
                     font=("Segoe UI", 10, "bold"),
                     bg="white", fg=self.style_manager.colors['success'],
                     padx=15, pady=5).pack(side="left", padx=10)
            
            tk.Button(button_frame, text="📊 Ver Estadísticas",
                     command=lambda: [self.show_detailed_stats(), celebration_window.destroy()],
                     font=("Segoe UI", 10, "bold"),
                     bg="white", fg=self.style_manager.colors['success'],
                     padx=15, pady=5).pack(side="left", padx=10)
            
            # Efecto de celebración en todas las celdas
            self.celebrate_completion()
            
        else:
            # Juego no completado exitosamente
            messagebox.showinfo("Juego Terminado", 
                              "El juego ha terminado.\n"
                              f"Puntuación: {score}\n"
                              f"Tiempo: {time_elapsed//60:02d}:{time_elapsed%60:02d}")
    
    def solicitar_nombre_ranking(self, is_new_record, time_elapsed):
        """Solicita el nombre del jugador para el ranking"""
        # Crear diálogo personalizado
        dialog = tk.Toplevel(self.root)
        dialog.title("🏆 ¡Agregar al Ranking!")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="#2E7D32")  # Verde oscuro
        
        # Centrar diálogo
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 125
        dialog.geometry(f"400x250+{x}+{y}")
        
        result = {"name": None}
        
        # Contenido del diálogo
        main_frame = tk.Frame(dialog, bg="#2E7D32")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título según si es récord o no
        if is_new_record:
            title = "🌟 ¡NUEVO RÉCORD PERSONAL!"
            subtitle = "¡Serás agregado al ranking!"
        else:
            title = "🏆 ¡SUDOKU COMPLETADO!"
            subtitle = "Ingresa tu nombre para el ranking"
        
        tk.Label(main_frame, text=title,
                font=("Segoe UI", 14, "bold"),
                fg="#FFD700", bg="#2E7D32").pack(pady=10)
        
        tk.Label(main_frame, text=subtitle,
                font=("Segoe UI", 11),
                fg="white", bg="#2E7D32").pack(pady=5)
        
        # Mostrar tiempo
        tiempo_str = f"{time_elapsed//60:02d}:{time_elapsed%60:02d}"
        tk.Label(main_frame, text=f"⏱️ Tiempo: {tiempo_str}",
                font=("Segoe UI", 12, "bold"),
                fg="#FFE4B5", bg="#2E7D32").pack(pady=5)
        
        # Campo de entrada
        tk.Label(main_frame, text="🎮 Tu nombre:",
                font=("Segoe UI", 10),
                fg="white", bg="#2E7D32").pack(pady=(15, 5))
        
        name_entry = tk.Entry(main_frame, font=("Segoe UI", 12), width=20, justify="center")
        name_entry.pack(pady=5)
        name_entry.focus_set()
        
        # Sugerir nombre actual si existe
        if self.current_user and self.current_user.get('nombre'):
            name_entry.insert(0, self.current_user['nombre'])
        
        # Botones
        button_frame = tk.Frame(main_frame, bg="#2E7D32")
        button_frame.pack(pady=15)
        
        def confirmar():
            result["name"] = name_entry.get().strip()
            dialog.destroy()
        
        def omitir():
            result["name"] = self.current_user.get('nombre', 'Anónimo') if self.current_user else 'Anónimo'
            dialog.destroy()
        
        tk.Button(button_frame, text="🏆 Agregar al Ranking",
                 command=confirmar,
                 font=("Segoe UI", 10, "bold"),
                 bg="#4CAF50", fg="white", padx=15, pady=5).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="⏭️ Omitir",
                 command=omitir,
                 font=("Segoe UI", 10),
                 bg="#757575", fg="white", padx=15, pady=5).pack(side="left", padx=5)
        
        # Permitir Enter para confirmar
        dialog.bind('<Return>', lambda e: confirmar())
        dialog.bind('<Escape>', lambda e: omitir())
        
        dialog.wait_window()
        return result["name"]
    
    def obtener_posicion_en_ranking(self, tiempo_actual, dificultad):
        """Obtiene la posición que tendría este tiempo en el ranking"""
        try:
            mejores_tiempos = self.database.obtener_mejores_tiempos(dificultad.capitalize(), 100)
            
            # Contar cuántos tiempos son mejores que el actual
            mejores = sum(1 for _, tiempo, _, _, _ in mejores_tiempos if tiempo < tiempo_actual)
            return mejores + 1
            
        except Exception:
            return None
    
    def celebrate_completion(self):
        """Efecto visual de celebración cuando se completa el juego"""
        def animate_cells(count=0):
            if count < 20:  # Animar por 2 segundos
                for row in range(9):
                    for col in range(9):
                        if (row + col + count) % 3 == 0:
                            entry = self.cell_entries[(row, col)]
                            if count % 2 == 0:
                                entry.configure(bg=self.style_manager.colors['success_bg'])
                            else:
                                entry.configure(bg=self.style_manager.colors['white'])
                
                self.root.after(100, lambda: animate_cells(count + 1))
        
        animate_cells()
    
    def on_cell_change(self, row, col, number, is_valid):
        """Callback cuando cambia una celda"""
        pass  # La actualización se maneja en make_move
    
    def on_game_complete(self, completed, score, time):
        """Callback cuando termina el juego"""
        if completed:
            messagebox.showinfo("¡Felicitaciones!", 
                              f"¡Has completado el Sudoku!\n\n"
                              f"Puntuación: {score}\n"
                              f"Tiempo: {time//60:02d}:{time%60:02d}")
        else:
            messagebox.showinfo("Juego Terminado", 
                              "El juego ha terminado.")
    
    def on_mistake(self, mistakes, max_mistakes):
        """Callback cuando se comete un error"""
        self.status_text.set(f"Error #{mistakes} de {max_mistakes}")
    
    def new_game_dialog(self):
        """Diálogo para nuevo juego"""
        if not self.current_user:
            self.current_user = {'id': 1, 'nombre': 'Jugador'}
        
        # Diálogo de selección de dificultad
        difficulty = self.select_difficulty()
        if difficulty:
            self.start_new_game_with_difficulty(difficulty)
    
    def select_difficulty(self):
        """Diálogo de selección de dificultad"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Seleccionar Dificultad")
        dialog.geometry("350x250")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar diálogo
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 175
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 125
        dialog.geometry(f"350x250+{x}+{y}")
        
        selected = tk.StringVar(value="facil")
        
        ttk.Label(dialog, text="🧩 Selecciona el nivel de dificultad:", 
                 font=("Arial", 14, "bold")).pack(pady=20)
        
        difficulties = [
            ("🟢 Fácil (30 celdas vacías)", "facil"),
            ("🟡 Medio (40 celdas vacías)", "medio"),
            ("🔴 Difícil (50 celdas vacías)", "dificil")
        ]
        
        frame = ttk.Frame(dialog)
        frame.pack(pady=10)
        
        for text, value in difficulties:
            ttk.Radiobutton(frame, text=text, variable=selected, 
                           value=value, style="Custom.TRadiobutton").pack(pady=8, anchor="w")
        
        result = None
        
        def on_ok():
            nonlocal result
            result = selected.get()
            dialog.destroy()
        
        def on_cancel():
            nonlocal result
            result = None
            dialog.destroy()
        
        # Botones
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="✅ Aceptar", 
                  command=on_ok, 
                  style="Action.TButton",
                  width=15).pack(side="left", padx=15)
        ttk.Button(button_frame, text="❌ Cancelar", 
                  command=on_cancel, 
                  style="Custom.TButton",
                  width=15).pack(side="left", padx=15)
        
        # Hacer que Enter active OK
        dialog.bind('<Return>', lambda e: on_ok())
        dialog.bind('<Escape>', lambda e: on_cancel())
        
        dialog.wait_window()
        return result
    
    def change_user_dialog(self):
        """Diálogo para cambiar usuario"""
        name = simpledialog.askstring("Usuario", "Ingresa tu nombre:", 
                                     parent=self.root)
        if name:
            # Buscar usuario existente
            user = self.database.obtener_usuario_por_nombre(name)
            if not user:
                # Crear nuevo usuario
                user_id = self.database.insertar_usuario(name)
                if user_id:
                    user = self.database.obtener_usuario_por_nombre(name)
            
            if user:
                self.current_user = {
                    'id': user[0],
                    'nombre': user[1],
                    'fecha_registro': user[2],
                    'juegos_jugados': user[3],
                    'juegos_completados': user[4],
                    'mejor_tiempo': user[5],
                    'puntuacion_total': user[6]
                }
                self.status_text.set(f"Usuario: {name}")
                return True
        return False
    
    def toggle_pause(self):
        """Pausa o reanuda el juego"""
        if not self.game:
            return
        
        if self.game.is_paused:
            self.game.resume_game()
            self.status_text.set("Juego reanudado")
            if self.pause_button:
                self.pause_button.configure(text="⏸️ Pausar")
            if not self.timer_running:
                self.start_timer()
        else:
            self.game.pause_game()
            self.status_text.set("Juego pausado")
            if self.pause_button:
                self.pause_button.configure(text="▶️ Continuar")
    
    def get_hint(self):
        """Obtiene una pista"""
        if not self.game:
            return
        
        hint = self.game.get_hint()
        if hint:
            self.update_board_display()
            self.update_game_info()
            self.status_text.set(f"Pista aplicada en fila {hint['row']+1}, "
                               f"columna {hint['col']+1}")
        else:
            self.status_text.set("No hay más pistas disponibles")
    
    def check_solution(self):
        """Verifica si la solución actual es correcta"""
        if not self.game:
            return
        
        if self.game.generator.is_complete(self.game.current_puzzle):
            if self.game.generator.is_solved(self.game.current_puzzle):
                messagebox.showinfo("¡Correcto!", "¡La solución es correcta!")
            else:
                messagebox.showwarning("Incorrecto", "La solución tiene errores.")
        else:
            messagebox.showinfo("Incompleto", "El sudoku aún no está completo.")
    
    def show_solution(self):
        """Muestra la solución completa"""
        if not self.game:
            return
        
        response = messagebox.askyesno("Mostrar Solución", 
                                     "¿Estás seguro de que quieres ver la solución?\n"
                                     "Esto terminará el juego actual.")
        if response:
            self.game.current_puzzle = [row[:] for row in self.game.solution]
            self.game.end_game(False)
            self.update_board_display()
            self.stop_timer()
            self.status_text.set("Solución mostrada")
    
    def save_game(self):
        """Guarda la partida actual"""
        if not self.game or not hasattr(self.game, 'current_puzzle') or not self.game.current_puzzle:
            messagebox.showwarning("Sin Partida", "No hay partida activa para guardar.")
            return
        
        if self.game.is_completed:
            messagebox.showinfo("Partida Completada", "Esta partida ya está completada y no necesita guardarse.")
            return
        
        try:
            self.game.save_progress()
            
            # Mostrar confirmación detallada
            tiempo_actual = self.game.get_elapsed_time()
            tiempo_str = f"{tiempo_actual//60:02d}:{tiempo_actual%60:02d}"
            
            # Calcular progreso
            celdas_llenas = sum(1 for i in range(9) for j in range(9) if self.game.current_puzzle[i][j] != 0)
            progreso = (celdas_llenas / 81) * 100
            
            mensaje = f"""💾 Partida Guardada Exitosamente
            
🎯 Dificultad: {self.game.difficulty.capitalize()}
⏱️ Tiempo jugado: {tiempo_str}
📊 Progreso: {progreso:.1f}%
🏆 Puntuación: {self.game.score:,}
💡 Pistas usadas: {self.game.hints_used}

La partida se ha guardado y puedes continuarla más tarde desde el menú 'Cargar Partida'."""
            
            messagebox.showinfo("Partida Guardada", mensaje)
            self.status_text.set("💾 Partida guardada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar partida: {e}")
            self.status_text.set("❌ Error al guardar partida")
    
    def load_game_dialog(self):
        """Diálogo para cargar partida"""
        if not self.current_user:
            messagebox.showwarning("Sin Usuario", "Primero debes seleccionar un usuario.")
            return
        
        # Obtener partidas guardadas
        partidas_guardadas = self.database.obtener_partidas_guardadas(self.current_user['id'])
        
        if not partidas_guardadas:
            messagebox.showinfo("Sin Partidas", "No hay partidas guardadas para cargar.")
            return
        
        # Crear ventana de selección
        dialog = tk.Toplevel(self.root)
        dialog.title("💾 Cargar Partida")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar diálogo
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 250
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 200
        dialog.geometry(f"500x400+{x}+{y}")
        
        ttk.Label(dialog, text="💾 Selecciona una partida guardada:", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # Lista de partidas
        listbox_frame = ttk.Frame(dialog)
        listbox_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")
        
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, font=("Consolas", 10))
        listbox.pack(fill="both", expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Agregar partidas a la lista
        for i, partida in enumerate(partidas_guardadas):
            fecha = partida['fecha_inicio'].split()[0]  # Solo fecha
            tiempo = f"{partida['tiempo_jugado']//60:02d}:{partida['tiempo_jugado']%60:02d}"
            texto = f"{i+1:2d}. {partida['dificultad']:<8} | {fecha} | Tiempo: {tiempo}"
            listbox.insert(tk.END, texto)
        
        # Botones
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def cargar_partida():
            selection = listbox.curselection()
            if selection:
                partida = partidas_guardadas[selection[0]]
                self.cargar_partida(partida)
                dialog.destroy()
            else:
                messagebox.showwarning("Selección", "Selecciona una partida para cargar.")
        
        ttk.Button(button_frame, text="💾 Cargar", 
                  command=cargar_partida, style="Action.TButton").pack(side="left", padx=10)
        ttk.Button(button_frame, text="❌ Cancelar", 
                  command=dialog.destroy, style="Custom.TButton").pack(side="left", padx=10)
    
    def show_best_times(self):
        """Muestra los mejores tiempos registrados"""
        # Crear ventana de mejores tiempos
        dialog = tk.Toplevel(self.root)
        dialog.title("🏆 Mejores Tiempos")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar diálogo
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 300
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 250
        dialog.geometry(f"600x500+{x}+{y}")
        
        ttk.Label(dialog, text="🏆 MEJORES TIEMPOS REGISTRADOS", 
                 font=("Arial", 14, "bold")).pack(pady=15)
        
        # Notebook para diferentes dificultades
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        dificultades = ['facil', 'medio', 'dificil']
        iconos = ['🟢', '🟡', '🔴']
        nombres = ['Fácil', 'Medio', 'Difícil']
        
        for dif, icono, nombre in zip(dificultades, iconos, nombres):
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=f"{icono} {nombre}")
            
            # Obtener mejores tiempos para esta dificultad
            mejores = self.database.obtener_mejores_tiempos(dif.capitalize(), 15)
            
            if mejores:
                # Crear tabla de resultados
                tree = ttk.Treeview(frame, columns=('pos', 'jugador', 'tiempo', 'puntos', 'fecha'), show='headings')
                tree.heading('pos', text='Pos')
                tree.heading('jugador', text='Jugador')
                tree.heading('tiempo', text='Tiempo')
                tree.heading('puntos', text='Puntos')
                tree.heading('fecha', text='Fecha')
                
                tree.column('pos', width=50, anchor='center')
                tree.column('jugador', width=150, anchor='w')
                tree.column('tiempo', width=100, anchor='center')
                tree.column('puntos', width=100, anchor='center')
                tree.column('fecha', width=120, anchor='center')
                
                # Agregar datos
                for i, (nombre, tiempo, puntos, _, fecha) in enumerate(mejores, 1):
                    tiempo_str = f"{tiempo//60:02d}:{tiempo%60:02d}"
                    fecha_str = fecha.split()[0] if fecha else 'N/A'
                    
                    # Destacar los primeros 3 puestos
                    tags = ()
                    if i == 1:
                        tags = ('gold',)
                    elif i == 2:
                        tags = ('silver',)
                    elif i == 3:
                        tags = ('bronze',)
                    
                    tree.insert('', 'end', values=(f"{i}º", nombre, tiempo_str, puntos, fecha_str), tags=tags)
                
                # Configurar colores para los primeros puestos
                tree.tag_configure('gold', background='#FFD700', foreground='black')
                tree.tag_configure('silver', background='#C0C0C0', foreground='black')
                tree.tag_configure('bronze', background='#CD7F32', foreground='white')
                
                tree.pack(fill="both", expand=True, padx=10, pady=10)
                
                # Scrollbar para la tabla
                scrollbar_tree = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
                tree.configure(yscrollcommand=scrollbar_tree.set)
                scrollbar_tree.pack(side="right", fill="y")
            else:
                ttk.Label(frame, text=f"No hay tiempos registrados para {nombre}", 
                         font=("Arial", 12)).pack(expand=True)
        
        # Botón de cerrar
        ttk.Button(dialog, text="❌ Cerrar", 
                  command=dialog.destroy, style="Custom.TButton").pack(pady=20)
    
    def show_player_stats(self):
        """Muestra estadísticas del jugador"""
        try:
            # Configurar el juego con los datos de la partida
            self.game.difficulty = partida_data['dificultad'].lower()
            self.game.initial_puzzle = partida_data['tablero_inicial']
            self.game.current_puzzle = partida_data['tablero_actual']
            self.game.solution = partida_data['tablero_solucion']
            self.game.game_id = partida_data['id']
            
            # Identificar celdas bloqueadas
            self.game.locked_cells = set()
            for i in range(9):
                for j in range(9):
                    if self.game.initial_puzzle[i][j] != 0:
                        self.game.locked_cells.add((i, j))
            
            # Restaurar estado del tiempo (aproximado)
            self.game.start_time = time.time() - partida_data['tiempo_jugado']
            self.game.is_completed = False
            self.game.is_paused = False
            
            # Actualizar visualización
            self.update_board_display()
            self.update_game_info()
            self.start_timer()
            
            self.status_text.set(f"💾 Partida cargada - {partida_data['dificultad']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar partida: {e}")
    
    def show_best_times(self):
        """Muestra estadísticas del jugador"""
        if not self.current_user:
            messagebox.showwarning("Sin Usuario", "Primero debes seleccionar un usuario.")
            return
        
        stats = self.database.obtener_estadisticas_usuario(self.current_user['id'])
        
        stats_text = f"""Estadísticas de {self.current_user['nombre']}:
        
Partidas jugadas: {stats.get('total_partidas', 0)}
Partidas completadas: {stats.get('completadas', 0)}
Mejor tiempo: {stats.get('mejor_tiempo', 0)//60:02d}:{stats.get('mejor_tiempo', 0)%60:02d}
Tiempo promedio: {int(stats.get('tiempo_promedio', 0))//60:02d}:{int(stats.get('tiempo_promedio', 0))%60:02d}
Puntuación total: {stats.get('puntuacion_total', 0)}
"""
        
        messagebox.showinfo("Estadísticas del Jugador", stats_text)
    
    def show_ranking(self):
        """Muestra el ranking de jugadores"""
        ranking = self.database.obtener_ranking(10)
        
        if ranking:
            ranking_text = "🏆 TOP 10 JUGADORES 🏆\n\n"
            for i, (nombre, puntuacion, completados, mejor_tiempo) in enumerate(ranking, 1):
                tiempo_str = f"{mejor_tiempo//60:02d}:{mejor_tiempo%60:02d}" if mejor_tiempo else "N/A"
                ranking_text += f"{i:2d}. {nombre:<15} {puntuacion:>8} pts  {completados:>3} completados  {tiempo_str}\n"
        else:
            ranking_text = "No hay jugadores registrados aún."
        
        messagebox.showinfo("Ranking", ranking_text)
    
    def show_instructions(self):
        """Muestra las instrucciones del juego"""
        instructions = """📖 CÓMO JUGAR SUDOKU

🎯 OBJETIVO:
Llenar una cuadrícula de 9×9 con números del 1 al 9.

📋 REGLAS:
• Cada fila debe contener todos los números del 1 al 9
• Cada columna debe contener todos los números del 1 al 9  
• Cada subcuadrícula de 3×3 debe contener todos los números del 1 al 9
• No se pueden repetir números en la misma fila, columna o subcuadrícula

🎮 CONTROLES:
• Haz clic en una celda para seleccionarla
• Escribe un número del 1-9 o usa los botones numéricos
• Presiona Backspace o el botón ❌ para borrar
• Usa el botón "Pista" si necesitas ayuda

⏱️ PUNTUACIÓN:
• Movimientos correctos: +10 puntos
• Errores: -50 puntos
• Pistas: -25 puntos
• Bonus por tiempo al completar

¡Buena suerte!"""
        
        messagebox.showinfo("Instrucciones", instructions)
    
    def show_about(self):
        """Muestra información sobre la aplicación"""
        about_text = """🧩 SUDOKU - Juego de Lógica

Versión: 1.0
Desarrollado con Python y Tkinter

Características:
• Generador automático de puzzles
• 3 niveles de dificultad
• Sistema de puntuación
• Base de datos de partidas
• Cronómetro integrado
• Estadísticas de jugador

© 2024 - Desarrollado como proyecto académico"""
        
        messagebox.showinfo("Acerca de", about_text)
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if self.game and self.game.game_id and not self.game.is_completed:
            response = messagebox.askyesno("Guardar Partida", 
                                         "¿Quieres guardar la partida actual antes de salir?")
            if response:
                self.game.save_progress()
        
        self.stop_timer()
        if self.database:
            self.database.cerrar_conexion()
        self.root.destroy()
    
    def initialize_default_game(self):
        """Inicializa la interfaz sin generar un juego"""
        # Solo inicializar la interfaz sin juego
        self.update_game_info()
        self.status_text.set("Selecciona 'Nuevo Juego' para comenzar")
    
    def start_new_game_with_difficulty(self, difficulty):
        """Inicia un nuevo juego con la dificultad seleccionada"""
        # Primero limpiar completamente el tablero
        self._clear_board_completely()
        
        # Luego iniciar el nuevo juego
        self.game.difficulty = difficulty
        self.game.new_game(self.current_user['id'])
        
        # Restaurar botón de pausa al estado inicial
        if self.pause_button:
            self.pause_button.configure(text="⏸️ Pausar")
        
        # Actualizar la visualización
        self.update_board_display()
        self.update_game_info()
        self.start_timer()
        self.status_text.set(f"Nuevo juego iniciado - Dificultad: {difficulty.capitalize()}")
    
    def _clear_board_completely(self):
        """Limpia completamente el tablero antes de cargar un nuevo juego"""
        for row in range(9):
            for col in range(9):
                if (row, col) in self.cell_entries:
                    entry = self.cell_entries[(row, col)]
                    frame = self.cell_frames[(row, col)]
                    
                    # Limpiar contenido
                    entry.delete(0, tk.END)
                    
                    # Restaurar estado normal (no readonly)
                    entry.configure(state='normal')
                    
                    # Aplicar estilo normal
                    self.apply_cell_style(entry, frame, 'normal')
        
    def run(self):
        """Ejecuta la aplicación"""
        # Configurar evento de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Crear usuario automático
        self.current_user = {'id': 1, 'nombre': 'Jugador'}
        
        # Preguntar dificultad y empezar juego
        difficulty = self.select_difficulty()
        if difficulty:
            self.start_new_game_with_difficulty(difficulty)
        else:
            self.status_text.set("Selecciona 'Nuevo Juego' para comenzar")
        
        # Iniciar aplicación
        self.root.mainloop()


def main():
    """Función principal"""
    app = SudokuGUI()
    app.run()


if __name__ == "__main__":
    main()