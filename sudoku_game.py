"""
Clase principal del juego Sudoku
Maneja la lógica del juego, puntuación, tiempo y estado de la partida
"""

import time
import copy
from datetime import datetime
from sudoku_generator import SudokuGenerator
from database import SudokuDatabase


class SudokuGame:
    def __init__(self, difficulty="medio"):
        """
        Inicializa una nueva partida de Sudoku
        
        Args:
            difficulty (str): Nivel de dificultad ("facil", "medio", "dificil")
        """
        self.generator = SudokuGenerator()
        self.database = SudokuDatabase()
        
        # Configuración del juego
        self.difficulty = difficulty
        self.start_time = None
        self.end_time = None
        self.paused_time = 0
        self.is_paused = False
        self.is_completed = False
        
        # Estado del tablero
        self.initial_puzzle = None
        self.current_puzzle = None
        self.solution = None
        self.locked_cells = set()  # Celdas que no se pueden modificar
        
        # Sistema de puntuación
        self.score = 0
        self.base_score = 1000
        self.hints_used = 0
        self.mistakes = 0
        self.max_mistakes = 3
        
        # ID de la partida en la base de datos
        self.game_id = None
        self.user_id = None
        
        # Callbacks para la interfaz
        self.on_cell_change = None
        self.on_game_complete = None
        self.on_mistake = None
        self.on_time_update = None
    
    def new_game(self, user_id=None):
        """
        Inicia una nueva partida
        
        Args:
            user_id (int): ID del usuario en la base de datos
        """
        # Generar nuevo puzzle
        self.initial_puzzle, self.solution = self.generator.generate_puzzle(self.difficulty)
        self.current_puzzle = copy.deepcopy(self.initial_puzzle)
        
        # Identificar celdas bloqueadas (números iniciales)
        self.locked_cells = set()
        for i in range(9):
            for j in range(9):
                if self.initial_puzzle[i][j] != 0:
                    self.locked_cells.add((i, j))
        
        # Reiniciar estado del juego
        self.start_time = time.time()
        self.end_time = None
        self.paused_time = 0
        self.is_paused = False
        self.is_completed = False
        self.score = self.base_score
        self.hints_used = 0
        self.mistakes = 0
        self.user_id = user_id
        
        # Guardar en base de datos si hay usuario
        if self.user_id and self.database:
            self.game_id = self.database.guardar_partida(
                self.user_id, 
                self.initial_puzzle, 
                self.current_puzzle, 
                self.solution, 
                self.difficulty.capitalize()
            )
        
        print(f"Nueva partida iniciada - Dificultad: {self.difficulty}")
    
    def make_move(self, row, col, number):
        """
        Realiza un movimiento en el tablero
        
        Args:
            row (int): Fila (0-8)
            col (int): Columna (0-8)
            number (int): Número a colocar (0-9, 0 para borrar)
            
        Returns:
            dict: Resultado del movimiento
        """
        # Verificar si la celda está bloqueada
        if (row, col) in self.locked_cells:
            return {
                'success': False,
                'message': 'No puedes modificar los números iniciales',
                'is_valid': False
            }
        
        # Verificar si el juego ya terminó
        if self.is_completed:
            return {
                'success': False,
                'message': 'El juego ya ha terminado',
                'is_valid': False
            }
        
        previous_value = self.current_puzzle[row][col]
        
        # Realizar el movimiento
        self.current_puzzle[row][col] = number
        
        # Validar movimiento si se está ingresando un número
        is_valid = True
        if number != 0:
            # Verificar si el número ya existe en la fila
            for c in range(9):
                if c != col and self.current_puzzle[row][c] == number:
                    is_valid = False
                    break
            
            # Verificar si el número ya existe in la columna
            if is_valid:
                for r in range(9):
                    if r != row and self.current_puzzle[r][col] == number:
                        is_valid = False
                        break
            
            # Verificar si el número ya existe en el cuadro 3x3
            if is_valid:
                start_row = (row // 3) * 3
                start_col = (col // 3) * 3
                for r in range(start_row, start_row + 3):
                    for c in range(start_col, start_col + 3):
                        if (r != row or c != col) and self.current_puzzle[r][c] == number:
                            is_valid = False
                            break
                    if not is_valid:
                        break
            
            if not is_valid:
                self.mistakes += 1
                self.score = max(0, self.score - 50)  # Penalización por error
                
                # Notificar error
                if self.on_mistake:
                    self.on_mistake(self.mistakes, self.max_mistakes)
                
                # Verificar si se acabaron los intentos
                if self.mistakes >= self.max_mistakes:
                    self.end_game(False)
                    return {
                        'success': False,
                        'message': f'Demasiados errores. Juego terminado.',
                        'is_valid': False,
                        'game_over': True
                    }
        
        # Actualizar puntuación por movimiento correcto
        if is_valid and number != 0:
            self.score += 10
        
        # Verificar si el juego está completo
        if self.generator.is_complete(self.current_puzzle):
            if self.generator.is_solved(self.current_puzzle):
                self.end_game(True)
                return {
                    'success': True,
                    'message': '¡Felicitaciones! Has completado el Sudoku',
                    'is_valid': True,
                    'completed': True
                }
            else:
                # El tablero está lleno pero incorrectamente
                self.mistakes += 1
                self.score = max(0, self.score - 100)
                return {
                    'success': False,
                    'message': 'El tablero está lleno pero hay errores',
                    'is_valid': False
                }
        
        # Guardar progreso en la base de datos
        self.save_progress()
        
        # Notificar cambio de celda
        if self.on_cell_change:
            self.on_cell_change(row, col, number, is_valid)
        
        return {
            'success': True,
            'message': 'Movimiento realizado',
            'is_valid': is_valid,
            'completed': False
        }
    
    def get_hint(self):
        """
        Obtiene una pista para el jugador
        
        Returns:
            dict: Información de la pista o None si no hay celdas vacías
        """
        if self.is_completed:
            return None
        
        hint = self.generator.get_hint(self.current_puzzle, self.solution)
        
        if hint:
            row, col, number = hint
            self.hints_used += 1
            self.score = max(0, self.score - 25)  # Penalización por usar pista
            
            # Aplicar la pista automáticamente
            self.current_puzzle[row][col] = number
            
            # Verificar si se completó el juego
            if self.generator.is_complete(self.current_puzzle):
                if self.generator.is_solved(self.current_puzzle):
                    self.end_game(True)
            
            self.save_progress()
            
            return {
                'row': row,
                'col': col,
                'number': number,
                'hints_used': self.hints_used,
                'score': self.score
            }
        
        return None
    
    def get_elapsed_time(self):
        """
        Obtiene el tiempo transcurrido en la partida
        
        Returns:
            int: Tiempo en segundos
        """
        if not self.start_time:
            return 0
        
        if self.is_completed and self.end_time:
            return int(self.end_time - self.start_time - self.paused_time)
        elif self.is_paused:
            return int(time.time() - self.start_time - self.paused_time)
        else:
            return int(time.time() - self.start_time - self.paused_time)
    
    def pause_game(self):
        """Pausa el juego"""
        if not self.is_completed and not self.is_paused:
            self.is_paused = True
            self.pause_start = time.time()
    
    def resume_game(self):
        """Reanuda el juego"""
        if self.is_paused and hasattr(self, 'pause_start'):
            self.paused_time += time.time() - self.pause_start
            self.is_paused = False
            delattr(self, 'pause_start')
    
    def end_game(self, completed=False):
        """
        Termina la partida actual
        
        Args:
            completed (bool): Si el juego fue completado exitosamente
        """
        self.end_time = time.time()
        self.is_completed = True
        self.is_paused = False
        
        # Calcular puntuación final
        if completed:
            elapsed_time = self.get_elapsed_time()
            time_bonus = max(0, 600 - elapsed_time)  # Bonus por tiempo
            difficulty_multiplier = {
                'facil': 1.0,
                'medio': 1.5,
                'dificil': 2.0
            }.get(self.difficulty.lower(), 1.0)
            
            self.score = int((self.score + time_bonus) * difficulty_multiplier)
        
        # Guardar resultado final en la base de datos
        self.save_progress()
        
        # Notificar finalización
        if self.on_game_complete:
            self.on_game_complete(completed, self.score, self.get_elapsed_time())
        
        print(f"Juego terminado - Completado: {completed}, Puntuación: {self.score}")
    
    def check_area_completion(self, row, col):
        """
        Verifica si una fila, columna o cuadro 3x3 se completó
        
        Args:
            row (int): Fila de la celda recién completada
            col (int): Columna de la celda recién completada
            
        Returns:
            dict: Información sobre áreas completadas
        """
        completed_areas = {
            'row': False,
            'column': False,
            'box': False,
            'row_cells': [],
            'column_cells': [],
            'box_cells': []
        }
        
        # Verificar fila
        row_complete = True
        row_cells = []
        for c in range(9):
            if self.current_puzzle[row][c] == 0:
                row_complete = False
                break
            row_cells.append((row, c))
        
        if row_complete:
            completed_areas['row'] = True
            completed_areas['row_cells'] = row_cells
        
        # Verificar columna
        column_complete = True
        column_cells = []
        for r in range(9):
            if self.current_puzzle[r][col] == 0:
                column_complete = False
                break
            column_cells.append((r, col))
        
        if column_complete:
            completed_areas['column'] = True
            completed_areas['column_cells'] = column_cells
        
        # Verificar cuadro 3x3
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        box_complete = True
        box_cells = []
        
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if self.current_puzzle[r][c] == 0:
                    box_complete = False
                    break
                box_cells.append((r, c))
            if not box_complete:
                break
        
        if box_complete:
            completed_areas['box'] = True
            completed_areas['box_cells'] = box_cells
        
        return completed_areas
    
    def save_progress(self):
        """Guarda el progreso actual en la base de datos"""
        if self.game_id and self.database:
            self.database.actualizar_partida(
                self.game_id,
                self.current_puzzle,
                self.get_elapsed_time(),
                self.is_completed,
                self.score,
                self.hints_used
            )
    
    def load_game(self, game_id):
        """
        Carga una partida guardada desde la base de datos
        
        Args:
            game_id (int): ID de la partida a cargar
            
        Returns:
            bool: True si se cargó exitosamente
        """
        if not self.database:
            return False
        
        game_data = self.database.cargar_partida(game_id)
        
        if game_data:
            self.game_id = game_data['id']
            self.user_id = game_data['usuario_id']
            self.initial_puzzle = game_data['tablero_inicial']
            self.current_puzzle = game_data['tablero_actual']
            self.solution = game_data['tablero_solucion']
            self.difficulty = game_data['dificultad'].lower()
            self.score = game_data['puntuacion']
            self.hints_used = game_data['pistas_usadas']
            self.is_completed = bool(game_data['completado'])
            
            # Reconstruir celdas bloqueadas
            self.locked_cells = set()
            for i in range(9):
                for j in range(9):
                    if self.initial_puzzle[i][j] != 0:
                        self.locked_cells.add((i, j))
            
            # Configurar tiempo (aproximado)
            if game_data['fecha_inicio']:
                if self.is_completed:
                    self.start_time = time.time() - game_data['tiempo_jugado']
                    self.end_time = time.time()
                else:
                    self.start_time = time.time() - game_data['tiempo_jugado']
            
            print(f"Partida {game_id} cargada exitosamente")
            return True
        
        return False
    
    def get_game_state(self):
        """
        Obtiene el estado actual del juego
        
        Returns:
            dict: Estado completo del juego
        """
        return {
            'current_puzzle': copy.deepcopy(self.current_puzzle),
            'initial_puzzle': copy.deepcopy(self.initial_puzzle),
            'solution': copy.deepcopy(self.solution),
            'locked_cells': self.locked_cells.copy(),
            'difficulty': self.difficulty,
            'score': self.score,
            'hints_used': self.hints_used,
            'mistakes': self.mistakes,
            'max_mistakes': self.max_mistakes,
            'elapsed_time': self.get_elapsed_time(),
            'is_completed': self.is_completed,
            'is_paused': self.is_paused,
            'user_id': self.user_id,
            'game_id': self.game_id
        }
    
    def get_cell_conflicts(self, row, col):
        """
        Obtiene las celdas en conflicto para una posición específica
        
        Args:
            row (int): Fila
            col (int): Columna
            
        Returns:
            list: Lista de posiciones (row, col) en conflicto
        """
        conflicts = []
        if self.current_puzzle[row][col] == 0:
            return conflicts
        
        number = self.current_puzzle[row][col]
        
        # Verificar fila
        for j in range(9):
            if j != col and self.current_puzzle[row][j] == number:
                conflicts.append((row, j))
        
        # Verificar columna
        for i in range(9):
            if i != row and self.current_puzzle[i][col] == number:
                conflicts.append((i, col))
        
        # Verificar subcuadrícula 3x3
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if (i, j) != (row, col) and self.current_puzzle[i][j] == number:
                    conflicts.append((i, j))
        
        return conflicts
    
    def get_statistics(self):
        """
        Obtiene estadísticas de la partida actual
        
        Returns:
            dict: Estadísticas del juego
        """
        filled_cells = sum(1 for i in range(9) for j in range(9) 
                          if self.current_puzzle[i][j] != 0)
        total_cells = 81
        initial_filled = sum(1 for i in range(9) for j in range(9) 
                           if self.initial_puzzle[i][j] != 0)
        progress = ((filled_cells - initial_filled) / (total_cells - initial_filled)) * 100
        
        return {
            'filled_cells': filled_cells,
            'total_cells': total_cells,
            'progress_percentage': min(100, max(0, progress)),
            'elapsed_time': self.get_elapsed_time(),
            'score': self.score,
            'hints_used': self.hints_used,
            'mistakes': self.mistakes,
            'difficulty': self.difficulty.capitalize()
        }


# Función de prueba
def test_sudoku_game():
    """Función de prueba para la clase SudokuGame"""
    print("Probando la clase SudokuGame...")
    
    # Crear nueva partida
    game = SudokuGame("medio")
    game.new_game()
    
    # Mostrar estado inicial
    print("\nTablero inicial:")
    game.generator.print_grid(game.current_puzzle)
    
    # Probar algunos movimientos
    print("\nProbando movimientos...")
    
    # Buscar una celda vacía para probar
    for i in range(9):
        for j in range(9):
            if game.current_puzzle[i][j] == 0:
                correct_number = game.solution[i][j]
                print(f"\nProbando movimiento correcto en ({i+1}, {j+1}) → {correct_number}")
                result = game.make_move(i, j, correct_number)
                print(f"Resultado: {result}")
                break
        else:
            continue
        break
    
    # Probar pista
    print("\nObteniendo pista...")
    hint = game.get_hint()
    if hint:
        print(f"Pista aplicada: Fila {hint['row']+1}, Columna {hint['col']+1} → {hint['number']}")
    
    # Mostrar estadísticas
    print("\nEstadísticas:")
    stats = game.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    test_sudoku_game()