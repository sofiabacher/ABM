class Factura:
    def __init__(self, id_factura, tipo, fecha, total, estado, cliente_id):
        self.id_factura = id_factura
        self.tipo = tipo
        self.fecha = fecha
        self.total = total
        self.estado = estado
        self.cliente_id = cliente_id

    def __str__(self):
        return f"Factura {self.id_factura}"