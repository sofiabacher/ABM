from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Cliente:
    nombre: str
    apellido: str
    dni: str
    telefono: str
    direccion: str
    email: str
    estado: bool = True
    fecha_alta: Optional[datetime] = None
    id_cliente: Optional[int] = None

    @classmethod
    def from_row(cls, row):     #row = select * from clientes
        (id_cliente, nombre, apellido, dni, telefono, email, direccion, fecha_alta, estado) = row
        
        return cls(
            id_cliente=id_cliente,
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            telefono=telefono,
            direccion=direccion,
            email=email,
            fecha_alta=fecha_alta,
            estado=bool(estado),
        )

    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "email": self.email,
            "fecha_alta": self.fecha_alta,
            "estado": self.estado,
        }
    
    def __str__(self):
        return f"{self.id_cliente} - {self.nombre} - {self.apellido}"