# MACUIN Platform - Sistema de Gestión de Autopartes

## Arquitectura

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Web Clientes    │     │   API Central    │     │  Web Interno     │
│  (Laravel)       │────▶│   (FastAPI)      │◀────│  (Flask)         │
│  Puerto: 8080    │     │   Puerto: 8000   │     │  Puerto: 5000    │
└──────────────────┘     └────────┬─────────┘     └──────────────────┘
                                  │
                         ┌────────▼─────────┐
                         │  PostgreSQL 16   │
                         │  Puerto: 5432    │
                         └──────────────────┘
```

**Solo la API accede a la base de datos.** Laravel y Flask consumen la API vía HTTP/REST.

## Ejecución

```bash
cd macuin-platform
docker compose up --build
```

Primera vez tarda ~3-5 minutos.

## URLs de Acceso

| Sistema | URL | Descripción |
|---------|-----|-------------|
| API Swagger | http://localhost:8000/docs | Documentación interactiva |
| Portal Clientes | http://localhost:8080 | Laravel - clientes externos |
| Panel Interno | http://localhost:5000 | Flask - personal interno |

## Puertos (todos únicos)

| Servicio | Puerto |
|----------|--------|
| PostgreSQL | 5432 |
| FastAPI | 8000 |
| Flask | 5000 |
| Laravel | 8080 |

## Credenciales de Prueba

**Password universal: `password123`**

### Panel Interno (Flask - http://localhost:5000)
| Email | Rol |
|-------|-----|
| admin@macuin.com | Administrador |
| ventas@macuin.com | Personal Interno |
| almacen@macuin.com | Personal Interno |
| logistica@macuin.com | Personal Interno |

### Portal Clientes (Laravel - http://localhost:8080)
| Email | Tipo |
|-------|------|
| taller.roma@mail.com | Taller Mecánico |
| refac.central@mail.com | Refaccionaria |

También puedes registrar nuevos clientes desde el portal.

## Rúbrica Cubierta

### Front - API - BD
1. ✅ 2 Frontends: Flask (interno) + Laravel (externo)
2. ✅ Toda la lógica en API FastAPI
3. ✅ API con routers estructurados por carpetas
4. ✅ Modelos SQLAlchemy para BD
5. ✅ Solo la API accede a la BD
6. ✅ Cada componente en su contenedor Docker
7. ✅ Registro de usuarios externos vía endpoint POST /api/v1/auth/register

### Frontend 1 - Cliente Externo (Laravel)
1. ✅ Login y registro
2. ✅ Catálogo con filtros de búsqueda
3. ✅ Diferenciación disponible/agotado
4. ✅ Creación y cancelación de pedidos
5. ✅ Historial y estatus de pedidos
6. ✅ Descarga de PDF del pedido
7. ✅ Contenedor Docker funcional

### Frontend 2 - Personal Interno (Flask)
1. ✅ Login para empleados
2. ✅ CRUD completo de autopartes
3. ✅ Gestión de empleados (CRUD)
4. ✅ Visualización y cambio de estatus: recibido, en_proceso, enviado
5. ✅ Reportes: pedidos, clientes, ventas
6. ✅ Contenedor Docker funcional

## Flujo de Demostración

1. Cliente crea pedido en http://localhost:8080
2. Personal interno ve pedido en http://localhost:5000/pedidos
3. Personal cambia estatus: recibido → en_proceso → enviado
4. Cliente ve el estatus actualizado y descarga PDF

## Comandos

```bash
docker compose up --build        # Levantar
docker compose down              # Detener
docker compose down -v           # Detener y borrar BD
docker compose logs -f           # Ver logs
docker compose build --no-cache  # Reconstruir
```
