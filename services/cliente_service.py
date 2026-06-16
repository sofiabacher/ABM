from services.base_service import BaseService

class ClienteService(BaseService):
    def __init__(self):
        super().__init__("clientes")

    def validar_campos(self, identificador, nombre, apellido, dni, direccion):
        if identificador.strip() == "":
            return False, "Debe ingresar un identificador"
    
        if not identificador.isDigit():
            return False, "El identificador debe ser numérico"

        if nombre.strip() == "":
            return False, "Debe completar el nombre"
        
        if apellido.strip() == "":
            return False, "Debe completar el apellido"
        
        if dni.strip() == "":
            return False, "Debe completar el dni"
        
        if not dni.isDigit():
            return False, "El dni debe ser numérico"
        
        if direccion.strip() == "":
            return False, "Debe completar el direccion"
        
        return True, ""

    def alta(self, identificador, nombre, apellido, dni, direccion, estado):
        if self.buscar_por_id(identificador):
            return False, "El identificador ya existe"

        query = """
            INSERT INTO clientes VALUES(%s,%s,%s,%s,%s,%s)
        """
        valores = (identificador, nombre, apellido, dni, direccion, estado)
        
        self.insertar(query, valores)

        return True, "Cliente agregado correctamente"
    
    def baja(self, identificador):
        if not self.buscar_por_id(identificador):
            return False, "Cliente no encontrado"
        
        self.baja_logica(identificador)
    
        return True, "Cliente dado de baja"
        
    def modificar(self, identificador, nombre, apellido, dni, direccion, estado):
        if not self.buscar_por_id(identificador):
            return False, "Cliente no encontrado"
        
        query = """
            UPDATE clientes 
            SET        
                nombre=%s,
                apellido=%s,
                dni=%s,
                direccion=%s,
                estado=%s
            WHERE id=%s
        """
        valores = (nombre,  apellido, dni, direccion, estado, identificador)

        super().modificar(query, valores)
    
        return True, "Cliente modificado"