# reporte_repository.py
from datetime import datetime
from conexion import Conexion
from reporte import Reporte


class ReporteRepository:

    def guardar(self, reporte: Reporte) -> bool:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            sql = """
                INSERT INTO reportes (tipo, formato, fecha_creacion, contenido)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (
                reporte.tipo,
                reporte.formato,
                datetime.now(),
                reporte.contenido
            ))
            conexion.commit()
            reporte.id = cursor.lastrowid
            print(f"[OK] Reporte '{reporte.tipo}' guardado en BD con ID {reporte.id}.")
            return True
        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return False
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"[ERROR AL GUARDAR REPORTE] {e}")
            return False
        finally:
            if conexion:
                conexion.close()

    def listar(self) -> list:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, tipo, formato, fecha_creacion FROM reportes ORDER BY fecha_creacion DESC")
            return cursor.fetchall()
        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return []
        except Exception as e:
            print(f"[ERROR AL LISTAR REPORTES] {e}")
            return []
        finally:
            if conexion:
                conexion.close()
