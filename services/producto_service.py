from services.base_service import BaseService, RegistroDuplicadoError
from models.producto import Producto

class ProductoService(BaseService):
    def __init__(self):
        super().__init__("productos", "id_producto", Producto)

    def validar_campos(self, codigo, nombre, precio_compra, precio_venta, id_categoria):
        if codigo.strip() == "":
            return False, "Debe completar el código"

        if nombre.strip() == "":
            return False, "Debe completar el nombre"

        try:
            precio_compra = float(precio_compra)
            precio_venta = float(precio_venta)

        except (TypeError, ValueError):
            return False, "Los precios deben ser numéricos"

        if precio_compra < 0 or precio_venta < 0:
            return False, "Los precios no pueden ser negativos"

        if not id_categoria:
            return False, "Debe seleccionar una categoría"

        return True, ""

    def alta(self, codigo, nombre, precio_compra, precio_venta, id_categoria, descripcion=None, talle=None, color=None, stock_actual=0, stock_minimo=0, estado=True):
        valido, mensaje = self.validar_campos(codigo, nombre, precio_compra, precio_venta, id_categoria)

        if not valido:
            return False, mensaje

        query = """
            INSERT INTO productos
                (codigo, nombre, descripcion, talle, color, precio_compra, precio_venta, stock_actual, stock_minimo, estado, id_categoria)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (codigo, nombre, descripcion, talle, color, precio_compra, precio_venta, stock_actual, stock_minimo, estado, id_categoria)

        try:
            nuevo_id = self.insertar(query, valores)

        except RegistroDuplicadoError as error:
            return False, str(error)

        return True, f"Producto agregado correctamente (id={nuevo_id})"

    def baja(self, id_producto):
        if not self.buscar_por_id(id_producto):
            return False, "Producto no encontrado"

        self.baja_logica(id_producto)

        return True, "Producto dado de baja"

    def modificar(self, id_producto, codigo, nombre, precio_compra, precio_venta, id_categoria, descripcion=None, talle=None, color=None, stock_minimo=0, estado=True):
        if not self.buscar_por_id(id_producto):
            return False, "Producto no encontrado"

        valido, mensaje = self.validar_campos(codigo, nombre, precio_compra, precio_venta, id_categoria)

        if not valido:
            return False, mensaje

        query = """
            UPDATE productos
            SET codigo=%s, nombre=%s, descripcion=%s, talle=%s, color=%s,
                precio_compra=%s, precio_venta=%s, stock_minimo=%s,
                estado=%s, id_categoria=%s
            WHERE id_producto=%s
        """
        valores = (codigo, nombre, descripcion, talle, color, precio_compra, precio_venta, stock_minimo, estado, id_categoria, id_producto)
        super().modificar(query, valores)

        return True, "Producto modificado"
