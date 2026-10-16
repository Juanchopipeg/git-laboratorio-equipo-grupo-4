
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )
    password_hash = db.Column(db.String(255), nullable=False)

    def establecer_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verificar_password(self, password):
        return check_password_hash(self.password_hash, password)
