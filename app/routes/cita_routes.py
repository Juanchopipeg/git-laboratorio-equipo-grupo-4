
from datetime import date
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
)
from app.models.cita import Cita
from app.models.paciente import Paciente
from app.models.medico import Medico
from app import db


cita_bp = Blueprint("cita", __name__)


# Horario de atención: lunes a viernes.
# Mañana: 08:00 a 12:00.
# Tarde: 13:00 a 17:00.
# Cada cita dura 30 minutos.
def generar_horarios():
    horarios = []

    for hora in range(8, 12):
        horarios.append(f"{hora:02d}:00")
        horarios.append(f"{hora:02d}:30")

    for hora in range(13, 17):
        horarios.append(f"{hora:02d}:00")
        horarios.append(f"{hora:02d}:30")

    return horarios


def es_dia_atencion(fecha):
    fecha_obj = date.fromisoformat(fecha)
    return fecha_obj.weekday() < 5


def obtener_datos_formulario():
    fecha = request.form.get("fecha", "").strip()
    hora = request.form.get("hora", "").strip()
    motivo = request.form.get("motivo", "").strip()
    paciente_id = request.form.get("paciente_id", "").strip()
    medico_id = request.form.get("medico_id", "").strip()

    if not all([fecha, hora, paciente_id, medico_id]):
        return None, "Completa todos los campos obligatorios."

    try:
        fecha_obj = date.fromisoformat(fecha)
        paciente_id = int(paciente_id)
        medico_id = int(medico_id)
    except (ValueError, TypeError):
        return None, "La fecha, el paciente o el médico no son válidos."

    if fecha_obj < date.today():
        return None, "No puedes registrar citas en fechas pasadas."

    if not es_dia_atencion(fecha):
        return None, "Solo se pueden reservar citas de lunes a viernes."

    if hora not in generar_horarios():
        return None, "Selecciona un horario válido de 30 minutos."

    paciente = db.session.get(Paciente, paciente_id)
    medico = db.session.get(Medico, medico_id)

    if paciente is None:
        return None, "El paciente seleccionado no existe."

    if medico is None:
        return None, "El médico seleccionado no existe."

    datos = {
        "fecha": fecha,
        "hora": hora,
        "motivo": motivo or None,
        "paciente_id": paciente_id,
        "medico_id": medico_id,
    }

    return datos, None


def existe_cita(fecha, hora, medico_id, excluir_id=None):
    consulta = Cita.query.filter_by(
        fecha=fecha,
        hora=hora,
        medico_id=medico_id,
    )

    if excluir_id is not None:
        consulta = consulta.filter(Cita.id != excluir_id)

    return consulta.first() is not None


def render_formulario_nueva_cita():
    pacientes = Paciente.query.order_by(Paciente.nombre).all()
    medicos = Medico.query.order_by(Medico.nombre).all()

    return render_template(
        "nueva_cita.html",
        pacientes=pacientes,
        medicos=medicos,
        fecha_minima=date.today().isoformat(),
    )


# Listar citas y permitir filtrar por paciente o médico.
@cita_bp.route("/citas", methods=["GET"])
def listar_citas():
    paciente_id = request.args.get("paciente_id", "").strip()
    medico_id = request.args.get("medico_id", "").strip()

    consulta = Cita.query

    if paciente_id:
        try:
            consulta = consulta.filter_by(paciente_id=int(paciente_id))
        except ValueError:
            flash("El paciente seleccionado no es válido.", "error")

    if medico_id:
        try:
            consulta = consulta.filter_by(medico_id=int(medico_id))
        except ValueError:
            flash("El médico seleccionado no es válido.", "error")

    citas = consulta.order_by(Cita.fecha, Cita.hora).all()
    pacientes = Paciente.query.order_by(Paciente.nombre).all()
    medicos = Medico.query.order_by(Medico.nombre).all()

    return render_template(
        "citas.html",
        citas=citas,
        pacientes=pacientes,
        medicos=medicos,
        paciente_id=paciente_id,
        medico_id=medico_id,
    )


# Formulario para registrar una cita.
@cita_bp.route("/citas/nueva", methods=["GET", "POST"])
def nueva_cita():
    if request.method == "POST":
        datos, error = obtener_datos_formulario()

        if error:
            flash(error, "error")
            return render_formulario_nueva_cita(), 400

        if existe_cita(
            datos["fecha"],
            datos["hora"],
            datos["medico_id"],
        ):
            flash(
                "Ese horario ya está ocupado para el médico seleccionado.",
                "error",
            )
            return render_formulario_nueva_cita(), 409

        try:
            cita = Cita(**datos)
            db.session.add(cita)
            db.session.commit()

            flash("La cita se registró correctamente.", "success")
            return redirect(url_for("cita.listar_citas"))

        except Exception:
            db.session.rollback()
            flash("No se pudo registrar la cita. Inténtalo de nuevo.", "error")
            return render_formulario_nueva_cita(), 500

    return render_formulario_nueva_cita()


