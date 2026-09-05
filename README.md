```markdown
# SenaVotos - Sistema de Votaciones SENA

Sistema web para gestionar votaciones de aprendices del SENA, con roles diferenciados (votante, recepcionista, administrador, visualizador de resultados). Desarrollado con Flask, SQLAlchemy y MySQL.

## Características

- Autenticación por número de documento (clave deshabilitada en desarrollo).
- Asignación automática de mesa (computador) mediante cola aleatoria.
- Votación por jornada (mañana, tarde, mixta, virtual) con horario de cierre configurable (22:00).
- Panel de administración con filtros y exportación a Excel (incluye gráfico de barras).
- Visualización de resultados en tiempo real con Chart.js.
- Gestión de fichas (carga masiva de aprendices desde Excel).
- CRUD completo de candidatos con foto.
- Interfaz responsive y moderna.

## Tecnologías

- **Backend**: Flask, SQLAlchemy, PyMySQL
- **Frontend**: HTML5, CSS3, JavaScript (jQuery, Chart.js, SweetAlert2)
- **Base de datos**: MySQL / MariaDB
- **Procesamiento de archivos**: Pandas, OpenPyXL

## Requisitos previos

- Python 3.8 o superior
- MySQL/MariaDB instalado y en ejecución
- Entorno virtual (recomendado)

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/JuanK07100/SenaVotos-local.git
cd SenaVotos-local
```

2. Crea y activa un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura la base de datos:
   - Asegúrate de que MySQL esté corriendo.
   - Crea la base de datos: `CREATE DATABASE senavotos;`
   - Ajusta las credenciales en `src/config.py` si es necesario.

5. Inicializa las tablas y crea un usuario administrador:
```bash
cd src
python seed.py
```

6. Ejecuta la aplicación:
```bash
python app.py
```

7. Abre http://127.0.0.1:5000 en tu navegador.

## Configuración

El archivo `src/config.py` contiene:

- `SECRET_KEY`: Clave secreta de Flask.
- `SQLALCHEMY_DATABASE_URI`: Conexión a MySQL.
- `UPLOAD_FOLDER`: Carpeta para archivos subidos.
- `ALLOWED_EXTENSIONS`: Extensiones permitidas para carga.

## Estructura del proyecto

```
src/
├── app.py                 # Punto de entrada (fábrica de la app)
├── config.py              # Configuraciones
├── extensions.py          # Instancia de SQLAlchemy
├── models.py              # Definición de modelos (Ficha, Usuario, Candidato, Voto)
├── seed.py                # Script para crear datos iniciales (admin)
├── blueprints/            # Módulos por funcionalidad
│   ├── auth.py            # Login, carga
│   ├── eleccion.py        # Votación
│   ├── admin.py           # Panel de administración
│   ├── recepcionista.py   # Asignación de mesa
│   ├── candidatos.py      # CRUD de candidatos
│   ├── resultados.py      # Resultados en tiempo real
│   └── fichas.py          # Carga masiva de fichas
├── templates/             # Plantillas HTML
├── static/                # CSS, JS, imágenes
├── utils/                 # Decoradores y helpers
└── uploads/               # Archivos subidos (creada automáticamente)
```

## Roles y rutas

| Rol | Descripción | Ruta principal |
|-----|-------------|----------------|
| Votante (1) | Vota por un candidato | `/eleccion` |
| Administrador (2) | Gestiona votos, fichas, candidatos | `/admin` |
| Recepcionista (3) | Valida documento y asigna mesa | `/recepcionista` |
| Resultados (4) | Visualiza gráficos en vivo | `/resultados` |

## Script seed.py

El script `seed.py` crea automáticamente:
- Una ficha de prueba (`123456` - ADSO).
- Un usuario administrador con documento `123456789`, contraseña (deshabilitada) y rol 2.

Ejecútalo una sola vez al iniciar el proyecto para tener un admin funcional.

## Archivo .gitignore recomendado

Crea un archivo `.gitignore` en la raíz con este contenido:

```gitignore
# Entornos virtuales
venv/
env/
.venv/
*.pyc
__pycache__/

# Archivos de base de datos locales
*.db
*.sqlite
*.sqlite3

# Archivos de configuración sensibles
*.env
config_local.py

# Uploads y archivos generados
src/uploads/
*.xlsx
*.xls
*.log

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Scripts de snapshot (para no subir el generador de estructura)
snapshot_*.txt
estructura_*.txt

# Sistema operativo
.DS_Store
Thumbs.db
```

## Contribución

1. Haz un fork del repositorio.
2. Crea una rama con tu feature: `git checkout -b feature/nueva-funcionalidad`.
3. Realiza tus cambios y haz commit: `git commit -m "Agrega nueva funcionalidad"`.
4. Sube a tu fork: `git push origin feature/nueva-funcionalidad`.
5. Abre un Pull Request en el repositorio original.

## Licencia

Este proyecto es de uso interno del SENA y no tiene licencia pública definida. Consulta con el administrador del sistema para más información.

## Contacto

Para dudas o reportes, contacta al equipo de desarrollo del SENA (o al autor del repositorio).
```

### Nota adicional sobre el script seed y el .gitignore

- **Script seed**: Como explico en el README, solo crea un admin de prueba. Puedes ejecutarlo cuantas veces quieras, pero si ya existen los datos, no los duplicará (valida existencia). Si deseas resetear la base, puedes eliminar las tablas y volver a ejecutarlo.

- **Archivo .gitignore**: Te he incluido un bloque en el README con el contenido recomendado. Crea el archivo `.gitignore` en la raíz de tu proyecto y pega ese contenido. Asegura que no se suban `venv/`, `snapshot_*.txt` (tu script de estructura), `src/uploads/`, etc. Luego haz `git add .gitignore` y commitea.

Si necesitas que ajuste algo del README (ejemplo: cambiar el nombre del usuario, agregar más detalles de la instalación, etc.), dímelo y lo modifico.