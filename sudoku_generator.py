"""
Generador y Solucionador de Sudoku
Implementa algoritmos para crear sudokus válidos con diferentes niveles de dificultad
"""

import random
import copy


class SudokuGenerator:
    def __init__(self):
        """Inicializa el generador de Sudoku"""
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
    
    def is_valid(self, grid, row, col, num):
        """
        Verifica si es válido colocar un número en una posición específica
        
        Args:
            grid (list): Tablero 9x9
            row (int): Fila (0-8)
            col (int): Columna (0-8)
            num (int): Número a verificar (1-9)
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        # Verificar fila
        for x in range(9):
            if grid[row][x] == num:
                return False
        
        # Verificar columna
        for x in range(9):
            if grid[x][col] == num:
                return False
        
        # Verificar subcuadrícula 3x3
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def solve_sudoku(self, grid):
        """
        Resuelve el sudoku usando backtracking
        
        Args:
            grid (list): Tablero 9x9 a resolver
            
        Returns:
            bool: True si tiene solución, False en caso contrario
        """
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(grid, i, j, num):
                            grid[i][j] = num
                            if self.solve_sudoku(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True
    
    def fill_diagonal(self, grid):
        """
        Llena las tres subcuadrículas diagonales del tablero
        
        Args:
            grid (list): Tablero 9x9 a llenar
        """
        for i in range(0, 9, 3):
            self.fill_box(grid, i, i)
    
    def fill_box(self, grid, row, col):
        """
        Llena una subcuadrícula 3x3 con números aleatorios válidos
        
        Args:
            grid (list): Tablero 9x9
            row (int): Fila inicial de la subcuadrícula
            col (int): Columna inicial de la subcuadrícula
        """
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        for i in range(3):
            for j in range(3):
                grid[row + i][col + j] = numbers[i * 3 + j]
    
    def generate_complete_sudoku(self):
        """
        Genera un sudoku completo válido usando un enfoque más simple
        
        Returns:
            list: Tablero 9x9 completamente lleno y válido
        """
        # Empezar con un sudoku base válido conocido
        base_sudoku = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        
        # Crear una copia y randomizarla
        grid = copy.deepcopy(base_sudoku)
        
        # Aplicar transformaciones aleatorias que preservan la validez
        self.randomize_sudoku(grid)
        
        return grid
    
    def randomize_sudoku(self, grid):
        """
        Aplica transformaciones aleatorias que preservan la validez del Sudoku
        
        Args:
            grid (list): Tablero válido a randomizar
        """
        # Intercambiar filas dentro de cada banda (grupos de 3 filas)
        for band in range(3):
            rows = list(range(band * 3, (band + 1) * 3))
            random.shuffle(rows)
            original_rows = [grid[i][:] for i in range(band * 3, (band + 1) * 3)]
            for i, new_row_idx in enumerate(rows):
                grid[band * 3 + i] = original_rows[new_row_idx - band * 3]
        
        # Intercambiar columnas dentro de cada grupo de 3
        for col_group in range(3):
            cols = list(range(col_group * 3, (col_group + 1) * 3))
            random.shuffle(cols)
            for row in range(9):
                original_values = [grid[row][j] for j in range(col_group * 3, (col_group + 1) * 3)]
                for i, new_col_idx in enumerate(cols):
                    grid[row][col_group * 3 + i] = original_values[new_col_idx - col_group * 3]
        
        # Intercambiar bandas (grupos de 3 filas)
        bands = list(range(3))
        random.shuffle(bands)
        original_grid = copy.deepcopy(grid)
        for i, band_idx in enumerate(bands):
            for row in range(3):
                grid[i * 3 + row] = original_grid[band_idx * 3 + row]
        
        # Intercambiar grupos de columnas
        col_groups = list(range(3))
        random.shuffle(col_groups)
        original_grid = copy.deepcopy(grid)
        for i, group_idx in enumerate(col_groups):
            for row in range(9):
                for col in range(3):
                    grid[row][i * 3 + col] = original_grid[row][group_idx * 3 + col]
        
        # Reemplazar números (1-9) por una permutación aleatoria
        numbers = list(range(1, 10))
        shuffled_numbers = numbers[:]
        random.shuffle(shuffled_numbers)
        number_map = {numbers[i]: shuffled_numbers[i] for i in range(9)}
        
        for row in range(9):
            for col in range(9):
                grid[row][col] = number_map[grid[row][col]]
    
    def remove_numbers(self, grid, difficulty="medio"):
        """
        Remueve números del tablero completo según la dificultad
        
        Args:
            grid (list): Tablero completo 9x9
            difficulty (str): Nivel de dificultad ("facil", "medio", "dificil")
            
        Returns:
            list: Tablero con números removidos
        """
        # Definir cantidad de celdas a remover según dificultad
        cells_to_remove = {
            "facil": 30,
            "medio": 40,
            "dificil": 50
        }
        
        puzzle = copy.deepcopy(grid)
        remove_count = cells_to_remove.get(difficulty.lower(), 40)
        
        # Lista de todas las posiciones
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        # Remover números de manera más simple
        for i in range(min(remove_count, len(positions))):
            row, col = positions[i]
            puzzle[row][col] = 0
        
        return puzzle
    
    def has_unique_solution(self, grid):
        """
        Verifica si el puzzle tiene una solución única
        
        Args:
            grid (list): Tablero 9x9 parcialmente lleno
            
        Returns:
            bool: True si tiene solución única
        """
        grid_copy = copy.deepcopy(grid)
        solutions = []
        
        def solve_all(grid_temp, solutions_list):
            """Encuentra todas las soluciones posibles"""
            if len(solutions_list) > 1:
                return
                
            for i in range(9):
                for j in range(9):
                    if grid_temp[i][j] == 0:
                        for num in range(1, 10):
                            if self.is_valid(grid_temp, i, j, num):
                                grid_temp[i][j] = num
                                solve_all(grid_temp, solutions_list)
                                grid_temp[i][j] = 0
                        return
            
            # Si llegamos aquí, encontramos una solución completa
            solutions_list.append(copy.deepcopy(grid_temp))
        
        solve_all(grid_copy, solutions)
        return len(solutions) == 1
    
    def generate_puzzle(self, difficulty="medio"):
        """
        Genera un puzzle de Sudoku completo
        
        Args:
            difficulty (str): Nivel de dificultad
            
        Returns:
            tuple: (puzzle, solution) - Tableros inicial y solución
        """
        # Generar sudoku completo (solución)
        solution = self.generate_complete_sudoku()
        
        # Crear puzzle removiendo números
        puzzle = self.remove_numbers(solution, difficulty)
        
        return puzzle, solution
    
    def print_grid(self, grid):
        """
        Imprime el tablero en formato legible
        
        Args:
            grid (list): Tablero 9x9 a imprimir
        """
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("------+-------+------")
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                if j == 8:
                    print(grid[i][j] if grid[i][j] != 0 else ".")
                else:
                    print(str(grid[i][j]) if grid[i][j] != 0 else ".", end=" ")
    
    def count_filled_cells(self, grid):
        """
        Cuenta las celdas llenas en el tablero
        
        Args:
            grid (list): Tablero 9x9
            
        Returns:
            int: Número de celdas llenas
        """
        return sum(1 for i in range(9) for j in range(9) if grid[i][j] != 0)
    
    def get_hint(self, puzzle, solution):
        """
        Obtiene una pista para el puzzle actual
        
        Args:
            puzzle (list): Tablero actual del jugador
            solution (list): Solución completa
            
        Returns:
            tuple: (row, col, number) o None si no hay celdas vacías
        """
        empty_cells = [(i, j) for i in range(9) for j in range(9) 
                       if puzzle[i][j] == 0]
        
        if empty_cells:
            row, col = random.choice(empty_cells)
            return row, col, solution[row][col]
        
        return None
    
    def validate_move(self, grid, row, col, num):
        """
        Valida si un movimiento es correcto según las reglas del Sudoku
        
        Args:
            grid (list): Tablero actual
            row (int): Fila
            col (int): Columna
            num (int): Número a colocar
            
        Returns:
            bool: True si el movimiento es válido
        """
        return self.is_valid(grid, row, col, num)
    
    def is_complete(self, grid):
        """
        Verifica si el tablero está completamente lleno
        
        Args:
            grid (list): Tablero 9x9
            
        Returns:
            bool: True si está completo
        """
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return False
        return True
    
    def is_solved(self, grid):
        """
        Verifica si el tablero está correctamente resuelto
        
        Args:
            grid (list): Tablero 9x9
            
        Returns:
            bool: True si está resuelto correctamente
        """
        if not self.is_complete(grid):
            return False
            
        # Verificar todas las filas, columnas y subcuadrículas
        for i in range(9):
            for j in range(9):
                num = grid[i][j]
                grid[i][j] = 0  # Temporalmente vacía para verificar
                if not self.is_valid(grid, i, j, num):
                    grid[i][j] = num  # Restaurar
                    return False
                grid[i][j] = num  # Restaurar
        
        return True
    
    def get_difficulty_stats(self, puzzle):
        """
        Analiza la dificultad del puzzle basado en celdas llenas
        
        Args:
            puzzle (list): Tablero del puzzle
            
        Returns:
            dict: Estadísticas del puzzle
        """
        filled = self.count_filled_cells(puzzle)
        empty = 81 - filled
        
        if empty <= 35:
            difficulty = "Fácil"
        elif empty <= 45:
            difficulty = "Medio"
        else:
            difficulty = "Difícil"
        
        return {
            'filled_cells': filled,
            'empty_cells': empty,
            'difficulty': difficulty,
            'completion_percentage': (filled / 81) * 100
        }


# Función de prueba
def test_generator():
    """Función de prueba para el generador de Sudoku"""
    print("Probando el generador de Sudoku...")
    
    generator = SudokuGenerator()
    
    # Generar puzzle de dificultad media
    puzzle, solution = generator.generate_puzzle("medio")
    
    print("\nPuzzle generado:")
    generator.print_grid(puzzle)
    
    print("\nSolución:")
    generator.print_grid(solution)
    
    print("\nEstadísticas del puzzle:")
    stats = generator.get_difficulty_stats(puzzle)
    print(f"Celdas llenas: {stats['filled_cells']}")
    print(f"Celdas vacías: {stats['empty_cells']}")
    print(f"Dificultad: {stats['difficulty']}")
    print(f"Porcentaje de completado: {stats['completion_percentage']:.1f}%")
    
    # Probar una pista
    hint = generator.get_hint(puzzle, solution)
    if hint:
        row, col, num = hint
        print(f"\nPista: Fila {row+1}, Columna {col+1} → {num}")


if __name__ == "__main__":
    test_generator()