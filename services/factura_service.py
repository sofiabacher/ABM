from datetime import datetime
from database.connection import get_connection

class FacturaService:
    def obtener_clientes_activos(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nombre, apellido FROM clientes WHERE estado='ACTIVO'
        """)

        clientes = [
            f"{id_cliente} - {nombre} {apellido}"
            for id_cliente, nombre, apellido
            in cursor.fetchall()
        ]

        conn.close()
        return clientes
    
    def obtener_productos_activos(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, descripcion, precio FROM productos WHERE estado='ACTIVO'
        """)

        productos = {}

        for id_producto, descripcion, precio in cursor.fetchall():
            productos[
                f"{id_producto} - {descripcion}"
            ] = float(precio)
        
        conn.close()
        return productos
    
    def generar_factura(self, cliente, tipo_factura, estado_pago, items_factura):
        numero = datetime.now().strftime("%Y%m%d%H%M%S")
        fecha = datetime.now().strftime("%d/%m/%Y")
        total = sum(item["subtotal"] for item in items_factura)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO facturas VALUES(%s,%s,%s,%s,%s,%s)
        """,(numero, tipo_factura, fecha, total, estado_pago, cliente)
        )

        for item in items_factura:
            cursor.execute("""
                INSERT INTO detalle_factura(numero_factura, producto, cantidad, precio, subtotal)
                VALUES(%s,%s,%s,%s,%s)
            """,(numero, item["poducto"], item["cantidad"], item["precio"], item["subtotal"])
            )
        
        conn.commit()
        conn.close()
        return True, "Factura generada correctamente"