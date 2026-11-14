# proyecto_repository.py
from conexion import Conexion
from proyecto import Proyecto


class ProyectoRepository:
    def guardar(self, proyecto: Proyecto) -> bool:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            sql = "INSERT INTO proyectos (nombre, descripcion, fecha_inicio) VALUES (%s, %s, %s)"
            cursor.execute(sql, (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio))
            conexion.commit()
            proyecto.id = cursor.lastrowid
            print(f"[OK] Proyecto '{proyecto.nombre}' guardado con ID {proyecto.id}.")
            return True
        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return False
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"[ERROR AL GUARDAR PROYECTO] {e}")
            return False
        finally:
            if conexion:
                conexion.close()

    def listar(self) -> list:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, descripcion, fecha_inicio FROM proyectos")
            return cursor.fetchall()
        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return []
        except Exception as e:
            print(f"[ERROR AL LISTAR PROYECTOS] {e}")
            return []
        finally:
            if conexion:
                conexion.close()

    def asignar_empleado(self, empleado_id: int, proyecto_id: int) -> bool:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            sql = "INSERT IGNORE INTO empleado_proyecto (empleado_id, proyecto_id) VALUES (%s, %s)"
            cursor.execute(sql, (empleado_id, proyecto_id))
            conexion.commit()
            print(f"[OK] Empleado {empleado_id} asignado a Proyecto {proyecto_id} en BD.")
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"[ERROR AL ASIGNAR EMPLEADO] {e}")
            return False
        finally:
            if conexion:
                conexion.close()

    def eliminar(self, id_proyecto: int) -> bool:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM proyectos WHERE id = %s", (id_proyecto,))
            conexion.commit()
            if cursor.rowcount == 0:
                print(f"[AVISO] No se encontró proyecto con ID {id_proyecto}.")
                return False
            print(f"[OK] Proyecto ID {id_proyecto} eliminado correctamente.")
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"[ERROR AL ELIMINAR PROYECTO] {e}")
            return False
        finally:
            if conexion:
                conexion.close()
