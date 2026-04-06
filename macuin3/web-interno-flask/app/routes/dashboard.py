from flask import Blueprint, render_template, session, redirect, url_for
from app.services.api_client import api_get
from functools import wraps
dashboard_bp = Blueprint("dashboard", __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "token" not in session: return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated

@dashboard_bp.route("/dashboard")
@login_required
def index():
    token = session["token"]
    rep = api_get("/reportes/ventas", token=token)
    reporte = rep.json() if rep.status_code == 200 else {}
    ped = api_get("/pedidos", token=token)
    pedidos = ped.json()[:5] if ped.status_code == 200 else []
    return render_template("dashboard/index.html", reporte=reporte, pedidos_recientes=pedidos, user=session.get("user"))
