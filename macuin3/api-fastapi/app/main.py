from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, autopartes, categorias, inventario, pedidos, reportes, empleados

app = FastAPI(title="MACUIN API Central", description="API central para gestión de autopartes", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router, prefix="/api/v1")
app.include_router(autopartes.router, prefix="/api/v1")
app.include_router(categorias.router, prefix="/api/v1")
app.include_router(inventario.router, prefix="/api/v1")
app.include_router(pedidos.router, prefix="/api/v1")
app.include_router(reportes.router, prefix="/api/v1")
app.include_router(empleados.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "MACUIN API Central v1.0", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}
