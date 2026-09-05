from flask import Blueprint, render_template, jsonify
from extensions import db
from models import Candidato, Voto
from utils.decorators import no_cache
from sqlalchemy import func

bp = Blueprint('resultados', __name__, url_prefix='/resultados')

@bp.route('/')
@no_cache
def resultados():
    # Obtener conteos por candidato y jornada
    resultados = db.session.query(
        Candidato.idcandidato,
        Candidato.nombre_candidato,
        Candidato.jornada,
        func.count(Voto.idvoto).label('total_votos')
    ).outerjoin(Voto, Voto.candidatos_idcandidato == Candidato.idcandidato)\
     .group_by(Candidato.idcandidato, Candidato.jornada)\
     .all()

    # Agrupar por jornada
    resultados_por_jornada = {
        "mañana": [],
        "tarde": [],
        "mixta": [],
        "virtual": []
    }
    for r in resultados:
        jornada = r.jornada
        if jornada in resultados_por_jornada:
            resultados_por_jornada[jornada].append({
                'idcandidato': r.idcandidato,
                'nombre_candidato': r.nombre_candidato,
                'total_votos': r.total_votos,
                'jornada': r.jornada
            })

    return render_template('resultados.html', resultados=resultados_por_jornada)

@bp.route('/datos')
def actualizar_resultados():
    resultados = db.session.query(
        Candidato.idcandidato,
        Candidato.nombre_candidato,
        Candidato.jornada,
        func.count(Voto.idvoto).label('total_votos')
    ).outerjoin(Voto, Voto.candidatos_idcandidato == Candidato.idcandidato)\
     .group_by(Candidato.idcandidato, Candidato.jornada)\
     .all()

    resultados_por_jornada = {
        "mañana": [],
        "tarde": [],
        "mixta": [],
        "virtual": []
    }
    for r in resultados:
        jornada = r.jornada
        if jornada in resultados_por_jornada:
            resultados_por_jornada[jornada].append({
                'idcandidato': r.idcandidato,
                'nombre_candidato': r.nombre_candidato,
                'total_votos': r.total_votos,
                'jornada': r.jornada
            })
    return jsonify(resultados_por_jornada)