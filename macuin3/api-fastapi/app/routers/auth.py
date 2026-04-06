from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.schemas import LoginRequest, RegisterRequest
from app.services.services import authenticate_user, register_cliente

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return authenticate_user(db, data.email, data.password)

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return register_cliente(db, data)

@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "nombre": current_user.nombre,
            "apellido": current_user.apellido, "telefono": current_user.telefono,
            "rol": {"id": current_user.rol.id, "nombre": current_user.rol.nombre}, "activo": current_user.activo}
