from flask import Blueprint, render_template, request, redirect, url_for
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

        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]

        especialidad = Especialidad(
            nombre=nombre,
            descripcion=descripcion
        )

        db.session.add(especialidad)
        db.session.commit()

        return redirect(
            url_for("especialidad.listar_especialidades")
        )

    return render_template("nueva_especialidad.html")


@especialidad_bp.route(
    "/especialidades/editar/<int:id>",
    methods=["GET", "POST"]
)
def editar_especialidad(id):

    especialidad = Especialidad.query.get_or_404(id)

    if request.method == "POST":

        especialidad.nombre = request.form["nombre"]
        especialidad.descripcion = request.form["descripcion"]

        db.session.commit()

        return redirect(
            url_for("especialidad.listar_especialidades")
        )

    return render_template(
        "editar_especialidad.html",
        especialidad=especialidad
    )


@especialidad_bp.route("/especialidades/eliminar/<int:id>")
def eliminar_especialidad(id):

    especialidad = Especialidad.query.get_or_404(id)

    db.session.delete(especialidad)
    db.session.commit()

    return redirect(
        url_for("especialidad.listar_especialidades")
    )