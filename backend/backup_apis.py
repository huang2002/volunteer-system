import shutil
from flask import Flask
from common import *


def inject_backup_apis(app: Flask):

    @app.get('/api/create/backup')
    def create_backup():
        timestamp = time.strftime('%Y.%m.%d_%H:%M:%S')
        target_path = os.path.join(BACKUP_PATH, timestamp)
        if os.path.exists(target_path):
            return RESPONSE_TOO_FREQUENT
        shutil.copytree(DATA_PATH, target_path)
