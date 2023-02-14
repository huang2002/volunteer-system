from werkzeug.datastructures import FileStorage
from ..common import *

__all__ = [
    'FileStorage',
    'WHITESPACE_PATTERN',
    'ImportTableError',
    'COLUMN_MAP',
    'IGNORED_COLUMN_PATTERN',
]

WHITESPACE_PATTERN = re.compile(r'\s+')


class ImportTableError(Exception):

    def __init__(self, message=''):
        self.message = message
        super().__init__(message)


# whitespace characters will be ignored automatically
COLUMN_MAP: Dict[str, str] = {
    **dict((col, col) for col in COLUMNS),
    '学院': 'student_school',
    '学院（全称）': 'student_school',
    '班级': 'student_class',
    '姓名': 'student_name',
    '学号': 'student_id',
    '联系方式': 'student_contact',
    '联系方式（电话）': 'student_contact',
    '联系电话': 'student_contact',
    '电话': 'student_contact',
    '志愿时': 'activity_length',
    '志愿时长': 'activity_length',
    '志愿时长（小时）': 'activity_length',
    '服务开始日期': 'activity_begin',
    '开始日期': 'activity_begin',
    '服务结束日期': 'activity_end',
    '结束日期': 'activity_end',
    '服务截止日期': 'activity_end',
    '截止日期': 'activity_end',
    '服务日期': 'activity_date',
    '服务日期（xxxx/xx/xx）': 'activity_date',
    '活动名称': 'activity_name',
    '志愿项目名称': 'activity_name',
    '志愿项目名称（全称）': 'activity_name',
    '活动类别': 'activity_type',
    '志愿类别': 'activity_type',
    '志愿活动类别': 'activity_type',
    '志愿项目类别': 'activity_type',
    '志愿服务类别': 'activity_type',
    '举办单位': 'activity_host',
    '负责人姓名': 'manager_name',
    '项目负责人姓名': 'manager_name',
    '负责人电话': 'manager_contact',
    '项目负责人电话': 'manager_contact',
    '负责人QQ号': 'manager_qq',
    '项目负责人QQ号': 'manager_qq',
    '备注': 'notes',
}

# whitespaces will be striped before test
IGNORED_COLUMN_PATTERN = re.compile(r'^(?:记录编号|编号|序号|Unnamed:\d+)$', re.I)
