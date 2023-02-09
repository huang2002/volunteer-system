from ..common import *
from .common import *
from .detect_skiprows import detect_skiprows
from .load_dataframe import load_dataframe
from .handle_activity_date import handle_activity_date

SPECIAL_COLUMNS = {
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
    for col_raw in df_raw.columns:
        if col_raw in IGNORED_COLUMNS:
            continue
        if not col_raw in COLUMN_MAP:
            raise ImportTableError(
                f'无法识别的列：{col_raw}，文件：{filename}'
            )
        col = COLUMN_MAP[col_raw]
        if col in df_result.columns:
            raise ImportTableError(
                f'多余的列：{col_raw}，文件：{filename}'
            )
        try:
            if col in SPECIAL_COLUMNS:
                SPECIAL_COLUMNS[col](df_result, df_raw[col_raw])
            elif col in DATE_COLUMNS:
                # Don't use `convert_date` here
                # since the date format needs to be inferred.
                df_result[col] = pd.to_datetime(df_raw[col_raw])
            else:
                dtype = NON_DATE_DTYPES[col]
                df_result[col] = df_raw[col_raw].astype(dtype)
        except ImportTableError as error:
            raise ImportTableError(
                f'{error.message}，文件：{filename}'
            )
        except:
            raise ImportTableError(
                f'未能转换的列：{col_raw}，文件：{filename}'
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
