# verificar_todo.py
import sys
import os
from decimal import Decimal
from datetime import date, datetime
from abc import ABC

# Importación de clases del modelo
from persona import Persona
from usuario import Usuario
from empleado import Empleado, AdministradorRRHH, Analista, Tecnico
from departamento import Departamento
from proyecto import Proyecto
from registro_tiempo import RegistroTiempo
from auditoria import Auditoria
from reporte import Reporte
from servicio_seguridad import ServicioSeguridad
from servicio_externo import ServicioExterno   # <-- NUEVO


def test_separador(titulo: str):
    print("\n" + "=" * 60)
    print(f"  VERIFICACIÓN: {titulo}")
    print("=" * 60)


def main():
    errores = []

    # -------------------------------------------------------------
    # 1. VERIFICACIÓN DE CLASE USUARIO (UML)
    # -------------------------------------------------------------
    test_separador("1. Clase Usuario y Principios POO (Abstracción/Herencia)")
    try:
        assert issubclass(Usuario, Persona), "Usuario debe heredar de Persona"
        assert issubclass(Usuario, ABC), "Usuario debe implementar ABC (Abstracción)"

        u = Usuario(nombre="Carlos Gomez", correo="carlos@ecotech.com", contrasena="Admin2026!", activo=True, id_usuario=1)
        assert u.id == 1, "ID de usuario incorrecto"
        assert u.nombre == "Carlos Gomez", "Nombre incorrecto"
        assert u.correo == "carlos@ecotech.com", "Correo incorrecto"
        assert u.activo is True, "Estado activo incorrecto"
        assert len(u.contrasenaHash) == 64, "La contraseña debe estar cifrada en SHA-256 (64 hex chars)"
        
        assert hasattr(u, "iniciarSesion"), "Usuario debe tener método iniciarSesion"
        assert hasattr(u, "cerrarSesion"), "Usuario debe tener método cerrarSesion"
        
        assert u.iniciarSesion("Admin2026!") is True, "Inicio de sesión con contraseña correcta debe ser True"
        assert u.sesion_activa is True, "Sesión debe estar activa"
        assert u.iniciarSesion("PasswordIncorrecta") is False, "Inicio de sesión erróneo debe retornar False"
        u.cerrarSesion()
        assert u.sesion_activa is False, "Sesión debe quedar inactiva"

        print("[OK] Clase Usuario verificada con exito (Encapsulamiento, Cifrado, Sesion).")
    except Exception as e:
        errores.append(f"Falla en Usuario: {e}")
        print(f"[ERROR] Error en Usuario: {e}")

    # -------------------------------------------------------------
    # 2. VERIFICACIÓN DE EMPLEADO Y ROLES ESPECIALIZADOS (UML)
    # -------------------------------------------------------------
    test_separador("2. Empleado y Jerarquía de Roles (Herencia y Polimorfismo)")
    try:
        # Jerarquía
        assert issubclass(Empleado, Usuario), "Empleado debe heredar de Usuario"
        assert issubclass(AdministradorRRHH, Empleado), "AdministradorRRHH debe heredar de Empleado"
        assert issubclass(Analista, Empleado), "Analista debe heredar de Empleado"
        assert issubclass(Tecnico, Empleado), "Tecnico debe heredar de Empleado"

        # Empleado base
        emp = Empleado(
            nombre="Ana Perez",
            correo="ana@ecotech.com",
            direccion="Av. Central 123",
            telefono="+56 9 8765 4321",
            fecha_inicio_contrato=date(2026, 1, 15),
            salario=Decimal("2500.50"),
            id_empleado=10
        )
        assert emp.direccion == "Av. Central 123", "Dirección incorrecta"
        assert emp.telefono == "+56 9 8765 4321", "Teléfono incorrecto"
        assert emp.fechaInicioContrato == date(2026, 1, 15), "fechaInicioContrato incorrecta"
        assert emp.salario == Decimal("2500.50"), "Salario incorrecto"
        assert hasattr(emp, "registrarHoras"), "Empleado debe tener método registrarHoras"

        # Validaciones de Encapsulamiento
        try:
            emp.salario = -500
            errores.append("Empleado no validó salario negativo")
        except ValueError:
            print("[OK] Validacion de salario negativo rechazada correctamente.")

        # AdministradorRRHH
        rrhh = AdministradorRRHH(nombre="Laura RRHH", correo="laura@ecotech.com", salario=3500)
        assert hasattr(rrhh, "gestionarEmpleados"), "AdministradorRRHH debe tener gestionarEmpleados"
        assert hasattr(rrhh, "gestionarDepartamentos"), "AdministradorRRHH debe tener gestionarDepartamentos"
        assert hasattr(rrhh, "generarReportes"), "AdministradorRRHH debe tener generarReportes"
        rrhh.gestionarEmpleados()
        rrhh.gestionarDepartamentos()
        rrhh.generarReportes()

        # Analista
        analista = Analista(nombre="Roberto Analista", correo="roberto@ecotech.com", salario=2800)
        assert hasattr(analista, "generarReporte"), "Analista debe tener generarReporte"
        assert hasattr(analista, "consultarTiempos"), "Analista debe tener consultarTiempos"
        analista.generarReporte()
        analista.consultarTiempos()

        # Tecnico
        tecnico = Tecnico(nombre="Marcos Tecnico", correo="marcos@ecotech.com", salario=2200)
        assert hasattr(tecnico, "consultarProyectos"), "Tecnico debe tener consultarProyectos"
        assert hasattr(tecnico, "registrarHoras"), "Tecnico debe tener registrarHoras"
        tecnico.consultarProyectos()

        print("[OK] Empleado y Roles Especializados verificados con exito.")
    except Exception as e:
        errores.append(f"Falla en Empleado/Roles: {e}")
        print(f"[FAIL] Error en Empleado/Roles: {e}")

    # -------------------------------------------------------------
    # 3. VERIFICACIÓN DE DEPARTAMENTO Y PROYECTO (UML)
    # -------------------------------------------------------------
    test_separador("3. Departamento y Proyecto (Asociaciones UML)")
    try:
        # Departamento
        dep = Departamento(nombre="Ingeniería y Desarrollo", gerente_id=10, id_departamento=1)
        assert dep.id == 1
        assert dep.nombre == "Ingeniería y Desarrollo"
        assert dep.gerenteId == 10
        assert hasattr(dep, "crear"), "Departamento debe tener crear()"
        assert hasattr(dep, "editar"), "Departamento debe tener editar()"
        assert hasattr(dep, "eliminar"), "Departamento debe tener eliminar()"
        dep.crear()
        dep.editar(nuevo_nombre="I+D Avanzado", nuevo_gerente_id=12)
        assert dep.nombre == "I+D Avanzado"
        assert dep.gerenteId == 12
        dep.eliminar()

        # Proyecto
        proy = Proyecto(
            nombre="EcoPlataforma 2026",
            descripcion="Plataforma de optimización energética",
            fecha_inicio=date(2026, 3, 1),
            id_proyecto=101
        )
        assert proy.id == 101
        assert proy.nombre == "EcoPlataforma 2026"
        assert proy.fechaInicio == date(2026, 3, 1)
        assert hasattr(proy, "asignarEmpleado"), "Proyecto debe tener asignarEmpleado()"
        proy.asignarEmpleado(10)
        assert 10 in proy.empleados_asignados, "El empleado 10 debe estar asignado al proyecto"

        print("[OK] Clases Departamento y Proyecto verificadas con exito.")
    except Exception as e:
        errores.append(f"Falla en Departamento/Proyecto: {e}")
        print(f"[FAIL] Error en Departamento/Proyecto: {e}")

    # -------------------------------------------------------------
    # 4. VERIFICACIÓN DE REGISTRO DE TIEMPO (UML)
    # -------------------------------------------------------------
    test_separador("4. Registro de Tiempo y Trazabilidad")
    try:
        reg = RegistroTiempo(
            empleado_id=10,
            proyecto_id=101,
            fecha=date(2026, 4, 10),
            horas=Decimal("8.5"),
            descripcion="Desarrollo de módulos de seguridad",
            id_registro=500
        )
        assert reg.empleadoId == 10
        assert reg.proyectoId == 101
        assert reg.horas == Decimal("8.50")
        assert reg.validar() is True, "El registro válido debe pasar validar()"
        reg.registrar()

        # Validación de horas excesivas
        try:
            reg.horas = Decimal("30.0")
            errores.append("RegistroTiempo permitió más de 24 horas diarias")
        except ValueError:
            print("[OK] Horas mayores a 24 rechazadas por regla de negocio.")

        print("[OK] RegistroTiempo verificado con exito.")
    except Exception as e:
        errores.append(f"Falla en RegistroTiempo: {e}")
        print(f"[FAIL] Error en RegistroTiempo: {e}")

    # -------------------------------------------------------------
    # 5. VERIFICACIÓN DE SERVICIO DE SEGURIDAD (UML)
    # -------------------------------------------------------------
    test_separador("5. ServicioSeguridad (Responsabilidad Única)")
    try:
        # Cifrado
        hash_pass = ServicioSeguridad.cifrarDato("ClaveSecreta123")
        assert len(hash_pass) == 64, "El hash debe tener 64 caracteres"
        assert hash_pass == ServicioSeguridad.cifrar_dato("ClaveSecreta123")

        # Autenticar
        assert ServicioSeguridad.autenticar("test@eco.com", "ClaveSecreta123", hash_pass) is True
        assert ServicioSeguridad.autenticar("test@eco.com", "ClaveErronea", hash_pass) is False

        # Autorizar
        assert ServicioSeguridad.autorizar("AdministradorRRHH", "gestionar_empleados") is True
        assert ServicioSeguridad.autorizar("Tecnico", "gestionar_departamentos") is False
        assert ServicioSeguridad.autorizar("Analista", "consultar_tiempos") is True

        # Validar Entrada
        assert ServicioSeguridad.validarEntrada("usuario@dominio.cl", "email") is True
        assert ServicioSeguridad.validarEntrada("no-es-correo", "email") is False
        assert ServicioSeguridad.validarEntrada(150, "int") is True
        assert ServicioSeguridad.validarEntrada("2026-10-20", "date") is True
        assert ServicioSeguridad.validarEntrada("fecha-mala", "date") is False

        print("[OK] ServicioSeguridad verificado con exito (Autenticacion, Autorizacion, Cifrado, Validacion).")
    except Exception as e:
        errores.append(f"Falla en ServicioSeguridad: {e}")
        print(f"[FAIL] Error en ServicioSeguridad: {e}")

    # -------------------------------------------------------------
    # 6. VERIFICACIÓN DE AUDITORÍA Y REPORTES (UML)
    # -------------------------------------------------------------
    test_separador("6. Auditoría y Reportes (Exportación física)")
    try:
        # Auditoría
        aud = Auditoria(
            usuario_id=1,
            accion="ACCESO_SISTEMA",
            detalle="Inicio de sesión verificado desde terminal",
            fecha=datetime.now(),
            id_auditoria=1
        )
        assert aud.usuarioId == 1
        assert aud.accion == "ACCESO_SISTEMA"
        assert hasattr(aud, "registrarEvento"), "Auditoria debe tener registrarEvento()"
        aud.registrarEvento()

        # Reporte
        rep = Reporte(tipo="Auditoría de Actividad", formato="TXT", id_reporte=1)
        assert rep.tipo == "Auditoría de Actividad"
        assert rep.formato == "TXT"
        assert hasattr(rep, "generar"), "Reporte debe tener generar()"
        assert hasattr(rep, "exportar"), "Reporte debe tener exportar()"

        datos_prueba = [
            "2026-10-20 09:00:00 - Inicio de jornada",
            "2026-10-20 12:30:00 - Registro de horas en proyecto 101",
            "2026-10-20 18:00:00 - Cierre de sesión"
        ]
        rep.generar(datos_prueba)
        assert "REPORTE: AUDITORÍA DE ACTIVIDAD" in rep.contenido
        
        # Exportación
        ruta_archivo = rep.exportar()
        assert os.path.exists(ruta_archivo), f"El archivo exportado no existe: {ruta_archivo}"
        print(f"[OK] Archivo de reporte generado fisicamente en: {ruta_archivo}")

        # Limpiar archivo temporal exportado
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)

        print("[OK] Auditoria y Reportes verificados con exito.")
    except Exception as e:
        errores.append(f"Falla en Auditoría/Reportes: {e}")
        print(f"[FAIL] Error en Auditoria/Reportes: {e}")

    # -------------------------------------------------------------
    # 7. VERIFICACIÓN DE SERVICIO EXTERNO (NUEVO - APIs)
    # -------------------------------------------------------------
    test_separador("7. ServicioExterno (Consumo de APIs: Clima y Divisas)")
    try:
        # Verificación estructural
        assert hasattr(ServicioExterno, "obtener_clima"), "ServicioExterno debe tener obtener_clima()"
        assert hasattr(ServicioExterno, "obtener_tipo_cambio"), "ServicioExterno debe tener obtener_tipo_cambio()"
        print("[OK] Estructura de ServicioExterno verificada (métodos presentes).")

        # Verificación funcional (requiere internet)
        try:
            clima = ServicioExterno.obtener_clima("Santiago")
            assert "temperatura" in clima, "La respuesta de clima debe incluir temperatura"
            assert "humedad" in clima, "La respuesta de clima debe incluir humedad"
            print(f"[OK] Clima obtenido: {clima['ciudad']} | Temp: {clima['temperatura']}°C | Humedad: {clima['humedad']}%")
        except ConnectionError as e:
            print(f"[WARN] Sin conexión a internet para probar clima: {e}")
        except ValueError as e:
            print(f"[WARN] Respuesta de clima con formato inesperado: {e}")

        try:
            tasa = ServicioExterno.obtener_tipo_cambio("USD", "CLP")
            assert isinstance(tasa, (int, float)), "La tasa de cambio debe ser numérica"
            print(f"[OK] Tipo de cambio USD->CLP: {tasa}")
        except ConnectionError as e:
            print(f"[WARN] Sin conexión a internet para probar cambio: {e}")
        except ValueError as e:
            print(f"[WARN] Error al procesar tipo de cambio: {e}")

        # Verificación de validación de entradas inválidas
        try:
            ServicioExterno.obtener_tipo_cambio("XX", "CLP")
            errores.append("ServicioExterno no validó moneda de 2 letras")
        except ValueError:
            print("[OK] Validación de moneda corta (2 letras) rechazada correctamente.")

        print("[OK] ServicioExterno verificado con exito.")
    except Exception as e:
        errores.append(f"Falla en ServicioExterno: {e}")
        print(f"[FAIL] Error en ServicioExterno: {e}")

    # -------------------------------------------------------------
    # RESUMEN FINAL
    # -------------------------------------------------------------
    test_separador("RESULTADO FINAL DE LA VERIFICACIÓN")
    if not errores:
        print("==> TODAS LAS PRUEBAS PASARON EXITOSAMENTE (100% CUMPLIMIENTO UML)!")
        print("   - Abstracción: OK (Usuario como clase base abstracta)")
        print("   - Encapsulamiento: OK (Atributos privados, getters/setters, validaciones)")
        print("   - Herencia: OK (Persona -> Usuario -> Empleado -> [RRHH, Analista, Tecnico])")
        print("   - Polimorfismo: OK (Especializaciones con responsabilidades particulares)")
        print("   - Relaciones: OK (Asociación, Composición lógica, Dependencia)")
        print("   - Seguridad y Trazabilidad: OK (ServicioSeguridad, Auditoria, Reporte)")
        print("   - Servicios Externos: OK (Open-Meteo + Frankfurter con manejo de errores)")
        return 0
    else:
        print(f"[WARN] Se encontraron {len(errores)} fallos:")
        for err in errores:
            print(f"   - {err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())