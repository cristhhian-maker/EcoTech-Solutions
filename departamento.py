# departamento.py

class Departamento:
    """
    Clase que representa un departamento en la empresa.

    Atributos UML:
    - id: int
    - nombre: String
    - gerenteId: int

    Métodos UML:
    + crear(): void
    + editar(): void
    + eliminar(): void
    """

    def __init__(self, nombre: str, gerente_id: int | None = None, id_departamento: int | None = None):
        self.id = id_departamento
        self.nombre = nombre
        self.gerente_id = gerente_id

    # --- Propiedad: id ---
    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, valor: int | None):
        self.__id = valor

    # --- Propiedad: nombre ---
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del departamento no puede estar vacío.")
        self.__nombre = valor.strip()

    # --- Propiedad: gerenteId / gerente_id ---
    @property
    def gerente_id(self) -> int | None:
        return self.__gerente_id

    @gerente_id.setter
    def gerente_id(self, valor: int | None):
        if valor is not None:
            try:
                valor = int(valor)
                if valor <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                raise ValueError("El gerenteId debe ser un ID de empleado válido (entero positivo).")
        self.__gerente_id = valor

    @property
    def gerenteId(self) -> int | None:
        return self.__gerente_id

    # --- Métodos del diagrama UML ---
    def crear(self) -> None:
        """
        Inicializa o confirma la creación del departamento.
        Corresponde a crear(): void en el diagrama UML.
        """
        print(f"[OK] Departamento '{self.nombre}' inicializado exitosamente (Gerente ID: {self.gerente_id}).")

    def editar(self, nuevo_nombre: str | None = None, nuevo_gerente_id: int | None = None) -> None:
        """
        Modifica los atributos del departamento validándolos.
        Corresponde a editar(): void en el diagrama UML.
        """
        if nuevo_nombre is not None:
            self.nombre = nuevo_nombre
        if nuevo_gerente_id is not None:
            self.gerente_id = nuevo_gerente_id
        print(f"[OK] Departamento ID {self.id} actualizado: Nombre='{self.nombre}', Gerente ID={self.gerente_id}")

    def eliminar(self) -> None:
        """
        Marca o gestiona la eliminación del departamento.
        Corresponde a eliminar(): void en el diagrama UML.
        """
        print(f"[OK] Departamento '{self.nombre}' (ID: {self.id}) marcado para eliminación.")

    def __str__(self) -> str:
        return f"ID: {self.id} | Departamento: {self.nombre} | Gerente ID: {self.gerente_id}"
