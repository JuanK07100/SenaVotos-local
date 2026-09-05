# SenaVotos-local
SenaVotos/
├── src/
│   ├── __init__.py          # (opcional) para convertir en paquete
│   ├── app.py               # (punto de entrada, con create_app)
│   ├── config.py
│   ├── extensions.py
│   ├── blueprints/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── eleccion.py
│   │   ├── admin.py
│   │   ├── recepcionista.py
│   │   ├── candidatos.py
│   │   ├── resultados.py
│   │   └── fichas.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── decorators.py
│   │   └── helpers.py
│   ├── static/              (sin cambios)
│   └── templates/           (sin cambios)
├── uploads/                 (ya existe)
└── (otros archivos como README.md)