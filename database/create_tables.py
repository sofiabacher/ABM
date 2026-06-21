from pathlib import Path
from connection import get_connection

def ejecutar_script(cursor, nombre_archivo):
    ruta = Path(__file__).parent / nombre_archivo

    with open(ruta, "r", encoding="utf-8") as archivo:
            script = archivo.read()

    sentencias = script.split(";")

    for sentencia in sentencias:
            sentencia = sentencia.strip()
            if sentencia:
                cursor.execute(sentencia)

def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        ejecutar_script(cursor, "schema.sql")
        ejecutar_script(cursor, "seed.sql")
        
        conn.commit()
        print("Base de datos inicializada correctamente")
    
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    crear_tablas()