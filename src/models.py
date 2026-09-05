from extensions import db
from datetime import datetime

class Ficha(db.Model):
    __tablename__ = 'fichas'

    idfichas = db.Column(db.String(20), primary_key=True)
    nombre_programa = db.Column(db.String(100), nullable=False)
    clave = db.Column(db.String(255), nullable=False)

    usuarios = db.relationship('Usuario', backref='ficha', lazy=True)


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    idusuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    documento = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(15))
    correo = db.Column(db.String(100))
    rol = db.Column(db.Integer, default=1)
    jornada = db.Column(db.Enum('mañana', 'tarde', 'mixta', 'virtual'), nullable=False)
    asistencia_voto = db.Column(db.Boolean, default=False)
    mesa = db.Column(db.Integer)

    fichas_idfichas = db.Column(db.String(20), db.ForeignKey('fichas.idfichas'), nullable=False)

    votos = db.relationship('Voto', backref='usuario', lazy=True)


class Candidato(db.Model):
    __tablename__ = 'candidatos'

    idcandidato = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_candidato = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.LargeBinary)
    jornada = db.Column(db.Enum('mañana', 'tarde', 'mixta', 'virtual'), nullable=False)

    votos = db.relationship('Voto', backref='candidato', lazy=True)


class Voto(db.Model):
    __tablename__ = 'votos'

    idvoto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)

    usuarios_idusuario = db.Column(db.Integer, db.ForeignKey('usuarios.idusuario'), nullable=False)
    candidatos_idcandidato = db.Column(db.Integer, db.ForeignKey('candidatos.idcandidato'), nullable=False)