from ..common import *
from .common import *
from .construct_tree import construct_tree

table_blueprint = Blueprint('table', __name__, url_prefix='/table')


@table_blueprint.get('/list')
def api_table_list():
    return jsonify(
        sorted(get_table_names())
    )


@table_blueprint.get('/create/<table_name>')
def api_table_create(table_name: str):

    if not is_valid_table_name(table_name):
        return RESPONSE_INVALID_TABLE_NAME

    table_path = get_table_path(table_name)
    if os.path.exists(table_path):
        return RESPONSE_DUPLICATE_TABLE

    init_table(table_path)
    return RESPONSE_SUCCESS


@table_blueprint.get('/rename/<source>/<destination>')
def api_table_rename(source: str, destination: str):

    if not (
        is_valid_table_name(source)
        and is_valid_table_name(destination)
    ):
        return RESPONSE_INVALID_TABLE_NAME

    source_path = get_table_path(source)
    if not os.path.exists(source_path):
        return RESPONSE_TABLE_NOT_FOUND

    destination_path = get_table_path(destination)
    if os.path.exists(destination_path):
        return RESPONSE_DUPLICATE_TABLE

    os.rename(source_path, destination_path)
    return RESPONSE_SUCCESS


@table_blueprint.get('/view/<table_name>')
def api_table_view(table_name: str):

    if not is_valid_table_name(table_name):
        return RESPONSE_INVALID_TABLE_NAME

    table_path = get_table_path(table_name)
    if not os.path.exists(table_path):
        return RESPONSE_TABLE_NOT_FOUND

    df = read_table(table_path)
    return make_table_response(df)


@table_blueprint.post('/append/<table_name>')
def api_table_append(table_name: str):

    if not is_valid_table_name(table_name):
        return RESPONSE_INVALID_TABLE_NAME

    table_path = get_table_path(table_name)
    if not os.path.exists(table_path):
        return RESPONSE_TABLE_NOT_FOUND

    records = request.get_json()
    if not (
        isinstance(records, list)
        and all(
            all((key in record) for key in COLUMNS)
            for record in records
        )
    ):
        return RESPONSE_INVALID_DATA

    n = len(records)
    if n == 0:
        return RESPONSE_SUCCESS

    if INDEX_NAME in records[0]:
        indices = [record[INDEX_NAME] for record in records]
    else:
        init_id = create_record_id()
        indices = [(init_id + i) for i in range(n)]
    index = pd.Index(indices, name=INDEX_NAME)

    data = [
        [record[key] for key in COLUMNS]
        for record in records
    ]
    df_addition = pd.DataFrame(
        data=data,
        columns=COLUMNS,
        index=index,
    )
    append_table(table_path, df_addition)

    return RESPONSE_SUCCESS


@table_blueprint.get('/delete/<table_name>')
def api_table_delete(table_name: str):

    if not is_valid_table_name(table_name):
        return RESPONSE_INVALID_TABLE_NAME

    table_path = get_table_path(table_name)
    if not os.path.exists(table_path):
        return RESPONSE_TABLE_NOT_FOUND

    os.remove(table_path)
    return RESPONSE_SUCCESS


@table_blueprint.get('/tree')
def api_table_tree():
    return jsonify(construct_tree())
