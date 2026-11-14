# empleado.py
from datetime import date, datetime
from decimal import Decimal
from usuario import Usuario
from registro_tiempo import RegistroTiempo


class Empleado(Usuario):
    def __init__(self, nombre: str, correo: str, 
                 direccion: str = "Sin dirección", 
                 telefono: str = "000-0000", 
                 fecha_inicio_contrato: date | str | None = None, 
                 salario: float | Decimal = 1000.0,
                 puesto: str = "Empleado",
                 departamento_id: int | None = None,
                 contrasena: str = "123456",
                 activo: bool = True,
                 id_empleado: int | None = None):

        super().__init__(nombre=nombre, correo=correo, contrasena=contrasena, 
                         activo=activo, id_usuario=id_empleado)

        self.direccion = direccion
        self.telefono = telefono
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.salario = salario
        self.puesto = puesto
        self.departamento_id = departamento_id
        self.__codigo_interno = self.__generar_codigo()

    @property
    def direccion(self) -> str:
        return self.__direccion

    @direccion.setter
    def direccion(self, valor: str):
        self.__direccion = str(valor).strip() if valor else "Sin dirección"

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        val = str(valor).strip()
        if not val:
            self.__telefono = "000-0000"
        else:
            self.__telefono = val
    @property
    def fecha_inicio_contrato(self) -> date:
        return self.__fecha_inicio_contrato

    @fecha_inicio_contrato.setter
    def fecha_inicio_contrato(self, valor: date | str | None):
        if valor is None:
            self.__fecha_inicio_contrato = date.today()
        elif isinstance(valor, str):
            try:
                self.__fecha_inicio_contrato = datetime.strptime(valor.strip(), "%Y-%m-%d").date()
            except ValueError:
                self.__fecha_inicio_contrato = date.today()
        elif isinstance(valor, datetime):
            self.__fecha_inicio_contrato = valor.date()
        elif isinstance(valor, date):
            self.__fecha_inicio_contrato = valor
        else:
            self.__fecha_inicio_contrato = date.today()

    @property
    def fechaInicioContrato(self) -> date:
        return self.__fecha_inicio_contrato

    @property
    def salario(self) -> Decimal:
        return self.__salario

    @salario.setter
    def salario(self, valor: float | int | Decimal | str):
        try:
            val_num = Decimal(str(valor))
        except Exception:
            raise ValueError(f"El salario '{valor}' debe ser un valor numérico válido.")

        if val_num <= 0:
            raise ValueError("El salario debe ser mayor a 0.")
        self.__salario = round(val_num, 2)

    @property
    def puesto(self) -> str:
        return self.__puesto

    @puesto.setter
    def puesto(self, valor: str):
        self.__puesto = str(valor).strip() if valor else "Empleado"

    @property
    def departamento_id(self) -> int | None:
        return self.__departamento_id

    @departamento_id.setter
    def departamento_id(self, valor: int | None):
        self.__departamento_id = int(valor) if valor is not None else None

    def __generar_codigo(self) -> str:
        prefijo = self.nombre[:3].upper() if self.nombre else "EMP"
        return f"EMP-{prefijo}"

    def get_codigo_interno(self) -> str:
        return self.__codigo_interno

    def registrar_horas(self, proyecto_id: int, horas: float | Decimal, 
                        fecha: str | date | None = None, descripcion: str = "") -> RegistroTiempo:
       
        emp_id = self.id if self.id else 1
        fecha_reg = fecha if fecha else date.today()
        registro = RegistroTiempo(
            empleado_id=emp_id,
            proyecto_id=proyecto_id,
            fecha=fecha_reg,
            horas=horas,
            descripcion=descripcion
        )
        registro.registrar()
        return registro

    registrarHoras = registrar_horas

    def mostrar_datos(self) -> str:
        return (f"ID: {self.id} | {self.nombre} | {self.correo} | Tel: {self.telefono} | "
                f"Puesto: {self.puesto} | Salario: ${self.salario:,.2f} | Contrato: {self.fecha_inicio_contrato}")


# =====================================================================
#             ROLES / SUBCLASES ESPECIALIZADAS DEL UML
# =====================================================================

class AdministradorRRHH(Empleado):
    def __init__(self, nombre: str, correo: str, **kwargs):
        kwargs.setdefault("puesto", "Administrador RRHH")
        super().__init__(nombre=nombre, correo=correo, **kwargs)

    def gestionar_empleados(self) -> None:
        print(f"[OK] [RRHH - {self.nombre}] Accediendo a la gestión integral de empleados.")

    gestionarEmpleados = gestionar_empleados

    def gestionar_departamentos(self) -> None:
        print(f"[OK] [RRHH - {self.nombre}] Accediendo a la gestión de departamentos.")

    gestionarDepartamentos = gestionar_departamentos

    def generar_reportes(self) -> None:
        print(f"[OK] [RRHH - {self.nombre}] Generando reportes de recursos humanos y personal.")
    generarReportes = generar_reportes


class Analista(Empleado):
    def __init__(self, nombre: str, correo: str, **kwargs):
        kwargs.setdefault("puesto", "Analista")
        super().__init__(nombre=nombre, correo=correo, **kwargs)

    def generar_reporte(self) -> None:
        
        print(f"[OK] [Analista - {self.nombre}] Generando reporte analítico de rendimiento y métricas.")

    generarReporte = generar_reporte

    def consultar_tiempos(self) -> None:
        print(f"[OK] [Analista - {self.nombre}] Consultando registros de tiempo y horas cargadas.")

    consultarTiempos = consultar_tiempos


class Tecnico(Empleado):
    def __init__(self, nombre: str, correo: str, **kwargs):
        kwargs.setdefault("puesto", "Técnico")
        super().__init__(nombre=nombre, correo=correo, **kwargs)

    def consultar_proyectos(self) -> None:
        print(f"[OK] [Técnico - {self.nombre}] Consultando proyectos asignados.")

    consultarProyectos = consultar_proyectos
