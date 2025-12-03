"""
Aplicador de estilos CSS para la aplicación Sudoku
Convierte estilos CSS a configuraciones de Tkinter/TTK
"""

import tkinter as tk
from tkinter import ttk
import json


class StyleManager:
    def __init__(self, root):
        """
        Inicializa el gestor de estilos
        
        Args:
            root: Ventana raíz de Tkinter
        """
        self.root = root
        self.style = ttk.Style()
        
        # Paleta de colores personalizada
        self.colors = {
            'primary': '#3498db',
            'primary_dark': '#2980b9',
            'secondary': '#95a5a6',
            'success': '#27ae60',
            'success_dark': '#229954',
            'warning': '#f39c12',
            'warning_dark': '#e67e22',
            'danger': '#e74c3c',
            'danger_dark': '#c0392b',
            'info': '#17a2b8',
            'info_dark': '#138496',
            'dark': '#2c3e50',
            'light': '#ecf0f1',
            'white': '#ffffff',
            'background': '#f8f9fa',
            'text': '#2c3e50',
            'text_light': '#6c757d',
            'border': '#dee2e6',
            'hover': '#e8f4fd',
            'selected': '#3498db',
            'error_bg': '#fdf2f2',
            'error_border': '#e74c3c',
            'success_bg': '#f0f9f0',
            'success_border': '#27ae60'
        }
        
        # Configurar tema base
        self.setup_theme()
    
    def setup_theme(self):
        """Configura el tema base de la aplicación"""
        # Configurar tema general
        available_themes = self.style.theme_names()
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        elif 'alt' in available_themes:
            self.style.theme_use('alt')
        
        # Configurar ventana principal
        self.root.configure(bg=self.colors['background'])
        
        # Aplicar estilos personalizados
        self.apply_custom_styles()
    
    def apply_custom_styles(self):
        """Aplica estilos personalizados a los widgets"""
        
        # === ESTILOS PARA FRAMES ===
        self.style.configure("Custom.TFrame",
                           background=self.colors['background'],
                           relief="flat")
        
        self.style.configure("Header.TFrame",
                           background=self.colors['primary'],
                           relief="flat",
                           borderwidth=0)
        
        self.style.configure("Board.TFrame",
                           background=self.colors['dark'],
                           relief="solid",
                           borderwidth=3)
        
        self.style.configure("Block.TFrame",
                           background=self.colors['dark'],
                           relief="solid",
                           borderwidth=2)
        
        # === ESTILOS PARA LABELS ===
        self.style.configure("Custom.TLabel",
                           background=self.colors['background'],
                           foreground=self.colors['text'],
                           font=('Segoe UI', 10))
        
        self.style.configure("Header.TLabel",
                           background=self.colors['primary'],
                           foreground=self.colors['white'],
                           font=('Segoe UI', 12, 'bold'))
        
        self.style.configure("Title.TLabel",
                           background=self.colors['background'],
                           foreground=self.colors['text'],
                           font=('Segoe UI', 16, 'bold'))
        
        self.style.configure("Info.TLabel",
                           background=self.colors['background'],
                           foreground=self.colors['text_light'],
                           font=('Segoe UI', 9))
        
        self.style.configure("Timer.TLabel",
                           background=self.colors['background'],
                           foreground=self.colors['danger'],
                           font=('Segoe UI', 16, 'bold'))
        
        self.style.configure("Score.TLabel",
                           background=self.colors['background'],
                           foreground=self.colors['success'],
                           font=('Segoe UI', 12, 'bold'))
        
        self.style.configure("Status.TLabel",
                           background=self.colors['dark'],
                           foreground=self.colors['light'],
                           font=('Segoe UI', 9),
                           padding=(10, 5))
        
        # === ESTILOS PARA BOTONES ===
        # Botón principal
        self.style.configure("Action.TButton",
                           background=self.colors['primary'],
                           foreground=self.colors['white'],
                           font=('Segoe UI', 10, 'bold'),
                           padding=(15, 8),
                           relief="flat",
                           borderwidth=0)
        
        self.style.map("Action.TButton",
                      background=[('active', self.colors['primary_dark']),
                                ('pressed', self.colors['primary_dark'])])
        
        # Botón de éxito
        self.style.configure("Success.TButton",
                           background=self.colors['success'],
                           foreground=self.colors['white'],
                           font=('Segoe UI', 10, 'bold'),
                           padding=(15, 8),
                           relief="flat")
        
        self.style.map("Success.TButton",
                      background=[('active', self.colors['success_dark'])])
        
        # Botón de advertencia
        self.style.configure("Warning.TButton",
                           background=self.colors['warning'],
                           foreground=self.colors['white'],
                           font=('Segoe UI', 10, 'bold'),
                           padding=(15, 8),
                           relief="flat")
        
        self.style.map("Warning.TButton",
                      background=[('active', self.colors['warning_dark'])])
        
        # Botón de peligro
        self.style.configure("Danger.TButton",
                           background=self.colors['danger'],
                           foreground=self.colors['white'],
                           font=('Segoe UI', 10, 'bold'),
                           padding=(15, 8),
                           relief="flat")
        
        self.style.map("Danger.TButton",
                      background=[('active', self.colors['danger_dark'])])
        
        # Botón personalizado (gris)
        self.style.configure("Custom.TButton",
                           background=self.colors['secondary'],
                           foreground=self.colors['white'],
                           font=('Segoe UI', 10, 'bold'),
                           padding=(15, 8),
                           relief="flat",
                           borderwidth=0)
        
        self.style.map("Custom.TButton",
                      background=[('active', self.colors['dark']),
                                ('pressed', self.colors['dark'])])
        
        # Botones numéricos
        self.style.configure("Number.TButton",
                           background=self.colors['info'],
                           foreground=self.colors['white'],
                           font=('Segoe UI', 14, 'bold'),
                           padding=(12, 12),
                           relief="flat")
        
        self.style.map("Number.TButton",
                      background=[('active', self.colors['info_dark'])])
        
        # Botón de borrar
        self.style.configure("Clear.TButton",
                           background=self.colors['danger'],
                           foreground=self.colors['white'],
                           font=('Segoe UI', 12, 'bold'),
                           padding=(12, 12),
                           relief="flat")
        
        # Botón de pista
        self.style.configure("Hint.TButton",
                           background=self.colors['warning'],
                           foreground=self.colors['white'],
                           font=('Segoe UI', 10, 'bold'),
                           padding=(15, 8),
                           relief="flat")
        
        # Botón de verificar
        self.style.configure("Check.TButton",
                           background=self.colors['info'],
                           foreground=self.colors['white'],
                           font=('Segoe UI', 10, 'bold'),
                           padding=(15, 8),
                           relief="flat")
        
        # === ESTILOS PARA LABELFRAMES ===
        self.style.configure("Custom.TLabelframe",
                           background=self.colors['background'],
                           foreground=self.colors['text'],
                           borderwidth=2,
                           relief="solid")
        
        self.style.configure("Custom.TLabelframe.Label",
                           background=self.colors['background'],
                           foreground=self.colors['text'],
                           font=('Segoe UI', 11, 'bold'))
        
        # === ESTILOS PARA ENTRADAS ===
        self.style.configure("Custom.TEntry",
                           relief="solid",
                           borderwidth=1,
                           insertcolor=self.colors['primary'],
                           fieldbackground=self.colors['white'])
        
        self.style.map("Custom.TEntry",
                      focuscolor=[('focus', self.colors['primary'])],
                      bordercolor=[('focus', self.colors['primary'])])
        
        # === ESTILOS PARA RADIOBUTTONS ===
        self.style.configure("Custom.TRadiobutton",
                           background=self.colors['background'],
                           foreground=self.colors['text'],
                           font=('Segoe UI', 10),
                           focuscolor="none")
        
        self.style.map("Custom.TRadiobutton",
                      background=[('active', self.colors['hover'])])
        
        # === ESTILOS PARA NOTEBOOK ===
        self.style.configure("Custom.TNotebook",
                           background=self.colors['background'],
                           borderwidth=0,
                           tabmargins=[2, 5, 2, 0])
        
        self.style.configure("Custom.TNotebook.Tab",
                           background=self.colors['secondary'],
                           foreground=self.colors['text'],
                           padding=[12, 8],
                           font=('Segoe UI', 10))
        
        self.style.map("Custom.TNotebook.Tab",
                      background=[('selected', self.colors['primary']),
                                ('active', self.colors['hover'])],
                      foreground=[('selected', self.colors['white'])])
        
        # === PROGRESSBAR ===
        self.style.configure("Custom.Horizontal.TProgressbar",
                           background=self.colors['success'],
                           troughcolor=self.colors['light'],
                           borderwidth=0,
                           lightcolor=self.colors['success'],
                           darkcolor=self.colors['success'])
    
    def create_cell_styles(self):
        """Crea estilos específicos para las celdas del Sudoku"""
        return {
            'normal': {
                'bg': self.colors['white'],
                'fg': self.colors['text'],
                'font': ('Segoe UI', 16, 'normal'),
                'relief': 'solid',
                'bd': 1,
                'borderwidth': 1,
                'highlightthickness': 0
            },
            'locked': {
                'bg': self.colors['light'],
                'fg': self.colors['dark'],
                'font': ('Segoe UI', 16, 'bold'),
                'relief': 'solid',
                'bd': 1,
                'state': 'readonly'
            },
            'selected': {
                'bg': self.colors['selected'],
                'fg': self.colors['white'],
                'highlightbackground': self.colors['primary_dark'],
                'highlightthickness': 2
            },
            'highlighted': {
                'bg': self.colors['hover'],
                'fg': self.colors['text']
            },
            'error': {
                'bg': self.colors['error_bg'],
                'fg': self.colors['danger'],
                'highlightbackground': self.colors['error_border'],
                'highlightthickness': 2
            },
            'correct': {
                'bg': self.colors['success_bg'],
                'fg': self.colors['success'],
                'highlightbackground': self.colors['success_border']
            }
        }
    
    def create_frame_styles(self):
        """Crea estilos para los frames del tablero"""
        return {
            'cell_frame': {
                'bg': self.colors['white'],
                'relief': 'solid',
                'bd': 1,
                'highlightthickness': 0
            },
            'cell_frame_locked': {
                'bg': self.colors['border'],
                'relief': 'solid',
                'bd': 1
            },
            'cell_frame_selected': {
                'bg': self.colors['selected'],
                'relief': 'solid',
                'bd': 2
            },
            'cell_frame_highlighted': {
                'bg': self.colors['hover'],
                'relief': 'solid',
                'bd': 1
            },
            'cell_frame_error': {
                'bg': self.colors['error_border'],
                'relief': 'solid',
                'bd': 2
            }
        }
    
    def apply_animation_effect(self, widget, effect_type='pulse'):
        """
        Aplica efectos de animación a un widget
        
        Args:
            widget: Widget a animar
            effect_type (str): Tipo de efecto ('pulse', 'shake', 'glow')
        """
        if effect_type == 'pulse':
            self._pulse_effect(widget)
        elif effect_type == 'shake':
            self._shake_effect(widget)
        elif effect_type == 'glow':
            self._glow_effect(widget)
    
    def _pulse_effect(self, widget, count=0):
        """Efecto de pulso para un widget"""
        if count < 6:
            current_bg = widget.cget('background') if hasattr(widget, 'cget') else None
            if current_bg:
                if count % 2 == 0:
                    widget.configure(background=self.colors['primary'])
                else:
                    widget.configure(background=self.colors['light'])
                widget.after(200, lambda: self._pulse_effect(widget, count + 1))
    
    def _shake_effect(self, widget, count=0):
        """Efecto de vibración para un widget"""
        if count < 10:
            if count % 2 == 0:
                widget.place(x=widget.winfo_x() + 3, y=widget.winfo_y())
            else:
                widget.place(x=widget.winfo_x() - 3, y=widget.winfo_y())
            widget.after(50, lambda: self._shake_effect(widget, count + 1))
    
    def _glow_effect(self, widget):
        """Efecto de brillo para un widget"""
        widget.configure(highlightbackground=self.colors['success'],
                        highlightthickness=3)
        widget.after(2000, lambda: widget.configure(highlightthickness=0))
    
    def create_gradient_frame(self, parent, color1, color2, width, height):
        """
        Crea un frame con efecto de gradiente simulado
        
        Args:
            parent: Widget padre
            color1 (str): Color inicial
            color2 (str): Color final
            width (int): Ancho
            height (int): Alto
            
        Returns:
            tk.Frame: Frame con gradiente
        """
        frame = tk.Frame(parent, width=width, height=height)
        
        # Crear canvas para el gradiente
        canvas = tk.Canvas(frame, width=width, height=height, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # Simular gradiente con rectángulos
        steps = 50
        for i in range(steps):
            # Interpolar colores (simplificado)
            y = int(height * i / steps)
            h = int(height / steps) + 1
            
            # Color interpolado (simplificado)
            if i < steps // 2:
                color = color1
            else:
                color = color2
            
            canvas.create_rectangle(0, y, width, y + h, fill=color, outline=color)
        
        return frame
    
    def update_theme(self, theme_name='default'):
        """
        Actualiza el tema de la aplicación
        
        Args:
            theme_name (str): Nombre del tema ('default', 'dark', 'light')
        """
        if theme_name == 'dark':
            self.colors.update({
                'background': '#1e1e1e',
                'text': '#ffffff',
                'white': '#2d2d2d',
                'light': '#404040'
            })
        elif theme_name == 'light':
            self.colors.update({
                'background': '#ffffff',
                'text': '#000000',
                'white': '#f8f9fa',
                'light': '#e9ecef'
            })
        
        # Reaplicar estilos
        self.apply_custom_styles()
    
    def apply_animation_effect(self, widget, effect_type='glow', duration=600):
        """
        Aplica efectos de animación a widgets preservando el contenido
        
        Args:
            widget: Widget al que aplicar el efecto
            effect_type (str): Tipo de efecto ('glow', 'shake', 'success', 'error', 'completion')
            duration (int): Duración en milisegundos
        """
        try:
            original_bg = widget.cget('bg') if hasattr(widget, 'cget') else '#ffffff'
            original_fg = widget.cget('fg') if hasattr(widget, 'cget') else '#000000'
            
            # Preservar el contenido actual de la celda
            current_value = ""
            if hasattr(widget, 'get'):
                current_value = widget.get()
        except:
            return  # Si hay error, no aplicar efecto
        
        if effect_type == 'success':
            # Efecto de éxito: verde brillante
            widget.configure(bg='#4caf50', fg='white')
            widget.after(duration//3, lambda: self._safe_configure(widget, bg='#66bb6a', value=current_value))
            widget.after(duration//2, lambda: self._safe_configure(widget, bg='#e3f2fd', fg='#1976d2', value=current_value))
            widget.after(duration, lambda: self._safe_configure(widget, bg=original_bg, fg=original_fg, value=current_value))
            
        elif effect_type == 'error':
            # Efecto de error: rojo con vibración
            widget.configure(bg='#f44336', fg='white')
            widget.after(duration//4, lambda: self._safe_configure(widget, bg='#ef5350', value=current_value))
            widget.after(duration//2, lambda: self._safe_configure(widget, bg='#ffebee', fg='#d32f2f', value=current_value))
            widget.after(duration, lambda: self._safe_configure(widget, bg=original_bg, fg=original_fg, value=current_value))
            
        elif effect_type == 'completion':
            # Efecto de completado: naranja brillante sin cambiar fuente
            widget.configure(bg='#ff9800', fg='white')
            widget.after(duration//3, lambda: self._safe_configure(widget, bg='#ffb74d', value=current_value))
            widget.after(duration//2, lambda: self._safe_configure(widget, bg='#fff3e0', fg='#f57c00', value=current_value))
            widget.after(duration, lambda: self._safe_configure(widget, bg=original_bg, fg=original_fg, value=current_value))
            
        elif effect_type == 'glow':
            # Efecto de brillo: azul suave
            widget.configure(bg='#2196f3', fg='white')
            widget.after(duration//2, lambda: self._safe_configure(widget, bg='#e3f2fd', fg='#1976d2', value=current_value))
            widget.after(duration, lambda: self._safe_configure(widget, bg=original_bg, fg=original_fg, value=current_value))
            
        elif effect_type == 'shake':
            # Efecto de vibración con color rojo
            self._shake_widget(widget, 5, duration, current_value)
    
    def _safe_configure(self, widget, value=None, **config_options):
        """Configura un widget de forma segura preservando su contenido"""
        try:
            widget.configure(**config_options)
            # Restaurar valor si se especifica
            if value is not None and hasattr(widget, 'delete') and hasattr(widget, 'insert'):
                current = widget.get() if hasattr(widget, 'get') else ""
                if current != value:
                    widget.delete(0, 'end')
                    widget.insert(0, value)
        except:
            pass  # Ignorar errores de configuración
    
    def _shake_widget(self, widget, count, total_duration, preserve_value=""):
        """Efecto de vibración para widgets preservando contenido"""
        if count > 0:
            # Obtener posición actual
            try:
                x = widget.winfo_x()
                y = widget.winfo_y()
                
                # Mover ligeramente
                widget.place(x=x + 2, y=y)
                widget.after(total_duration//10, 
                           lambda: widget.place(x=x - 2, y=y) if count > 1 else None)
                widget.after(total_duration//5, 
                           lambda: self._shake_widget(widget, count - 1, total_duration, preserve_value))
            except:
                # Si no se puede mover, solo cambiar color
                widget.configure(bg='#f44336', fg='white')
                # Preservar valor durante el efecto
                if preserve_value and hasattr(widget, 'get'):
                    current_value = widget.get()
                    if current_value != preserve_value:
                        widget.delete(0, 'end')
                        widget.insert(0, preserve_value)
                widget.after(total_duration//5, 
                           lambda: self._shake_widget(widget, count - 1, total_duration, preserve_value))
    
    def highlight_completion_area(self, widget_list, area_type='row'):
        """
        Resalta un área completa (fila, columna o cuadro)
        
        Args:
            widget_list: Lista de widgets a resaltar
            area_type (str): Tipo de área ('row', 'column', 'box')
        """
        for widget in widget_list:
            self.apply_animation_effect(widget, 'completion', 1500)
    
    def flash_success(self, widget):
        """Efecto rápido de éxito"""
        self.apply_animation_effect(widget, 'success', 400)
    
    def flash_error(self, widget):
        """Efecto rápido de error"""
        self.apply_animation_effect(widget, 'error', 500)
    
    def get_color(self, color_name):
        """
        Obtiene un color de la paleta
        
        Args:
            color_name (str): Nombre del color
            
        Returns:
            str: Código hexadecimal del color
        """
        return self.colors.get(color_name, '#000000')
    
    def save_theme_config(self, filename='theme_config.json'):
        """
        Guarda la configuración del tema actual
        
        Args:
            filename (str): Nombre del archivo
        """
        with open(filename, 'w') as f:
            json.dump(self.colors, f, indent=4)
    
    def load_theme_config(self, filename='theme_config.json'):
        """
        Carga configuración de tema desde archivo
        
        Args:
            filename (str): Nombre del archivo
        """
        try:
            with open(filename, 'r') as f:
                loaded_colors = json.load(f)
                self.colors.update(loaded_colors)
            self.apply_custom_styles()
        except FileNotFoundError:
            print(f"Archivo de tema {filename} no encontrado. Usando tema por defecto.")


def apply_modern_theme(root):
    """
    Función de conveniencia para aplicar tema moderno
    
    Args:
        root: Ventana raíz de Tkinter
        
    Returns:
        StyleManager: Instancia del gestor de estilos
    """
    style_manager = StyleManager(root)
    return style_manager


# Función de prueba
def test_styles():
    """Función de prueba para los estilos"""
    root = tk.Tk()
    root.title("Prueba de Estilos")
    root.geometry("600x400")
    
    # Aplicar estilos
    style_manager = apply_modern_theme(root)
    
    # Crear widgets de prueba
    main_frame = ttk.Frame(root, style="Custom.TFrame")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título
    ttk.Label(main_frame, text="Prueba de Estilos CSS", 
             style="Title.TLabel").pack(pady=10)
    
    # Botones
    button_frame = ttk.Frame(main_frame, style="Custom.TFrame")
    button_frame.pack(pady=20)
    
    ttk.Button(button_frame, text="Primario", style="Action.TButton").pack(side="left", padx=5)
    ttk.Button(button_frame, text="Éxito", style="Success.TButton").pack(side="left", padx=5)
    ttk.Button(button_frame, text="Advertencia", style="Warning.TButton").pack(side="left", padx=5)
    ttk.Button(button_frame, text="Peligro", style="Danger.TButton").pack(side="left", padx=5)
    
    # Información
    ttk.Label(main_frame, text="Los estilos han sido aplicados correctamente.", 
             style="Info.TLabel").pack(pady=10)
    
    root.mainloop()


if __name__ == "__main__":
    test_styles()