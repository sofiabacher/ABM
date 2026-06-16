class Proveedor:
    def __init__(self, id_proveedor, razon_social, cuit, direccion, telefono, email, estado):
        self.id_proveedor = id_proveedor
        self.razon_social = razon_social
        self.cuit = cuit
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.estado = estado

    def __str__(self):
        return f"{self.id_proveedor} - {self.razon_social}"