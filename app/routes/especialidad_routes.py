
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from app.models.especialidad import Especialidad
from app import db

especialidad_bp = Blueprint("especialidad", __name__)


@especialidad_bp.route("/especialidades")
def listar_especialidades():
    especialidades = Especialidad.query.all()
    return render_template(
        "especialidades.html",
        especialidades=especialidades
    )


@especialidad_bp.route("/especialidades/nueva", methods=["GET", "POST"])
def nueva_especialidad():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        if not nombre:
            flash("El nombre de la especialidad es obligatorio.", "error")
            return render_template("nueva_especialidad.html")

        especialidad = Especialidad(
            nombre=nombre,
            descripcion=descripcion
        )

        try:
            db.session.add(especialidad)
            db.session.commit()
            flash("Especialidad creada correctamente.", "success")
            return redirect(url_for("especialidad.listar_especialidades"))
        except SQLAlchemyError:
            db.session.rollback()
            flash("No se pudo crear la especialidad.", "error")

    return render_template("nueva_especialidad.html")


@especialidad_bp.route(
    "/especialidades/editar/<int:id>",
    methods=["GET", "POST"]
)
def editar_especialidad(id):
    especialidad = Especialidad.query.get_or_404(id)

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        if not nombre:
            flash("El nombre de la especialidad es obligatorio.", "error")
            return render_template(
                "editar_especialidad.html",
                especialidad=especialidad
            )

        especialidad.nombre = nombre
        especialidad.descripcion = descripcion

        try:
            db.session.commit()
            flash("Especialidad actualizada correctamente.", "success")
            return redirect(url_for("especialidad.listar_especialidades"))
        except SQLAlchemyError:
            db.session.rollback()
            flash("No se pudo actualizar la especialidad.", "error")

    return render_template(
        "editar_especialidad.html",
        especialidad=especialidad
    )


@especialidad_bp.route(
    "/especialidades/eliminar/<int:id>",
    methods=["POST"]
)
def eliminar_especialidad(id):
    especialidad = Especialidad.query.get_or_404(id)

    try:
        db.session.delete(especialidad)
        db.session.commit()
        flash("Especialidad eliminada correctamente.", "success")
    except SQLAlchemyError:
        db.session.rollback()
        flash(
            "No se pudo eliminar la especialidad. Comprueba si tiene médicos asociados.",
            "error"
        )

    return redirect(url_for("especialidad.listar_especialidades"))
