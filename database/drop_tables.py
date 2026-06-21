from connection import get_connection

def eliminar_tablas():
    conn = get_connection()
    cursor = conn.cursor()

    tablas = [
         "bitacora",
        "facturas",
        "detalle_venta",
        "detalle_compra",
        "ventas",
        "compras",
        "productos",
        "proveedores",
        "clientes",
        "usuarios",
        "categorias",
        "sucursales"
    ]

    try:
        cursor.execute("set foreign_key_checks = 0")

        for tabla in tablas:
            cursor.execute(f"drop table if exists {tabla}")
            print(f"Eliminada: {tabla}")
        
        cursor.execute("set foreign_key_checks = 1")

        conn.commit()
        print("Todas las tablas fueron eliminadas")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    eliminar_tablas()