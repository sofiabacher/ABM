from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class DetalleVenta:
    id_venta: int
    id_producto: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    id_detalle_venta: Optional[int] = None

    @classmethod
    def from_row(cls, row):
        (id_detalle_venta, cantidad, precio_unitario, subtotal, id_venta, id_producto) = row
        
        return cls(
            id_detalle_venta=id_detalle_venta,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal,
            id_venta=id_venta,
            id_producto=id_producto,
        )

    def to_dict(self):
        return {
            "id_detalle_venta": self.id_detalle_venta,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "subtotal": self.subtotal,
            "id_venta": self.id_venta,
            "id_producto": self.id_producto,
        }
