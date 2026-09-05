class Config:
    
    SECRET_KEY = 'd4i8e2g1o7n#'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:DdiegoCenT4821#@localhost/senavotos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'xlsx'}