from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.api_client import api_get, api_post, api_put, api_delete
from app.routes.dashboard import login_required
autopartes_bp = Blueprint("autopartes", __name__, url_prefix="/autopartes")

@autopartes_bp.route("")
@login_required
def index():
    t = session["token"]; params = {}
    if request.args.get("search"): params["search"] = request.args["search"]
    if request.args.get("categoria_id"): params["categoria_id"] = request.args["categoria_id"]
    r = api_get("/autopartes", token=t, params=params); cats = api_get("/categorias", token=t)
    return render_template("autopartes/index.html", autopartes=r.json() if r.status_code == 200 else [],
                           categorias=cats.json() if cats.status_code == 200 else [],
                           search=request.args.get("search",""), cat_id=request.args.get("categoria_id",""), user=session.get("user"))

@autopartes_bp.route("/crear", methods=["GET","POST"])
@login_required
def crear():
    t = session["token"]
    if request.method == "POST":
        data = {"sku": request.form["sku"], "nombre": request.form["nombre"], "descripcion": request.form.get("descripcion",""),
                "marca": request.form.get("marca",""), "categoria_id": int(request.form["categoria_id"]) if request.form.get("categoria_id") else None,
                "precio": float(request.form["precio"]), "compatibilidad_vehicular": request.form.get("compatibilidad_vehicular",""),
                "imagen_url": request.form.get("imagen_url",""), "activo": True,
                "stock_inicial": int(request.form.get("stock_inicial",0)), "stock_minimo": int(request.form.get("stock_minimo",5))}
        r = api_post("/autopartes", token=t, json=data)
        if r.status_code == 200: flash("Autoparte creada.", "success"); return redirect(url_for("autopartes.index"))
        flash(r.json().get("detail","Error"), "danger")
    cats = api_get("/categorias", token=t)
    return render_template("autopartes/crear.html", categorias=cats.json() if cats.status_code == 200 else [], user=session.get("user"))

@autopartes_bp.route("/editar/<int:id>", methods=["GET","POST"])
@login_required
def editar(id):
    t = session["token"]
    if request.method == "POST":
        data = {"nombre": request.form["nombre"], "descripcion": request.form.get("descripcion",""),
                "marca": request.form.get("marca",""), "categoria_id": int(request.form["categoria_id"]) if request.form.get("categoria_id") else None,
                "precio": float(request.form["precio"]), "compatibilidad_vehicular": request.form.get("compatibilidad_vehicular",""),
                "imagen_url": request.form.get("imagen_url",""), "activo": request.form.get("activo") == "on"}
        r = api_put(f"/autopartes/{id}", token=t, json=data)
        if r.status_code == 200: flash("Actualizada.", "success"); return redirect(url_for("autopartes.index"))
        flash(r.json().get("detail","Error"), "danger")
    r = api_get(f"/autopartes/{id}", token=t); cats = api_get("/categorias", token=t)
    return render_template("autopartes/editar.html", autoparte=r.json() if r.status_code == 200 else {},
                           categorias=cats.json() if cats.status_code == 200 else [], user=session.get("user"))

@autopartes_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    api_delete(f"/autopartes/{id}", token=session["token"]); flash("Desactivada.", "success")
    return redirect(url_for("autopartes.index"))
