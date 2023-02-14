from ..common import *
from .common import *

CLASS_PATTERN = re.compile(r'\d+')


def transform_class(raw_value: Any) -> str:
    if isinstance(raw_value, int):
        return str(raw_value)
    else:
        raw_value = str(raw_value)
    search_result = CLASS_PATTERN.search(raw_value)
    if search_result == None:
        raise ImportTableError(
            f'无法确定班号的班级：{raw_value}'
        )
    return search_result.group(0)


def handle_student_class(
    df_result: pd.DataFrame,
    series_raw: pd.Series,
    **params,
) -> NoReturn:

    df_result['student_class'] = series_raw.map(transform_class)
