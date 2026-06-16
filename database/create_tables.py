from connection import get_connection

def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()

    tablas = [
        "CREATE TABLE IF NOT EXISTS clientes(id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, apellido TEXT NOT NULL, dni TEXT NOT NULL, direccion TEXT NOT NULL, estado TEXT NOT NULL)",
        "CREATE TABLE IF NOT EXISTS productos(id INTEGER PRIMARY KEY AUTO_INCREMENT, descripcion TEXT NOT NULL, categoria TEXT NOT NULL, precio REAL NOT NULL, talle TEXT NOT NULL, color TEXT NOT NULL, estado TEXT NOT NULL)",
        "CREATE TABLE IF NOT EXISTS proveedores(id INTEGER PRIMARY KEY AUTO_INCREMENT, razon_social TEXT NOT NULL, cuit TEXT NOT NULL, direccion TEXT NOT NULL, telefono TEXT NOT NULL, email TEXT NOT NULL, estado TEXT NOT NULL)",
        "CREATE TABLE IF NOT EXISTS facturas(numero INTEGER PRIMARY KEY, tipo_factura TEXT NOT NULL, fecha TEXT NOT NULL, total REAL NOT NULL, estado_pago TEXT NOT NULL, cliente TEXT NOT NULL)",
        "CREATE TABLE IF NOT EXISTS detalle_factura(id INTEGER PRIMARY KEY AUTO_INCREMENT, numero_factura TEXT NOT NULL, producto TEXT NOT NULL, cantidad INTEGER NOT NULL, precio REAL NOT NULL, subtotal REAL NOT NULL)"
    ]

    for tabla in tablas:
        try:
            cursor.execute(tabla)
            print(f"Ejecutado correctamente: {tabla[:30]}...")
        except Exception as e:
            print(f"Error al crear tabla: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()

    print("Proceso finalizado")

crear_tablas()