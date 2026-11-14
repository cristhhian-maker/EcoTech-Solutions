# registro_tiempo.py
from datetime import date, datetime
from decimal import Decimal
from servicio_seguridad import ServicioSeguridad


class RegistroTiempo:
    def __init__(self, empleado_id: int, proyecto_id: int, fecha: date | str, 
                 horas: float | Decimal, descripcion: str = "", id_registro: int | None = None):
        self.id = id_registro
        self.empleado_id = empleado_id
        self.proyecto_id = proyecto_id
        self.fecha = fecha
        self.horas = horas
        self.descripcion = descripcion

    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, valor: int | None):
        self.__id = valor

   
    @property
    def empleado_id(self) -> int:
        return self.__empleado_id

    @empleado_id.setter
    def empleado_id(self, valor: int):
        if not ServicioSeguridad.validar_entrada(valor, "int") or int(valor) <= 0:
            raise ValueError("empleadoId debe ser un ID entero positivo.")
        self.__empleado_id = int(valor)

    @property
    def empleadoId(self) -> int:
        return self.__empleado_id

    @property
    def proyecto_id(self) -> int:
        return self.__proyecto_id

    @proyecto_id.setter
    def proyecto_id(self, valor: int):
        if not ServicioSeguridad.validar_entrada(valor, "int") or int(valor) <= 0:
            raise ValueError("proyectoId debe ser un ID entero positivo.")
        self.__proyecto_id = int(valor)

    @property
    def proyectoId(self) -> int:
        return self.__proyecto_id

    @property
    def fecha(self) -> date:
        return self.__fecha

    @fecha.setter
    def fecha(self, valor: date | str):
        if isinstance(valor, str):
            if not ServicioSeguridad.validar_entrada(valor, "date"):
                raise ValueError(f"Formato de fecha inválido '{valor}'. Use YYYY-MM-DD.")
            self.__fecha = datetime.strptime(valor.strip(), "%Y-%m-%d").date()
        elif isinstance(valor, datetime):
            self.__fecha = valor.date()
        elif isinstance(valor, date):
            self.__fecha = valor
        else:
            self.__fecha = date.today()

    @property
    def horas(self) -> Decimal:
        return self.__horas

    @horas.setter
    def horas(self, valor: float | Decimal | int | str):
        if not ServicioSeguridad.validar_entrada(valor, "decimal"):
            raise ValueError(f"Las horas deben ser un número positivo válido: '{valor}'")
        num = Decimal(str(valor))
        if num <= 0 or num > 24:
            raise ValueError("Las horas registradas deben ser mayores a 0 y como máximo 24 por registro.")
        self.__horas = round(num, 2)

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str):
        self.__descripcion = str(valor).strip() if valor else ""

    def validar(self) -> bool:
        try:
            valido_emp = ServicioSeguridad.validar_entrada(self.empleado_id, "int") and self.empleado_id > 0
            valido_proy = ServicioSeguridad.validar_entrada(self.proyecto_id, "int") and self.proyecto_id > 0
            valido_horas = 0 < self.horas <= 24
            return bool(valido_emp and valido_proy and valido_horas)
        except Exception:
            return False

    def registrar(self) -> None:
        if not self.validar():
            raise ValueError("No se puede registrar: los datos de tiempo no son válidos.")
        print(f"[OK] Horas registradas: {self.horas}h para Empleado {self.empleado_id} en Proyecto {self.proyecto_id} ({self.fecha}).")

    def __str__(self) -> str:
        return f"ID: {self.id} | Fecha: {self.fecha} | Horas: {self.horas} | Emp: {self.empleado_id} | Proy: {self.proyecto_id} | Desc: {self.descripcion}"
