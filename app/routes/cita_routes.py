from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.models.cita import Cita
from app.models.paciente import Paciente
from app.models.medico import Medico
from app import db


cita_bp = Blueprint("cita", __name__)


@cita_bp.route("/citas")
def listar_citas():

    paciente_id = request.args.get("paciente_id")
    medico_id = request.args.get("medico_id")

    pacientes = Paciente.query.all()
    medicos = Medico.query.all()

    consulta = Cita.query

    if paciente_id:
        consulta = consulta.filter_by(paciente_id=paciente_id)

    if medico_id:
        consulta = consulta.filter_by(medico_id=medico_id)

    citas = consulta.all()

    return render_template(
        "citas.html",
        citas=citas,
        pacientes=pacientes,
        medicos=medicos,
        paciente_id=paciente_id,
        medico_id=medico_id
    )


@cita_bp.route("/citas/nueva", methods=["GET", "POST"])
def nueva_cita():

    pacientes = Paciente.query.all()
    medicos = Medico.query.all()

    if request.method == "POST":

        fecha = request.form["fecha"]
        hora = request.form["hora"]
        motivo = request.form["motivo"]
        paciente_id = request.form["paciente_id"]
        medico_id = request.form["medico_id"]

        # Verificar si el médico ya tiene una cita
        # en la misma fecha y hora.
        cita_existente = Cita.query.filter_by(
            fecha=fecha,
            hora=hora,
            medico_id=medico_id
        ).first()

        if cita_existente:

            flash(
                "El médico ya tiene una cita reservada "
                "para esa fecha y hora.",
                "error"
            )

            return render_template(
                "nueva_cita.html",
                pacientes=pacientes,
                medicos=medicos
            )

        # Crear la nueva cita
        cita = Cita(
            fecha=fecha,
            hora=hora,
            motivo=motivo,
            paciente_id=paciente_id,
            medico_id=medico_id
        )

        db.session.add(cita)
        db.session.commit()

        flash(
            "La cita fue registrada correctamente.",
            "success"
        )

        return redirect(
            url_for("cita.listar_citas")
        )

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

        fecha = request.form["fecha"]
        hora = request.form["hora"]
        motivo = request.form["motivo"]
        paciente_id = request.form["paciente_id"]
        medico_id = request.form["medico_id"]

        # Verificar si existe OTRA cita
        # con el mismo médico, fecha y hora.
        cita_existente = Cita.query.filter(
            Cita.fecha == fecha,
            Cita.hora == hora,
            Cita.medico_id == medico_id,
            Cita.id != cita.id
        ).first()

        if cita_existente:

            flash(
                "El médico ya tiene otra cita reservada "
                "para esa fecha y hora.",
                "error"
            )

            return render_template(
                "editar_cita.html",
                cita=cita,
                pacientes=pacientes,
                medicos=medicos
            )

        # Actualizar la cita
        cita.fecha = fecha
        cita.hora = hora
        cita.motivo = motivo
        cita.paciente_id = paciente_id
        cita.medico_id = medico_id

        db.session.commit()

        flash(
            "La cita fue actualizada correctamente.",
            "success"
        )

        return redirect(
            url_for("cita.listar_citas")
        )

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

    flash(
        "La cita fue cancelada correctamente.",
        "success"
    )

    return redirect(
        url_for("cita.listar_citas")
    )
    
@cita_bp.route("/disponibilidad", methods=["GET", "POST"])
def disponibilidad():

    medicos = Medico.query.all()

    citas = []

    medico_seleccionado = None

    fecha_seleccionada = None

    if request.method == "POST":

        medico_id = request.form["medico_id"]

        fecha = request.form["fecha"]

        medico_seleccionado = Medico.query.get_or_404(
            medico_id
        )

        fecha_seleccionada = fecha

        citas = Cita.query.filter_by(
            medico_id=medico_id,
            fecha=fecha
        ).order_by(
            Cita.hora
        ).all()

    return render_template(
        "disponibilidad.html",
        medicos=medicos,
        citas=citas,
        medico_seleccionado=medico_seleccionado,
        fecha_seleccionada=fecha_seleccionada
    )