from services.base_service import BaseService, RegistroDuplicadoError
from models.categoria import Categoria

class CategoriaService(BaseService):
    def __init__(self):
        super().__init__("categorias", "id_categora", Categoria)
    
    def validar_campos(self, nombre, descripcion=None):
        if nombre.strip() == "":
            return False, "Debe completar el nombre"
        
    def alta(self, nombre, descripcion=None):
        valido, mensaje = self.validar_campos(nombre, descripcion)

        if not valido:
            return False, mensaje
        
        query = "INSERT INTO categorias (nombre, descripcion) values  VALUES (%s, %s)"

        try:
            nuevo_id = self.insertar(query, (nombre, descripcion))
        
        except RegistroDuplicadoError as error:
            return False, str(error)
        
        return True, f"Categoría agregada correctamente (id={nuevo_id})"

def modificar(self, id_categoria, nombre, descripcion=None):
    if not self.buscar_por_id(id_categoria):
        return False, "Categoria no encontrada"
    
    valido, mensaje = self.validar_campos(nombre, descripcion)

    if not valido:
        return False, mensaje

    query = "UPDATE categorias SET nombre=%, descripcion=% WHERE id_categoria=%"
    super().modificar(query, (nombre, descripcion, id_categoria))

    return True, "Categoría modificada"