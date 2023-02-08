from ..common import *

__all__ = [
    'RESPONSE_INVALID_TABLE_NAME',
    'RESPONSE_DUPLICATE_TABLE',
    'RESPONSE_TABLE_NOT_FOUND',
    'RESPONSE_INVALID_RECORD',
    'RESPONSE_RECORD_NOT_FOUND',
    'is_valid_table_name',
    'get_table_path',
    'init_table',
    'read_table',
    'save_table',
]

RESPONSE_INVALID_TABLE_NAME = ('表名不符合要求', 403)
RESPONSE_DUPLICATE_TABLE = ('指定的表已经存在', 403)
RESPONSE_TABLE_NOT_FOUND = ('指定的表不存在', 404)
RESPONSE_INVALID_RECORD = ('记录不符合要求', 400)
RESPONSE_RECORD_NOT_FOUND = ('指定的记录不存在', 404)

PATTERN_TABLE_NAME = re.compile(r'^\d{2}$')


def is_valid_table_name(table_name: str) -> bool:
    return PATTERN_TABLE_NAME.match(table_name) != None


def get_table_path(table_name: str) -> str:
    assert is_valid_table_name(table_name)
    return os.path.join(DATA_DIR, f'{table_name}.csv')


def init_table(path: str) -> NoReturn:
    df = pd.DataFrame(columns=[INDEX_NAME, *COLUMNS])
    df.to_csv(path, index=False)


def read_table(path: str) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        index_col=INDEX_NAME,
        infer_datetime_format=True,
        dtype=NON_DATE_DTYPES,
        converters=CONVERTERS,
        parse_dates=DATE_COLUMNS,
    )
    for col in DATE_COLUMNS:
        df[col] = df[col].astype(DATE_DTYPE)
    return df


def save_table(df: pd.DataFrame, path: str) -> NoReturn:
    df.to_csv(
        path,
        date_format=DATE_FORMAT,
    )
