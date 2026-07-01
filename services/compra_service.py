from datetime import datetime
from decimal import Decimal

from database.connection import get_connection
from models.bitacora import Bitacora

class CompraService:
    def obtener_proveedores_activos(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id_proveedor, razon_social FROM proveedores WHERE estado=TRUE")

        proveedores = [
            f"{id_proveedor} - {razon_social}"
            for id_proveedor, razon_social in cursor.fetchall()
        ]

        conn.close()
        return proveedores
    
    def obtener_productos_activos(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id_producto, nombre, precio_compra, stock_actual FROM productos WHERE estado=TRUE")
        
        productos = {}

        for id_producto, nombre, precio_compra, stock_actual in cursor.fetchall():
            productos[f"{id_producto} - {nombre}"] = {
                "id_producto":  id_producto,
                "precio": Decimal(precio_compra),
                "stock_actual": stock_actual,
            }

        conn.close()
        return productos
    
    def registrar_compra(self, id_proveedor, id_usuario, id_sucursal, num_comprobante, items):
        if not items:
            return False, "Debe agregar al menos un producto"

        total = sum(item["subtotal"] for item in items)

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO compras (num_comprobante, total, id_proveedor, id_usuario, id_sucursal)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (num_comprobante or None, total, id_proveedor, id_usuario, id_sucursal),
            )

            id_compra = cursor.lastrowid

            for item in items:
                cursor.execute("""
                    INSERT INTO detalle_compra (cantidad, precio_unitario, subtotal, id_compra, id_producto)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (item["cantidad"], item["precio_unitario"], item["subtotal"], id_compra, item["id_producto"]),
                )

                cursor.execute(
                    "UPDATE productos SET stock_actual = stock_actual + %s WHERE id_producto=%s",
                    (item["cantidad"], item["id_producto"]),
                )

                movimiento = Bitacora.movimiento_stock(
                    id_usuario=id_usuario,
                    id_producto=item["id_producto"],
                    tipo_movimiento="ENTRADA_COMPRA",
                    cantidad=item["cantidad"],
                    referencia=f"compra:{id_compra}",
                )

                cursor.execute("""
                    INSERT INTO bitacora (accion, tabla_afectada, descripcion, id_usuario)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (movimiento.accion, movimiento.tabla_afectada, movimiento.descripcion, movimiento.id_usuario),
                )

            conn.commit()
            return True, f"Compra #{id_compra} registrada correctamente (total: ${total:.2f})"

        except Exception as error:
            conn.rollback()
            return False, f"No se pudo registrar la compra: {error}"

        finally:
            conn.close()

    def obtener_compras(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id_compra, c.num_comprobante, c.fecha, c.total, p.razon_social FROM compras c
            JOIN proveedores p ON p.id_proveedor = c.id_proveedor
            ORDER BY c.fecha DESC
            """
        )

        compras = cursor.fetchall()
        conn.close()
        return compras

    def obtener_detalle_compra(self, id_compra):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT pr.nombre, dc.cantidad, dc.precio_unitario, dc.subtotal FROM detalle_compra dc
            JOIN productos pr ON pr.id_producto = dc.id_producto
            WHERE dc.id_compra=%s
            """,
            (id_compra,),
        )

        detalle = cursor.fetchall()
        conn.close()
        return detalle