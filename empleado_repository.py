# empleado_repository.py
from conexion import Conexion
from empleado import Empleado


class EmpleadoRepository:
    """
    Repositorio responsable de la persistencia de objetos Empleado en la BD.

    Operaciones disponibles: guardar, listar, eliminar, actualizar.

    Principios OOP aplicados:
    - Responsabilidad única (SRP): solo maneja operaciones CRUD de empleados
    - Encapsulamiento: el manejo de conexiones es interno a cada método
    - Manejo de excepciones: captura errores de BD y los reporta claramente
    """

    def guardar(self, empleado: Empleado) -> bool:
        """
        Persiste un objeto Empleado en la base de datos.
        Soporta los nuevos campos del UML (direccion, telefono, fecha_inicio_contrato, etc.)
        con compatibilidad hacia atrás en caso de esquemas previos.
        """
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor   = conexion.cursor()

            # Intento de inserción con esquema completo del UML
            try:
                # 1. Asegurar o crear usuario base si la tabla usuarios existe
                cursor.execute("""
                    INSERT INTO usuarios (nombre, correo, contrasena_hash, activo, rol)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)
                """, (
                    empleado.nombre,
                    empleado.correo,
                    empleado.contrasena_hash,
                    empleado.activo,
                    empleado.puesto
                ))
                usuario_id = cursor.lastrowid

                sql_completo = """
                    INSERT INTO empleados (usuario_id, nombre, correo, direccion, telefono, 
                                          fecha_inicio_contrato, salario, departamento_id, puesto, codigo_interno)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_completo, (
                    usuario_id,
                    empleado.nombre,
                    empleado.correo,
                    empleado.direccion,
                    empleado.telefono,
                    empleado.fecha_inicio_contrato,
                    float(empleado.salario),
                    empleado.departamento_id,
                    empleado.puesto,
                    empleado.get_codigo_interno()
                ))
            except Exception:
                # Fallback al esquema simple si la tabla no fue migrada aún
                sql_simple = """
                    INSERT INTO empleados (nombre, correo, puesto, salario, codigo_interno)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql_simple, (
                    empleado.nombre,
                    empleado.correo,
                    empleado.puesto,
                    float(empleado.salario),
                    empleado.get_codigo_interno()
                ))

            conexion.commit()
            empleado.id = cursor.lastrowid
            print(f"[OK] Empleado '{empleado.nombre}' guardado correctamente.")
            return True

        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return False

        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"[ERROR AL GUARDAR] No se pudo registrar el empleado: {e}")
            return False

        finally:
            if conexion:
                conexion.close()

    def listar(self) -> list:
        """
        Recupera todos los empleados registrados en la base de datos.
        """
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor   = conexion.cursor()

            cursor.execute("SELECT * FROM empleados")
            empleados = cursor.fetchall()
            return empleados

        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return []

        except Exception as e:
            print(f"[ERROR AL LISTAR] No se pudieron recuperar los empleados: {e}")
            return []

        finally:
            if conexion:
                conexion.close()

    def eliminar(self, id_empleado: int) -> bool:
        """
        Elimina un empleado de la base de datos según su ID.
        """
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor   = conexion.cursor()

            # Compatible con nombre de columna id o id_empleado
            try:
                sql = "DELETE FROM empleados WHERE id = %s"
                cursor.execute(sql, (id_empleado,))
            except Exception:
                sql = "DELETE FROM empleados WHERE id_empleado = %s"
                cursor.execute(sql, (id_empleado,))

            conexion.commit()

            if cursor.rowcount == 0:
                print(f"[AVISO] No se encontró ningún empleado con ID {id_empleado}.")
                return False

            print(f"[OK] Empleado con ID {id_empleado} eliminado correctamente.")
            return True

        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return False

        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"[ERROR AL ELIMINAR] {e}")
            return False

        finally:
            if conexion:
                conexion.close()

    def actualizar(self, id_empleado: int, nombre: str, correo: str, puesto: str, salario: float) -> bool:
        """
        Actualiza los datos de un empleado existente en la base de datos.
        """
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor   = conexion.cursor()

            try:
                sql = """
                    UPDATE empleados
                    SET nombre = %s, correo = %s, puesto = %s, salario = %s
                    WHERE id = %s
                """
                cursor.execute(sql, (nombre, correo, puesto, salario, id_empleado))
            except Exception:
                sql = """
                    UPDATE empleados
                    SET nombre = %s, correo = %s, puesto = %s, salario = %s
                    WHERE id_empleado = %s
                """
                cursor.execute(sql, (nombre, correo, puesto, salario, id_empleado))

            conexion.commit()

            if cursor.rowcount == 0:
                print(f"[AVISO] No se encontró ningún empleado con ID {id_empleado}.")
                return False

            print(f"[OK] Empleado con ID {id_empleado} actualizado correctamente.")
            return True

        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return False

        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"[ERROR AL ACTUALIZAR] {e}")
            return False

        finally:
            if conexion:
                conexion.close()
