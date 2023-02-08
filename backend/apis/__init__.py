from flask import Flask
from .table import inject_table_apis
from .backup import inject_backup_apis
from .common import *

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

inject_table_apis(app)
inject_backup_apis(app)
