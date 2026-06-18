from connection import get_connection

def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()

    tablas = [
        "CREATE TABLE IF NOT EXISTS clientes(id INT PRIMARY KEY, nombre VARCHAR(50) NOT NULL, apellido VARCHAR(50) NOT NULL, dni VARCHAR(20) NOT NULL, direccion VARCHAR(150) NOT NULL, estado VARCHAR(20) NOT NULL)",
        "CREATE TABLE IF NOT EXISTS productos(id INT PRIMARY KEY, descripcion VARCHAR(50) NOT NULL, categoria VARCHAR(50) NOT NULL, precio DECIMAL(10,2) NOT NULL, talle VARCHAR(10) NOT NULL, color VARCHAR(20) NOT NULL, estado VARCHAR(20) NOT NULL)",
        "CREATE TABLE IF NOT EXISTS proveedores(id INT PRIMARY KEY, razon_social VARCHAR(100) NOT NULL, cuit VARCHAR(20) NOT NULL, direccion VARCHAR(150) NOT NULL, telefono VARCHAR(30) NOT NULL, email VARCHAR(100) NOT NULL, estado VARCHAR(20) NOT NULL)",
        "CREATE TABLE IF NOT EXISTS facturas(numero VARCHAR(20) PRIMARY KEY, tipo_factura VARCHAR(1) NOT NULL, fecha DATE NOT NULL, total DECIMAL(10,2) NOT NULL, estado_pago VARCHAR(20) NOT NULL, cliente VARCHAR(100) NOT NULL)",
        "CREATE TABLE IF NOT EXISTS detalle_factura(id INT PRIMARY KEY AUTO_INCREMENT, numero_factura VARCHAR(20) NOT NULL, producto VARCHAR(100) NOT NULL, cantidad INT NOT NULL, precio DECIMAL(10,2) NOT NULL, subtotal DECIMAL(10,2) NOT NULL)"
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