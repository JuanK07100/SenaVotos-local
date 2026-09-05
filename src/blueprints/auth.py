from flask import Blueprint, render_template, request, session, redirect, url_for
from extensions import db
from models import Usuario, Ficha
from utils.decorators import no_cache

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['GET', 'POST'])
@no_cache
def home():
    mensaje = None

    if request.method == 'POST':
        documento = request.form.get('documento')
        # Buscar usuario con su ficha (para obtener la clave)
        usuario = Usuario.query.join(Ficha, Usuario.fichas_idfichas == Ficha.idfichas)\
                               .filter(Usuario.documento == documento)\
                               .add_columns(Ficha.clave).first()
        if usuario:
            user, clave_ficha = usuario
            # (Validación de clave deshabilitada)
            if user.rol not in [2, 3, 4] and user.jornada != 'virtual' and not user.asistencia_voto:
                mensaje = "Debes pasar por recepción antes de continuar a la votación."
            else:
                session.permanent = True
                session['usuario'] = {
                    'documento': user.documento,
                    'nombre': user.nombre,
                    'rol': user.rol,
                    'jornada': user.jornada,
                    'idusuario': user.idusuario
                }
                # Redirigir según rol
                if user.rol == 1:
                    destino = 'eleccion'
                elif user.rol == 2:
                    destino = 'admin'
                elif user.rol == 3:
                    destino = 'recepcionista'
                elif user.rol == 4:
                    destino = 'resultados'
                else:
                    destino = 'eleccion'
                return redirect(url_for('auth.carga', destino=destino))
        else:
            mensaje = "El número de documento ingresado no está registrado. Por favor, inténtelo de nuevo."

    return render_template('index.html', mensaje=mensaje)

@bp.route('/carga')
@no_cache
def carga():
    destino = request.args.get('destino', 'eleccion')
    return render_template('carga.html', destino=destino)