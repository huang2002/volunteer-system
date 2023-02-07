import shutil
from flask import Flask
from common import *
from common_backup import *


def inject_backup_apis(app: Flask):

    @app.get('/api/list/backups')
    def list_backups():
        return jsonify([
            os.path.splitext(backup_path)[0]
            for backup_path in os.listdir(BACKUP_DIR)
            if os.path.isdir(backup_path)
        ])

    @app.get('/api/create/backup/<backup_name>')
    def create_backup(backup_name: str):
        if not is_valid_backup_name(backup_name):
            return RESPONSE_INVALID_BACKUP_NAME
        target_path = os.path.join(BACKUP_DIR, backup_name)
        if os.path.exists(target_path):
            return RESPONSE_DUPLICATE_BACKUP
        shutil.copytree(DATA_DIR, target_path)
