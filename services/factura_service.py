from database.connection import get_connection

class FacturaService():
    def obtener_facturas(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT f.id_factura, f.num_factura, f.tipo_factura, f.fecha_emision, f.subtotal, f.impuestos, f.total, f.estado, f.id_venta, c.nombre, c.apellido
            FROM facturas f
            JOIN ventas   v ON v.id_venta   = f.id_venta
            JOIN clientes c ON c.id_cliente = v.id_cliente
            ORDER BY f.fecha_emision DESC
            """
        )

        facturas = cursor.fetchall()
        conn.close()
        return facturas

    def obtener_detalle(self, id_venta):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.nombre, dv.cantidad, dv.precio_unitario, dv.subtotal
            FROM detalle_venta dv
            JOIN productos p ON p.id_producto = dv.id_producto
            WHERE dv.id_venta=%s
            """,
            (id_venta,),
        )

        detalle = cursor.fetchall()
        conn.close()
        return detalle