from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_roles
from app.schemas.schemas import EmpleadoCreate, EmpleadoUpdate
from app.services.services import get_empleados, create_empleado, update_empleado, delete_empleado

router = APIRouter(prefix="/empleados", tags=["Empleados"])

@router.get("")
def listar(db: Session = Depends(get_db), u=Depends(require_roles("admin", "personal_interno"))):
    return get_empleados(db)

@router.post("")
def crear(data: EmpleadoCreate, db: Session = Depends(get_db), u=Depends(require_roles("admin", "personal_interno"))):
    return create_empleado(db, data)

@router.put("/{eid}")
def actualizar(eid: int, data: EmpleadoUpdate, db: Session = Depends(get_db), u=Depends(require_roles("admin", "personal_interno"))):
    return update_empleado(db, eid, data)

@router.delete("/{eid}")
def eliminar(eid: int, db: Session = Depends(get_db), u=Depends(require_roles("admin", "personal_interno"))):
    return delete_empleado(db, eid)
