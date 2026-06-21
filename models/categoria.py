from dataclasses import dataclass
from typing import Optional

@dataclass
class Categoria:
    nombre: str
    descripcion: Optional[str] = None
    id_categoria: Optional[int] = None

    @classmethod
    def from_row(cls, row):
        id_categoria, nombre, descripcion = row
        return cls(
            id_categoria=id_categoria,
            nombre=nombre,
            descripcion=descripcion,
        )

    def to_dict(self):
        return {
            "id_categoria": self.id_categoria,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
        }

    def __str__(self):
        return self.nombre
