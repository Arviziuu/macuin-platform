from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_roles
from app.services.services import (
    get_reporte_ventas, get_reporte_inventario, get_reporte_pedidos, get_reporte_clientes,
    generar_pdf_reporte_ventas, generar_pdf_reporte_inventario, generar_pdf_reporte_pedidos, generar_pdf_reporte_clientes,
    generar_xlsx_reporte_ventas, generar_xlsx_reporte_inventario, generar_xlsx_reporte_pedidos, generar_xlsx_reporte_clientes,
    generar_docx_reporte_ventas, generar_docx_reporte_inventario, generar_docx_reporte_pedidos, generar_docx_reporte_clientes,
)

router = APIRouter(prefix="/reportes", tags=["Reportes"])
_auth = Depends(require_roles("admin", "personal_interno"))


# ===== VENTAS =====
@router.get("/ventas")
def ventas(db: Session = Depends(get_db), u=_auth):
    return get_reporte_ventas(db)

@router.get("/ventas/pdf")
def ventas_pdf(db: Session = Depends(get_db), u=_auth):
    buf = generar_pdf_reporte_ventas(db)
    return StreamingResponse(buf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=reporte_ventas.pdf"})

@router.get("/ventas/xlsx")
def ventas_xlsx(db: Session = Depends(get_db), u=_auth):
    buf = generar_xlsx_reporte_ventas(db)
    return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=reporte_ventas.xlsx"})

@router.get("/ventas/docx")
def ventas_docx(db: Session = Depends(get_db), u=_auth):
    buf = generar_docx_reporte_ventas(db)
    return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                             headers={"Content-Disposition": "attachment; filename=reporte_ventas.docx"})


# ===== INVENTARIO =====
@router.get("/inventario")
def inventario(db: Session = Depends(get_db), u=_auth):
    return get_reporte_inventario(db)

@router.get("/inventario/pdf")
def inventario_pdf(db: Session = Depends(get_db), u=_auth):
    buf = generar_pdf_reporte_inventario(db)
    return StreamingResponse(buf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=reporte_inventario.pdf"})

@router.get("/inventario/xlsx")
def inventario_xlsx(db: Session = Depends(get_db), u=_auth):
    buf = generar_xlsx_reporte_inventario(db)
    return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=reporte_inventario.xlsx"})

@router.get("/inventario/docx")
def inventario_docx(db: Session = Depends(get_db), u=_auth):
    buf = generar_docx_reporte_inventario(db)
    return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                             headers={"Content-Disposition": "attachment; filename=reporte_inventario.docx"})


# ===== PEDIDOS =====
@router.get("/pedidos")
def pedidos(db: Session = Depends(get_db), u=_auth):
    return get_reporte_pedidos(db)

@router.get("/pedidos/pdf")
def pedidos_pdf(db: Session = Depends(get_db), u=_auth):
    buf = generar_pdf_reporte_pedidos(db)
    return StreamingResponse(buf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=reporte_pedidos.pdf"})

@router.get("/pedidos/xlsx")
def pedidos_xlsx(db: Session = Depends(get_db), u=_auth):
    buf = generar_xlsx_reporte_pedidos(db)
    return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=reporte_pedidos.xlsx"})

@router.get("/pedidos/docx")
def pedidos_docx(db: Session = Depends(get_db), u=_auth):
    buf = generar_docx_reporte_pedidos(db)
    return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                             headers={"Content-Disposition": "attachment; filename=reporte_pedidos.docx"})


# ===== CLIENTES =====
@router.get("/clientes")
def clientes(db: Session = Depends(get_db), u=_auth):
    return get_reporte_clientes(db)

@router.get("/clientes/pdf")
def clientes_pdf(db: Session = Depends(get_db), u=_auth):
    buf = generar_pdf_reporte_clientes(db)
    return StreamingResponse(buf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=reporte_clientes.pdf"})

@router.get("/clientes/xlsx")
def clientes_xlsx(db: Session = Depends(get_db), u=_auth):
    buf = generar_xlsx_reporte_clientes(db)
    return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=reporte_clientes.xlsx"})

@router.get("/clientes/docx")
def clientes_docx(db: Session = Depends(get_db), u=_auth):
    buf = generar_docx_reporte_clientes(db)
    return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                             headers={"Content-Disposition": "attachment; filename=reporte_clientes.docx"})
