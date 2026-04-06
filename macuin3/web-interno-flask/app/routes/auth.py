from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.api_client import api_post
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def index():
    return redirect(url_for("dashboard.index")) if "token" in session else redirect(url_for("auth.login"))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        r = api_post("/auth/login", json={"email": request.form["email"], "password": request.form["password"]})
        if r.status_code == 200:
            data = r.json()
            if data["user"]["rol"]["nombre"] not in ("admin", "personal_interno"):
                flash("Sin permisos para el panel interno.", "danger")
                return render_template("auth/login.html")
            session["token"] = data["access_token"]; session["user"] = data["user"]
            return redirect(url_for("dashboard.index"))
        flash("Credenciales inválidas.", "danger")
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear(); return redirect(url_for("auth.login"))
