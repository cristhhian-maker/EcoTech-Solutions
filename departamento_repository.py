# departamento_repository.py
from conexion import Conexion
from departamento import Departamento


class DepartamentoRepository:
    """
    Repositorio responsable de la persistencia de Departamentos en MySQL.
    """

    def guardar(self, depto: Departamento) -> bool:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            sql = "INSERT INTO departamentos (nombre, gerente_id) VALUES (%s, %s)"
            cursor.execute(sql, (depto.nombre, depto.gerente_id))
            conexion.commit()
            depto.id = cursor.lastrowid
            print(f"[OK] Departamento '{depto.nombre}' guardado con ID {depto.id}.")
            return True
        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return False
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"[ERROR AL GUARDAR DEPARTAMENTO] {e}")
            return False
        finally:
            if conexion:
                conexion.close()

    def listar(self) -> list:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, gerente_id FROM departamentos")
            return cursor.fetchall()
        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return []
        except Exception as e:
            print(f"[ERROR AL LISTAR DEPARTAMENTOS] {e}")
            return []
        finally:
            if conexion:
                conexion.close()

    def eliminar(self, id_departamento: int) -> bool:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM departamentos WHERE id = %s", (id_departamento,))
            conexion.commit()
            if cursor.rowcount == 0:
                print(f"[AVISO] No se encontró departamento con ID {id_departamento}.")
                return False
            print(f"[OK] Departamento ID {id_departamento} eliminado correctamente.")
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"[ERROR AL ELIMINAR DEPARTAMENTO] {e}")
            return False
        finally:
            if conexion:
                conexion.close()
