from flask import Blueprint, render_template, session, send_file, Response
from app.services.api_client import api_get
from app.routes.dashboard import login_required
import io

reportes_bp = Blueprint("reportes", __name__, url_prefix="/reportes")

@reportes_bp.route("")
@login_required
def index():
    r = api_get("/interno/reportes/ventas", token=session["token"])
    return render_template("reportes/index.html", reporte=r.json() if r.status_code == 200 else {}, user=session.get("user"))

@reportes_bp.route("/<tipo>/<formato>")
@login_required
def descargar(tipo, formato):
    mimes = {
        "pdf":  "application/pdf",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }
    extensiones = {"pdf": "pdf", "xlsx": "xlsx", "docx": "docx"}
    if tipo not in ("ventas", "inventario", "pedidos", "clientes") or formato not in mimes:
        return "Formato no válido", 400
    r = api_get(f"/interno/reportes/{tipo}/{formato}", token=session["token"])
    if r.status_code == 200:
        return Response(
            r.content,
            mimetype=mimes[formato],
            headers={"Content-Disposition": f"attachment; filename=reporte_{tipo}.{extensiones[formato]}"}
        )
    return f"Error al generar reporte: {r.status_code}", 500
