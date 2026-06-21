from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class DetalleCompra:
    id_compra: int
    id_producto: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    id_detalle_compra: Optional[int] = None

    @classmethod
    def from_row(cls, row):
        (id_detalle_compra, cantidad, precio_unitario, subtotal, id_compra, id_producto) = row
        
        return cls(
            id_detalle_compra=id_detalle_compra,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal,
            id_compra=id_compra,
            id_producto=id_producto,
        )

    def to_dict(self):
        return {
            "id_detalle_compra": self.id_detalle_compra,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "subtotal": self.subtotal,
            "id_compra": self.id_compra,
            "id_producto": self.id_producto,
        }
