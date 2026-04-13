from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, autopartes, categorias, inventario, pedidos, reportes, empleados

app = FastAPI(
    title="MACUIN API Central",
    description="API central — /api/v1 compartido | /api/v1/interno para personal | /api/v1/externo para clientes",
    version="1.0.0",
    openapi_tags=[
        {"name": "Autenticación", "description": "Login, registro y refresh"},
        {"name": "Autopartes",    "description": "Catálogo público de autopartes"},
        {"name": "Categorías",    "description": "Categorías de autopartes"},
        {"name": "Pedidos",       "description": "Gestión de pedidos (clientes y personal)"},
        {"name": "Empleados",     "description": "[INTERNO] CRUD de empleados"},
        {"name": "Inventario",    "description": "[INTERNO] Gestión de inventario"},
        {"name": "Reportes",      "description": "[INTERNO] Reportes en PDF, xlsx y docx"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5000",
        "http://localhost:8080",
        "http://web-interno:5000",
        "http://web-clientes:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints compartidos (auth + catálogo público)
app.include_router(auth.router,       prefix="/api/v1")
app.include_router(categorias.router, prefix="/api/v1")
app.include_router(autopartes.router, prefix="/api/v1")
app.include_router(pedidos.router,    prefix="/api/v1")

# Endpoints internos — solo personal (Flask)
app.include_router(empleados.router,  prefix="/api/v1/interno")
app.include_router(inventario.router, prefix="/api/v1/interno")
app.include_router(reportes.router,   prefix="/api/v1/interno")

@app.get("/")
def root():
    return {"message": "MACUIN API Central v1.0", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}
