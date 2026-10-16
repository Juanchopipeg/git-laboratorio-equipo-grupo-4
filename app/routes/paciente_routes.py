
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.paciente import Paciente
from app import db


paciente_bp = Blueprint("paciente", __name__)


# LISTAR PACIENTES
@paciente_bp.route("/pacientes")
def listar_pacientes():
    pacientes = Paciente.query.all()

    return render_template(
        "pacientes.html",
        pacientes=pacientes
    )


# REGISTRAR NUEVO PACIENTE
@paciente_bp.route("/pacientes/nuevo", methods=["GET", "POST"])
def nuevo_paciente():

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        documento = request.form.get("documento", "").strip()
        telefono = request.form.get("telefono", "").strip()
        correo = request.form.get("correo", "").strip()
        historial_clinico = request.form.get(
            "historial_clinico", ""
        ).strip()

        # Validar campos obligatorios
        if not nombre or not apellido or not documento:
            flash(
                "Nombre, apellido y documento son obligatorios.",
                "error"
            )
            return render_template("nuevo_paciente.html")

        # Comprobar si el documento ya existe
        paciente_existente = Paciente.query.filter_by(
            documento=documento
        ).first()

        if paciente_existente:
            flash(
                "Ya existe un paciente con ese documento.",
                "error"
            )
            return render_template("nuevo_paciente.html")

        paciente = Paciente(
            nombre=nombre,
            apellido=apellido,
            documento=documento,
            telefono=telefono or None,
            correo=correo or None,
            historial_clinico=historial_clinico or None
        )

        try:
            db.session.add(paciente)
            db.session.commit()

            flash(
                "Paciente registrado correctamente.",
                "success"
            )

            return redirect(
                url_for("paciente.listar_pacientes")
            )

        except IntegrityError:
            db.session.rollback()

            flash(
                "No se pudo registrar el paciente. "
                "El documento puede estar registrado por otro usuario.",
                "error"
            )

        except SQLAlchemyError:
            db.session.rollback()

            flash(
                "Ocurrió un error al guardar el paciente. "
                "Inténtalo nuevamente.",
                "error"
            )

        return render_template("nuevo_paciente.html")

    return render_template("nuevo_paciente.html")


# EDITAR PACIENTE
@paciente_bp.route(
    "/pacientes/editar/<int:id>",
    methods=["GET", "POST"]
)
def editar_paciente(id):

    paciente = Paciente.query.get_or_404(id)

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        documento = request.form.get("documento", "").strip()
        telefono = request.form.get("telefono", "").strip()
        correo = request.form.get("correo", "").strip()
        historial_clinico = request.form.get(
            "historial_clinico", ""
        ).strip()

        # Validar campos obligatorios
        if not nombre or not apellido or not documento:
            flash(
                "Nombre, apellido y documento son obligatorios.",
                "error"
            )

            return render_template(
                "editar_paciente.html",
                paciente=paciente
            )

        # Comprobar si otro paciente tiene el mismo documento
        paciente_existente = Paciente.query.filter(
            Paciente.documento == documento,
            Paciente.id != paciente.id
        ).first()

        if paciente_existente:
            flash(
                "Otro paciente ya tiene ese documento.",
                "error"
            )

            return render_template(
                "editar_paciente.html",
                paciente=paciente
            )

        paciente.nombre = nombre
        paciente.apellido = apellido
        paciente.documento = documento
        paciente.telefono = telefono or None
        paciente.correo = correo or None
        paciente.historial_clinico = historial_clinico or None

        try:
            db.session.commit()

            flash(
                "Paciente actualizado correctamente.",
                "success"
            )

            return redirect(
                url_for("paciente.listar_pacientes")
            )

        except IntegrityError:
            db.session.rollback()

            flash(
                "No se pudo actualizar el paciente. "
                "Comprueba que el documento no esté duplicado.",
                "error"
            )

        except SQLAlchemyError:
            db.session.rollback()

            flash(
                "Ocurrió un error al actualizar el paciente.",
                "error"
            )

        return render_template(
            "editar_paciente.html",
            paciente=paciente
        )

    return render_template(
        "editar_paciente.html",
        paciente=paciente
    )


# ELIMINAR PACIENTE
@paciente_bp.route(
    "/pacientes/eliminar/<int:id>",
    methods=["POST"]
)
def eliminar_paciente(id):

    paciente = Paciente.query.get_or_404(id)

    try:
        db.session.delete(paciente)
        db.session.commit()

        flash(
            "Paciente eliminado correctamente.",
            "success"
        )

    except SQLAlchemyError:
        db.session.rollback()

        flash(
            "No se pudo eliminar el paciente. "
            "Comprueba si tiene citas asociadas.",
            "error"
        )

    return redirect(
        url_for("paciente.listar_pacientes")
    )
