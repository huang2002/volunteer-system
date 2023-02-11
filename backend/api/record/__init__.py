from ..common import *
from ..table.common import *
from .common import *

record_blueprint = Blueprint('record', __name__)


@record_blueprint.get('/delete/<table_name>/<int:record_id>')
def api_record_delete(table_name: str, record_id: int):

    if not is_valid_table_name(table_name):
        return RESPONSE_INVALID_TABLE_NAME

    table_path = get_table_path(table_name)
    if not os.path.exists(table_path):
        return RESPONSE_TABLE_NOT_FOUND

    df = read_table(table_path)
    if not record_id in df.index:
        return RESPONSE_RECORD_NOT_FOUND

    df = df.drop(index=record_id)
    save_table(df, table_path)
    return RESPONSE_SUCCESS


@record_blueprint.post('/update/<table_name>/<int:record_id>')
def api_record_update(table_name: str, record_id: int):

    if not is_valid_table_name(table_name):
        return RESPONSE_INVALID_TABLE_NAME

    table_path = get_table_path(table_name)
    if not os.path.exists(table_path):
        return RESPONSE_TABLE_NOT_FOUND

    df = read_table(table_path)
    if not record_id in df.index:
        return RESPONSE_RECORD_NOT_FOUND

    addition = request.get_json()
    if not isinstance(addition, dict):
        return RESPONSE_INVALID_DATA
    for key, value in addition.items():
        if not key in COLUMNS:
            return RESPONSE_INVALID_DATA
        raw_value = addition[key]
        dtype = DATE_DTYPE if key in DATE_COLUMNS else NON_DATE_DTYPES[key]
        if dtype == 'string':
            value = str(raw_value)
        elif dtype.startswith('float'):
            try:
                value = float(raw_value)
            except:
                return RESPONSE_INVALID_DATA
        elif dtype == DATE_DTYPE:
            try:
                value = pd.to_datetime(raw_value, format=DATE_FORMAT)
            except:
                return RESPONSE_INVALID_DATA
        else:
            raise Exception(f'failed to set value of type: {dtype}')
        df.loc[record_id, key] = value

    save_table(df, table_path)
    return RESPONSE_SUCCESS
