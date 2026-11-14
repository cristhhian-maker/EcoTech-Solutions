# cliente.py
from persona import Persona

class Cliente(Persona):

    def __init__(self, nombre: str, correo: str, telefono: str):
        super().__init__(nombre, correo)
        self.telefono = telefono
        self.__codigo_interno = self.__generar_codigo()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El teléfono no puede estar vacío.")
        caracteres_validos = set("0123456789 +-")
        if not all(c in caracteres_validos for c in valor.strip()):
            raise ValueError(f"El teléfono '{valor}' contiene caracteres no válidos.")
        self.__telefono = valor.strip()

    def __generar_codigo(self) -> str:
        prefijo = self.nombre[:3].upper()
        return f"CLI-{prefijo}"

    def get_codigo_interno(self) -> str:
        return self.__codigo_interno

    def actualizar_telefono(self, nuevo_tel: str):
        self.telefono = nuevo_tel

    def mostrar_datos(self) -> str:
        datos_padre = super().mostrar_datos_basicos()
        return f"{datos_padre} | Tel: {self.__telefono} | Cód: {self.__codigo_interno}"