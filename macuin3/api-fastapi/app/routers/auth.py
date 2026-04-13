from fastapi import APIRouter, Depends
from datetime import timedelta
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, create_access_token
from app.core.config import get_settings
from app.schemas.schemas import LoginRequest, RegisterRequest
from app.services.services import authenticate_user, register_cliente

router = APIRouter(prefix="/auth", tags=["Autenticación"])
settings = get_settings()

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return authenticate_user(db, data.email, data.password)

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return register_cliente(db, data)

@router.post("/refresh")
def refresh(current_user=Depends(get_current_user)):
    """Renueva el token JWT sin volver a pedir credenciales."""
    token = create_access_token(
        {"sub": str(current_user.id), "rol": current_user.rol.nombre},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "nombre": current_user.nombre,
            "apellido": current_user.apellido, "telefono": current_user.telefono,
            "rol": {"id": current_user.rol.id, "nombre": current_user.rol.nombre}, "activo": current_user.activo}
