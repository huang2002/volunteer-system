from werkzeug.datastructures import FileStorage
from typing import Any
from ..common import *


class ImportTableError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(message)


# all extensions will be in lower case
ACCEPTABLE_EXCEL_EXTENSIONS = ['.xlsx']
ACCEPTABLE_CSV_EXTENSIONS = ['.csv', '.csv.gz']
ACCEPTABLE_TSV_EXTENSIONS = ['.tsv', '.tsv.gz']


def load_dataframe(
    file: FileStorage,
    *,
    skiprows=0,
    nrows=None,
) -> pd.DataFrame:
    filename = str(file.filename)
    filename_lower = filename.lower()
    if filename_lower.endswith(ACCEPTABLE_EXCEL_EXTENSIONS):
        df = pd.read_excel(
            file.stream,
            skiprows=skiprows,
            nrows=nrows,
        )
    elif filename_lower.endswith(ACCEPTABLE_CSV_EXTENSIONS):
        df = pd.read_csv(
            file.stream,
            skiprows=skiprows,
            nrows=nrows,
        )
    elif filename_lower.endswith(ACCEPTABLE_TSV_EXTENSIONS):
        df = pd.read_csv(
            file.stream,
            sep='\t',
            skiprows=skiprows,
            nrows=nrows,
        )
    else:
        raise ImportTableError(f'无法识别的表格：{filename}')


# whitespace characters will be ignored automatically
COLUMN_MAP: dict[str, str] = {
    **dict((col, col) for col in COLUMNS),
    '学院（全称）': 'student_school',
    '班级': 'student_class',
    '姓名': 'student_name',
    '学号': 'student_id',
    '联系方式': 'student_contact',
    '志愿时长（小时）': 'activity_length',
    '服务日期': 'activity_date',
    '服务日期（xxxx/xx/xx）': 'activity_date',
    '志愿项目名称（全称）': 'activity_name',
    '志愿项目类别': 'activity_type',
    '举办单位': 'activity_host',
    '项目负责人姓名': 'manager_name',
    '项目负责人电话': 'manager_contact',
    '项目负责人QQ号': 'manager_qq',
    '备注': 'notes',
}

# A row is recognized as a header row
# if it contains at least `RECOGNIZE_THRESHOLD`
# words listed in `RECOGNIZABLE_COLUMNS`.
RECOGNIZE_THRESHOLD = 5
RECOGNIZABLE_COLUMNS = COLUMN_MAP.keys()
RECOGNIZE_NROWS = 5
MAX_SKIPROWS = 3


def detect_skiprows(file: FileStorage) -> int:
    for n in range(MAX_SKIPROWS + 1):
        df = load_dataframe(
            file,
            nrows=nrows,
            skiprows=n,
        )
        recognized_count = 0
        for word in RECOGNIZABLE_COLUMNS:
            if word in df.columns:
                recognized_count += 1
        if recognized_count >= RECOGNIZE_THRESHOLD:
            return n
    return MAX_SKIPROWS


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
            if col in DATE_COLUMNS:
                # Don't use `convert_date` here
                # because the date format needs to be inferred.
                df_result[col] = pd.to_datetime(df_raw[col_raw])
            else:
                dtype = NON_DATE_DTYPES[col]
                df_result[col] = df_raw[col_raw].astype(dtype)
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

    # set indices
    index_count = len(df_result.index)
    init_index = create_record_id()
    new_index = pd.Index(
        [init_index + i for i in range(index_count)],
        name=INDEX_NAME,
    )
    df_result.index = new_index

    return df_result
