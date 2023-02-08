from common import *
from werkzeug.utils import safe_join

__all__ = [
    'RESPONSE_DUPLICATE_BACKUP',
    'is_valid_backup_name',
    'get_backup_path',
]

RESPONSE_INVALID_BACKUP_NAME = ('备份名称不符合要求', 403)
RESPONSE_DUPLICATE_BACKUP = ('备份名称已经存在', 403)
RESPONSE_BACKUP_NOT_FOUND = ('指定的备份不存在', 404)


def is_valid_backup_name(name: str) -> bool:
    return safe_join('', name) == name


def get_backup_path(backup_name: str) -> str:
    assert is_valid_backup_name(backup_name)
    return os.path.join(BACKUP_DIR, backup_name)
