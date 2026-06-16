class Cliente:
    def __init__(self, id_cliente, nombre, apellido, dni, direccion, estado):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.direccion = direccion
        self.estado = estado

    def __str__(self):
        return f"{self.id_cliente} - {self.nombre} {self.apellido}"