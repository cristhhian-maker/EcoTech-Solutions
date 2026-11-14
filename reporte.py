# reporte.py
import os
from datetime import datetime
from servicio_seguridad import ServicioSeguridad


class Reporte:

    FORMATOS_VALIDOS = ("TXT", "CSV", "JSON", "PDF")

    def __init__(self, tipo: str, formato: str = "TXT", id_reporte: int | None = None, contenido: str = ""):
        self.id = id_reporte
        self.tipo = tipo
        self.formato = formato
        self.__contenido = contenido
        self.__fecha_creacion = datetime.now()

    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, valor: int | None):
        self.__id = valor

    @property
    def tipo(self) -> str:
        return self.__tipo

    @tipo.setter
    def tipo(self, valor: str):
        if not ServicioSeguridad.validar_entrada(valor, "string"):
            raise ValueError("El tipo de reporte no puede estar vacío.")
        self.__tipo = valor.strip()

    @property
    def formato(self) -> str:
        return self.__formato

    @formato.setter
    def formato(self, valor: str):
        formato_limpio = str(valor).strip().upper()
        if formato_limpio not in self.FORMATOS_VALIDOS:
            raise ValueError(f"Formato no admitido '{valor}'. Permitidos: {', '.join(self.FORMATOS_VALIDOS)}")
        self.__formato = formato_limpio

    @property
    def contenido(self) -> str:
        return self.__contenido

    @contenido.setter
    def contenido(self, valor: str):
        self.__contenido = str(valor)

    def generar(self, datos: list | dict | None = None) -> None:
        
        encabezado = f"=========================================\n" \
                     f"           REPORTE: {self.tipo.upper()}\n" \
                     f"  Fecha: {self.__fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}\n" \
                     f"  Formato: {self.formato}\n" \
                     f"=========================================\n"

        cuerpo = ""
        if isinstance(datos, list):
            for i, item in enumerate(datos, 1):
                cuerpo += f"{i}. {item}\n"
        elif isinstance(datos, dict):
            for k, v in datos.items():
                cuerpo += f"- {k}: {v}\n"
        elif datos:
            cuerpo = str(datos) + "\n"
        else:
            cuerpo = "Sin datos registrados para este reporte.\n"

        self.__contenido = encabezado + "\n" + cuerpo
        print(f"[OK] Reporte '{self.tipo}' generado exitosamente.")

    def exportar(self, carpeta_destino: str = ".") -> str:
        if not self.__contenido:
            self.generar()

        timestamp = self.__fecha_creacion.strftime("%Y%m%d_%H%M%S")
        tipo_slug = self.tipo.lower().replace(" ", "_")
        nombre_archivo = f"reporte_{tipo_slug}_{timestamp}.{self.formato.lower()}"
        ruta_completa = os.path.join(carpeta_destino, nombre_archivo)

        try:
            with open(ruta_completa, "w", encoding="utf-8") as f:
                f.write(self.__contenido)
            print(f"[OK] Archivo exportado: {ruta_completa}")
            return ruta_completa
        except Exception as e:
            print(f"[ERROR AL EXPORTAR] No se pudo guardar el archivo: {e}")
            return ""

    def __str__(self) -> str:
        return f"ID: {self.id} | Tipo: {self.tipo} | Formato: {self.formato} | Fecha: {self.__fecha_creacion.strftime('%Y-%m-%d %H:%M')}"
