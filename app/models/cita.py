from app import db


class Cita(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    fecha = db.Column(
        db.String(20),
        nullable=False
    )

    hora = db.Column(
        db.String(10),
        nullable=False
    )

    motivo = db.Column(
        db.String(200)
    )

    paciente_id = db.Column(
        db.Integer,
        db.ForeignKey("pacientes.id"),
        nullable=False
    )

    medico_id = db.Column(
        db.Integer,
        db.ForeignKey("medico.id"),
        nullable=False
    )