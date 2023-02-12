from ..common import *

__all__ = [
    'ExportError',
    'RESPONSE_INVALID_LEVEL',
    'KEY_BEGIN_DATE',
    'KEY_END_DATE',
    'GRADE_COLUMN_NAME',
    'EXPORT_DATE_FORMAT',
    'EXPORT_TIME_FORMAT',
    'EXPORT_LEVELS',
    'LEVEL_KEYS',
    'LEVEL_DISPLAY_NAMES',
    'get_export_path',
    'export_table',
]


class ExportError(Exception):
    def __init__(self, message=''):
        self.message = message
        super().__init__(message)


RESPONSE_INVALID_LEVEL = ('未知的报表级别', 400)

KEY_BEGIN_DATE = 'begin_date'
KEY_END_DATE = 'end_date'
GRADE_COLUMN_NAME = 'grade'
EXPORT_DATE_FORMAT = '%Y.%m.%d'
EXPORT_TIME_FORMAT = '%Y.%m.%d-%H.%M.%S'
EXCEL_FREEZE_PANES = (1, 2)

EXPORT_LEVELS = [
    'school',
    'grade',
    'class',
]

LEVEL_KEYS = {
    'school': 'student_school',
    'grade': GRADE_COLUMN_NAME,
    'class': 'student_class',
}

LEVEL_DISPLAY_NAMES = {
    'school': '按学院导出',
    'grade': '按年级导出',
    'class': '按班级导出',
}

TABLE_EXPORTERS = {
    'xlsx': lambda df, path, **params: df.to_excel(path, **params),
    'csv': lambda df, path, **params: df.to_csv(path, **params),
    'tsv': lambda df, path, **params: df.to_csv(path, sep='\t', **params),
}

FORMAT_DEFAULT_ENCODINGS = {
    'xlsx': 'gb2312',
    'csv': 'utf8',
    'tsv': 'utf8',
}

FORMAT_EXTENSIONS = {
    'xlsx': '.xlsx',
    'csv': '.csv',
    'tsv': '.tsv',
}

EXPORT_INDEX_NAME = '记录编号'
EXPORT_COLUMNS, EXPORT_HEADER = zip(
    ('student_id', '学号'),
    ('student_school', '学院'),
    ('student_class', '班级'),
    ('student_name', '姓名'),
    ('student_contact', '联系方式'),
    ('activity_begin', '开始日期'),
    ('activity_end', '结束日期'),
    ('activity_length', '志愿时长'),
    ('activity_name', '活动名称'),
    ('activity_type', '活动类型'),
    ('activity_host', '举办单位'),
    ('manager_name', '负责人姓名'),
    ('manager_contact', '负责人联系方式'),
    ('manager_qq', '负责人QQ'),
    ('notes', '备注'),
)


def get_export_path(path: str) -> str:
    return os.path.join(EXPORT_DIR, path)


def export_table(
    df_data: pd.DataFrame,
    path: str,
    *,
    output_format: str = 'csv',
    encoding: Optional[str] = None,
) -> NoReturn:

    if not output_format in TABLE_EXPORTERS:
        raise ExportError(
            f'未定义的输出格式：{output_format}'
        )

    # Convert all data to strings to keep persistence.
    df_output = pd.DataFrame()
    for col in df_data.columns:
        if col in DATE_COLUMNS:
            df_output[col] = df_data[col].dt.strftime(DATE_FORMAT)
        else:
            dtype = NON_DATE_DTYPES[col]
            if dtype == 'string':
                df_output[col] = df_data[col]
            else:
                df_output[col] = df_data[col].astype('string')
    df_output.index = df_output.index.astype('string')

    if encoding == None:
        encoding = FORMAT_DEFAULT_ENCODINGS[output_format]

    params = {
        'encoding': encoding,
        'index_label': EXPORT_INDEX_NAME,
        'columns': EXPORT_COLUMNS,
        'header': EXPORT_HEADER,
    }
    if output_format == 'xlsx':
        params['freeze_panes'] = EXCEL_FREEZE_PANES
        del params['encoding']

    ext = FORMAT_EXTENSIONS[output_format]
    TABLE_EXPORTERS[output_format](
        df_output,
        path + '_' + encoding + ext,
        **params,
    )
