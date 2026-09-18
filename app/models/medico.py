from app import db


class Medico(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    # Se mantiene por ahora para no perder
    # la información que ya existía.
    especialidad = db.Column(
        db.String(100),
        nullable=False
    )

    especialidad_id = db.Column(
        db.Integer,
        db.ForeignKey("especialidades.id"),
        nullable=True
    )

    telefono = db.Column(
        db.String(20)
    )

    correo = db.Column(
        db.String(100)
    )

    especialidad_relacion = db.relationship(
        "Especialidad",
        backref="medicos"
    )