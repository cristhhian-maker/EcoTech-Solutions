# cliente_repository.py
from conexion import Conexion
from cliente import Cliente


class ClienteRepository:
    """
    Repositorio responsable de la persistencia de objetos Cliente en la BD.

    Operaciones disponibles: guardar, listar, eliminar, actualizar.

    Principios OOP aplicados:
    - Responsabilidad única (SRP): solo maneja operaciones CRUD de clientes
    - Encapsulamiento: el manejo de conexiones es interno a cada método
    - Manejo de excepciones: captura errores de BD y los reporta claramente
    """

    def guardar(self, cliente: Cliente) -> bool:
        """
        Persiste un objeto Cliente en la base de datos.

        Args:
            cliente: instancia de Cliente a guardar.

        Returns:
            True si se guardó correctamente, False en caso contrario.
        """
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor   = conexion.cursor()

            sql = """
                INSERT INTO clientes (nombre, correo, telefono, codigo_interno)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (
                cliente.nombre,
                cliente.correo,
                cliente.telefono,
                cliente.get_codigo_interno()
            ))

            conexion.commit()
            print(f"[OK] Cliente '{cliente.nombre}' guardado correctamente.")
            return True

        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return False

        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"[ERROR AL GUARDAR] No se pudo registrar el cliente: {e}")
            return False

        finally:
            if conexion:
                conexion.close()

    def listar(self) -> list:
        """
        Recupera todos los clientes registrados en la base de datos.

        Returns:
            Lista de tuplas (id_cliente, nombre, correo, telefono, codigo_interno),
            o lista vacía si ocurre un error.
        """
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor   = conexion.cursor()

            cursor.execute("SELECT * FROM clientes")
            clientes = cursor.fetchall()
            return clientes

        except ConnectionError as e:
            print(f"[ERROR DE CONEXIÓN] {e}")
            return []

        except Exception as e:
            print(f"[ERROR AL LISTAR] No se pudieron recuperar los clientes: {e}")
            return []

        finally:
            if conexion:
                conexion.close()

    def eliminar(self, id_cliente: int) -> bool:
        """
        Elimina un cliente de la base de datos según su ID.

        Args:
            id_cliente: identificador único del cliente a eliminar.

        Returns:
            True si se eliminó correctamente, False en caso contrario.
        """
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor   = conexion.cursor()

            sql = "DELETE FROM clientes WHERE id_cliente = %s"
            cursor.execute(sql, (id_cliente,))
            conexion.commit()

            if cursor.rowcount == 0:
                # rowcount == 0 significa que ninguna fila fue afectada
                print(f"[AVISO] No se encontró ningún cliente con ID {id_cliente}.")
                return False

            print(f"[OK] Cliente con ID {id_cliente} eliminado correctamente.")
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

    def actualizar(self, id_cliente: int, nombre: str, correo: str, telefono: str) -> bool:
        """
        Actualiza los datos de un cliente existente en la base de datos.

        Args:
            id_cliente: identificador único del cliente a actualizar.
            nombre:     nuevo nombre.
            correo:     nuevo correo.
            telefono:   nuevo teléfono.

        Returns:
            True si se actualizó correctamente, False en caso contrario.
        """
        conexion = None
        try:
            conexion = Conexion.conectar()
            cursor   = conexion.cursor()

            sql = """
                UPDATE clientes
                SET nombre = %s, correo = %s, telefono = %s
                WHERE id_cliente = %s
            """
            cursor.execute(sql, (nombre, correo, telefono, id_cliente))
            conexion.commit()

            if cursor.rowcount == 0:
                print(f"[AVISO] No se encontró ningún cliente con ID {id_cliente}.")
                return False

            print(f"[OK] Cliente con ID {id_cliente} actualizado correctamente.")
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