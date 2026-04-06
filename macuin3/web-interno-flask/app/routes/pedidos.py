from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.api_client import api_get, api_put
from app.routes.dashboard import login_required
pedidos_bp = Blueprint("pedidos", __name__, url_prefix="/pedidos")

@pedidos_bp.route("")
@login_required
def index():
    t = session["token"]; params = {}
    if request.args.get("estatus"): params["estatus"] = request.args["estatus"]
    r = api_get("/pedidos", token=t, params=params)
    return render_template("pedidos/index.html", pedidos=r.json() if r.status_code == 200 else [],
                           estatus_filtro=request.args.get("estatus",""), user=session.get("user"))

@pedidos_bp.route("/<int:id>")
@login_required
def detalle(id):
    r = api_get(f"/pedidos/{id}", token=session["token"])
    return render_template("pedidos/detalle.html", pedido=r.json() if r.status_code == 200 else {}, user=session.get("user"))

@pedidos_bp.route("/<int:id>/estatus", methods=["POST"])
@login_required
def cambiar_estatus(id):
    r = api_put(f"/pedidos/{id}/estatus", token=session["token"],
                json={"estatus": request.form["estatus"], "comentario": request.form.get("comentario","")})
    flash("Estatus actualizado." if r.status_code == 200 else r.json().get("detail","Error"),
          "success" if r.status_code == 200 else "danger")
    return redirect(url_for("pedidos.detalle", id=id))
