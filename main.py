# main.py
import sys
import re

from cliente import Cliente
from cliente_repository import ClienteRepository
from empleado import Empleado, AdministradorRRHH, Analista, Tecnico
from empleado_repository import EmpleadoRepository
from usuario import Usuario
from usuario_repository import UsuarioRepository
from departamento import Departamento
from departamento_repository import DepartamentoRepository
from proyecto import Proyecto
from proyecto_repository import ProyectoRepository
from registro_tiempo import RegistroTiempo
from registro_tiempo_repository import RegistroTiempoRepository
from auditoria import Auditoria
from auditoria_repository import AuditoriaRepository
from reporte import Reporte
from reporte_repository import ReporteRepository
from servicio_seguridad import ServicioSeguridad
from servicio_externo import ServicioExterno


# =====================================================================
#         VARIABLE GLOBAL DE SESIÓN (control de acceso a APIs)
# =====================================================================
USUARIO_AUTENTICADO = None


# =====================================================================
#                   VALIDACIONES DE ENTRADA PARA APIS
# =====================================================================
def validar_ciudad(ciudad: str) -> str:
    """Solo letras, espacios y guiones. Previene inyecciones."""
    if not ciudad or not ciudad.strip():
        raise ValueError("El nombre de la ciudad no puede estar vacío.")
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-]+$', ciudad.strip()):
        raise ValueError("La ciudad contiene caracteres no permitidos.")
    return ciudad.strip().capitalize()


def validar_moneda(moneda: str) -> str:
    """Código ISO de 3 letras."""
    if not moneda or not moneda.strip():
        raise ValueError("El código de moneda no puede estar vacío.")
    moneda_limpia = moneda.strip().upper()
    if not re.match(r'^[A-Z]{3}$', moneda_limpia):
        raise ValueError("El código de moneda debe tener 3 letras (ej. USD, CLP).")
    return moneda_limpia


# =====================================================================
#                   MENÚ DE SERVICIOS EXTERNOS (NUEVO)
# =====================================================================
def menu_servicios_externos():
    """Solo accesible si hay sesión activa."""
    global USUARIO_AUTENTICADO

    if not USUARIO_AUTENTICADO:
        print("\n[ACCESO DENEGADO] Debe iniciar sesión primero.")
        print("Vaya a la opción 7 (Seguridad y Auditoría) -> 1) Autenticar Usuario.")
        return

    while True:
        print("\n" + "-" * 42)
        print("   Servicios Externos (Clima y Divisas)")
        print("-" * 42)
        print("  1) Consultar clima de una ciudad")
        print("  2) Consultar tipo de cambio entre monedas")
        print("  3) Volver al menú principal")

        try:
            opcion = int(input("Ingrese una opción: "))
        except ValueError:
            print("[AVISO] Ingrese un número válido.")
            continue

        if opcion == 1:
            try:
                ciudad = input("Ingrese el nombre de la ciudad: ")
                ciudad_valida = validar_ciudad(ciudad)
                print(f"\nConsultando clima para '{ciudad_valida}'...")
                clima = ServicioExterno.obtener_clima(ciudad_valida)
                print("\n" + "=" * 45)
                print(f"  CLIMA EN {clima['ciudad'].upper()}")
                print("=" * 45)
                print(f"  Temperatura: {clima['temperatura']} °C")
                print(f"  Viento:      {clima['viento']} km/h")
                print(f"  Humedad:     {clima['humedad']} %")
                print("=" * 45)
            except ValueError as e:
                print(f"[ERROR DE VALIDACIÓN] {e}")
            except ConnectionError as e:
                print(f"[ERROR DE SERVICIO] {e}")

        elif opcion == 2:
            try:
                origen = input("Moneda origen (ej. USD): ")
                destino = input("Moneda destino (ej. CLP): ")
                origen_val = validar_moneda(origen)
                destino_val = validar_moneda(destino)
                print(f"\nConsultando tipo de cambio {origen_val} -> {destino_val}...")
                tasa = ServicioExterno.obtener_tipo_cambio(origen_val, destino_val)
                print("\n" + "=" * 45)
                print(f"  TIPO DE CAMBIO: 1 {origen_val} = {tasa:.2f} {destino_val}")
                print("=" * 45)
            except ValueError as e:
                print(f"[ERROR DE VALIDACIÓN] {e}")
            except ConnectionError as e:
                print(f"[ERROR DE SERVICIO] {e}")

        elif opcion == 3:
            break
        else:
            print("[AVISO] Opción fuera de rango.")


