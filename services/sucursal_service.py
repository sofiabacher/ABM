from services.base_service import BaseService, RegistroDuplicadoError
from models.proveedor import Proveedor

class ProveedorService(BaseService):
    def __init__(self):
        super().__init__("proveedores", "id_proveedor", Proveedor)

    def validar_campos(self, razon_social, cuit, email, telefono, provincia, direccion):
        if razon_social.strip() == "":
            return False, "Debe completar la razón social"

        if cuit.strip() == "":
            return False, "Debe ingresar un cuit"

        if not cuit.isdigit():
            return False, "El cuit debe ser numérico"

        if email.strip() == "" or "@" not in email:
            return False, "Debe ingresar un email válido"

        if telefono.strip() == "":
            return False, "Debe completar el teléfono"

        if provincia.strip() == "":
            return False, "Debe completar la provincia"

        if direccion.strip() == "":
            return False, "Debe completar la dirección"

        return True, ""

    def alta(self, razon_social, cuit, email, telefono, provincia, direccion, estado=True):
        valido, mensaje = self.validar_campos(razon_social, cuit, email, telefono, provincia, direccion)

        if not valido:
            return False, mensaje

        query = """
            INSERT INTO proveedores (razon_social, cuit, email, telefono, provincia, direccion, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        valores = (razon_social, cuit, email, telefono, provincia, direccion, estado)

        try:
            nuevo_id = self.insertar(query, valores)

        except RegistroDuplicadoError as error:
            return False, str(error)

        return True, f"Proveedor agregado correctamente (id={nuevo_id})"

    def baja(self, id_proveedor):
        if not self.buscar_por_id(id_proveedor):
            return False, "Proveedor no encontrado"

        self.baja_logica(id_proveedor)

        return True, "Proveedor dado de baja"

    def modificar(self, id_proveedor, razon_social, cuit, email, telefono, provincia, direccion, estado=True):
        if not self.buscar_por_id(id_proveedor):
            return False, "Proveedor no encontrado"

        valido, mensaje = self.validar_campos(razon_social, cuit, email, telefono, provincia, direccion)

        if not valido:
            return False, mensaje

        query = """
            UPDATE proveedores
            SET razon_social=%s, cuit=%s, email=%s, telefono=%s, provincia=%s, direccion=%s, estado=%s
            WHERE id_proveedor=%s
        """
        valores = (razon_social, cuit, email, telefono, provincia, direccion, estado, id_proveedor)
        
        super().modificar(query, valores)
        
        return True, "Proveedor modificado"
