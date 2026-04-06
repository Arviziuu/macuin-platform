from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from fastapi import HTTPException
from decimal import Decimal
from datetime import datetime
import io

from app.models.models import (
    Usuario, Rol, Cliente, Empleado, Categoria, Autoparte,
    Inventario, MovimientoInventario, Pedido, DetallePedido, HistorialEstatusPedido
)
from app.core.security import hash_password, verify_password, create_access_token


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    if not user.activo:
        raise HTTPException(status_code=403, detail="Cuenta desactivada")
    token = create_access_token({"sub": str(user.id), "rol": user.rol.nombre})
    return {"access_token": token, "token_type": "bearer", "user": _user_dict(user)}


def register_cliente(db: Session, data):
    if db.query(Usuario).filter(Usuario.email == data.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    rol = db.query(Rol).filter(Rol.nombre == "cliente_externo").first()
    if not rol:
        raise HTTPException(status_code=500, detail="Rol cliente_externo no encontrado")
    usuario = Usuario(email=data.email, password_hash=hash_password(data.password),
                      nombre=data.nombre, apellido=data.apellido, telefono=data.telefono, rol_id=rol.id, activo=True)
    db.add(usuario)
    db.flush()
    cliente = Cliente(usuario_id=usuario.id, razon_social=data.razon_social, rfc=data.rfc,
                      direccion=data.direccion, ciudad=data.ciudad, estado=data.estado,
                      codigo_postal=data.codigo_postal, tipo_cliente=data.tipo_cliente or "general")
    db.add(cliente)
    db.commit()
    db.refresh(usuario)
    token = create_access_token({"sub": str(usuario.id), "rol": rol.nombre})
    return {"access_token": token, "token_type": "bearer", "user": _user_dict(usuario)}


def _user_dict(user):
    return {"id": user.id, "email": user.email, "nombre": user.nombre, "apellido": user.apellido,
            "telefono": user.telefono, "rol": {"id": user.rol.id, "nombre": user.rol.nombre}, "activo": user.activo}


# ===== CATEGORIAS =====
def get_categorias(db: Session):
    return [{"id": c.id, "nombre": c.nombre, "descripcion": c.descripcion, "activo": c.activo}
            for c in db.query(Categoria).filter(Categoria.activo == True).all()]

def create_categoria(db: Session, data):
    cat = Categoria(nombre=data.nombre, descripcion=data.descripcion)
    db.add(cat); db.commit(); db.refresh(cat)
    return {"id": cat.id, "nombre": cat.nombre, "descripcion": cat.descripcion, "activo": cat.activo}


# ===== AUTOPARTES =====
def _autoparte_dict(db, a):
    inv = db.query(Inventario).filter(Inventario.autoparte_id == a.id).first()
    return {"id": a.id, "sku": a.sku, "nombre": a.nombre, "descripcion": a.descripcion,
            "marca": a.marca, "categoria_id": a.categoria_id,
            "categoria_nombre": a.categoria.nombre if a.categoria else None,
            "precio": float(a.precio), "compatibilidad_vehicular": a.compatibilidad_vehicular,
            "imagen_url": a.imagen_url, "activo": a.activo,
            "stock_actual": inv.stock_actual if inv else 0, "stock_minimo": inv.stock_minimo if inv else 0}

def get_autopartes(db: Session, search=None, categoria_id=None, marca=None, solo_activos=True):
    q = db.query(Autoparte)
    if solo_activos: q = q.filter(Autoparte.activo == True)
    if search:
        q = q.filter((Autoparte.nombre.ilike(f"%{search}%")) | (Autoparte.sku.ilike(f"%{search}%")) |
                      (Autoparte.descripcion.ilike(f"%{search}%")) | (Autoparte.compatibilidad_vehicular.ilike(f"%{search}%")))
    if categoria_id: q = q.filter(Autoparte.categoria_id == categoria_id)
    if marca: q = q.filter(Autoparte.marca.ilike(f"%{marca}%"))
    return [_autoparte_dict(db, a) for a in q.order_by(Autoparte.nombre).all()]

def get_autoparte(db: Session, aid: int):
    a = db.query(Autoparte).filter(Autoparte.id == aid).first()
    if not a: raise HTTPException(404, "Autoparte no encontrada")
    return _autoparte_dict(db, a)

def create_autoparte(db: Session, data):
    if db.query(Autoparte).filter(Autoparte.sku == data.sku).first():
        raise HTTPException(400, "SKU ya existe")
    a = Autoparte(sku=data.sku, nombre=data.nombre, descripcion=data.descripcion, marca=data.marca,
                  categoria_id=data.categoria_id, precio=data.precio, compatibilidad_vehicular=data.compatibilidad_vehicular,
                  imagen_url=data.imagen_url, activo=data.activo)
    db.add(a); db.flush()
    inv = Inventario(autoparte_id=a.id, stock_actual=data.stock_inicial, stock_minimo=data.stock_minimo)
    db.add(inv); db.commit(); db.refresh(a)
    return get_autoparte(db, a.id)

def update_autoparte(db: Session, aid: int, data):
    a = db.query(Autoparte).filter(Autoparte.id == aid).first()
    if not a: raise HTTPException(404, "Autoparte no encontrada")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(a, k, v)
    db.commit(); db.refresh(a)
    return get_autoparte(db, a.id)

def delete_autoparte(db: Session, aid: int):
    a = db.query(Autoparte).filter(Autoparte.id == aid).first()
    if not a: raise HTTPException(404, "Autoparte no encontrada")
    a.activo = False; db.commit()
    return {"message": "Autoparte desactivada"}


# ===== INVENTARIO =====
def get_inventario(db: Session):
    return [{"id": inv.id, "autoparte_id": inv.autoparte_id,
             "autoparte_nombre": inv.autoparte.nombre if inv.autoparte else None,
             "autoparte_sku": inv.autoparte.sku if inv.autoparte else None,
             "stock_actual": inv.stock_actual, "stock_minimo": inv.stock_minimo,
             "ubicacion_almacen": inv.ubicacion_almacen}
            for inv in db.query(Inventario).all()]

def update_inventario(db: Session, autoparte_id: int, data, usuario_id: int):
    inv = db.query(Inventario).filter(Inventario.autoparte_id == autoparte_id).first()
    if not inv: raise HTTPException(404, "Inventario no encontrado")
    old = inv.stock_actual
    if data.tipo == "entrada": inv.stock_actual += data.cantidad
    elif data.tipo == "salida":
        if inv.stock_actual < data.cantidad: raise HTTPException(400, "Stock insuficiente")
        inv.stock_actual -= data.cantidad
    else: inv.stock_actual = data.cantidad
    db.add(MovimientoInventario(autoparte_id=autoparte_id, tipo=data.tipo, cantidad=data.cantidad,
                                 stock_anterior=old, stock_nuevo=inv.stock_actual, motivo=data.motivo, usuario_id=usuario_id))
    db.commit()
    return {"stock_actual": inv.stock_actual, "message": "Inventario actualizado"}


# ===== EMPLEADOS =====
def get_empleados(db: Session):
    emps = db.query(Empleado).all()
    result = []
    for e in emps:
        u = e.usuario
        result.append({"id": e.id, "usuario_id": u.id, "email": u.email, "nombre": u.nombre, "apellido": u.apellido,
                        "telefono": u.telefono, "numero_empleado": e.numero_empleado, "departamento": e.departamento,
                        "puesto": e.puesto, "activo": u.activo})
    return result

def create_empleado(db: Session, data):
    if db.query(Usuario).filter(Usuario.email == data.email).first():
        raise HTTPException(400, "Email ya registrado")
    if db.query(Empleado).filter(Empleado.numero_empleado == data.numero_empleado).first():
        raise HTTPException(400, "Número de empleado ya existe")
    rol = db.query(Rol).filter(Rol.nombre == "personal_interno").first()
    u = Usuario(email=data.email, password_hash=hash_password(data.password), nombre=data.nombre,
                apellido=data.apellido, telefono=data.telefono, rol_id=rol.id, activo=True)
    db.add(u); db.flush()
    e = Empleado(usuario_id=u.id, numero_empleado=data.numero_empleado, departamento=data.departamento, puesto=data.puesto)
    db.add(e); db.commit(); db.refresh(e)
    return get_empleados(db)[-1]

def update_empleado(db: Session, eid: int, data):
    e = db.query(Empleado).filter(Empleado.id == eid).first()
    if not e: raise HTTPException(404, "Empleado no encontrado")
    u = e.usuario
    d = data.model_dump(exclude_unset=True)
    if "nombre" in d: u.nombre = d["nombre"]
    if "apellido" in d: u.apellido = d["apellido"]
    if "telefono" in d: u.telefono = d["telefono"]
    if "departamento" in d: e.departamento = d["departamento"]
    if "puesto" in d: e.puesto = d["puesto"]
    if "activo" in d: u.activo = d["activo"]
    db.commit()
    return {"message": "Empleado actualizado"}

def delete_empleado(db: Session, eid: int):
    e = db.query(Empleado).filter(Empleado.id == eid).first()
    if not e: raise HTTPException(404, "Empleado no encontrado")
    e.usuario.activo = False; db.commit()
    return {"message": "Empleado desactivado"}


# ===== PEDIDOS =====
def _gen_folio(db):
    y = datetime.now().year
    last = db.query(Pedido).filter(Pedido.folio.like(f"PED-{y}-%")).order_by(desc(Pedido.id)).first()
    n = int(last.folio.split("-")[-1]) + 1 if last else 1
    return f"PED-{y}-{n:04d}"

def create_pedido(db: Session, data, usuario_id: int):
    cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario_id).first()
    if not cliente: raise HTTPException(400, "Perfil de cliente no encontrado")
    if not data.items: raise HTTPException(400, "Agrega al menos un producto")
    folio = _gen_folio(db)
    subtotal = Decimal("0"); detalles = []
    for item in data.items:
        ap = db.query(Autoparte).filter(Autoparte.id == item.autoparte_id, Autoparte.activo == True).first()
        if not ap: raise HTTPException(404, f"Autoparte {item.autoparte_id} no encontrada")
        inv = db.query(Inventario).filter(Inventario.autoparte_id == item.autoparte_id).first()
        if not inv or inv.stock_actual < item.cantidad: raise HTTPException(400, f"Stock insuficiente: {ap.nombre}")
        s = ap.precio * item.cantidad; subtotal += s
        detalles.append({"autoparte_id": item.autoparte_id, "cantidad": item.cantidad, "precio_unitario": ap.precio, "subtotal": s})
        inv.stock_actual -= item.cantidad
        db.add(MovimientoInventario(autoparte_id=item.autoparte_id, tipo="salida", cantidad=item.cantidad,
                                     stock_anterior=inv.stock_actual + item.cantidad, stock_nuevo=inv.stock_actual,
                                     motivo=f"Pedido {folio}", usuario_id=usuario_id))
    imp = subtotal * Decimal("0.16"); total = subtotal + imp
    pedido = Pedido(folio=folio, cliente_id=cliente.id, estatus="recibido", subtotal=subtotal, impuesto=imp, total=total, notas=data.notas)
    db.add(pedido); db.flush()
    for d in detalles: db.add(DetallePedido(pedido_id=pedido.id, **d))
    db.add(HistorialEstatusPedido(pedido_id=pedido.id, estatus_nuevo="recibido", comentario="Pedido creado", usuario_id=usuario_id))
    db.commit()
    return _pedido_dict(db, pedido)

