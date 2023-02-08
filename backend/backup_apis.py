import shutil
from flask import Flask, jsonify
from common import *
from common_backup import *


def inject_backup_apis(app: Flask):

    @app.get('/api/list/backups')
    def list_backups():
        return jsonify(
            sorted(
                backup_name
                for backup_name in os.listdir(BACKUP_DIR)
                if os.path.isdir(get_backup_path(backup_name))
            )
        )

    @app.get('/api/create/backup/<backup_name>')
    def create_backup(backup_name: str):
        if not is_valid_backup_name(backup_name):
            return RESPONSE_INVALID_BACKUP_NAME
        target_path = get_backup_path(backup_name)
        if os.path.exists(target_path):
            return RESPONSE_DUPLICATE_BACKUP
        shutil.copytree(DATA_DIR, target_path)
        return RESPONSE_SUCCESS

    @app.get('/api/rename/backup/<source>/<destination>')
    def rename_backup(source: str, destination: str):

        if not (
            is_valid_backup_name(source)
            and is_valid_backup_name(destination)
        ):
            return RESPONSE_INVALID_BACKUP_NAME

        source_path = get_backup_path(source)
        if not os.path.exists(source_path):
            return RESPONSE_BACKUP_NOT_FOUND

        destination_path = get_backup_path(destination)
        if os.path.exists(destination_path):
            return RESPONSE_DUPLICATE_BACKUP

        os.rename(source_path, destination_path)
        return RESPONSE_SUCCESS

    @app.get('/api/delete/backup/<backup_name>')
    def delete_backup(backup_name: str):

        if not is_valid_backup_name(backup_name):
            return RESPONSE_INVALID_BACKUP_NAME

        backup_path = get_backup_path(backup_name)
        if not os.path.exists(backup_path):
            return RESPONSE_BACKUP_NOT_FOUND

        shutil.rmtree(backup_path)
        return RESPONSE_SUCCESS