# =====================================================================
#                        FUNCIONES DE CLIENTES
# =====================================================================
def crear_cliente(repo: ClienteRepository):
    try:
        nombre   = input("Nombre:    ").strip()
        correo   = input("Correo:    ").strip()
        telefono = input("Teléfono:  ").strip()

        cliente = Cliente(nombre, correo, telefono)
        repo.guardar(cliente)
    except ValueError as e:
        print(f"[DATO INVÁLIDO] {e}")


def mostrar_clientes(repo: ClienteRepository):
    clientes = repo.listar()
    print("\n" + "=" * 65)
    print(f"  {'ID':<6} {'NOMBRE':<20} {'CORREO':<25} {'TELÉFONO':<12} CÓD.")
    print("=" * 65)
    if not clientes:
        print("  No hay clientes registrados aún.")
    else:
        for id_cliente, nombre, correo, telefono, codigo_interno in clientes:
            print(f"  {id_cliente:<6} {nombre:<20} {correo:<25} {telefono:<12} {codigo_interno}")
    print("=" * 65)


def eliminar_cliente(repo: ClienteRepository):
    mostrar_clientes(repo)
    try:
        id_cliente = int(input("\nIngrese el ID del cliente a eliminar: "))
        repo.eliminar(id_cliente)
    except ValueError:
        print("[AVISO] El ID debe ser un número entero.")


def actualizar_cliente(repo: ClienteRepository):
    mostrar_clientes(repo)
    try:
        id_cliente = int(input("\nIngrese el ID del cliente a actualizar: "))
        print("(Deje en blanco y presione Enter para mantener el valor actual)")
        nombre   = input("Nuevo nombre:    ").strip()
        correo   = input("Nuevo correo:    ").strip()
        telefono = input("Nuevo teléfono:  ").strip()

        if nombre or correo or telefono:
            clientes = repo.listar()
            cliente_actual = next((c for c in clientes if c[0] == id_cliente), None)
            if not cliente_actual:
                print(f"[AVISO] No se encontró ningún cliente con ID {id_cliente}.")
                return

            nombre_final   = nombre   if nombre   else cliente_actual[1]
            correo_final   = correo   if correo   else cliente_actual[2]
            telefono_final = telefono if telefono else cliente_actual[3]

            Cliente(nombre_final, correo_final, telefono_final)
            repo.actualizar(id_cliente, nombre_final, correo_final, telefono_final)
        else:
            print("[AVISO] No se realizaron cambios (todos los campos estaban vacíos).")
    except ValueError as e:
        print(f"[DATO INVÁLIDO] {e}")


def menu_clientes(repo: ClienteRepository):
    while True:
        print("\n" + "-" * 32)
        print("      Gestión de Clientes")
        print("-" * 32)
        print("  1) Crear cliente")
        print("  2) Mostrar clientes")
        print("  3) Actualizar cliente")
        print("  4) Eliminar cliente")
        print("  5) Volver al menú principal")

        try:
            opcion = int(input("Ingrese una opción: "))
        except ValueError:
            print("[AVISO] Ingrese un número válido (1–5).")
            continue

        if opcion == 1:
            crear_cliente(repo)
        elif opcion == 2:
            mostrar_clientes(repo)
        elif opcion == 3:
            actualizar_cliente(repo)
        elif opcion == 4:
            eliminar_cliente(repo)
        elif opcion == 5:
            break


# =====================================================================
#             FUNCIONES DE EMPLEADOS Y ROLES (UML)
# =====================================================================
def crear_empleado(repo: EmpleadoRepository, repo_auditoria: AuditoriaRepository):
    try:
        print("\n--- Registro de Nuevo Empleado (UML) ---")
        nombre    = input("Nombre:                   ").strip()
        correo    = input("Correo:                   ").strip()
        direccion = input("Dirección:                ").strip()
        telefono  = input("Teléfono:                 ").strip()
        salario   = input("Salario:                  ").strip()
        
        print("\nSeleccione Rol / Especialización:")
        print("  1) Empleado General")
        print("  2) Administrador RRHH")
        print("  3) Analista")
        print("  4) Técnico")
        opc_rol = input("Opción (1-4, defecto 1): ").strip()

        if opc_rol == "2":
            emp = AdministradorRRHH(nombre=nombre, correo=correo, direccion=direccion, 
                                    telefono=telefono, salario=salario)
        elif opc_rol == "3":
            emp = Analista(nombre=nombre, correo=correo, direccion=direccion, 
                           telefono=telefono, salario=salario)
        elif opc_rol == "4":
            emp = Tecnico(nombre=nombre, correo=correo, direccion=direccion, 
                          telefono=telefono, salario=salario)
        else:
            emp = Empleado(nombre=nombre, correo=correo, direccion=direccion, 
                           telefono=telefono, salario=salario)

        guardado = repo.guardar(emp)
        if guardado:
            repo_auditoria.guardar(Auditoria(
                usuario_id=emp.id if emp.id else 1,
                accion="CREAR_EMPLEADO",
                detalle=f"Se registró el empleado '{emp.nombre}' con rol '{emp.puesto}'"
            ))

    except ValueError as e:
        print(f"[DATO INVÁLIDO] {e}")


