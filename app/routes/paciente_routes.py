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

@paciente_bp.route("/pacientes/editar/<int:id>", methods=["GET", "POST"])
def editar_paciente(id):

    paciente = Paciente.query.get_or_404(id)

    if request.method == "POST":

        paciente.nombre = request.form["nombre"]
        paciente.apellido = request.form["apellido"]
        paciente.documento = request.form["documento"]
        paciente.telefono = request.form["telefono"]
        paciente.correo = request.form["correo"]

        db.session.commit()

        return redirect(url_for("paciente.listar_pacientes"))

    return render_template(
        "editar_paciente.html",
        paciente=paciente
    )
    
@paciente_bp.route("/pacientes/eliminar/<int:id>")
def eliminar_paciente(id):

    paciente = Paciente.query.get_or_404(id)

    db.session.delete(paciente)
    db.session.commit()

    return redirect(url_for("paciente.listar_pacientes"))