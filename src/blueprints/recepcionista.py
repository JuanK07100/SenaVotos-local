from flask import Blueprint, render_template, request, jsonify, session
from extensions import db
from models import Usuario
from utils.decorators import no_cache
import random

bp = Blueprint('recepcionista', __name__, url_prefix='/recepcionista')

@bp.route('/')
@no_cache
def recepcionista():
    return render_template('recepcionista.html')

@bp.route('/buscar_votante', methods=['POST'])
@no_cache
def buscar_votante():
    data = request.get_json()
    documento = data.get('documento')
    if not documento:
        return jsonify({"status": "error", "message": "Documento no proporcionado."})

    usuario = Usuario.query.filter_by(documento=documento).first()
    if not usuario:
        return jsonify({"status": "error", "message": "Documento no Registrado."})

    if usuario.asistencia_voto == 0:
        # Cola de mesas en sesión (como antes)
        if 'cola_mesas' not in session or not session['cola_mesas']:
            mesas = list(range(1, 11))
            random.shuffle(mesas)
            session['cola_mesas'] = mesas
        mesa_asignada = session['cola_mesas'].pop(0)

        # Actualizar
        usuario.asistencia_voto = True
        usuario.mesa = mesa_asignada
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"{usuario.nombre} Listo Para Votar.",
            "data": {
                "documento": usuario.documento,
                "nombre": usuario.nombre,
                "ficha": usuario.fichas_idfichas,
                "jornada": usuario.jornada,
                "mesa": mesa_asignada
            }
        })
    else:
        return jsonify({
            "status": "warning",
            "message": f"{usuario.nombre} Ya Votó.",
            "data": {
                "documento": usuario.documento,
                "nombre": usuario.nombre,
                "ficha": usuario.fichas_idfichas,
                "jornada": usuario.jornada,
                "mesa": usuario.mesa
            }
        })