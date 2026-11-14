# auditoria_repository.py
from conexion import Conexion
from auditoria import Auditoria


class AuditoriaRepository:
    """
    Repositorio responsable de la persistencia de Auditoria en MySQL.
    """

    def guardar(self, auditoria: Auditoria) -> bool:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            sql = """
                INSERT INTO auditorias (usuario_id, accion, fecha, detalle)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (
                auditoria.usuario_id,
                auditoria.accion,
                auditoria.fecha,
                auditoria.detalle
            ))
            conexion.commit()
            auditoria.id = cursor.lastrowid
            return True
        except ConnectionError as e:
            # En auditoría no mostramos error fatal para no interrumpir el flujo si la BD no responde
            return False
        except Exception as e:
            if conexion:
                conexion.rollback()
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
                SELECT id, usuario_id, accion, fecha, detalle 
                FROM auditorias 
                ORDER BY fecha DESC
            """)
            return cursor.fetchall()
        except Exception:
            return []
        finally:
            if conexion:
                conexion.close()