def get_pedidos(db, cliente_id=None, estatus=None):
    q = db.query(Pedido)
    if cliente_id: q = q.filter(Pedido.cliente_id == cliente_id)
    if estatus: q = q.filter(Pedido.estatus == estatus)
    return [_pedido_dict(db, p, False) for p in q.order_by(desc(Pedido.created_at)).all()]

def get_pedido(db, pid):
    p = db.query(Pedido).filter(Pedido.id == pid).first()
    if not p: raise HTTPException(404, "Pedido no encontrado")
    return _pedido_dict(db, p)

def get_pedidos_cliente(db, usuario_id):
    c = db.query(Cliente).filter(Cliente.usuario_id == usuario_id).first()
    if not c: raise HTTPException(400, "Cliente no encontrado")
    return get_pedidos(db, cliente_id=c.id)

def cambiar_estatus(db, pid, nuevo, comentario, uid):
    p = db.query(Pedido).filter(Pedido.id == pid).first()
    if not p: raise HTTPException(404, "Pedido no encontrado")
    trans = {"recibido": ["en_proceso", "cancelado"], "en_proceso": ["enviado", "cancelado"],
             "enviado": ["entregado"], "entregado": [], "cancelado": []}
    if nuevo not in trans.get(p.estatus, []): raise HTTPException(400, f"Transición inválida: {p.estatus} → {nuevo}")
    if nuevo == "cancelado":
        for d in p.detalles:
            inv = db.query(Inventario).filter(Inventario.autoparte_id == d.autoparte_id).first()
            if inv:
                old = inv.stock_actual; inv.stock_actual += d.cantidad
                db.add(MovimientoInventario(autoparte_id=d.autoparte_id, tipo="entrada", cantidad=d.cantidad,
                                             stock_anterior=old, stock_nuevo=inv.stock_actual,
                                             motivo=f"Cancelación {p.folio}", usuario_id=uid))
    ant = p.estatus; p.estatus = nuevo
    db.add(HistorialEstatusPedido(pedido_id=p.id, estatus_anterior=ant, estatus_nuevo=nuevo, comentario=comentario, usuario_id=uid))
    db.commit()
    return _pedido_dict(db, p)