def mostrar_empleados(repo: EmpleadoRepository):
    empleados = repo.listar()
    print("\n" + "=" * 85)
    print(f"  {'ID':<6} {'NOMBRE':<18} {'CORREO':<24} {'PUESTO/ROL':<18} {'SALARIO':<12}")
    print("=" * 85)
    if not empleados:
        print("  No hay empleados registrados aún.")
    else:
        for fila in empleados:
            id_emp = fila[0]
            nombre = fila[1] if len(fila) > 1 else ""
            correo = fila[2] if len(fila) > 2 else ""
            puesto = fila[3] if len(fila) > 3 else "Empleado"
            salario = fila[4] if len(fila) > 4 else 0.0
            salario_fmt = f"${float(salario):,.2f}"
            print(f"  {id_emp:<6} {nombre:<18} {correo:<24} {puesto:<18} {salario_fmt:<12}")
    print("=" * 85)


def probar_metodos_rol():
    print("\n--- Demostración Polimórfica de Roles (UML) ---")
    rrhh = AdministradorRRHH(nombre="Laura Gómez", correo="laura.rrhh@empresa.com", salario=3200)
    analista = Analista(nombre="Carlos Méndez", correo="carlos.analista@empresa.com", salario=2500)
    tecnico = Tecnico(nombre="Sofía Torres", correo="sofia.tecnica@empresa.com", salario=2100)

    print("\n[1. AdministradorRRHH]:")
    rrhh.gestionar_empleados()
    rrhh.gestionar_departamentos()
    rrhh.generar_reportes()

    print("\n[2. Analista]:")
    analista.generar_reporte()
    analista.consultar_tiempos()

    print("\n[3. Técnico]:")
    tecnico.consultar_proyectos()
    tecnico.registrar_horas(proyecto_id=101, horas=4.5, descripcion="Mantenimiento en servidor")


def menu_empleados(repo: EmpleadoRepository, repo_auditoria: AuditoriaRepository):
    while True:
        print("\n" + "-" * 32)
        print("  Gestión de Empleados y Roles")
        print("-" * 32)
        print("  1) Crear empleado / rol")
        print("  2) Mostrar empleados")
        print("  3) Probar métodos de Roles (RRHH, Analista, Técnico)")
        print("  4) Eliminar empleado")
        print("  5) Volver al menú principal")

        try:
            opcion = int(input("Ingrese una opción: "))
        except ValueError:
            print("[AVISO] Ingrese un número válido (1–5).")
            continue

        if opcion == 1:
            crear_empleado(repo, repo_auditoria)
        elif opcion == 2:
            mostrar_empleados(repo)
        elif opcion == 3:
            probar_metodos_rol()
        elif opcion == 4:
            mostrar_empleados(repo)
            try:
                id_e = int(input("Ingrese ID del empleado a eliminar: "))
                repo.eliminar(id_e)
            except ValueError:
                print("[AVISO] ID inválido.")
        elif opcion == 5:
            break


