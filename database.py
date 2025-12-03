"""
Módulo para manejo de la base de datos SQLite del juego Sudoku
Gestiona usuarios, partidas, estadísticas y operaciones CRUD
"""

import sqlite3
import datetime
import json


class SudokuDatabase:
    def __init__(self, db_name="sudoku.db"):
        """
        Inicializa la conexión a la base de datos
        
        Args:
            db_name (str): Nombre del archivo de base de datos
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establece conexión con la base de datos SQLite"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Conexión exitosa a la base de datos: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
    
    def create_tables(self):
        """Crea las tablas necesarias si no existen"""
        try:
            # Tabla de usuarios
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                    juegos_jugados INTEGER DEFAULT 0,
                    juegos_completados INTEGER DEFAULT 0,
                    mejor_tiempo INTEGER DEFAULT 0,
                    puntuacion_total INTEGER DEFAULT 0
                )
            ''')
            
            # Tabla de partidas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS partidas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER,
                    tablero_inicial TEXT NOT NULL,
                    tablero_actual TEXT NOT NULL,
                    tablero_solucion TEXT NOT NULL,
                    dificultad TEXT DEFAULT 'Fácil',
                    fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
                    fecha_fin DATETIME,
                    tiempo_jugado INTEGER DEFAULT 0,
                    completado BOOLEAN DEFAULT 0,
                    puntuacion INTEGER DEFAULT 0,
                    pistas_usadas INTEGER DEFAULT 0,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                )
            ''')
            
            # Tabla de estadísticas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS estadisticas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER,
                    fecha DATE DEFAULT CURRENT_DATE,
                    partidas_jugadas INTEGER DEFAULT 0,
                    partidas_completadas INTEGER DEFAULT 0,
                    tiempo_total INTEGER DEFAULT 0,
                    puntuacion_dia INTEGER DEFAULT 0,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                )
            ''')
            
            self.connection.commit()
            print("Tablas creadas exitosamente")
            
        except sqlite3.Error as e:
            print(f"Error al crear tablas: {e}")
    
    def insertar_usuario(self, nombre):
        """
        Inserta un nuevo usuario en la base de datos
        
        Args:
            nombre (str): Nombre del usuario
            
        Returns:
            int: ID del usuario insertado o None si hay error
        """
        try:
            self.cursor.execute(
                "INSERT INTO usuarios (nombre) VALUES (?)",
                (nombre,)
            )
            self.connection.commit()
            user_id = self.cursor.lastrowid
            print(f"Usuario '{nombre}' insertado con ID: {user_id}")
            return user_id
        except sqlite3.IntegrityError:
            print(f"El usuario '{nombre}' ya existe")
            return None
        except sqlite3.Error as e:
            print(f"Error al insertar usuario: {e}")
            return None
    
    def obtener_usuario_por_nombre(self, nombre):
        """
        Obtiene un usuario por su nombre
        
        Args:
            nombre (str): Nombre del usuario
            
        Returns:
            tuple: Datos del usuario o None si no existe
        """
        try:
            self.cursor.execute(
                "SELECT * FROM usuarios WHERE nombre = ?",
                (nombre,)
            )
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al consultar usuario: {e}")
            return None
    
    def guardar_partida(self, usuario_id, tablero_inicial, tablero_actual, 
                       tablero_solucion, dificultad="Fácil"):
        """
        Guarda una nueva partida en la base de datos
        
        Args:
            usuario_id (int): ID del usuario
            tablero_inicial (list): Estado inicial del tablero
            tablero_actual (list): Estado actual del tablero
            tablero_solucion (list): Solución del tablero
            dificultad (str): Nivel de dificultad
            
        Returns:
            int: ID de la partida guardada
        """
        try:
            tablero_inicial_json = json.dumps(tablero_inicial)
            tablero_actual_json = json.dumps(tablero_actual)
            tablero_solucion_json = json.dumps(tablero_solucion)
            
            self.cursor.execute('''
                INSERT INTO partidas (usuario_id, tablero_inicial, tablero_actual, 
                                    tablero_solucion, dificultad)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario_id, tablero_inicial_json, tablero_actual_json, 
                  tablero_solucion_json, dificultad))
            
            self.connection.commit()
            partida_id = self.cursor.lastrowid
            print(f"Partida guardada con ID: {partida_id}")
            return partida_id
        except sqlite3.Error as e:
            print(f"Error al guardar partida: {e}")
            return None
    
    def actualizar_partida(self, partida_id, tablero_actual, tiempo_jugado, 
                          completado=False, puntuacion=0, pistas_usadas=0):
        """
        Actualiza el estado de una partida existente
        
        Args:
            partida_id (int): ID de la partida
            tablero_actual (list): Estado actual del tablero
            tiempo_jugado (int): Tiempo jugado en segundos
            completado (bool): Si la partida está completada
            puntuacion (int): Puntuación obtenida
            pistas_usadas (int): Número de pistas utilizadas
        """
        try:
            tablero_actual_json = json.dumps(tablero_actual)
            fecha_fin = datetime.datetime.now() if completado else None
            
            self.cursor.execute('''
                UPDATE partidas 
                SET tablero_actual = ?, tiempo_jugado = ?, completado = ?, 
                    puntuacion = ?, pistas_usadas = ?, fecha_fin = ?
                WHERE id = ?
            ''', (tablero_actual_json, tiempo_jugado, completado, 
                  puntuacion, pistas_usadas, fecha_fin, partida_id))
            
            self.connection.commit()
            print(f"Partida {partida_id} actualizada")
        except sqlite3.Error as e:
            print(f"Error al actualizar partida: {e}")
    
    def actualizar_nombre_usuario_ranking(self, usuario_id, nuevo_nombre):
        """
        Actualiza el nombre de un usuario para el ranking
        
        Args:
            usuario_id (int): ID del usuario
            nuevo_nombre (str): Nuevo nombre para mostrar en rankings
        """
        try:
            self.cursor.execute('''
                UPDATE usuarios SET nombre = ? WHERE id = ?
            ''', (nuevo_nombre, usuario_id))
            
            self.connection.commit()
            print(f"Nombre de usuario actualizado a: {nuevo_nombre}")
            return True
        except sqlite3.Error as e:
            print(f"Error al actualizar nombre de usuario: {e}")
            return False
    
    def cargar_partida(self, partida_id):
        """
        Carga una partida específica desde la base de datos
        
        Args:
            partida_id (int): ID de la partida
            
        Returns:
            dict: Datos de la partida o None si no existe
        """
        try:
            self.cursor.execute(
                "SELECT * FROM partidas WHERE id = ?",
                (partida_id,)
            )
            partida = self.cursor.fetchone()
            
            if partida:
                return {
                    'id': partida[0],
                    'usuario_id': partida[1],
                    'tablero_inicial': json.loads(partida[2]),
                    'tablero_actual': json.loads(partida[3]),
                    'tablero_solucion': json.loads(partida[4]),
                    'dificultad': partida[5],
                    'fecha_inicio': partida[6],
                    'fecha_fin': partida[7],
                    'tiempo_jugado': partida[8],
                    'completado': partida[9],
                    'puntuacion': partida[10],
                    'pistas_usadas': partida[11]
                }
            return None
        except sqlite3.Error as e:
            print(f"Error al cargar partida: {e}")
            return None
    
    def obtener_estadisticas_usuario(self, usuario_id):
        """
        Obtiene las estadísticas de un usuario
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            dict: Estadísticas del usuario
        """
        try:
            self.cursor.execute('''
                SELECT 
                    COUNT(*) as total_partidas,
                    SUM(CASE WHEN completado = 1 THEN 1 ELSE 0 END) as completadas,
                    MIN(CASE WHEN completado = 1 THEN tiempo_jugado END) as mejor_tiempo,
                    AVG(CASE WHEN completado = 1 THEN tiempo_jugado END) as tiempo_promedio,
                    SUM(puntuacion) as puntuacion_total
                FROM partidas 
                WHERE usuario_id = ?
            ''', (usuario_id,))
            
            stats = self.cursor.fetchone()
            return {
                'total_partidas': stats[0] or 0,
                'completadas': stats[1] or 0,
                'mejor_tiempo': stats[2] or 0,
                'tiempo_promedio': stats[3] or 0,
                'puntuacion_total': stats[4] or 0
            }
        except sqlite3.Error as e:
            print(f"Error al obtener estadísticas: {e}")
            return {}
    
    def eliminar_partida(self, partida_id):
        """
        Elimina una partida de la base de datos
        
        Args:
            partida_id (int): ID de la partida a eliminar
        """
        try:
            self.cursor.execute("DELETE FROM partidas WHERE id = ?", (partida_id,))
            self.connection.commit()
            print(f"Partida {partida_id} eliminada")
        except sqlite3.Error as e:
            print(f"Error al eliminar partida: {e}")
    
    def obtener_ranking(self, limite=10):
        """
        Obtiene el ranking de jugadores por puntuación
        
        Args:
            limite (int): Número de jugadores a mostrar
            
        Returns:
            list: Lista de jugadores ordenados por puntuación
        """
        try:
            self.cursor.execute('''
                SELECT u.nombre, u.puntuacion_total, u.juegos_completados, u.mejor_tiempo
                FROM usuarios u
                ORDER BY u.puntuacion_total DESC
                LIMIT ?
            ''', (limite,))
            
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener ranking: {e}")
            return []
    
    def obtener_mejores_tiempos(self, dificultad=None, limite=10):
        """
        Obtiene los mejores tiempos registrados
        
        Args:
            dificultad (str): Filtrar por dificultad específica
            limite (int): Número máximo de registros
            
        Returns:
            list: Lista de mejores tiempos
        """
        try:
            if dificultad:
                self.cursor.execute('''
                    SELECT u.nombre, p.tiempo_jugado, p.puntuacion, p.dificultad, p.fecha_fin
                    FROM partidas p
                    JOIN usuarios u ON p.usuario_id = u.id
                    WHERE p.completado = 1 AND p.dificultad = ?
                    ORDER BY p.tiempo_jugado ASC
                    LIMIT ?
                ''', (dificultad, limite))
            else:
                self.cursor.execute('''
                    SELECT u.nombre, p.tiempo_jugado, p.puntuacion, p.dificultad, p.fecha_fin
                    FROM partidas p
                    JOIN usuarios u ON p.usuario_id = u.id
                    WHERE p.completado = 1
                    ORDER BY p.tiempo_jugado ASC
                    LIMIT ?
                ''', (limite,))
            
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener mejores tiempos: {e}")
            return []
    
    def obtener_partidas_guardadas(self, usuario_id):
        """
        Obtiene las partidas guardadas (no completadas) de un usuario
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            list: Lista de partidas guardadas
        """
        try:
            self.cursor.execute('''
                SELECT id, dificultad, fecha_inicio, tiempo_jugado,
                       tablero_inicial, tablero_actual, tablero_solucion
                FROM partidas
                WHERE usuario_id = ? AND completado = 0
                ORDER BY fecha_inicio DESC
            ''', (usuario_id,))
            
            partidas = []
            for row in self.cursor.fetchall():
                partida = {
                    'id': row[0],
                    'dificultad': row[1],
                    'fecha_inicio': row[2],
                    'tiempo_jugado': row[3],
                    'tablero_inicial': json.loads(row[4]),
                    'tablero_actual': json.loads(row[5]),
                    'tablero_solucion': json.loads(row[6])
                }
                partidas.append(partida)
            
            return partidas
        except sqlite3.Error as e:
            print(f"Error al obtener partidas guardadas: {e}")
            return []
    
    def actualizar_mejor_tiempo(self, usuario_id, tiempo):
        """
        Actualiza el mejor tiempo de un usuario si es mejor que el actual
        
        Args:
            usuario_id (int): ID del usuario
            tiempo (int): Tiempo en segundos
        """
        try:
            # Obtener el mejor tiempo actual
            self.cursor.execute('''
                SELECT mejor_tiempo FROM usuarios WHERE id = ?
            ''', (usuario_id,))
            
            resultado = self.cursor.fetchone()
            if resultado:
                mejor_tiempo_actual = resultado[0]
                
                # Si es el primer tiempo o es mejor que el actual
                if mejor_tiempo_actual == 0 or tiempo < mejor_tiempo_actual:
                    self.cursor.execute('''
                        UPDATE usuarios SET mejor_tiempo = ? WHERE id = ?
                    ''', (tiempo, usuario_id))
                    
                    self.connection.commit()
                    print(f"Nuevo mejor tiempo actualizado: {tiempo} segundos")
                    return True
            
            return False
        except sqlite3.Error as e:
            print(f"Error al actualizar mejor tiempo: {e}")
            return False
    
    def obtener_estadisticas_completas(self, usuario_id):
        """
        Obtiene estadísticas completas de un usuario
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            dict: Estadísticas completas del usuario
        """
        try:
            # Estadísticas básicas del usuario
            self.cursor.execute('''
                SELECT nombre, fecha_registro, juegos_jugados, juegos_completados,
                       mejor_tiempo, puntuacion_total
                FROM usuarios WHERE id = ?
            ''', (usuario_id,))
            
            user_stats = self.cursor.fetchone()
            if not user_stats:
                return None
            
            # Estadísticas por dificultad
            self.cursor.execute('''
                SELECT dificultad, COUNT(*) as total, 
                       SUM(CASE WHEN completado = 1 THEN 1 ELSE 0 END) as completados,
                       AVG(CASE WHEN completado = 1 THEN tiempo_jugado ELSE NULL END) as tiempo_promedio,
                       MIN(CASE WHEN completado = 1 THEN tiempo_jugado ELSE NULL END) as mejor_tiempo_dif
                FROM partidas 
                WHERE usuario_id = ?
                GROUP BY dificultad
            ''', (usuario_id,))
            
            stats_por_dificultad = {}
            for row in self.cursor.fetchall():
                stats_por_dificultad[row[0]] = {
                    'total': row[1],
                    'completados': row[2],
                    'tiempo_promedio': row[3] or 0,
                    'mejor_tiempo': row[4] or 0
                }
            
            return {
                'nombre': user_stats[0],
                'fecha_registro': user_stats[1],
                'juegos_jugados': user_stats[2],
                'juegos_completados': user_stats[3],
                'mejor_tiempo': user_stats[4],
                'puntuacion_total': user_stats[5],
                'por_dificultad': stats_por_dificultad
            }
            
        except sqlite3.Error as e:
            print(f"Error al obtener estadísticas completas: {e}")
            return None
    
    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos"""
        try:
            if self.connection:
                self.connection.close()
                print("Conexión a la base de datos cerrada")
        except sqlite3.Error as e:
            print(f"Error al cerrar conexión: {e}")
    
    def __del__(self):
        """Destructor que asegura el cierre de la conexión"""
        self.cerrar_conexion()


# Función de prueba para demostrar el funcionamiento
def test_database():
    """Función de prueba para la base de datos"""
    db = SudokuDatabase()
    
    # Insertar usuario de prueba
    user_id = db.insertar_usuario("Jugador1")
    
    if user_id:
        # Crear tableros de ejemplo
        tablero_inicial = [[5,3,0,0,7,0,0,0,0] for _ in range(9)]
        tablero_actual = [[5,3,4,0,7,0,0,0,0] for _ in range(9)]
        tablero_solucion = [[5,3,4,6,7,8,9,1,2] for _ in range(9)]
        
        # Guardar partida
        partida_id = db.guardar_partida(user_id, tablero_inicial, 
                                       tablero_actual, tablero_solucion)
        
        # Actualizar partida
        if partida_id:
            db.actualizar_partida(partida_id, tablero_actual, 180, False, 100, 1)
        
        # Mostrar estadísticas
        stats = db.obtener_estadisticas_usuario(user_id)
        print(f"Estadísticas: {stats}")
    
    db.cerrar_conexion()


if __name__ == "__main__":
    test_database()