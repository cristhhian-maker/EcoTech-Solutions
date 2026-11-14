# persona.py

class Persona:
    def __init__(self, nombre: str, correo: str):
        self.nombre = nombre   
        self.correo = correo   

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        if not isinstance(valor, str) or "@" not in valor or "." not in valor:
            raise ValueError(f"El correo '{valor}' no tiene un formato válido.")
        self.__correo = valor.strip().lower()

    def mostrar_datos_basicos(self) -> str:
        return f"Nombre: {self.__nombre} | Correo: {self.__correo}"