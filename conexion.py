# conexion.py
import pymysql
from pymysql.connections import Connection


class Conexion:
    """
    Clase utilitaria para gestionar la conexión a la base de datos MySQL.

    Usa @staticmethod porque no necesita estado de instancia:
    su única responsabilidad es entregar una conexión configurada.

    Principios aplicados:
    - Responsabilidad única (SRP): solo maneja la conexión
    - Encapsulamiento: los parámetros de conexión están centralizados aquí
    - Manejo de excepciones: captura errores propios de pymysql
    """

    # Parámetros de conexión centralizados como constantes de clase
    __HOST     = "localhost"
    __USUARIO  = "root"
    __PASSWORD = ""
    __BASE     = "EcoTech"

    @staticmethod
    def conectar() -> Connection:
        """
        Establece y retorna una conexión a la base de datos.

        Returns:
            Connection: objeto de conexión activa a MySQL.

        Raises:
            ConnectionError: si no se puede establecer la conexión.
        """
        try:
            conexion = pymysql.connect(
                host     = Conexion.__HOST,
                user     = Conexion.__USUARIO,
                password = Conexion.__PASSWORD,
                database = Conexion.__BASE
            )
            return conexion

        except pymysql.err.OperationalError as e:
            # Error de red, credenciales incorrectas o servidor caído
            raise ConnectionError(
                f"No se pudo conectar a la base de datos '{Conexion.__BASE}'. "
                f"Verifique que MySQL esté activo y las credenciales sean correctas.\n"
                f"Detalle técnico: {e}"
            )