# =====================================================================
#             GESTIÓN DE DEPARTAMENTOS (UML)
# =====================================================================
def menu_departamentos(repo: DepartamentoRepository):
    while True:
        print("\n" + "-" * 32)
        print("    Gestión de Departamentos")
        print("-" * 32)
        print("  1) Crear departamento")
        print("  2) Listar departamentos")
        print("  3) Eliminar departamento")
        print("  4) Volver al menú principal")

        try:
            opcion = int(input("Ingrese una opción: "))
        except ValueError:
            print("[AVISO] Ingrese un número válido.")
            continue

        if opcion == 1:
            try:
                nombre = input("Nombre del departamento: ").strip()
                gerente_id = input("ID de Empleado Gerente (opcional): ").strip()
                g_id = int(gerente_id) if gerente_id else None
                depto = Departamento(nombre=nombre, gerente_id=g_id)
                depto.crear()
                repo.guardar(depto)
            except ValueError as e:
                print(f"[ERROR] {e}")

        elif opcion == 2:
            deptos = repo.listar()
            print("\n" + "=" * 55)
            print(f"  {'ID':<6} {'DEPARTAMENTO':<30} {'GERENTE ID'}")
            print("=" * 55)
            if not deptos:
                print("  No hay departamentos registrados.")
            else:
                for d_id, nom, g_id in deptos:
                    print(f"  {d_id:<6} {nom:<30} {str(g_id) if g_id else 'Sin Gerente'}")
            print("=" * 55)

        elif opcion == 3:
            try:
                d_id = int(input("Ingrese ID del departamento a eliminar: "))
                repo.eliminar(d_id)
            except ValueError:
                print("[AVISO] ID inválido.")

        elif opcion == 4:
            break


# =====================================================================
#             GESTIÓN DE PROYECTOS (UML)
# =====================================================================
def menu_proyectos(repo: ProyectoRepository):
    while True:
        print("\n" + "-" * 32)
        print("      Gestión de Proyectos")
        print("-" * 32)
        print("  1) Crear proyecto")
        print("  2) Listar proyectos")
        print("  3) Asignar empleado a proyecto")
        print("  4) Eliminar proyecto")
        print("  5) Volver al menú principal")

        try:
            opcion = int(input("Ingrese una opción: "))
        except ValueError:
            print("[AVISO] Ingrese un número válido.")
            continue

        if opcion == 1:
            try:
                nombre = input("Nombre del proyecto: ").strip()
                desc   = input("Descripción:         ").strip()
                fecha  = input("Fecha Inicio (YYYY-MM-DD): ").strip()
                proy = Proyecto(nombre=nombre, descripcion=desc, fecha_inicio=fecha)
                repo.guardar(proy)
            except ValueError as e:
                print(f"[ERROR] {e}")

        elif opcion == 2:
            proyectos = repo.listar()
            print("\n" + "=" * 70)
            print(f"  {'ID':<6} {'NOMBRE':<25} {'INICIO':<12} {'DESCRIPCIÓN'}")
            print("=" * 70)
            if not proyectos:
                print("  No hay proyectos registrados.")
            else:
                for p_id, p_nom, p_desc, p_fecha in proyectos:
                    print(f"  {p_id:<6} {p_nom:<25} {str(p_fecha):<12} {p_desc}")
            print("=" * 70)

        elif opcion == 3:
            try:
                p_id = int(input("ID del proyecto: "))
                e_id = int(input("ID del empleado a asignar: "))
                repo.asignar_empleado(e_id, p_id)
            except ValueError:
                print("[AVISO] Debe ingresar números enteros.")

        elif opcion == 4:
            try:
                p_id = int(input("ID del proyecto a eliminar: "))
                repo.eliminar(p_id)
            except ValueError:
                print("[AVISO] ID inválido.")

        elif opcion == 5:
            break


# =====================================================================
#             REGISTRO Y CONTROL DE TIEMPO (UML)
# =====================================================================
def menu_registro_tiempo(repo: RegistroTiempoRepository):
    while True:
        print("\n" + "-" * 32)
        print("    Control de Horas / Tiempo")
        print("-" * 32)
        print("  1) Registrar horas de trabajo")
        print("  2) Ver todos los registros")
        print("  3) Consultar horas por empleado")
        print("  4) Volver al menú principal")

        try:
            opcion = int(input("Ingrese una opción: "))
        except ValueError:
            print("[AVISO] Ingrese un número válido.")
            continue

        if opcion == 1:
            try:
                emp_id = int(input("ID de Empleado:       "))
                proy_id = int(input("ID de Proyecto:       "))
                fecha   = input("Fecha (YYYY-MM-DD):   ").strip()
                horas   = input("Horas dedicadas:      ").strip()
                desc    = input("Descripción tarea:    ").strip()

                reg = RegistroTiempo(empleado_id=emp_id, proyecto_id=proy_id, 
                                     fecha=fecha, horas=horas, descripcion=desc)
                if reg.validar():
                    repo.guardar(reg)
                else:
                    print("[ERROR] Los datos de tiempo no superaron la validación.")
            except ValueError as e:
                print(f"[ERROR] {e}")

        elif opcion == 2:
            registros = repo.listar()
            print("\n" + "=" * 75)
            print(f"  {'ID':<6} {'FECHA':<12} {'HORAS':<8} {'EMP_ID':<8} {'PROY_ID':<8} DESCRIPCIÓN")
            print("=" * 75)
            if not registros:
                print("  No hay registros de tiempo cargados.")
            else:
                for r_id, r_fecha, r_horas, r_desc, r_emp, r_proy in registros:
                    print(f"  {r_id:<6} {str(r_fecha):<12} {float(r_horas):<8.2f} {r_emp:<8} {r_proy:<8} {r_desc}")
            print("=" * 75)

        elif opcion == 3:
            try:
                emp_id = int(input("Ingrese ID del empleado: "))
                registros = repo.listar_por_empleado(emp_id)
                total_horas = sum(float(r[2]) for r in registros)
                print(f"\nTotal horas acumuladas para Empleado {emp_id}: {total_horas:.2f}h")
            except ValueError:
                print("[AVISO] Ingrese un ID válido.")

        elif opcion == 4:
            break


