from flask import Blueprint, render_template, request, session, redirect, url_for
from extensions import db
from models import Usuario, Candidato, Voto
from utils.decorators import no_cache
import pytz
from datetime import datetime
from base64 import b64encode

bp = Blueprint('eleccion', __name__)

@bp.route('/eleccion', methods=['GET', 'POST'])
@no_cache
def eleccion():
    # Verificar hora de cierre (22:00)
    zona_colombia = pytz.timezone("America/Bogota")
    hora_actual = datetime.now(zona_colombia).time()
    hora_cierre = datetime.strptime("22:00", "%H:%M").time()
    if hora_actual >= hora_cierre:
        return render_template('eleccion_cerrada.html')

    if 'usuario' not in session:
        return redirect(url_for('auth.home'))

    usuario_id = session['usuario']['idusuario']
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return redirect(url_for('auth.home'))

    # Verificar si ya votó
    voto_existente = Voto.query.filter_by(usuarios_idusuario=usuario_id).first()
    if voto_existente:
        return render_template('eleccion.html', candidatos=[], mensaje="Ya has votado. No puedes realizar más de un voto.")

    # Obtener candidatos de la misma jornada
    candidatos = Candidato.query.filter_by(jornada=usuario.jornada).all()
    # Convertir fotos a base64 para mostrarlas
    for c in candidatos:
        if c.foto:
            c.foto_b64 = b64encode(c.foto).decode('utf-8')

    if request.method == 'POST':
        candidato_id = request.form.get('candidato_id')
        if candidato_id:
            # Verificar nuevamente que no haya votado (por seguridad)
            if Voto.query.filter_by(usuarios_idusuario=usuario_id).first():
                return redirect(url_for('eleccion.gracias'))
            nuevo_voto = Voto(
                usuarios_idusuario=usuario_id,
                candidatos_idcandidato=candidato_id,
                fecha_hora=datetime.now(zona_colombia)
            )
            db.session.add(nuevo_voto)
            db.session.commit()
            return redirect(url_for('eleccion.gracias'))
        else:
            mensaje = "Debe seleccionar un candidato para continuar."
            return render_template('eleccion.html', candidatos=candidatos, mensaje=mensaje)

    return render_template('eleccion.html', candidatos=candidatos, mensaje=None)

@bp.route('/gracias')
@no_cache
def gracias():
    return render_template('gracias.html')