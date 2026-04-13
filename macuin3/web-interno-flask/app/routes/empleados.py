from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.api_client import api_get, api_post, api_put, api_delete
from app.routes.dashboard import login_required
empleados_bp = Blueprint("empleados", __name__, url_prefix="/empleados")

@empleados_bp.route("")
@login_required
def index():
    r = api_get("/interno/empleados", token=session["token"])
    return render_template("empleados/index.html", empleados=r.json() if r.status_code == 200 else [], user=session.get("user"))

@empleados_bp.route("/crear", methods=["GET","POST"])
@login_required
def crear():
    if request.method == "POST":
        data = {"email": request.form["email"], "password": request.form["password"], "nombre": request.form["nombre"],
                "apellido": request.form["apellido"], "telefono": request.form.get("telefono",""),
                "numero_empleado": request.form["numero_empleado"], "departamento": request.form.get("departamento",""),
                "puesto": request.form.get("puesto","")}
        r = api_post("/interno/empleados", token=session["token"], json=data)
        if r.status_code == 200: flash("Empleado creado.", "success"); return redirect(url_for("empleados.index"))
        flash(r.json().get("detail","Error"), "danger")
    return render_template("empleados/crear.html", user=session.get("user"))

@empleados_bp.route("/editar/<int:id>", methods=["GET","POST"])
@login_required
def editar(id):
    if request.method == "POST":
        data = {"nombre": request.form["nombre"], "apellido": request.form["apellido"],
                "telefono": request.form.get("telefono",""), "departamento": request.form.get("departamento",""),
                "puesto": request.form.get("puesto",""), "activo": request.form.get("activo") == "on"}
        r = api_put(f"/interno/empleados/{id}", token=session["token"], json=data)
        if r.status_code == 200: flash("Actualizado.", "success"); return redirect(url_for("empleados.index"))
        flash(r.json().get("detail","Error"), "danger")
    emps = api_get("/interno/empleados", token=session["token"])
    emp = next((e for e in (emps.json() if emps.status_code == 200 else []) if e["id"] == id), {})
    return render_template("empleados/editar.html", empleado=emp, user=session.get("user"))

@empleados_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    api_delete(f"/interno/empleados/{id}", token=session["token"]); flash("Empleado desactivado.", "success")
    return redirect(url_for("empleados.index"))
