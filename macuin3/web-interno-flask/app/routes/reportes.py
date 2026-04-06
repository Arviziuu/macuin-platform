from flask import Blueprint, render_template, session
from app.services.api_client import api_get
from app.routes.dashboard import login_required
reportes_bp = Blueprint("reportes", __name__, url_prefix="/reportes")

@reportes_bp.route("")
@login_required
def index():
    r = api_get("/reportes/ventas", token=session["token"])
    return render_template("reportes/index.html", reporte=r.json() if r.status_code == 200 else {}, user=session.get("user"))
