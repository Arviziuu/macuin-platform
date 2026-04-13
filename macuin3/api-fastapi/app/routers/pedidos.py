from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.schemas.schemas import PedidoCreate, CambioEstatusRequest
from app.services.services import create_pedido, get_pedidos, get_pedido, get_pedidos_cliente, cambiar_estatus, cancelar_pedido_cliente, generar_pdf_pedido, generar_docx_pedido

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("")
def crear(data: PedidoCreate, db: Session = Depends(get_db), u=Depends(require_roles("cliente_externo"))):
    return create_pedido(db, data, u.id)

@router.get("")
def listar(estatus: Optional[str] = None, db: Session = Depends(get_db), u=Depends(get_current_user)):
    if u.rol.nombre == "cliente_externo": return get_pedidos_cliente(db, u.id)
    return get_pedidos(db, estatus=estatus)

@router.get("/{pid}")
def detalle(pid: int, db: Session = Depends(get_db), u=Depends(get_current_user)):
    return get_pedido(db, pid)

@router.put("/{pid}/estatus")
def estatus(pid: int, data: CambioEstatusRequest, db: Session = Depends(get_db), u=Depends(require_roles("admin", "personal_interno"))):
    return cambiar_estatus(db, pid, data.estatus, data.comentario, u.id)

@router.post("/{pid}/cancelar")
def cancelar(pid: int, db: Session = Depends(get_db), u=Depends(require_roles("cliente_externo"))):
    return cancelar_pedido_cliente(db, pid, u.id)

@router.get("/{pid}/pdf")
def pdf(pid: int, db: Session = Depends(get_db), u=Depends(get_current_user)):
    buf = generar_pdf_pedido(db, pid)
    p = get_pedido(db, pid)
    return StreamingResponse(buf, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={p['folio']}.pdf"})

@router.get("/{pid}/docx")
def docx(pid: int, db: Session = Depends(get_db), u=Depends(get_current_user)):
    buf = generar_docx_pedido(db, pid)
    p = get_pedido(db, pid)
    return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                             headers={"Content-Disposition": f"attachment; filename={p['folio']}.docx"})
