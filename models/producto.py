from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class Producto:
    codigo: str
    nombre: str
    precio_compra: Decimal
    precio_venta: Decimal
    id_categoria: int
    descripcion: Optional[str] = None
    talle: Optional[str] = None
    color: Optional[str] = None
    stock_actual: int = 0
    stock_minimo: int = 0
    estado: bool = True
    id_producto: Optional[int] = None

    @classmethod
    def from_row(cls, row):
        (id_producto, codigo, nombre, descripcion, talle, color, precio_compra, precio_venta, stock_actual, stock_minimo, estado, id_categoria) = row
        
        return cls(
            id_producto=id_producto,
            codigo=codigo,
            nombre=nombre,
            descripcion=descripcion,
            talle=talle,
            color=color,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock_actual=stock_actual,
            stock_minimo=stock_minimo,
            estado=bool(estado),
            id_categoria=id_categoria,
        )

    def to_dict(self):
        return {
            "id_producto": self.id_producto,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "talle": self.talle,
            "color": self.color,
            "precio_compra": self.precio_compra,
            "precio_venta": self.precio_venta,
            "stock_actual": self.stock_actual,
            "stock_minimo": self.stock_minimo,
            "estado": self.estado,
            "id_categoria": self.id_categoria,
        }

    @property
    def necesita_reposicion(self) -> bool:   #Devuelve true si se cumple
        return self.stock_actual <= self.stock_minimo

    def __str__(self):
        return f"{self.id_producto} - {self.nombre}"
