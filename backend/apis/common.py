import os
import time
import datetime
import re
import pandas as pd
from flask import Flask, request, jsonify
from typing import NoReturn

BACKEND_PATH = os.path.join(os.path.dirname(__file__), '..')
FRONTEND_PATH = os.path.join(BACKEND_PATH, '../frontend')
DATA_DIR = os.path.join(BACKEND_PATH, '../data')
BACKUP_DIR = os.path.join(BACKEND_PATH, '../backup')

RESPONSE_SUCCESS = ('success', 200)
RESPONSE_TOO_FREQUENT = ('操作太频繁，请稍后重试', 403)

DATE_DTYPE = 'datetime64'
DATE_FORMAT = '%Y/%m/%d'

INDEX_NAME = 'record_id'
NON_DATE_DTYPES: dict[str, str] = {
    'student_school': 'string',
    'student_class': 'string',
    'student_name': 'string',
    'student_id': 'string',
    'student_contact': 'string',
    'activity_length': 'float',
    'activity_name': 'string',
    'activity_type': 'string',
    'activity_host': 'string',
    'manager_name': 'string',
    'manager_contact': 'string',
    'manager_qq': 'string',
    'notes': 'string',
}
DATE_COLUMNS = [
    'activity_begin',
    'activity_end',
]
COLUMNS: list[str] = DATE_COLUMNS + list(NON_DATE_DTYPES.keys())
OPTIONAL_COLUMNS = [
    'student_contact',
    'manager_contact',
    'manager_qq',
    'notes',
]


def convert_date(x):
    return pd.to_datetime(x, format=DATE_FORMAT)


CONVERTERS = dict(
    (col, convert_date)
    for col in DATE_COLUMNS
)


def create_record_id() -> int:
    return time.time_ns()


def make_table_response(df: pd.DataFrame):
    for col in DATE_COLUMNS:
        df[col] = df[col].dt.strftime(DATE_FORMAT)
    df.reset_index(inplace=True)  # return index to a column
    df.fillna('', inplace=True)
    return jsonify(df.to_dict('records'))