# =====================================================================
#             GENERACIÓN Y EXPORTACIÓN DE REPORTES (UML)
# =====================================================================
def menu_reportes(repo_reporte: ReporteRepository, repo_tiempo: RegistroTiempoRepository, repo_emp: EmpleadoRepository):
    while True:
        print("\n" + "-" * 32)
        print("   Generación de Reportes")
        print("-" * 32)
        print("  1) Generar Reporte de Horas Trabajadas")
        print("  2) Generar Reporte de Empleados")
        print("  3) Exportar Reporte a Archivo")
        print("  4) Ver historial de reportes en BD")
        print("  5) Volver al menú principal")

        try:
            opcion = int(input("Ingrese una opción: "))
        except ValueError:
            print("[AVISO] Ingrese un número válido.")
            continue

        if opcion == 1:
            registros = repo_tiempo.listar()
            rep = Reporte(tipo="Registro de Horas por Proyecto", formato="TXT")
            rep.generar(registros)
            print("\nVista previa:")
            print(rep.contenido)
            repo_reporte.guardar(rep)

        elif opcion == 2:
            empleados = repo_emp.listar()
            rep = Reporte(tipo="Padrón General de Empleados", formato="TXT")
            rep.generar(empleados)
            print("\nVista previa:")
            print(rep.contenido)
            repo_reporte.guardar(rep)

        elif opcion == 3:
            tipo = input("Tipo de reporte (ej. Finanzas, Personal): ").strip() or "General"
            formato = input("Formato (TXT, CSV, JSON): ").strip().upper() or "TXT"
            rep = Reporte(tipo=tipo, formato=formato)
            rep.generar(["Item 1: OK", "Item 2: Aprobado", "Item 3: En progreso"])
            archivo = rep.exportar()
            if archivo:
                repo_reporte.guardar(rep)

        elif opcion == 4:
            reportes = repo_reporte.listar()
            print("\n" + "=" * 65)
            print(f"  {'ID':<6} {'TIPO':<32} {'FORMATO':<10} FECHA")
            print("=" * 65)
            if not reportes:
                print("  No hay reportes registrados.")
            else:
                for r_id, r_tipo, r_fmt, r_fecha in reportes:
                    print(f"  {r_id:<6} {r_tipo:<32} {r_fmt:<10} {str(r_fecha)}")
            print("=" * 65)

        elif opcion == 5:
            break


