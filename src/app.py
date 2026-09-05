from flask import Flask
from config import Config
from extensions import mysql
from utils.helpers import base64_encode

# Importar blueprints
from blueprints.auth import bp as auth_bp
from blueprints.eleccion import bp as eleccion_bp
from blueprints.admin import bp as admin_bp
from blueprints.recepcionista import bp as recepcionista_bp
from blueprints.candidatos import bp as candidatos_bp
from blueprints.resultados import bp as resultados_bp
from blueprints.fichas import bp as fichas_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    mysql.init_app(app)

    # Registrar filtro
    app.add_template_filter(base64_encode, 'b64encode')

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(eleccion_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(recepcionista_bp)
    app.register_blueprint(candidatos_bp)
    app.register_blueprint(resultados_bp)
    app.register_blueprint(fichas_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)