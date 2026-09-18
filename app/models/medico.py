from app import db

class Medico(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    especialidad = db.Column(
        db.String(100),
        nullable=False
    )

    telefono = db.Column(
        db.String(20)
    )

    correo = db.Column(
        db.String(100)
    )