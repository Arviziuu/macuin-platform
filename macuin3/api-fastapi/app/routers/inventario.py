from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.schemas.schemas import InventarioUpdate
from app.services.services import get_inventario, update_inventario

router = APIRouter(prefix="/inventario", tags=["Inventario"])

@router.get("")
def listar(db: Session = Depends(get_db), u=Depends(require_roles("admin", "personal_interno"))):
    return get_inventario(db)

@router.put("/{autoparte_id}")
def actualizar(autoparte_id: int, data: InventarioUpdate, db: Session = Depends(get_db),
               u=Depends(require_roles("admin", "personal_interno"))):
    return update_inventario(db, autoparte_id, data, u.id)
