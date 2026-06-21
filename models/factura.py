from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from models.enums import EstadoFactura, TipoFactura

@dataclass
class Factura:
    id_venta: int
    num_factura: str
    subtotal: Decimal
    impuestos: Decimal
    total: Decimal
    tipo_factura: TipoFactura = TipoFactura.B
    estado: EstadoFactura = EstadoFactura.EMITIDA
    fecha_emision: Optional[datetime] = None
    id_factura: Optional[int] = None

    @classmethod
    def from_row(cls, row):
        (id_factura, num_factura, tipo_factura, fecha_emision, subtotal, impuestos, total, estado, id_venta) = row
        
        return cls(
            id_factura=id_factura,
            num_factura=num_factura,
            tipo_factura=TipoFactura(tipo_factura),
            fecha_emision=fecha_emision,
            subtotal=subtotal,
            impuestos=impuestos,
            total=total,
            estado=EstadoFactura(estado),
            id_venta=id_venta,
        )

    def to_dict(self):
        return {
            "id_factura": self.id_factura,
            "num_factura": self.num_factura,
            "tipo_factura": self.tipo_factura.value,
            "fecha_emision": self.fecha_emision,
            "subtotal": self.subtotal,
            "impuestos": self.impuestos,
            "total": self.total,
            "estado": self.estado.value,
            "id_venta": self.id_venta,
        }

    def __str__(self):
        return f"Factura {self.num_factura}"
