from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import require_roles
from app.schemas.schemas import AutoparteCreate, AutoparteUpdate
from app.services.services import get_autopartes, get_autoparte, create_autoparte, update_autoparte, delete_autoparte

router = APIRouter(prefix="/autopartes", tags=["Autopartes"])

@router.get("")
def listar(search: Optional[str] = Query(None), categoria_id: Optional[int] = Query(None),
           marca: Optional[str] = Query(None), solo_activos: Optional[bool] = Query(True), db: Session = Depends(get_db)):
    return get_autopartes(db, search=search, categoria_id=categoria_id, marca=marca, solo_activos=solo_activos)

@router.get("/{aid}")
def detalle(aid: int, db: Session = Depends(get_db)):
    return get_autoparte(db, aid)

@router.post("")
def crear(data: AutoparteCreate, db: Session = Depends(get_db), u=Depends(require_roles("admin", "personal_interno"))):
    return create_autoparte(db, data)

@router.put("/{aid}")
def actualizar(aid: int, data: AutoparteUpdate, db: Session = Depends(get_db), u=Depends(require_roles("admin", "personal_interno"))):
    return update_autoparte(db, aid, data)

@router.delete("/{aid}")
def eliminar(aid: int, db: Session = Depends(get_db), u=Depends(require_roles("admin", "personal_interno"))):
    return delete_autoparte(db, aid)
