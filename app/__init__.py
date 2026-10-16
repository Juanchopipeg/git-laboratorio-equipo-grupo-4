
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    session,
    request
)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    from app.models.paciente import Paciente
    from app.models.medico import Medico
    from app.models.cita import Cita
    from app.models.especialidad import Especialidad
    from app.models.usuario import Usuario

    from app.routes.paciente_routes import paciente_bp
    from app.routes.medico_routes import medico_bp
    from app.routes.cita_routes import cita_bp
    from app.routes.especialidad_routes import especialidad_bp
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(paciente_bp)
    app.register_blueprint(medico_bp)
    app.register_blueprint(cita_bp)
    app.register_blueprint(especialidad_bp)
    app.register_blueprint(auth_bp)

    @app.route("/")
    def inicio():
        return render_template("inicio.html")
    
    @app.before_request
    def proteger_paginas():
        # El login y los archivos estáticos son públicos.
        if request.endpoint in ("auth.login", "static"):
            return None

        # Si no hay sesión iniciada, ir al login.
        if not session.get("usuario_id"):
            return redirect(url_for("auth.login"))
    return app
