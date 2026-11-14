# servicio_seguridad.py
import hashlib
import re
from datetime import datetime


class ServicioSeguridad:

    __PERMISOS = {
        "AdministradorRRHH": ["gestionar_empleados", "gestionar_departamentos", "generar_reportes", "ver_tiempos", "auditar"],
        "Analista": ["generar_reportes", "ver_tiempos", "consultar_tiempos"],
        "Tecnico": ["consultar_proyectos", "registrar_horas"],
        "Empleado": ["registrar_horas", "consultar_proyectos"],
        "Admin": ["*"]
    }

    @staticmethod
    def cifrar_dato(dato: str) -> str:
        if dato is None:
            return ""
        return hashlib.sha256(str(dato).encode("utf-8")).hexdigest()
    cifrarDato = cifrar_dato

    @staticmethod
    def autenticar(correo: str, contrasena: str, hash_almacenado: str) -> bool:
      
        if not correo or not contrasena or not hash_almacenado:
            return False
        
        hash_calculado = ServicioSeguridad.cifrar_dato(contrasena)
        return hash_calculado == hash_almacenado

    @staticmethod
    def autorizar(rol: str, accion: str) -> bool:
        if not rol or not accion:
            return False
        
        permisos_rol = ServicioSeguridad.__PERMISOS.get(rol, [])
        if "*" in permisos_rol:
            return True
        
        return accion.lower() in [p.lower() for p in permisos_rol]

    @staticmethod
    def validar_entrada(dato: any, tipo_esperado: str) -> bool:
        if dato is None:
            return False

        tipo = tipo_esperado.lower().strip()

        if tipo in ("email", "correo"):
            patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            return bool(re.match(patron, str(dato).strip()))

        elif tipo in ("int", "entero"):
            try:
                int(dato)
                return True
            except (ValueError, TypeError):
                return False

        elif tipo in ("decimal", "float", "numero"):
            try:
                val = float(dato)
                return val >= 0
            except (ValueError, TypeError):
                return False

        elif tipo in ("date", "fecha"):
            try:
                datetime.strptime(str(dato).strip(), "%Y-%m-%d")
                return True
            except ValueError:
                return False

        elif tipo in ("string", "texto"):
            return isinstance(dato, str) and len(dato.strip()) > 0

        elif tipo in ("bool", "booleano"):
            return isinstance(dato, bool) or str(dato).lower() in ("true", "false", "1", "0")

        return True

    validarEntrada = validar_entrada
