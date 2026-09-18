from flask import Blueprint, render_template
from app.models.paciente import Paciente

paciente_bp = Blueprint("paciente", __name__)

@paciente_bp.route("/pacientes")
def listar_pacientes():
    pacientes = Paciente.query.all()
    return render_template(
        "pacientes.html",
        pacientes=pacientes
    )