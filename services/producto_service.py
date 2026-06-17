from services.base_service import BaseService

class ProductoService(BaseService):
    def __init__(self):
        super().__init__("productos")

    def validar_campos(self, identificador, descripcion, categoria, precio):
        if identificador.strip() == "":
            return False, "Debe ingresar un identificador"
    
        if not identificador.isdigit():
            return False, "El identificador debe ser numérico"

        if descripcion.strip() == "":
            return False, "Debe completar la descripcion"
        
        if categoria.strip() == "":
            return False, "Debe completar el categoria"
        
        if precio.strip() == "":
            return False, "Debe completar el precio"
        
        try:
            float(precio)
        except ValueError:
            return False, "El precio debe ser numérico"
        
        return True, ""

    def alta(self, identificador, descripcion, categoria, precio, talle, color, estado):
        if self.buscar_por_id(identificador):
            return False, "El identificador ya existe"
        
        valido, mensaje = self.validar_campos(identificador, descripcion, categoria, precio)
        
        if not valido:
            return False, mensaje
        
        query = """
            INSERT INTO productos VALUES(%s,%s,%s,%s,%s,%s,%s)
        """
        valores = (identificador, descripcion, categoria, precio, talle, color, estado)
        
        self.insertar(query, valores)

        return True, "Producto agregado correctamente"
    
    def baja(self, identificador):
        if not self.buscar_por_id(identificador):
            return False, "Producto no encontrado"
        
        self.baja_logica(identificador)
    
        return True, "Producto dado de baja"
        
    def modificar(self, identificador, descripcion, categoria, precio, talle, color, estado):
        if not self.buscar_por_id(identificador):
            return False, "Producto no encontrado"
        
        valido, mensaje = self.validar_campos(identificador, descripcion, categoria, precio)
        
        if not valido:
            return False, mensaje
        
        query = """
            UPDATE productos 
            SET        
                descripcion=%s,
                categoria=%s,
                precio=%s,
                talle=%s,
                color=%s,
                estado=%s
            WHERE id=%s
        """
        valores = (descripcion, categoria, precio, talle, color, estado, identificador)

        super().modificar(query, valores)
    
        return True, "Producto modificado"