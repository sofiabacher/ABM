from datetime import datetime
from decimal import Decimal

from database.connection import get_connection
from models.bitacora import Bitacora

class FacturaService():
    IVA = Decimal("0,21")

    def obtener_clientes_activos(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id_cliente, nombre, apellido FROM clientes WHERE estado=TRUE")

        clientes = [
            f"{id_cliente} - {nombre} {apellido}"
            for id_cliente, nombre, apellido in cursor.fetchall()
        ]

        conn.close()
        return clientes
    
    def obtener_productos_activos(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id_producto, nombre, precio_venta, stock_actual FROM productos WHERE estado=TRUE")
        
        productos = {}

        for id_producto, nombre, precio_venta, stock_actual in cursor.fetchall():
            productos[f"{id_producto} - {nombre}"] = {
                "id_producto": id_producto,
                "precio": Decimal(precio_venta),
                "stock_actual": stock_actual
            }

        conn.close()
        return productos
    
    def generar_factura(self, id_cliente, id_usuario, id_sucursal, tipo_factura, metodo_pago, items_factura):
        if not items_factura:
            return False, "Debe agregar al menos un productos"
        
        subtotal = sum(item["subtotal"] for item in items_factura)
        impuestos = (subtotal * self.IVA).quantize(Decimal("0.01"))
        total = subtotal + impuestos

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO ventas ((metodo_pago, total, id_cliente, id_usuario, id_sucursal)
                VALUES (%s, %s, %s, %s, %s)
                """, 
                (metodo_pago, total, id_cliente, id_usuario, id_sucursal),
            )
            id_venta = cursor.lastrowid

            for item in items_factura:
                cursor.execute("""
                    INSERT INTO detalle_venta (cantidad, precio_unitario, subtotal, id_venta, id_producto)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (item["cantidad"], item["precio_unitario"], item["subtotal"],
                     id_venta, item["id_producto"]),
                )

                cursor.execute(
                    "UPDATE productos SET stock_actual = stock_actual - %s WHERE id_producto=%s",
                    (item["cantidad"], item["id_producto"]),
                )

                movimiento = Bitacora.movimiento_stock(
                    id_usuario=id_usuario,
                    id_producto=item["id_producto"],
                    tipo_movimiento="SALIDA_VENTA",
                    cantidad=item["cantidad"],
                    referencia=f"venta:{id_venta}",
                )

                cursor.execute("""
                    INSERT INTO bitacora (accion, tabla_afectada, descripcion, id_usuario)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (movimiento.accion, movimiento.tabla_afectada,
                     movimiento.descripcion, movimiento.id_usuario),
                )
            
            numero = f"FAC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            cursor.execute("""
                INSERT INTO facturas (num_factura, tipo_factura, subtotal, impuestos, total, id_venta)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (numero, tipo_factura, subtotal, impuestos, total, id_venta),
            )

            conn.commit()
            return True, f"Factura {numero} generada correctamente"
        
        except Exception as error:
            conn.rollback()
            return False, f"No se pudo generar la factura: {error}"
        
        finally:
            conn.close()

    def obtener_facturas(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute( """
            SELECT f.id_factura, f.num_factura, f.tipo_factura, f.fecha_emision, f.subtotal, f.impuestos, f.total, f.estado, f.id_venta, v.id_cliente
            FROM facturas f
            JOIN ventas v ON v.id_venta = f.id_venta
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