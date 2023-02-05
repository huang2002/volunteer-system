import os
import time
import re
import pandas as pd
from typing import NoReturn

BACKEND_PATH = os.path.dirname(__file__)
FRONTEND_PATH = os.path.join(BACKEND_PATH, '../frontend')
DATA_PATH = os.path.join(BACKEND_PATH, '../data')
BACKUP_PATH = os.path.join(BACKEND_PATH, '../backup')

DATE_FORMAT = '%Y/%m/%d'
PATTERN_TABLE_NAME = re.compile(r'^\d{2}$')

INDEX_NAME = 'record_id'
DTYPES: dict[str, str] = {
    'student_school': 'string',
    'student_class': 'string',
    'student_name': 'string',
    'student_id': 'string',
    'activity_length': 'string',
    'activity_name': 'string',
    'activity_type': 'string',
    'activity_host': 'string',
    'manager_name': 'string',
    'manager_qq': 'string',
    'notes': 'string',
}
DATE_COLUMNS = [
    'activity_date',
]
COLUMNS: list[str] = DATE_COLUMNS + list(DTYPES.keys())

RESPONSE_SUCCESS = ('success', 200)
RESPONSE_INVALID_TABLE_NAME = ('表名不符合要求', 403)
RESPONSE_DUPLICATE_TABLE_NAME = ('指定的表已经存在', 403)
RESPONSE_TABLE_NOT_FOUND = ('指定的表不存在', 400)
RESPONSE_INVALID_RECORD = ('记录不符合要求', 400)
RESPONSE_TOO_FREQUENT = ('操作太频繁，请稍后重试', 403)
RESPONSE_RECORD_NOT_FOUND = ('指定的记录不存在', 400)


def is_valid_table_name(table_name: str) -> bool:
    return PATTERN_TABLE_NAME.match(table_name) != None


def get_table_path(table_name: str) -> str:
    assert is_valid_table_name(table_name)
    return os.path.join(DATA_PATH, f'{table_name}.csv')


def init_table(path: str) -> NoReturn:
    df = pd.DataFrame(columns=[INDEX_NAME, *COLUMNS])
    df.to_csv(path, index=False)


def read_table(path: str) -> pd.DataFrame:
    return pd.read_csv(
        path,
        index_col=INDEX_NAME,
        infer_datetime_format=True,
        dtype=DTYPES,
        parse_dates=DATE_COLUMNS,
    )


def save_table(df: pd.DataFrame, path: str) -> NoReturn:
    df.to_csv(
        path,
        date_format=DATE_FORMAT,
    )
