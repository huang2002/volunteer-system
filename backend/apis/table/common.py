from ..common import *

__all__ = [
    'RESPONSE_INVALID_TABLE_NAME',
    'RESPONSE_DUPLICATE_TABLE',
    'RESPONSE_TABLE_NOT_FOUND',
    'RESPONSE_INVALID_DATA',
    'RESPONSE_RECORD_NOT_FOUND',
    'is_valid_table_name',
    'get_table_path',
    'init_table',
    'read_table',
    'save_table',
    'append_table',
]

RESPONSE_INVALID_TABLE_NAME = ('表名不符合要求', 403)
RESPONSE_DUPLICATE_TABLE = ('指定的表已经存在', 403)
RESPONSE_TABLE_NOT_FOUND = ('指定的表不存在', 404)
RESPONSE_INVALID_DATA = ('数据不符合要求', 400)
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
        # Currently, no NAs should exist in saved data.
        # So, pass `na_filter=False` to avoid empty strings
        # being recognized as NAs.
        na_filter=False,
    )
    for col in DATE_COLUMNS:
        df[col] = df[col].astype(DATE_DTYPE)
    return df


def save_table(df: pd.DataFrame, path: str) -> NoReturn:
    df.to_csv(
        path,
        date_format=DATE_FORMAT,
    )


def append_table(
    table_path: str,
    df_addition: pd.DataFrame,
) -> NoReturn:

    init_id = create_record_id()
    n = len(df_addition.index)
    index = pd.Index(
        [(init_id + i) for i in range(n)],
        name=INDEX_NAME,
    )
    df_addition.index = index

    for col in COLUMNS:
        if col in DATE_COLUMNS:
            if df_addition[col].dtype != DATE_DTYPE:
                df_addition[col] = convert_date(df_addition[col])
        else:
            dtype = NON_DATE_DTYPES[col]
            if df_addition[col].dtype != dtype:
                df_addition[col] = df_addition[col].astype(dtype)

    df_source = read_table(table_path)
    df_result = pd.concat(
        [df_source, df_addition],
        # Indices must be unique,
        # so this verification is a must.
        verify_integrity=True,
    )

    # Keep only first occurrances to avoid duplicates.
    df_result.drop_duplicates(inplace=True)

    save_table(df_result, table_path)
