
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from app.models.medico import Medico
from app.models.especialidad import Especialidad
from app import db

medico_bp = Blueprint("medico", __name__)


@medico_bp.route("/medicos")
def listar_medicos():
    medicos = Medico.query.all()
    return render_template("medicos.html", medicos=medicos)


@medico_bp.route("/medicos/nuevo", methods=["GET", "POST"])
def nuevo_medico():
    especialidades = Especialidad.query.all()

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        especialidad_id = request.form.get("especialidad_id", "").strip()
        telefono = request.form.get("telefono", "").strip()
        correo = request.form.get("correo", "").strip()

        if not all([nombre, especialidad_id, telefono, correo]):
            flash("Todos los campos son obligatorios.", "error")
            return render_template(
                "nuevo_medico.html", especialidades=especialidades
            )

        especialidad = db.session.get(Especialidad, especialidad_id)

        if not especialidad:
            flash("Selecciona una especialidad válida.", "error")
            return render_template(
                "nuevo_medico.html", especialidades=especialidades
            )

        medico = Medico(
            nombre=nombre,
            especialidad=especialidad.nombre,
            especialidad_id=especialidad.id,
            telefono=telefono,
            correo=correo
        )

        try:
            db.session.add(medico)
            db.session.commit()
            flash("Médico registrado correctamente.", "success")
            return redirect(url_for("medico.listar_medicos"))
        except SQLAlchemyError:
            db.session.rollback()
            flash("No se pudo registrar el médico.", "error")

    return render_template(
        "nuevo_medico.html", especialidades=especialidades
    )


@medico_bp.route("/medicos/editar/<int:id>", methods=["GET", "POST"])
def editar_medico(id):
    medico = Medico.query.get_or_404(id)
    especialidades = Especialidad.query.all()

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        especialidad_id = request.form.get("especialidad_id", "").strip()
        telefono = request.form.get("telefono", "").strip()
        correo = request.form.get("correo", "").strip()

        if not all([nombre, especialidad_id, telefono, correo]):
            flash("Todos los campos son obligatorios.", "error")
            return render_template(
                "editar_medico.html",
                medico=medico,
                especialidades=especialidades
            )

        especialidad = db.session.get(Especialidad, especialidad_id)

        if not especialidad:
            flash("Selecciona una especialidad válida.", "error")
            return render_template(
                "editar_medico.html",
                medico=medico,
                especialidades=especialidades
            )

        medico.nombre = nombre
        medico.especialidad = especialidad.nombre
        medico.especialidad_id = especialidad.id
        medico.telefono = telefono
        medico.correo = correo

        try:
            db.session.commit()
            flash("Médico actualizado correctamente.", "success")
            return redirect(url_for("medico.listar_medicos"))
        except SQLAlchemyError:
            db.session.rollback()
            flash("No se pudo actualizar el médico.", "error")

    return render_template(
        "editar_medico.html",
        medico=medico,
        especialidades=especialidades
    )


@medico_bp.route("/medicos/eliminar/<int:id>", methods=["POST"])
def eliminar_medico(id):
    medico = Medico.query.get_or_404(id)

    try:
        db.session.delete(medico)
        db.session.commit()
        flash("Médico eliminado correctamente.", "success")
    except SQLAlchemyError:
        db.session.rollback()
        flash(
            "No se pudo eliminar el médico. Puede tener citas asociadas.",
            "error"
        )

    return redirect(url_for("medico.listar_medicos"))
