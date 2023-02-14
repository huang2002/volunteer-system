from ..common import *
from .common import *
from .detect_skiprows import detect_skiprows
from .load_dataframe import load_dataframe
from .handle_activity_date import handle_activity_date

SpecialColumnHandler = Callable[[pd.DataFrame, pd.Series], NoReturn]
SPECIAL_COLUMNS: Dict[str, SpecialColumnHandler] = {
    'activity_date': handle_activity_date,
}


def convert_table(file: FileStorage) -> pd.DataFrame:

    filename = str(file.filename)

    # load the file
    try:
        skiprows = detect_skiprows(file)
        df_raw = load_dataframe(file, skiprows=skiprows)
    except ImportTableError as error:
        raise error
    except:
        raise ImportTableError(f'导入失败：{filename}')

    # copy data
    df_result = pd.DataFrame()
    for col_src in df_raw.columns:
        col_raw = WHITESPACE_PATTERN.sub('', col_src)
        if IGNORE_COLUMN_PATTERN.match(col_raw):
            continue
        col = None
        for pattern_col, pattern in COLUMN_PATTERNS:
            if pattern.search(col_raw):
                col = pattern_col
                break
        if col == None:
            raise ImportTableError(
                f'无法识别的列：{col_src}，文件：{filename}'
            )
        if col in df_result.columns:
            raise ImportTableError(
                f'多余的列：{col_src}，文件：{filename}'
            )
        try:
            if col in SPECIAL_COLUMNS:
                SPECIAL_COLUMNS[col](
                    df_result,
                    df_raw[col_src],
                    filename=filename,
                )
            elif col in DATE_COLUMNS:
                if df_raw[col_src].dtype == DATE_DTYPE:
                    df_result[col] = df_raw[col_src]
                else:
                    # Don't use `convert_date` here
                    # since the date format needs to be inferred.
                    df_result[col] = pd.to_datetime(df_raw[col_src])
            else:
                dtype = NON_DATE_DTYPES[col]
                if df_raw[col_src].dtype == dtype:
                    df_result[col] = df_raw[col_src]
                else:
                    df_result[col] = df_raw[col_src].astype(dtype)
        except ImportTableError as error:
            raise ImportTableError(
                f'{error.message}，文件：{filename}'
            )
        except:
            raise ImportTableError(
                f'未能转换的列：{col_src}，文件：{filename}'
            )

    # check missing columns
    for col in COLUMNS:
        if col in df_result.columns:
            continue
        if col in OPTIONAL_COLUMNS:
            if col in DATE_COLUMNS:
                df_result[col] = pd.NaT
            elif NON_DATE_DTYPES[col] == 'string':
                df_result[col] = ''
            else:
                df_result[col] = pd.NA
        else:
            raise ImportTableError(
                f'缺少必须的列：{col}，文件：{filename}'
            )

    return df_result
