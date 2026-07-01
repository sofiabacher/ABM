import bcrypt

from services.base_service import BaseService, RegistroDuplicadoError
from models.usuario import Usuario
from models.enums import RolUsuario

class UsuarioService(BaseService):
    def __init__(self):
        super().__init__("usuarios", "id_usuario", Usuario)

    @staticmethod
    def _hashear_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    @staticmethod
    def verificar_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

    def validar_campos(self, nombre, apellido, email, rol, id_sucursal, password=None, requiere_password=True):
        if nombre.strip() == "":
            return False, "Debe completar el nombre"

        if apellido.strip() == "":
            return False, "Debe completar el apellido"

        if email.strip() == "" or "@" not in email:
            return False, "Debe ingresar un email válido"

        if requiere_password and (not password or len(password) < 6):
            return False, "La contraseña debe tener al menos 6 caracteres"

        try:
            RolUsuario(rol)
        except ValueError:
            return False, "Rol inválido"

        if not id_sucursal:
            return False, "Debe seleccionar una sucursal"

        return True, ""

    def alta(self, nombre, apellido, email, password, rol, id_sucursal, estado=True):
        valido, mensaje = self.validar_campos(nombre, apellido, email, rol, id_sucursal, password, requiere_password=True)

        if not valido:
            return False, mensaje

        password_hash = self._hashear_password(password)

        query = """
            INSERT INTO usuarios (nombre, apellido, email, password, rol, estado, id_sucursal)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        valores = (nombre, apellido, email, password_hash, rol, estado, id_sucursal)

        try:
            nuevo_id = self.insertar(query, valores)

        except RegistroDuplicadoError as error:
            return False, str(error)

        return True, f"Usuario agregado correctamente (id={nuevo_id})"

    def baja(self, id_usuario):
        if not self.buscar_por_id(id_usuario):
            return False, "Usuario no encontrado"

        self.baja_logica(id_usuario)

        return True, "Usuario dado de baja"

    def modificar(self, id_usuario, nombre, apellido, email, rol, id_sucursal, estado=True, password=None):
        usuario_actual = self.buscar_por_id(id_usuario)

        if not usuario_actual:
            return False, "Usuario no encontrado"

        valido, mensaje = self.validar_campos(nombre, apellido, email, rol, id_sucursal, password, requiere_password=False)

        if not valido:
            return False, mensaje

        password_hash = self._hashear_password(password) if password else usuario_actual.password

        query = """
            UPDATE usuarios
            SET nombre=%s, apellido=%s, email=%s, password=%s, rol=%s, estado=%s, id_sucursal=%s
            WHERE id_usuario=%s
        """
        valores = (nombre, apellido, email, password_hash, rol, estado, id_sucursal, id_usuario)
        
        super().modificar(query, valores)

        return True, "Usuario modificado"