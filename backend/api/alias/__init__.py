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


@alias_blueprint.post('/delete/<column_name>/<list_name>')
def delete(column_name: str, list_name: str) -> ResponseType:
    alias_list = request.get_json()
    if not (
        isinstance(alias_list, list)
        and all(isinstance(alias, str) for alias in alias_list)
    ):
        return RESPONSE_INVALID_DATA
    delete_alias_list(column_name, list_name)
    return RESPONSE_SUCCESS
