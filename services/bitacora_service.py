from database.connection import get_connection
from services.base_service import BaseService
from models.bitacora import Bitacora

class BitacoraService(BaseService):
    def __init__(self):
        super().__init__("bitacora", "id_bitacora", Bitacora)
    
    def registrar(self, accion, tabla_afectada, id_usuario, descripcion=None):
        query = """
            INSERT INTO bitacora (accion, tabla_afectada, descipcion, id_usuario)
            VALUES (%s, %s, %s, %s)
        """

        nuevo_id = self.insertar(query, (accion, tabla_afectada, descripcion, id_usuario))

        return True, f"Movimiento registrado (id={nuevo_id})"

    def listar_por_tabla(self, tabla_afectada):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM bitacora WHERE tabla_afectada=%s ORDER BY fecha_hora DESC",
            (tabla_afectada,)
        )
        datos = cursor.fetchall()

        conn.close()
        return [Bitacora.from_row(fila) for fila in datos]