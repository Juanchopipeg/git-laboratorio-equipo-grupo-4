from flask import Blueprint, render_template, request, redirect, url_for
from app.models.cita import Cita
from app.models.paciente import Paciente
from app.models.medico import Medico
from app import db


cita_bp = Blueprint("cita", __name__)


@cita_bp.route("/citas")
def listar_citas():

    citas = Cita.query.all()

    return render_template(
        "citas.html",
        citas=citas
    )


@cita_bp.route("/citas/nueva", methods=["GET", "POST"])
def nueva_cita():

    pacientes = Paciente.query.all()
    medicos = Medico.query.all()

    if request.method == "POST":

        cita = Cita(
            fecha=request.form["fecha"],
            hora=request.form["hora"],
            motivo=request.form["motivo"],
            paciente_id=request.form["paciente_id"],
            medico_id=request.form["medico_id"]
        )

        db.session.add(cita)
        db.session.commit()

        return redirect(url_for("cita.listar_citas"))

    return render_template(
        "nueva_cita.html",
        pacientes=pacientes,
        medicos=medicos
    )


@cita_bp.route("/citas/editar/<int:id>", methods=["GET", "POST"])
def editar_cita(id):

    cita = Cita.query.get_or_404(id)

    pacientes = Paciente.query.all()
    medicos = Medico.query.all()

    if request.method == "POST":

        cita.fecha = request.form["fecha"]
        cita.hora = request.form["hora"]
        cita.motivo = request.form["motivo"]
        cita.paciente_id = request.form["paciente_id"]
        cita.medico_id = request.form["medico_id"]

        db.session.commit()

        return redirect(url_for("cita.listar_citas"))

    return render_template(
        "editar_cita.html",
        cita=cita,
        pacientes=pacientes,
        medicos=medicos
    )


@cita_bp.route("/citas/eliminar/<int:id>")
def eliminar_cita(id):

    cita = Cita.query.get_or_404(id)

    db.session.delete(cita)
    db.session.commit()

    return redirect(url_for("cita.listar_citas"))