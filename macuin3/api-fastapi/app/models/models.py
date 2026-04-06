from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Rol(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(200))
    created_at = Column(DateTime, server_default=func.now())
    usuarios = relationship("Usuario", back_populates="rol")


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(20))
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    rol = relationship("Rol", back_populates="usuarios")
    cliente = relationship("Cliente", back_populates="usuario", uselist=False)
    empleado = relationship("Empleado", back_populates="usuario", uselist=False)


class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False)
    razon_social = Column(String(200))
    rfc = Column(String(20))
    direccion = Column(Text)
    ciudad = Column(String(100))
    estado = Column(String(100))
    codigo_postal = Column(String(10))
    tipo_cliente = Column(String(50), default="general")
    created_at = Column(DateTime, server_default=func.now())
    usuario = relationship("Usuario", back_populates="cliente")
    pedidos = relationship("Pedido", back_populates="cliente")


class Empleado(Base):
    __tablename__ = "empleados"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False)
    numero_empleado = Column(String(20), unique=True, nullable=False)
    departamento = Column(String(100))
    puesto = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    usuario = relationship("Usuario", back_populates="empleado")


class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    autopartes = relationship("Autoparte", back_populates="categoria")


class Autoparte(Base):
    __tablename__ = "autopartes"
    id = Column(Integer, primary_key=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    marca = Column(String(100))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    precio = Column(Numeric(12, 2), nullable=False)
    compatibilidad_vehicular = Column(Text)
    imagen_url = Column(String(500))
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    categoria = relationship("Categoria", back_populates="autopartes")
    inventario = relationship("Inventario", back_populates="autoparte", uselist=False)


class Inventario(Base):
    __tablename__ = "inventario"
    id = Column(Integer, primary_key=True)
    autoparte_id = Column(Integer, ForeignKey("autopartes.id", ondelete="CASCADE"), unique=True, nullable=False)
    stock_actual = Column(Integer, nullable=False, default=0)
    stock_minimo = Column(Integer, nullable=False, default=5)
    ubicacion_almacen = Column(String(50))
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    autoparte = relationship("Autoparte", back_populates="inventario")


class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"
    id = Column(Integer, primary_key=True)
    autoparte_id = Column(Integer, ForeignKey("autopartes.id"), nullable=False)
    tipo = Column(String(20), nullable=False)
    cantidad = Column(Integer, nullable=False)
    stock_anterior = Column(Integer, nullable=False)
    stock_nuevo = Column(Integer, nullable=False)
    motivo = Column(String(200))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    created_at = Column(DateTime, server_default=func.now())
    autoparte = relationship("Autoparte")
    usuario = relationship("Usuario")


class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True)
    folio = Column(String(20), unique=True, nullable=False, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    estatus = Column(String(20), nullable=False, default="recibido")
    subtotal = Column(Numeric(12, 2), nullable=False, default=0)
    impuesto = Column(Numeric(12, 2), nullable=False, default=0)
    total = Column(Numeric(12, 2), nullable=False, default=0)
    notas = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    cliente = relationship("Cliente", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido", cascade="all, delete-orphan")
    historial = relationship("HistorialEstatusPedido", back_populates="pedido", cascade="all, delete-orphan")


class DetallePedido(Base):
    __tablename__ = "detalle_pedido"
    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False)
    autoparte_id = Column(Integer, ForeignKey("autopartes.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(12, 2), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    pedido = relationship("Pedido", back_populates="detalles")
    autoparte = relationship("Autoparte")


class HistorialEstatusPedido(Base):
    __tablename__ = "historial_estatus_pedido"
    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False)
    estatus_anterior = Column(String(20))
    estatus_nuevo = Column(String(20), nullable=False)
    comentario = Column(Text)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    created_at = Column(DateTime, server_default=func.now())
    pedido = relationship("Pedido", back_populates="historial")
    usuario = relationship("Usuario")
