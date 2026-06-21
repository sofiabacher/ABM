from dataclasses import dataclass
from typing import Optional

from models.enums import RolUsuario

@dataclass
class Usuario:
    nombre: str
    apellido: str
    email: str
    password: str
    id_sucursal: int
    rol: RolUsuario = RolUsuario.CONSULTA
    estado: bool = True
    id_usuario: Optional[int] = None

    @classmethod
    def from_row(cls, row):
        (id_usuario, nombre, apellido, email, password, rol, estado, id_sucursal) = row
        
        return cls(
            id_usuario=id_usuario,
            nombre=nombre,
            apellido=apellido,
            email=email,
            password=password,
            rol=RolUsuario(rol),
            estado=bool(estado),
            id_sucursal=id_sucursal,
        )

    def to_dict(self):
        # password NUNCA se expone fuera del modelo.
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "rol": self.rol.value,
            "estado": self.estado,
            "id_sucursal": self.id_sucursal,
        }

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol.value})"
