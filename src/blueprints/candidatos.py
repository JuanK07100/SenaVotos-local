from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from extensions import db
from models import Candidato
from utils.decorators import no_cache

bp = Blueprint('candidatos', __name__, url_prefix='/candidatos')

@bp.route('/crear', methods=['GET', 'POST'])
@no_cache
def crear_candidato():
    if request.method == 'POST':
        nombre = request.form['nombre_candidato']
        jornada = request.form['jornada']
        foto = request.files['foto_candidato'].read() if 'foto_candidato' in request.files else None

        nuevo = Candidato(nombre_candidato=nombre, jornada=jornada, foto=foto)
        db.session.add(nuevo)
        db.session.commit()
        flash('¡Candidato creado exitosamente!', 'success')
        return redirect(url_for('candidatos.crear_candidato'))

    # Listar candidatos agrupados por nombre (similar a antes)
    # Usamos SQLAlchemy para agrupar
    from sqlalchemy import func
    candidatos = db.session.query(
        func.min(Candidato.idcandidato).label('idcandidato'),
        Candidato.nombre_candidato,
        func.group_concat(Candidato.jornada, ', ').label('jornadas')
    ).group_by(Candidato.nombre_candidato).all()

    return render_template('crear_candidato.html', candidatos=candidatos)

@bp.route('/')
def listar_candidatos():
    from sqlalchemy import func
    candidatos = db.session.query(
        func.min(Candidato.idcandidato).label('idcandidato'),
        Candidato.nombre_candidato,
        func.group_concat(Candidato.jornada, ', ').label('jornadas')
    ).group_by(Candidato.nombre_candidato).all()
    return render_template('crear_candidato.html', candidatos=candidatos)

@bp.route('/foto/<int:idcandidato>')
def foto_candidato(idcandidato):
    candidato = Candidato.query.get(idcandidato)
    if candidato and candidato.foto:
        return Response(candidato.foto, mimetype="image/jpeg")
    return "Sin foto", 404

@bp.route('/editar/<int:idcandidato>', methods=['GET', 'POST'])
def editar_candidato(idcandidato):
    candidato = Candidato.query.get(idcandidato)
    if not candidato:
        flash('Candidato no encontrado', 'error')
        return redirect(url_for('candidatos.listar_candidatos'))

    if request.method == 'POST':
        candidato.nombre_candidato = request.form['nombre_candidato']
        candidato.jornada = request.form['jornada']
        if 'foto_candidato' in request.files and request.files['foto_candidato'].filename != '':
            candidato.foto = request.files['foto_candidato'].read()
        db.session.commit()
        flash('Candidato actualizado correctamente', 'success')
        return redirect(url_for('candidatos.listar_candidatos'))

    return render_template('editar_candidato.html', candidato=candidato)

@bp.route('/eliminar/<int:idcandidato>')
def eliminar_candidato(idcandidato):
    candidato = Candidato.query.get(idcandidato)
    if candidato:
        db.session.delete(candidato)
        db.session.commit()
        flash('Candidato eliminado correctamente', 'success')
    else:
        flash('Candidato no encontrado', 'error')
    return redirect(url_for('candidatos.listar_candidatos'))