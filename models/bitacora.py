from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Bitacora:
    accion: str
    tabla_afectada: str
    id_usuario: int
    descripcion: Optional[str] = None
    fecha_hora: Optional[datetime] = None
    id_bitacora: Optional[int] = None

    @classmethod
    def from_row(cls, row):
        (id_bitacora, accion, tabla_afectada, descripcion, fecha_hora, id_usuario) = row
        
        return cls(
            id_bitacora=id_bitacora,
            accion=accion,
            tabla_afectada=tabla_afectada,
            descripcion=descripcion,
            fecha_hora=fecha_hora,
            id_usuario=id_usuario,
        )

    def to_dict(self):
        return {
            "id_bitacora": self.id_bitacora,
            "accion": self.accion,
            "tabla_afectada": self.tabla_afectada,
            "descripcion": self.descripcion,
            "fecha_hora": self.fecha_hora,
            "id_usuario": self.id_usuario,
        }

    @classmethod
    def movimiento_stock(cls, id_usuario, id_producto, tipo_movimiento, cantidad, referencia=""):
        descripcion = (
            f"producto_id={id_producto} | tipo={tipo_movimiento} | "
            f"cantidad={cantidad} | referencia={referencia}"
        )
        
        return cls(
            accion="MOVIMIENTO_STOCK",
            tabla_afectada="productos",
            id_usuario=id_usuario,
            descripcion=descripcion,
        )

    def __str__(self):
        return f"[{self.fecha_hora}] {self.accion} sobre {self.tabla_afectada}"
