from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Ficha, Usuario
from utils.decorators import no_cache
from utils.helpers import allowed_file
import pandas as pd
import hashlib

bp = Blueprint('fichas', __name__, url_prefix='/fichas')

@bp.route('/upload', methods=['GET', 'POST'])
@no_cache
def upload():
    return render_template('upload.html')

@bp.route('/procesar_fichas', methods=['POST'])
@no_cache
def procesar_fichas():
    file = request.files.get('file')
    jornada = request.form.get('jornada')

    if not jornada or jornada not in ['mañana', 'tarde', 'mixta', 'virtual']:
        flash('Por favor, selecciona una jornada válida.', 'danger')
        return redirect(url_for('fichas.upload'))

    if not file or not allowed_file(file.filename):
        flash('Por favor, sube un archivo Excel válido (.xlsx).', 'danger')
        return redirect(url_for('fichas.upload'))

    try:
        df = pd.read_excel(file, sheet_name=0, header=None)

        ficha_combined = df.iloc[1, 2]
        if pd.isna(ficha_combined) or ficha_combined.strip() == '':
            raise ValueError("El campo 'Ficha de Caracterización' está vacío.")

        ficha_combined = ficha_combined.strip()
        if '-' in ficha_combined:
            id_ficha, nombre_programa = ficha_combined.split('-', 1)
            id_ficha = id_ficha.strip()
            nombre_programa = nombre_programa.strip()
        else:
            raise ValueError("Formato inválido: se esperaba 'ID - Nombre del programa'.")

        clave_original = f"{id_ficha[:3]}-{nombre_programa[:3]}".upper()
        clave_hash = hashlib.sha256(clave_original.encode('utf-8')).hexdigest()

        # Verificar si la ficha ya existe
        if Ficha.query.get(id_ficha):
            flash(f"La ficha con ID {id_ficha} ya existe en el sistema.", "danger")
            return redirect(url_for('fichas.upload'))

        # Crear ficha
        nueva_ficha = Ficha(idfichas=id_ficha, nombre_programa=nombre_programa, clave=clave_hash)
        db.session.add(nueva_ficha)

        # Procesar aprendices (filas 5 a 32)
        for row in df.iloc[5:33].itertuples(index=False):
            documento = row[1]
            nombre = row[2]
            apellidos = row[3]
            celular = str(row[4]).strip() if len(row) > 4 and not pd.isna(row[4]) else None
            correo = str(row[5]).strip() if len(row) > 5 and not pd.isna(row[5]) else None

            if pd.isna(documento) or pd.isna(nombre) or pd.isna(apellidos):
                continue

            nombre_completo = f"{nombre.strip()} {apellidos.strip()}"
            usuario = Usuario(
                documento=str(documento).strip(),
                nombre=nombre_completo,
                celular=celular,
                correo=correo,
                fichas_idfichas=id_ficha,
                jornada=jornada
            )
            db.session.add(usuario)

        db.session.commit()
        flash("Datos de la ficha y aprendices guardados correctamente.", "success")

    except Exception as e:
        db.session.rollback()
        flash("Error al procesar el archivo. Verifica que el formato sea correcto.", "danger")
        print("[ERROR]", str(e))

    return redirect(url_for('fichas.upload'))