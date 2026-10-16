
from getpass import getpass
from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():
    # Crea las tablas que falten, sin borrar las existentes.
    db.create_all()

    nombre = input("Nombre de usuario administrador: ").strip()

    if not nombre:
        print("El nombre de usuario no puede estar vacío.")
        raise SystemExit(1)

    existente = Usuario.query.filter_by(
        nombre_usuario=nombre
    ).first()

    if existente:
        print("Ese usuario ya existe. No se realizaron cambios.")
        raise SystemExit(0)

    password = getpass("Crea una contraseña: ")
    confirmacion = getpass("Repite la contraseña: ")

    if len(password) < 12:
        print("Usa una contraseña de al menos 12 caracteres.")
        raise SystemExit(1)

    if password != confirmacion:
        print("Las contraseñas no coinciden.")
        raise SystemExit(1)

    usuario = Usuario(nombre_usuario=nombre)
    usuario.establecer_password(password)

    db.session.add(usuario)
    db.session.commit()

    print("Usuario administrador creado correctamente.")
