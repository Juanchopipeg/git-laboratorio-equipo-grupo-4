
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash
)
from app.models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("usuario_id"):
        return redirect(url_for("inicio"))

    if request.method == "POST":
        nombre_usuario = request.form.get(
            "nombre_usuario", ""
        ).strip()
        password = request.form.get("password", "")

        usuario = Usuario.query.filter_by(
            nombre_usuario=nombre_usuario
        ).first()

        if usuario and usuario.verificar_password(password):
            session.clear()
            session["usuario_id"] = usuario.id
            session["nombre_usuario"] = usuario.nombre_usuario
            flash("Has iniciado sesión correctamente.", "success")
            return redirect(url_for("inicio"))

        flash("Usuario o contraseña incorrectos.", "error")

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Has cerrado sesión.", "success")
    return redirect(url_for("auth.login"))
