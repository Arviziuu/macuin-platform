from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_roles
from app.services.services import get_reporte_ventas

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/ventas")
def ventas(db: Session = Depends(get_db), u=Depends(require_roles("admin", "personal_interno"))):
    return get_reporte_ventas(db)
