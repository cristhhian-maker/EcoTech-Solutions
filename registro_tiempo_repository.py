# registro_tiempo_repository.py
from conexion import Conexion
from registro_tiempo import RegistroTiempo


class RegistroTiempoRepository:
   
    def guardar(self, registro: RegistroTiempo) -> bool:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            sql = """
                INSERT INTO registros_tiempo (fecha, horas, descripcion, empleado_id, proyecto_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                registro.fecha,
                float(registro.horas),
                registro.descripcion,
                registro.empleado_id,
                registro.proyecto_id
            ))
            conexion.commit()
            registro.id = cursor.lastrowid
            print(f"[OK] Registro de tiempo guardado con ID {registro.id}.")
            return True
        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return False
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"[ERROR AL GUARDAR REGISTRO DE TIEMPO] {e}")
            return False
        finally:
            if conexion:
                conexion.close()

    def listar(self) -> list:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id, fecha, horas, descripcion, empleado_id, proyecto_id 
                FROM registros_tiempo
                ORDER BY fecha DESC
            """)
            return cursor.fetchall()
        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return []
        except Exception as e:
            print(f"[ERROR AL LISTAR REGISTROS DE TIEMPO] {e}")
            return []
        finally:
            if conexion:
                conexion.close()

    def listar_por_empleado(self, empleado_id: int) -> list:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id, fecha, horas, descripcion, empleado_id, proyecto_id 
                FROM registros_tiempo 
                WHERE empleado_id = %s
                ORDER BY fecha DESC
            """, (empleado_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"[ERROR AL BUSCAR TIEMPOS] {e}")
            return []
        finally:
            if conexion:
                conexion.close()
