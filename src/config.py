import os

class Config:
    SECRET_KEY = 'd4i8e2g1o7n#'  # luego lo moverás a variables de entorno
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'DdiegoCenT4821#'
    MYSQL_DB = 'senavotos'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')  # o 'uploads/'
    ALLOWED_EXTENSIONS = {'xlsx'}