from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class Compra:
    id_proveedor: int
    id_usuario: int
    id_sucursal: int
    total: Decimal
    num_comprobante: Optional[str] = None
    fecha: Optional[datetime] = None
    id_compra: Optional[int] = None

    @classmethod
    def from_row(cls, row):
        (id_compra, fecha, num_comprobante, total, id_proveedor, id_usuario, id_sucursal) = row
        
        return cls(
            id_compra=id_compra,
            fecha=fecha,
            num_comprobante=num_comprobante,
            total=total,
            id_proveedor=id_proveedor,
            id_usuario=id_usuario,
            id_sucursal=id_sucursal,
        )

    def to_dict(self):
        return {
            "id_compra": self.id_compra,
            "fecha": self.fecha,
            "num_comprobante": self.num_comprobante,
            "total": self.total,
            "id_proveedor": self.id_proveedor,
            "id_usuario": self.id_usuario,
            "id_sucursal": self.id_sucursal,
        }

    def __str__(self):
        return f"Compra {self.id_compra} - ${self.total}"