def cancelar_pedido_cliente(db, pid, uid):
    c = db.query(Cliente).filter(Cliente.usuario_id == uid).first()
    p = db.query(Pedido).filter(Pedido.id == pid).first()
    if not p or p.cliente_id != c.id: raise HTTPException(404, "Pedido no encontrado")
    if p.estatus != "recibido": raise HTTPException(400, "Solo se pueden cancelar pedidos 'recibido'")
    return cambiar_estatus(db, pid, "cancelado", "Cancelado por cliente", uid)

def _pedido_dict(db, p, details=True):
    c = p.cliente; u = c.usuario if c else None
    r = {"id": p.id, "folio": p.folio, "estatus": p.estatus, "subtotal": float(p.subtotal),
         "impuesto": float(p.impuesto), "total": float(p.total), "notas": p.notas,
         "created_at": p.created_at.isoformat() if p.created_at else None,
         "updated_at": p.updated_at.isoformat() if p.updated_at else None,
         "cliente": {"id": c.id, "razon_social": c.razon_social, "nombre": u.nombre if u else None,
                     "apellido": u.apellido if u else None, "email": u.email if u else None} if c else None}
    if details:
        r["detalles"] = [{"id": d.id, "autoparte_id": d.autoparte_id,
                          "autoparte_nombre": d.autoparte.nombre if d.autoparte else None,
                          "autoparte_sku": d.autoparte.sku if d.autoparte else None,
                          "cantidad": d.cantidad, "precio_unitario": float(d.precio_unitario), "subtotal": float(d.subtotal)} for d in p.detalles]
        r["historial"] = [{"id": h.id, "estatus_anterior": h.estatus_anterior, "estatus_nuevo": h.estatus_nuevo,
                           "comentario": h.comentario, "usuario_nombre": f"{h.usuario.nombre} {h.usuario.apellido}" if h.usuario else None,
                           "created_at": h.created_at.isoformat() if h.created_at else None} for h in p.historial]
    return r


