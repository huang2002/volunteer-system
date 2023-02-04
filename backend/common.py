from os import path

BACKEND_PATH = path.dirname(__file__)
FRONTEND_PATH = path.join(BACKEND_PATH, '../dist')
DATA_PATH = path.join(BACKEND_PATH, '../data')

COLUMNS = [
    'record_id',  # 编号
    'student_school',  # 学院（全称）
    'student_class',  # 班级
    'student_name',  # 姓名
    'student_id',  # 学号
    'activity_length',  # 志愿时长（小时）
    'activity_date',  # 服务日期
    'activity_name',  # 志愿项目名称（全称）
    'activity_type',  # 志愿项目类别
    'activity_host',  # 举办单位
    'manager_name',  # 项目负责人姓名
    'manager_qq',  # 项目负责人QQ号
    'notes',  # 备注
]
