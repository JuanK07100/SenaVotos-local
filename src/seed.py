from app import create_app
from extensions import db
from models import Ficha, Usuario
import hashlib

app = create_app()
with app.app_context():
    # Crear ficha si no existe
    ficha_id = '123456'
    ficha = Ficha.query.get(ficha_id)
    if not ficha:
        ficha = Ficha(
            idfichas=ficha_id,
            nombre_programa='ADSO',
            clave=hashlib.sha256('ADSO-123'.encode()).hexdigest()
        )
        db.session.add(ficha)
        print("Ficha creada.")

    # Crear usuario admin si no existe
    admin = Usuario.query.filter_by(documento='123456789').first()
    if not admin:
        admin = Usuario(
            documento='123456789',
            nombre='Administrador',
            celular='3100000000',
            correo='admin@admin.com',
            rol=2,
            jornada='mañana',
            asistencia_voto=False,
            fichas_idfichas=ficha_id
        )
        db.session.add(admin)
        print("Administrador creado.")
    else:
        print("El administrador ya existe.")

    db.session.commit()
    print("Datos iniciales cargados correctamente.")