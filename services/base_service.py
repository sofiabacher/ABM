import mysql.connector
from database.connection import get_connection

class RegistroDuplicadoError(Exception):  #Por restricción unique
    pass

class BaseService:
    def __init__(self, tabla, columna_id, model_class=None):
        self.tabla = tabla
        self.columna_id = columna_id
        self.model_class = model_class

    def mapear(self, row):
        if row is None:
            return None
        
        if self.model_class is None:
            return row
        
        return self.model_class.from_row(row)
    
    def obtener_todos(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {self.tabla}")
        datos = cursor.fetchall()

        conn.close()
        return [self.mapear(fila) for fila in datos]
    
    def buscar_por_id(self, identificador):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT * FROM {self.tabla} WHERE {self.columna_id}=%s", 
            (identificador,)
        )

        dato = cursor.fetchone()

        conn.close()
        return self.mapear(dato)
    
    def baja_logica(self, identificador):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"UPDATE {self.tabla} SET estado=FALSE WHERE {self.columna_id}=%s",
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

        try:
            cursor.execute(query, valores)
            conn.commit()
            return cursor.lastrowid

        except mysql.connector.IntegrityError as error:
            conn.rollback()
            raise RegistroDuplicadoError(
                "Ya existe un registro con ese valor único"
                "(dni, cuit, email o código repetido)"
            ) from error

        finally:
            conn.close()