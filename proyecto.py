# proyecto.py
from datetime import date, datetime


class Proyecto:


    def __init__(self, nombre: str, descripcion: str, fecha_inicio: date | str, id_proyecto: int | None = None):
        self.id = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.__empleados_asignados = set()

    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, valor: int | None):
        self.__id = valor

  
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del proyecto no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str):
        self.__descripcion = str(valor).strip() if valor else ""

    @property
    def fecha_inicio(self) -> date:
        return self.__fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, valor: date | str):
        if isinstance(valor, str):
            try:
                self.__fecha_inicio = datetime.strptime(valor.strip(), "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"Formato de fecha inválido '{valor}'. Use YYYY-MM-DD.")
        elif isinstance(valor, datetime):
            self.__fecha_inicio = valor.date()
        elif isinstance(valor, date):
            self.__fecha_inicio = valor
        else:
            self.__fecha_inicio = date.today()

    @property
    def fechaInicio(self) -> date:
        return self.__fecha_inicio

    @property
    def empleados_asignados(self) -> list[int]:
        return sorted(list(self.__empleados_asignados))

    def asignar_empleado(self, empleado_id: int) -> None:
    
        try:
            emp_id = int(empleado_id)
            if emp_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError(f"ID de empleado inválido: {empleado_id}")

        self.__empleados_asignados.add(emp_id)
        print(f"[OK] Empleado ID {emp_id} asignado al proyecto '{self.nombre}' (ID: {self.id}).")

    asignarEmpleado = asignar_empleado

    def __str__(self) -> str:
        return f"ID: {self.id} | Proyecto: {self.nombre} | Inicio: {self.fecha_inicio} | Desc: {self.descripcion}"
