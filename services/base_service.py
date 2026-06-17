from database.connection import get_connection

class BaseService:
    def __init__(self, tabla):
        self.tabla = tabla
    
    def obtener_todos(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {self.tabla}")
        datos = cursor.fetchall()

        conn.close()
        return datos
    
    def buscar_por_id(self, identificador):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {self.tabla} WHERE id=%s", 
            (identificador,)
        )

        dato = cursor.fetchone()

        conn.close()
        return dato
    
    def baja_logica(self, identificador):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"UPDATE {self.tabla} SET estado='BAJA' WHERE id=%s",
            (identificador,)
        )

        conn.commit()
        conn.close()

    def modificar(self, query, valores):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query, valores)
        conn.commit()
        conn.close()
    
    def insertar(self, query, valores):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query, valores)
        conn.commit()
        conn.close()
    