# usuario_repository.py
from conexion import Conexion
from usuario import Usuario


class UsuarioRepository:
    def guardar(self, usuario: Usuario, rol: str = "Empleado") -> bool:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()

            sql = """
                INSERT INTO usuarios (nombre, correo, contrasena_hash, activo, rol)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                usuario.nombre,
                usuario.correo,
                usuario.contrasena_hash,
                usuario.activo,
                rol
            ))
            conexion.commit()
            usuario.id = cursor.lastrowid
            print(f"[OK] Usuario '{usuario.nombre}' guardado con ID {usuario.id}.")
            return True

        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return False
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"[ERROR AL GUARDAR USUARIO] {e}")
            return False
        finally:
            if conexion:
                conexion.close()

    def listar(self) -> list:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, correo, activo, rol FROM usuarios")
            return cursor.fetchall()
        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return []
        except Exception as e:
            print(f"[ERROR AL LISTAR USUARIOS] {e}")
            return []
        finally:
            if conexion:
                conexion.close()

    def buscar_por_correo(self, correo: str) -> dict | None:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            sql = "SELECT id, nombre, correo, contrasena_hash, activo, rol FROM usuarios WHERE correo = %s"
            cursor.execute(sql, (correo.strip().lower(),))
            fila = cursor.fetchone()
            if fila:
                return {
                    "id": fila[0],
                    "nombre": fila[1],
                    "correo": fila[2],
                    "contrasena_hash": fila[3],
                    "activo": bool(fila[4]),
                    "rol": fila[5]
                }
            return None
        except Exception as e:
            print(f"[ERROR AL BUSCAR USUARIO] {e}")
            return None
        finally:
            if conexion:
                conexion.close()

    def eliminar(self, id_usuario: int) -> bool:
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
            conexion.commit()
            if cursor.rowcount == 0:
                print(f"[AVISO] No se encontró usuario con ID {id_usuario}.")
                return False
            print(f"[OK] Usuario ID {id_usuario} eliminado correctamente.")
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"[ERROR AL ELIMINAR USUARIO] {e}")
            return False
        finally:
            if conexion:
                conexion.close()
