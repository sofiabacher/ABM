from database.connection import get_connection
from models.usuario import Usuario
from services.usuario_service import UsuarioService

class AuthService:
    _usuario_service = UsuarioService()

    def login(self, email: str, password: str) -> tuple[bool, str, Usuario | None]:
        if not email or not password:
            return False, "Debe completar email y contraseña", None
        
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT * FROM usuarios WHERE email=%s",
                (email.strip(),)
            )
            row = cursor.fetchone()
        
        finally:
            conn.close()
        
        if row is None:
            return False, "Credenciales incorrectas", None

        usuario = Usuario.from_row(row)

        if not usuario.estado:
            return False, "Usuario inactivo. Contacte al administrador", None

        if not self._usuario_service.verificar_password(password, usuario.password):
            return False, "Credenciales incorrectas", None

        return True, "", usuario