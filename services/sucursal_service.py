from services.base_service import BaseService, RegistroDuplicadoError
from models.sucursal import Sucursal

class SucursalService(BaseService):
    def __init__(self):
        super().__init__("sucursales", "id_sucursal", Sucursal)

    def validar_campos(self, nombre, direccion, ciudad, provincia, telefono, email):
        if nombre.strip() == "":
            return False, "Debe completar el nombre"

        if direccion.strip() == "":
            return False, "Debe completar la dirección"

        if ciudad.strip() == "":
            return False, "Debe completar la ciudad"

        if provincia.strip() == "":
            return False, "Debe completar la provincia"

        if telefono.strip() == "":
            return False, "Debe completar el teléfono"

        if email.strip() == "" or "@" not in email:
            return False, "Debe ingresar un email válido"

        return True, ""

    def alta(self, nombre, direccion, ciudad, provincia, telefono, email, estado=True):
        valido, mensaje = self.validar_campos(nombre, direccion, ciudad, provincia, telefono, email)

        if not valido:
            return False, mensaje

        query = """
            INSERT INTO sucursales (nombre, direccion, ciudad, provincia, telefono, email, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        valores = (nombre, direccion, ciudad, provincia, telefono, email, estado)

        try:
            nuevo_id = self.insertar(query, valores)
        except RegistroDuplicadoError as error:
            return False, str(error)

        return True, f"Sucursal agregada correctamente (id={nuevo_id})"

    def baja(self, id_sucursal):
        if not self.buscar_por_id(id_sucursal):
            return False, "Sucursal no encontrada"

        self.baja_logica(id_sucursal)

        return True, "Sucursal dada de baja"

    def modificar(self, id_sucursal, nombre, direccion, ciudad, provincia, telefono, email, estado=True):
        if not self.buscar_por_id(id_sucursal):
            return False, "Sucursal no encontrada"

        valido, mensaje = self.validar_campos(nombre, direccion, ciudad, provincia, telefono, email)

        if not valido:
            return False, mensaje

        query = """
            UPDATE sucursales
            SET nombre=%s, direccion=%s, ciudad=%s, provincia=%s, telefono=%s, email=%s, estado=%s
            WHERE id_sucursal=%s
        """
        valores = (nombre, direccion, ciudad, provincia, telefono, email, estado, id_sucursal)
        super().modificar(query, valores)

        return True, "Sucursal modificada"
