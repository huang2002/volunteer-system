from common import *
from werkzeug.utils import safe_join

__all__ = [
    'RESPONSE_DUPLICATE_BACKUP',
    'is_valid_backup_name',
]

RESPONSE_INVALID_BACKUP_NAME = ('备份名称不符合要求', 403)
RESPONSE_DUPLICATE_BACKUP = ('备份名称已经存在', 403)


def is_valid_backup_name(name: str) -> bool:
    return safe_join('', name) == name
