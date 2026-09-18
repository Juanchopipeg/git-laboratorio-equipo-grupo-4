from flask import Blueprint, render_template, request, redirect, url_for
from app.models.paciente import Paciente
from app import db

paciente_bp = Blueprint("paciente", __name__)

@paciente_bp.route("/pacientes")
def listar_pacientes():
    pacientes = Paciente.query.all()
    return render_template(
        "pacientes.html",
        pacientes=pacientes
    )

@paciente_bp.route("/pacientes/nuevo", methods=["GET", "POST"])
def nuevo_paciente():

    if request.method == "POST":

        paciente = Paciente(
            nombre=request.form["nombre"],
            apellido=request.form["apellido"],
            documento=request.form["documento"],
            telefono=request.form["telefono"],
            correo=request.form["correo"]
        )

        db.session.add(paciente)
        db.session.commit()

        return redirect(url_for("paciente.listar_pacientes"))

    return render_template("nuevo_paciente.html")