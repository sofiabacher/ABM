class Producto:
    def __init__(self, id_producto, nombre, categoria, precio, talle, color, estado):
        self.id_producto = id_producto
        self.nombre = nombre
        self.catgoria = categoria
        self.precio = precio
        self.talle = talle
        self.color = color
        self.estado = estado

    def __str__(self):
        return f"{self.id_producto} - {self.nombre}"