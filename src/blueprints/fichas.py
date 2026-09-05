from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import mysql
from utils.decorators import no_cache
from utils.helpers import allowed_file
import pandas as pd
import hashlib
import pymysql

bp = Blueprint('fichas', __name__, url_prefix='/fichas')  # o sin prefijo, según prefieras

@bp.route('/upload', methods=['GET', 'POST'])
@no_cache
def upload():
    return render_template('upload.html')

@bp.route('/procesar_fichas', methods=['POST'])
@no_cache
def procesar_fichas():
    # ... copia exacta
    return redirect(url_for('fichas.upload'))  # o 'upload' si usas el mismo blueprint