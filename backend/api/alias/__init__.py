from ..common import *
from .common import *

alias_blueprint = Blueprint('alias', __name__, url_prefix='/alias')


@alias_blueprint.get('/view/<column_name>')
def view(column_name: str) -> Any:
    alias_lists = [
        {'name': name, 'aliases': aliases}
        for name, aliases in get_alias_lists(column_name).items()
    ]
    return jsonify(
        sorted(
            alias_lists,
            key=lambda item: item['name'],
        )
    )


@alias_blueprint.post('/rename/<column_name>/<list_name>/<new_name>')
def rename(column_name: str, list_name: str, new_name: str) -> ResponseType:
    if not list_name in get_alias_lists(column_name):
        return RESPONSE_UNKNOWN_ALIAS_LIST
    rename_alias_list(column_name, list_name, new_name)
    return RESPONSE_SUCCESS


@alias_blueprint.post('/update/<column_name>/<list_name>')
def update(column_name: str, list_name: str) -> ResponseType:
    alias_list = request.get_json()
    if not (
        isinstance(alias_list, list)
        and all(isinstance(alias, str) for alias in alias_list)
    ):
        return RESPONSE_INVALID_DATA
    update_alias_list(column_name, list_name, alias_list)
    return RESPONSE_SUCCESS


@alias_blueprint.post('/delete/<column_name>')
def delete(column_name: str) -> ResponseType:
    list_names = request.get_json()
    if not (
        isinstance(list_names, list)
        and all(isinstance(alias_name, str) for alias_name in list_names)
    ):
        return RESPONSE_UNKNOWN_ALIAS_LIST
    for list_name in list_names:
        delete_alias_list(column_name, list_name)
    return RESPONSE_SUCCESS
