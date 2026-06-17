from services.base_service import BaseService

class ProveedorService(BaseService):
    def __init__(self):
        super().__init__("proveedores")
    
    def validar_campos(self, identificador, razon_social, cuit, direccion, telefono, email):
        if identificador.strip() == "":
            return False, "Debe ingresar un identificador"
    
        if not identificador.isdigit():
            return False, "El identificador debe ser numérico"

        if razon_social.strip() == "":
            return False, "Debe completar la razon_social"
        
        if cuit.strip() == "":
            return False, "Debe ingresar un cuit"
    
        if not cuit.isdigit():
            return False, "El cuit debe ser numérico"
        
        if direccion.strip() == "":
            return False, "Debe completar el direccion"
        
        if telefono.strip() == "":
            return False, "Debe completar el telefono"
        
        if email.strip() == "":
            return False, "Debe completar el email"
        
        return True, ""

    def alta(self, identificador, razon_social, cuit, direccion, telefono, email, estado):
        if self.buscar_por_id(identificador):
            return False, "El identificador ya existe"
        
        valido, mensaje = self.validar_campos(identificador, razon_social, cuit, direccion, telefono, email)
        
        if not valido:
            return False, mensaje
        
        query = """
            INSERT INTO proveedores VALUES(%s,%s,%s,%s,%s,%s,%s)
        """
        valores = (identificador, razon_social, cuit, direccion, telefono, email, estado)

        self.insertar(query, valores)

        return True, "Proveedor agregado correctamente"
    
    def baja(self, identificador):
        if not self.buscar_por_id(identificador):
            return False, "Proveedor no encontrado"
        
        self.baja_logica(identificador)
    
        return True, "Proveedor dado de baja"
        
    def modificar(self, identificador, razon_social, cuit, direccion, telefono, email, estado):
        if not self.buscar_por_id(identificador):
            return False, "Proveedor no encontrado"
        
        valido, mensaje = self.validar_campos(identificador, razon_social, cuit, direccion, telefono, email)
        
        if not valido:
            return False, mensaje
        
        query = """
            UPDATE proveedores 
            SET        
                razon_social=%s,
                cuit=%s,
                direccion=%s,
                telefono=%s,
                email=%s,
                estado=%s
            WHERE id=%s
        """
        valores = (razon_social, cuit, direccion, telefono, email, identificador)

        super().modificar(query, valores)
    
        return True, "Producto modificado"