# ===== REPORTES =====
def get_reporte_ventas(db):
    tv = db.query(func.sum(Pedido.total)).filter(Pedido.estatus != "cancelado").scalar() or 0
    tp = db.query(func.count(Pedido.id)).scalar() or 0
    est = {e: c for e, c in db.query(Pedido.estatus, func.count(Pedido.id)).group_by(Pedido.estatus).all()}
    ct = [{"id": c[0], "razon_social": c[1], "total_pedidos": c[2], "monto_total": float(c[3] or 0)}
          for c in db.query(Cliente.id, Cliente.razon_social, func.count(Pedido.id).label("tp"),
                            func.sum(Pedido.total).label("mt")).join(Pedido).filter(Pedido.estatus != "cancelado")
          .group_by(Cliente.id, Cliente.razon_social).order_by(desc("tp")).limit(10).all()]
    pt = [{"id": p[0], "nombre": p[1], "sku": p[2], "total_vendido": int(p[3] or 0)}
          for p in db.query(Autoparte.id, Autoparte.nombre, Autoparte.sku,
                            func.sum(DetallePedido.cantidad).label("tv")).join(DetallePedido).join(Pedido)
          .filter(Pedido.estatus != "cancelado").group_by(Autoparte.id, Autoparte.nombre, Autoparte.sku)
          .order_by(desc("tv")).limit(10).all()]
    sb = [{"id": inv.autoparte.id, "nombre": inv.autoparte.nombre, "sku": inv.autoparte.sku,
           "stock_actual": inv.stock_actual, "stock_minimo": inv.stock_minimo}
          for inv in db.query(Inventario).filter(Inventario.stock_actual <= Inventario.stock_minimo).all() if inv.autoparte]
    return {"total_ventas": float(tv), "total_pedidos": tp, "pedidos_por_estatus": est,
            "clientes_top": ct, "productos_top": pt, "productos_stock_bajo": sb}


