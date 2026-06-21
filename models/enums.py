from enum import Enum

class RolUsuario(str, Enum):  #Roles definidos para usuarios del sistema
    ADMIN = "ADMIN"
    VENTAS = "VENTAS"
    COMPRAS = "COMPRAS"
    CONSULTA = "CONSULTA"

class EstadoFactura(str, Enum):
    EMITIDA = "EMITIDA"
    ANULADA = "ANULADA"

class TipoFactura(str, Enum):
    A = "A"
    B = "B"
    C = "C"

class MetodoPago(str, Enum):
    EFECTIVO = "EFECTIVO"
    DEBITO = "DEBITO"
    CREDITO = "CREDITO"
    TRANSFERENCIA = "TRANSFERENCIA"
