from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    razon_social: Optional[str] = None
    rfc: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None
    tipo_cliente: Optional[str] = "general"

class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class AutoparteCreate(BaseModel):
    sku: str
    nombre: str
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    categoria_id: Optional[int] = None
    precio: Decimal
    compatibilidad_vehicular: Optional[str] = None
    imagen_url: Optional[str] = None
    activo: bool = True
    stock_inicial: int = 0
    stock_minimo: int = 5

class AutoparteUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    categoria_id: Optional[int] = None
    precio: Optional[Decimal] = None
    compatibilidad_vehicular: Optional[str] = None
    imagen_url: Optional[str] = None
    activo: Optional[bool] = None

class InventarioUpdate(BaseModel):
    cantidad: int
    tipo: str = Field(..., pattern="^(entrada|salida|ajuste)$")
    motivo: Optional[str] = None

class DetallePedidoCreate(BaseModel):
    autoparte_id: int
    cantidad: int

class PedidoCreate(BaseModel):
    items: List[DetallePedidoCreate]
    notas: Optional[str] = None

class CambioEstatusRequest(BaseModel):
    estatus: str = Field(..., pattern="^(recibido|en_proceso|enviado|entregado|cancelado)$")
    comentario: Optional[str] = None

class EmpleadoCreate(BaseModel):
    email: str
    password: str
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    numero_empleado: str
    departamento: Optional[str] = None
    puesto: Optional[str] = None

class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    departamento: Optional[str] = None
    puesto: Optional[str] = None
    activo: Optional[bool] = None