# ===== PDF =====
def generar_pdf_pedido(db, pid):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    p = db.query(Pedido).filter(Pedido.id == pid).first()
    if not p: raise HTTPException(404, "Pedido no encontrado")
    buf = io.BytesIO(); doc = SimpleDocTemplate(buf, pagesize=letter); styles = getSampleStyleSheet(); els = []
    els.append(Paragraph("MACUIN - Autopartes Automotrices", styles["Title"]))
    els.append(Spacer(1, 12))
    els.append(Paragraph(f"Pedido: {p.folio}", styles["Heading2"]))
    els.append(Paragraph(f"Estatus: {p.estatus.upper()} | Fecha: {p.created_at.strftime('%d/%m/%Y %H:%M')}", styles["Normal"]))
    if p.cliente and p.cliente.usuario:
        els.append(Paragraph(f"Cliente: {p.cliente.razon_social or ''} — {p.cliente.usuario.nombre} {p.cliente.usuario.apellido}", styles["Normal"]))
    els.append(Spacer(1, 20))
    data = [["SKU", "Producto", "Cant.", "P.Unit.", "Subtotal"]]
    for d in p.detalles:
        data.append([d.autoparte.sku, d.autoparte.nombre, str(d.cantidad), f"${d.precio_unitario:,.2f}", f"${d.subtotal:,.2f}"])
    t = Table(data, colWidths=[70, 200, 50, 80, 80])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0d47a1")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                           ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9),
                           ("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white])]))
    els.append(t); els.append(Spacer(1, 12))
    t2 = Table([["", "", "", "Subtotal:", f"${p.subtotal:,.2f}"], ["", "", "", "IVA 16%:", f"${p.impuesto:,.2f}"],
                ["", "", "", "TOTAL:", f"${p.total:,.2f}"]], colWidths=[70, 200, 50, 80, 80])
    t2.setStyle(TableStyle([("ALIGN", (3, 0), (-1, -1), "RIGHT"), ("FONTNAME", (3, 2), (-1, 2), "Helvetica-Bold")]))
    els.append(t2)
    if p.notas: els.append(Spacer(1, 20)); els.append(Paragraph(f"Notas: {p.notas}", styles["Normal"]))
    doc.build(els); buf.seek(0)
    return buf
