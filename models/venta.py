from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from models.enums import MetodoPago

@dataclass
class Venta:
    id_cliente: int
    id_usuario: int
    id_sucursal: int
    total: Decimal
    metodo_pago: MetodoPago = MetodoPago.EFECTIVO
    fecha: Optional[datetime] = None
    id_venta: Optional[int] = None

    @classmethod
    def from_row(cls, row):
        (id_venta, fecha, metodo_pago, total, id_cliente, id_usuario, id_sucursal) = row
        
        return cls(
            id_venta=id_venta,
            fecha=fecha,
            metodo_pago=MetodoPago(metodo_pago),
            total=total,
            id_cliente=id_cliente,
            id_usuario=id_usuario,
            id_sucursal=id_sucursal,
        )

    def to_dict(self):
        return {
            "id_venta": self.id_venta,
            "fecha": self.fecha,
            "metodo_pago": self.metodo_pago.value,
            "total": self.total,
            "id_cliente": self.id_cliente,
            "id_usuario": self.id_usuario,
            "id_sucursal": self.id_sucursal,
        }

    def __str__(self):
        return f"Venta {self.id_venta} - ${self.total}"