# =====================================================================
#             SEGURIDAD Y AUDITORÍA (MODIFICADO)
# =====================================================================
def menu_seguridad_auditoria(repo_auditoria: AuditoriaRepository, repo_usuarios: UsuarioRepository):
    global USUARIO_AUTENTICADO

    while True:
        print("\n" + "-" * 32)
        print("     Seguridad y Auditoría")
        print("-" * 32)
        print("  1) Autenticar Usuario (Iniciar Sesión)")
        print("  2) Registrar Evento de Auditoría")
        print("  3) Consultar Historial de Auditoría")
        print("  4) Probar Cifrado de Datos (SHA-256)")
        print("  5) Volver al menú principal")

        try:
            opcion = int(input("Ingrese una opción: "))
        except ValueError:
            print("[AVISO] Ingrese un número válido.")
            continue

        if opcion == 1:
            correo = input("Correo electrónico: ").strip()
            clave  = input("Contraseña:         ").strip()
            datos_usr = repo_usuarios.buscar_por_correo(correo)
            if datos_usr:
                usr = Usuario(nombre=datos_usr["nombre"], correo=datos_usr["correo"], 
                              contrasena=datos_usr["contrasena_hash"], activo=datos_usr["activo"], 
                              id_usuario=datos_usr["id"], es_hash=True)
                if usr.iniciar_sesion(clave):
                    USUARIO_AUTENTICADO = usr
                    repo_auditoria.guardar(Auditoria(
                        usuario_id=usr.id,
                        accion="LOGIN_EXITOSO",
                        detalle=f"Acceso concedido para {usr.nombre}"
                    ))
                else:
                    repo_auditoria.guardar(Auditoria(
                        usuario_id=usr.id,
                        accion="LOGIN_FALLIDO",
                        detalle=f"Intento fallido de contraseña"
                    ))
            else:
                print(f"[ACCESO DENEGADO] No existe usuario con correo '{correo}'.")

        elif opcion == 2:
            try:
                u_id = int(input("ID de Usuario: "))
                acc  = input("Acción realizada: ").strip()
                det  = input("Detalles: ").strip()
                aud  = Auditoria(usuario_id=u_id, accion=acc, detalle=det)
                aud.registrar_evento()
                repo_auditoria.guardar(aud)
            except ValueError as e:
                print(f"[ERROR] {e}")

        elif opcion == 3:
            eventos = repo_auditoria.listar()
            print("\n" + "=" * 80)
            print(f"  {'ID':<6} {'USUARIO':<10} {'FECHA':<20} {'ACCIÓN':<20} DETALLE")
            print("=" * 80)
            if not eventos:
                print("  No hay eventos registrados en auditoría.")
            else:
                for a_id, u_id, acc, f_dt, det in eventos:
                    print(f"  {a_id:<6} {u_id:<10} {str(f_dt):<20} {acc:<20} {det}")
            print("=" * 80)

        elif opcion == 4:
            texto = input("Ingrese texto a cifrar: ").strip()
            hash_res = ServicioSeguridad.cifrar_dato(texto)
            print(f"Texto original: '{texto}'")
            print(f"Hash SHA-256:   {hash_res}")

        elif opcion == 5:
            break


# =====================================================================
#                          MENÚ PRINCIPAL (MODIFICADO)
# =====================================================================
def menu():
    global USUARIO_AUTENTICADO

    repo_clientes     = ClienteRepository()
    repo_empleados    = EmpleadoRepository()
    repo_usuarios     = UsuarioRepository()
    repo_deptos       = DepartamentoRepository()
    repo_proyectos    = ProyectoRepository()
    repo_tiempo       = RegistroTiempoRepository()
    repo_auditoria    = AuditoriaRepository()
    repo_reportes     = ReporteRepository()

    while True:
        print("\n" + "=" * 48)
        print("     SISTEMA INTEGRAL DE GESTIÓN (UML)")
        print("=" * 48)
        estado_sesion = "Sesión: ACTIVA" if USUARIO_AUTENTICADO else "Sesión: NO INICIADA"
        print(f"  [{estado_sesion}]")
        print("=" * 48)
        print("  1) Gestión de Clientes")
        print("  2) Gestión de Empleados y Roles")
        print("  3) Gestión de Departamentos")
        print("  4) Gestión de Proyectos")
        print("  5) Control de Horas / Registro de Tiempo")
        print("  6) Generación y Exportación de Reportes")
        print("  7) Servicio de Seguridad y Auditoría")
        print("  8) Servicios Externos (Clima y Divisas)")
        print("  9) Salir")

        try:
            opcion = int(input("Ingrese una opción (1-9): "))
        except ValueError:
            print("[AVISO] Ingrese un número válido (1–9).")
            continue

        if opcion == 1:
            menu_clientes(repo_clientes)
        elif opcion == 2:
            menu_empleados(repo_empleados, repo_auditoria)
        elif opcion == 3:
            menu_departamentos(repo_deptos)
        elif opcion == 4:
            menu_proyectos(repo_proyectos)
        elif opcion == 5:
            menu_registro_tiempo(repo_tiempo)
        elif opcion == 6:
            menu_reportes(repo_reportes, repo_tiempo, repo_empleados)
        elif opcion == 7:
            menu_seguridad_auditoria(repo_auditoria, repo_usuarios)
        elif opcion == 8:
            menu_servicios_externos()
        elif opcion == 9:
            print("\n¡Gracias por utilizar el sistema! Hasta pronto.")
            break
        else:
            print("[AVISO] Opción fuera de rango. Elija entre 1 y 9.")


if __name__ == "__main__":
    menu()