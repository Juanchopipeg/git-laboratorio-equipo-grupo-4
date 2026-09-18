from app import db


class Especialidad(db.Model):

    __tablename__ = "especialidades"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    descripcion = db.Column(
        db.String(200)
    )