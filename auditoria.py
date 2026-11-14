# auditoria.py
from datetime import datetime


class Auditoria:
    """
    Clase que representa un registro de auditoría en el sistema.
    Asociada a Usuario (1 Usuario -> 1..* Auditoria).

    Atributos UML:
    - id: int
    - usuarioId: int
    - accion: String
    - fecha: DateTime
    - detalle: String

    Métodos UML:
    + registrarEvento(): void
    """

    def __init__(self, usuario_id: int, accion: str, detalle: str = "", 
                 fecha: datetime | None = None, id_auditoria: int | None = None):
        self.id = id_auditoria
        self.usuario_id = usuario_id
        self.accion = accion
        self.detalle = detalle
        self.fecha = fecha if fecha else datetime.now()

    # --- Propiedad: id ---
    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, valor: int | None):
        self.__id = valor

    # --- Propiedad: usuarioId / usuario_id ---
    @property
    def usuario_id(self) -> int:
        return self.__usuario_id

    @usuario_id.setter
    def usuario_id(self, valor: int):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("El usuarioId debe ser un entero positivo.")
        self.__usuario_id = valor

    @property
    def usuarioId(self) -> int:
        return self.__usuario_id

    # --- Propiedad: accion ---
    @property
    def accion(self) -> str:
        return self.__accion

    @accion.setter
    def accion(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La acción no puede estar vacía.")
        self.__accion = valor.strip()

    # --- Propiedad: fecha ---
    @property
    def fecha(self) -> datetime:
        return self.__fecha

    @fecha.setter
    def fecha(self, valor: datetime | str):
        if isinstance(valor, str):
            try:
                self.__fecha = datetime.fromisoformat(valor)
            except ValueError:
                self.__fecha = datetime.strptime(valor, "%Y-%m-%d %H:%M:%S")
        elif isinstance(valor, datetime):
            self.__fecha = valor
        else:
            self.__fecha = datetime.now()

    # --- Propiedad: detalle ---
    @property
    def detalle(self) -> str:
        return self.__detalle

    @detalle.setter
    def detalle(self, valor: str):
        self.__detalle = str(valor) if valor is not None else ""

    # --- Métodos del diagrama UML ---
    def registrar_evento(self) -> None:
        """
        Registra/muestra el evento de auditoría en consola o log.
        Corresponde a registrarEvento(): void en el diagrama UML.
        """
        fecha_str = self.fecha.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[AUDITORÍA {fecha_str}] Usuario ID {self.usuario_id} | Acción: {self.accion} | Detalle: {self.detalle}")

    # Alias según el diagrama UML
    registrarEvento = registrar_evento

    def __str__(self) -> str:
        return f"[{self.fecha.strftime('%Y-%m-%d %H:%M:%S')}] Usuario: {self.usuario_id} | {self.accion} | {self.detalle}"
