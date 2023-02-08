from .table import inject_table_apis
from .backup import inject_backup_apis
from .common import Flask, FRONTEND_PATH

__all__ = [
    'PORT',
    'app',
]

PORT = 2023

app = Flask(
    __name__,
    static_url_path='',
    static_folder=FRONTEND_PATH,
)

app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # bytes

inject_table_apis(app)
inject_backup_apis(app)
