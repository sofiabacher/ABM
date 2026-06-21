from dataclasses import dataclass
from typing import Optional

@dataclass
class Sucursal:
    nombre: str
    direccion: str
    ciudad: str
    provincia: str
    telefono: str
    email: str
    estado: bool = True
    id_sucursal: Optional[int] = None

    @classmethod
    def from_row(cls, row):
        (id_sucursal, nombre, direccion, ciudad, provincia, telefono, email, estado) = row
        
        return cls(
            id_sucursal=id_sucursal,
            nombre=nombre,
            direccion=direccion,
            ciudad=ciudad,
            provincia=provincia,
            telefono=telefono,
            email=email,
            estado=bool(estado),
        )

    def to_dict(self):
        return {
            "id_sucursal": self.id_sucursal,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "provincia": self.provincia,
            "telefono": self.telefono,
            "email": self.email,
            "estado": self.estado,
        }

    def __str__(self):
        return self.nombre