# Consultar automáticamente los horarios disponibles.
@cita_bp.route("/citas/horarios-disponibles", methods=["GET"])
def horarios_disponibles():
    medico_id = request.args.get("medico_id", "").strip()
    fecha = request.args.get("fecha", "").strip()

    try:
        medico_id = int(medico_id)
        fecha_obj = date.fromisoformat(fecha)
    except (ValueError, TypeError):
        return jsonify({
            "error": "Selecciona un médico y una fecha válida."
        }), 400

    if fecha_obj < date.today():
        return jsonify({
            "error": "No puedes reservar en una fecha pasada."
        }), 400

    if not es_dia_atencion(fecha):
        return jsonify({
            "error": "La atención es de lunes a viernes."
        }), 400

    medico = db.session.get(Medico, medico_id)

    if medico is None:
        return jsonify({
            "error": "El médico seleccionado no existe."
        }), 404

    citas = Cita.query.filter_by(
        medico_id=medico_id,
        fecha=fecha,
    ).all()

    horarios_ocupados = {cita.hora for cita in citas}

    horarios_libres = [
        hora for hora in generar_horarios()
        if hora not in horarios_ocupados
    ]

    return jsonify({"horarios": horarios_libres})


# Editar una cita existente.
@cita_bp.route("/citas/editar/<int:id>", methods=["GET", "POST"])
def editar_cita(id):
    cita = db.session.get(Cita, id)

    if cita is None:
        flash("La cita que buscas no existe.", "error")
        return redirect(url_for("cita.listar_citas"))

    if request.method == "POST":
        datos, error = obtener_datos_formulario()

        if error:
            flash(error, "error")
        elif existe_cita(
            datos["fecha"],
            datos["hora"],
            datos["medico_id"],
            excluir_id=cita.id,
        ):
            flash(
                "Ese horario ya está ocupado para el médico seleccionado.",
                "error",
            )
        else:
            try:
                cita.fecha = datos["fecha"]
                cita.hora = datos["hora"]
                cita.motivo = datos["motivo"]
                cita.paciente_id = datos["paciente_id"]
                cita.medico_id = datos["medico_id"]

                db.session.commit()
                flash("La cita se actualizó correctamente.", "success")
                return redirect(url_for("cita.listar_citas"))

            except Exception:
                db.session.rollback()
                flash("No se pudo actualizar la cita.", "error")

    pacientes = Paciente.query.order_by(Paciente.nombre).all()
    medicos = Medico.query.order_by(Medico.nombre).all()

    return render_template(
        "editar_cita.html",
        cita=cita,
        pacientes=pacientes,
        medicos=medicos,
    )


# Cancelar una cita mediante POST.
@cita_bp.route("/citas/eliminar/<int:id>", methods=["POST"])
def eliminar_cita(id):
    cita = db.session.get(Cita, id)

    if cita is None:
        flash("La cita no existe o ya fue cancelada.", "error")
        return redirect(url_for("cita.listar_citas"))

    try:
        db.session.delete(cita)
        db.session.commit()
        flash("La cita se canceló correctamente.", "success")

    except Exception:
        db.session.rollback()
        flash("No se pudo cancelar la cita.", "error")

    return redirect(url_for("cita.listar_citas"))


# Consultar todos los horarios de un médico en una fecha.
@cita_bp.route("/disponibilidad", methods=["GET", "POST"])
def disponibilidad():
    medicos = Medico.query.order_by(Medico.nombre).all()
    horarios = generar_horarios()
    citas = []
    horarios_ocupados = {}
    medico_seleccionado = None
    fecha_seleccionada = None

    if request.method == "POST":
        medico_id = request.form.get("medico_id", "").strip()
        fecha = request.form.get("fecha", "").strip()

        try:
            medico_id = int(medico_id)
            fecha_obj = date.fromisoformat(fecha)
        except (ValueError, TypeError):
            flash("Selecciona un médico y una fecha válida.", "error")
            return render_template(
                "disponibilidad.html",
                medicos=medicos,
                citas=citas,
                horarios=horarios,
                horarios_ocupados=horarios_ocupados,
                medico_seleccionado=medico_seleccionado,
                fecha_seleccionada=fecha_seleccionada,
            )

        if fecha_obj < date.today():
            flash("No puedes consultar fechas pasadas.", "error")

        elif not es_dia_atencion(fecha):
            flash("La atención está configurada de lunes a viernes.", "error")

        else:
            medico_seleccionado = db.session.get(Medico, medico_id)

            if medico_seleccionado is None:
                flash("El médico seleccionado no existe.", "error")
            else:
                fecha_seleccionada = fecha

                citas = Cita.query.filter_by(
                    medico_id=medico_id,
                    fecha=fecha,
                ).order_by(Cita.hora).all()

                horarios_ocupados = {
                    cita.hora: cita for cita in citas
                }

    return render_template(
        "disponibilidad.html",
        medicos=medicos,
        citas=citas,
        horarios=horarios,
        horarios_ocupados=horarios_ocupados,
        medico_seleccionado=medico_seleccionado,
        fecha_seleccionada=fecha_seleccionada,
    )
