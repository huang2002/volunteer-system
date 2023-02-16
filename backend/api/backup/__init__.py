from ..common import *
from .common import *

backup_blueprint = Blueprint('backup', __name__, url_prefix='/backup')


@backup_blueprint.get('/list')
def list_() -> Any:
    return jsonify([
        {
            'name': backup_name,
            'tables': [
                filename[:-4]
                for filename in os.listdir(
                    get_backup_path(backup_name)
                )
                if filename.endswith('.csv')
            ],
        }
        for backup_name in sorted(
            backup_name
            for backup_name in os.listdir(BACKUP_DIR)
            if os.path.isdir(get_backup_path(backup_name))
        )
    ])


@backup_blueprint.get('/create/<backup_name>')
def create(backup_name: str) -> ResponseType:
    if not is_valid_backup_name(backup_name):
        return RESPONSE_INVALID_BACKUP_NAME
    target_path = get_backup_path(backup_name)
    if os.path.exists(target_path):
        return RESPONSE_DUPLICATE_BACKUP
    shutil.copytree(DATA_DIR, target_path)
    return RESPONSE_SUCCESS


@backup_blueprint.get('/rename/<source>/<destination>')
def rename(source: str, destination: str) -> ResponseType:

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


@backup_blueprint.get('/load/<backup_name>')
def load(backup_name: str) -> ResponseType:

    if not is_valid_backup_name(backup_name):
        return RESPONSE_INVALID_BACKUP_NAME

    backup_path = get_backup_path(backup_name)
    if not os.path.exists(backup_path):
        return RESPONSE_BACKUP_NOT_FOUND

    shutil.rmtree(DATA_DIR)
    shutil.copytree(backup_path, DATA_DIR)
    return RESPONSE_SUCCESS


@backup_blueprint.get('/delete/<backup_name>')
def delete(backup_name: str) -> ResponseType:

    if not is_valid_backup_name(backup_name):
        return RESPONSE_INVALID_BACKUP_NAME

    backup_path = get_backup_path(backup_name)
    if not os.path.exists(backup_path):
        return RESPONSE_BACKUP_NOT_FOUND

    shutil.rmtree(backup_path)
    return RESPONSE_SUCCESS
