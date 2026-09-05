from flask import Blueprint, render_template, request, session, redirect, url_for
from extensions import mysql
from utils.decorators import no_cache
import MySQLdb.cursors
import pytz
from datetime import datetime

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['GET', 'POST'])
@no_cache
def home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mensaje = None
    # ... todo el código de home (igual que en app.py)
    return render_template('index.html', mensaje=mensaje)

@bp.route('/carga')
@no_cache
def carga():
    destino = request.args.get('destino', 'eleccion')
    return render_template('carga.html', destino=destino)