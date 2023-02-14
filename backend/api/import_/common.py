from werkzeug.datastructures import FileStorage
from ..common import *

__all__ = [
    'FileStorage',
    'WHITESPACE_PATTERN',
    'ImportTableError',
    'COLUMN_PATTERNS',
    'IGNORE_COLUMN_PATTERN',
]

WHITESPACE_PATTERN = re.compile(r'\s+')


class ImportTableError(Exception):

    def __init__(self, message=''):
        self.message = message
        super().__init__(message)


COLUMN_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ('student_school', re.compile(r'学院')),
    ('student_class', re.compile(r'班级')),
    ('student_name', re.compile(r'(?<!负责人)姓名')),
    ('student_id', re.compile(r'学号')),
    ('student_contact', re.compile(r'(?<!负责人)(?:联系方式|电话)')),
    ('activity_length', re.compile(r'志愿时')),
    ('activity_begin', re.compile(r'开始(?:日期|时间)')),
    ('activity_end', re.compile(r'(?:结束|截止)(?:日期|时间)')),
    ('activity_date', re.compile(r'服务日期')),
    ('activity_name', re.compile(r'(?:活动|项目)名称')),
    ('activity_type', re.compile(r'类别')),
    ('activity_host', re.compile(r'举办单位')),
    ('manager_name', re.compile(r'负责人姓名')),
    ('manager_contact', re.compile(r'负责人电话')),
    ('manager_qq', re.compile(r'负责人QQ')),
    ('notes', re.compile(r'备注')),
]

# whitespaces will be striped before test
IGNORE_COLUMN_PATTERN = re.compile(r'^(?:记录编号|编号|序号|Unnamed:\d+)$', re.I)
