class DetalleFactura:
    def __init__(self, factura_id, producto_id, cantidad, precio_unidad, subtotal):
        self.factura_id = factura_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unidad = precio_unidad
        self.subtotal = subtotal