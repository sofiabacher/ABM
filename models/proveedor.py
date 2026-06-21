from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Proveedor:
    razon_social: str
    cuit: str
    email: str
    telefono: str
    provincia: str
    direccion: str
    estado: bool = True
    fecha_alta: Optional[datetime] = None
    id_proveedor: Optional[int] = None

    @classmethod
    def from_row(cls, row):
        (id_proveedor, razon_social, cuit, email, telefono, provincia, direccion, fecha_alta, estado) = row
        
        return cls(
            id_proveedor=id_proveedor,
            razon_social=razon_social,
            cuit=cuit,
            email=email,
            telefono=telefono,
            provincia=provincia,
            direccion=direccion,
            fecha_alta=fecha_alta,
            estado=bool(estado),
        )

    def to_dict(self):
        return {
            "id_proveedor": self.id_proveedor,
            "razon_social": self.razon_social,
            "cuit": self.cuit,
            "email": self.email,
            "telefono": self.telefono,
            "provincia": self.provincia,
            "direccion": self.direccion,
            "fecha_alta": self.fecha_alta,
            "estado": self.estado,
        }

    def __str__(self):
        return f"{self.id_proveedor} - {self.razon_social}"
