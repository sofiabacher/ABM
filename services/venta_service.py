from datetime import datetime
from decimal import Decimal

from database.connection import get_connection
from models.bitacora import Bitacora

class VentaService:
    IVA = Decimal("0.21")

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
                "id_producto":  id_producto,
                "precio": Decimal(str(precio_venta)),
                "stock_actual": stock_actual,
            }

        conn.close()
        return productos

    def registrar_venta(self, id_cliente, id_usuario, id_sucursal, tipo_factura, metodo_pago, items):
        if not items:
            return False, "Debe agregar al menos un producto"

        subtotal = sum(item["subtotal"] for item in items)
        impuestos = (subtotal * self.IVA).quantize(Decimal("0.01"))
        total = subtotal + impuestos

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO ventas (metodo_pago, total, id_cliente, id_usuario, id_sucursal)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (metodo_pago, total, id_cliente, id_usuario, id_sucursal),
            )

            id_venta = cursor.lastrowid

            for item in items:
                cursor.execute("""
                    INSERT INTO detalle_venta (cantidad, precio_unitario, subtotal, id_venta, id_producto)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (item["cantidad"], item["precio_unitario"], item["subtotal"], id_venta, item["id_producto"]),
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
                    (movimiento.accion, movimiento.tabla_afectada, movimiento.descripcion, movimiento.id_usuario),
                )

            num_factura = f"FAC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            cursor.execute("""
                INSERT INTO facturas (num_factura, tipo_factura, subtotal, impuestos, total, id_venta)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (num_factura, tipo_factura, subtotal, impuestos, total, id_venta),
            )

            conn.commit()
            return True, f"Venta #{id_venta} registrada — Factura {num_factura} generada"

        except Exception as error:
            conn.rollback()
            return False, f"No se pudo registrar la venta: {error}"

        finally:
            conn.close()

    def obtener_ventas(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT v.id_venta, v.fecha, v.metodo_pago, v.total, c.nombre, c.apellido, f.num_factura
            FROM ventas v
            JOIN clientes c  ON c.id_cliente = v.id_cliente
            LEFT JOIN facturas f ON f.id_venta  = v.id_venta
            ORDER BY v.fecha DESC
            """
        )

        ventas = cursor.fetchall()
        conn.close()
        return ventas

    def obtener_detalle_venta(self, id_venta):
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