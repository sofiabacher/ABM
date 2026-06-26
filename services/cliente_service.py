from services.base_service import BaseService, RegistroDuplicadoError
from models.cliente import Cliente

class ClienteService(BaseService):
    def __init__(self):
        super().__init__("clientes", "id_cliente", Cliente)
    
    def validar_campos(self, nombre, apellido, dni, telefono, direccion, email=None):
        if nombre.strip() == "":
            return False, "Debe completar el nombre"
        
        if apellido.strip() == "":
            return False, "Debe completar el apellido"
        
        if dni.strip() == "":
            return False, "Debe completar el dni"
        
        if not dni.isdigit():
            return False, "El dni debe ser numérico"
        
        if telefono.strip() == "":
            return False, "Debe completar el telefono"
        
        if direccion.strip() == "":
            return False, "Debe completar el direccion"

        if email and "@" not in email:
            return False, "El email no tiene un formato válido"

        return True, ""
    
    def alta(self, nombre, apellido, dni, telefono, direccion, email=None, estado=True):
        valido, mensaje = self.validar_campos(nombre, apellido, dni, telefono, direccion, email)

        if not valido:
            return False, mensaje
        
        query = """
            INSERT INTO clientes (nombre, apellido, dni, telefono, direccion, email, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        valores = (nombre, apellido, dni, telefono, direccion, email, estado)

        try:
            nuevo_id = self.insertar(query, valores)

        except RegistroDuplicadoError as error:
            return False, str(error)

        return True, f"Cliente agregado correctamente (id={nuevo_id})"

    def baja(self, id_cliente):
        if not self.buscar_por_id(id_cliente):
            return False, "Cliente no encontrado"
        
        self.baja_logica(id_cliente)

        return True, "Cliente dado de baja"
    
    def modificar(self, id_cliente, nombre, apellido, dni, telefono, direccion, email=None, estado=True):
        if not self.buscar_por_id(id_cliente):
            return False, "Cliente no encontrado"
        
        valido, mensaje = self.validar_campos(nombre, apellido, dni, telefono, direccion, email)

        if not valido:
            return False, mensaje

        query = """
            UPDATE clientes
            SET nombre=%s, apellido=%s, dni=%s, telefono=%s, direccion=%s, email=%s, estado=%s
            WHERE id_cliente=%s
        """
        valores = (nombre, apellido, dni, telefono, direccion, email, estado, id_cliente)
        super().modificar(query, valores)

        return True, "Cliente modificado"