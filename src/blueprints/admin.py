from flask import Blueprint, render_template, request, jsonify, render_template_string, make_response, send_file
from extensions import mysql
from utils.decorators import no_cache
import MySQLdb.cursors
import io
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.chart import BarChart, Reference, Series
from openpyxl.utils import get_column_letter
from openpyxl.chart.label import DataLabelList

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@no_cache
def admin():
    # ... copia exacta
    return render_template('admin.html', votos=votos)

@bp.route('/votos')
def actualizar_votos():
    # ... copia exacta
    return jsonify(...)

@bp.route('/exportar_excel', methods=['POST'])
def exportar_excel():
    # ... copia exacta
    return send_file(...)