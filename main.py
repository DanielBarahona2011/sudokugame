"""
Archivo principal para ejecutar la aplicación de Sudoku
Punto de entrada único para la aplicación
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import traceback

# Agregar el directorio actual al path de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from sudoku_gui import SudokuGUI
    from database import SudokuDatabase
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    if hasattr(tk, 'Tk'):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error de Importación", 
                           f"No se pudieron cargar los módulos necesarios:\n{e}\n\n"
                           f"Asegúrate de que todos los archivos estén en el mismo directorio.")
        root.destroy()
    sys.exit(1)


class SudokuApp:
    """Clase principal de la aplicación Sudoku"""
    
    def __init__(self):
        """Inicializa la aplicación"""
        self.gui = None
        self.database = None
    
    def check_dependencies(self):
        """Verifica que todas las dependencias estén disponibles"""
        try:
            import ttkthemes
            return True
        except ImportError:
            messagebox.showerror("Dependencias Faltantes", 
                               "La biblioteca 'ttkthemes' no está instalada.\n\n"
                               "Para instalarla, ejecuta:\n"
                               "pip install ttkthemes")
            return False
    
    def initialize_database(self):
        """Inicializa la base de datos"""
        try:
            self.database = SudokuDatabase()
            print("✓ Base de datos inicializada correctamente")
            return True
        except Exception as e:
            print(f"❌ Error al inicializar la base de datos: {e}")
            messagebox.showerror("Error de Base de Datos", 
                               f"No se pudo inicializar la base de datos:\n{e}")
            return False
    
    def run(self):
        """Ejecuta la aplicación principal"""
        print("🧩 Iniciando aplicación Sudoku...")
        
        # Verificar dependencias
        if not self.check_dependencies():
            return False
        
        # Inicializar base de datos
        if not self.initialize_database():
            return False
        
        try:
            # Crear y ejecutar GUI
            self.gui = SudokuGUI()
            print("✓ Interfaz gráfica creada correctamente")
            
            # Ejecutar aplicación
            print("🎮 Ejecutando aplicación...")
            self.gui.run()
            
            return True
            
        except Exception as e:
            print(f"❌ Error al ejecutar la aplicación: {e}")
            traceback.print_exc()
            
            # Mostrar error en ventana si es posible
            try:
                if not hasattr(self, '_error_shown'):
                    self._error_shown = True
                    messagebox.showerror("Error de Ejecución", 
                                       f"Se produjo un error al ejecutar la aplicación:\n\n{e}\n\n"
                                       f"Consulta la consola para más detalles.")
            except:
                pass
            
            return False
        
        finally:
            # Limpieza final
            if self.database:
                try:
                    self.database.cerrar_conexion()
                except:
                    pass
            print("👋 Aplicación cerrada")
    
    def show_welcome_message(self):
        """Muestra mensaje de bienvenida"""
        welcome_text = """
        🧩 ¡Bienvenido a Sudoku! 🧩
        
        ✨ Características principales:
        • 3 niveles de dificultad
        • Sistema de puntuación avanzado
        • Cronómetro integrado
        • Validación en tiempo real
        • Base de datos de partidas
        • Estadísticas detalladas
        
        🎮 ¡Disfruta del juego!
        """
        
        try:
            messagebox.showinfo("¡Bienvenido!", welcome_text)
        except:
            print(welcome_text)


def main():
    """Función principal"""
    print("=" * 50)
    print("🧩 SUDOKU - JUEGO DE LÓGICA")
    print("Versión: 1.0")
    print("Desarrollado con Python y Tkinter")
    print("=" * 50)
    
    # Crear y ejecutar aplicación
    app = SudokuApp()
    success = app.run()
    
    # Código de salida
    if success:
        print("✓ Aplicación ejecutada exitosamente")
        sys.exit(0)
    else:
        print("❌ La aplicación terminó con errores")
        sys.exit(1)


if __name__ == "__main__":
    main()