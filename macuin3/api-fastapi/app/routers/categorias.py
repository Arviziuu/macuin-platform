from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_roles
from app.schemas.schemas import CategoriaCreate
from app.services.services import get_categorias, create_categoria

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("")
def listar(db: Session = Depends(get_db)):
    return get_categorias(db)

@router.post("")
def crear(data: CategoriaCreate, db: Session = Depends(get_db), u=Depends(require_roles("admin", "personal_interno"))):
    return create_categoria(db, data)
