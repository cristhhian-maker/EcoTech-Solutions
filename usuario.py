from abc import ABC
from persona import Persona
from servicio_seguridad import ServicioSeguridad


class Usuario(Persona, ABC):
    """
    Clase que representa a un Usuario en el sistema.
    Hereda de Persona (nombre, correo) y agrega atributos de seguridad y sesión.

    Atributos UML:
    - id: int
    - nombre: String (heredado)
    - correo: String (heredado)
    - contrasenaHash: String
    - activo: bool

    Métodos UML:
    + iniciarSesion(): Boolean
    + cerrarSesion(): void
    """

    def __init__(self, nombre: str, correo: str, contrasena: str, 
                 activo: bool = True, id_usuario: int | None = None, es_hash: bool = False):
        super().__init__(nombre, correo)
        
        self.id = id_usuario
        self.activo = activo
        self.__sesion_activa = False

        if es_hash:
            self.__contrasena_hash = contrasena
        else:
            self.establecer_contrasena(contrasena)

    # --- Propiedad: id ---
    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, valor: int | None):
        if valor is not None and not isinstance(valor, int):
            raise ValueError("El id debe ser un entero.")
        self.__id = valor

    # --- Propiedad: contrasenaHash / contrasena_hash ---
    @property
    def contrasena_hash(self) -> str:
        return self.__contrasena_hash

    @property
    def contrasenaHash(self) -> str:
        return self.__contrasena_hash

    def establecer_contrasena(self, contrasena_plana: str):
        if not isinstance(contrasena_plana, str) or len(contrasena_plana.strip()) < 4:
            raise ValueError("La contraseña debe tener al menos 4 caracteres.")
        self.__contrasena_hash = ServicioSeguridad.cifrar_dato(contrasena_plana.strip())

    @property
    def activo(self) -> bool:
        return self.__activo

    @activo.setter
    def activo(self, valor: bool):
        self.__activo = bool(valor)

    @property
    def sesion_activa(self) -> bool:
        return self.__sesion_activa

    def iniciar_sesion(self, contrasena: str) -> bool:
       
        if not self.activo:
            print(f"[ACCESO DENEGADO] El usuario '{self.correo}' está inactivo.")
            return False

        if ServicioSeguridad.autenticar(self.correo, contrasena, self.__contrasena_hash):
            self.__sesion_activa = True
            print(f"[OK] Sesión iniciada con éxito para '{self.nombre}'.")
            return True
        else:
            print(f"[ACCESO DENEGADO] Contraseña incorrecta para '{self.correo}'.")
            return False

    iniciarSesion = iniciar_sesion

    def cerrar_sesion(self) -> None:
        self.__sesion_activa = False
        print(f"[OK] Sesión finalizada para '{self.nombre}'.")

    cerrarSesion = cerrar_sesion

    def mostrar_datos(self) -> str:
        estado = "Activo" if self.activo else "Inactivo"
        sesion = "En línea" if self.__sesion_activa else "Desconectado"
        return f"ID: {self.id} | {super().mostrar_datos_basicos()} | Estado: {estado} | Sesión: {sesion}"
