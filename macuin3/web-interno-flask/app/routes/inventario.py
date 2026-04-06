from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.api_client import api_get, api_put
from app.routes.dashboard import login_required
inventario_bp = Blueprint("inventario", __name__, url_prefix="/inventario")

@inventario_bp.route("")
@login_required
def index():
    r = api_get("/inventario", token=session["token"])
    return render_template("dashboard/inventario.html", items=r.json() if r.status_code == 200 else [], user=session.get("user"))

@inventario_bp.route("/<int:autoparte_id>/actualizar", methods=["POST"])
@login_required
def actualizar(autoparte_id):
    r = api_put(f"/inventario/{autoparte_id}", token=session["token"],
                json={"cantidad": int(request.form["cantidad"]), "tipo": request.form["tipo"], "motivo": request.form.get("motivo","")})
    flash("Inventario actualizado." if r.status_code == 200 else r.json().get("detail","Error"),
          "success" if r.status_code == 200 else "danger")
    return redirect(url_for("inventario.index"))
