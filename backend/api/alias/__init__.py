from ..common import *
from .common import *

alias_blueprint = Blueprint('alias', __name__, url_prefix='/alias')


@alias_blueprint.get('/view/<map_name>')
def api_alias_view(map_name: str) -> Any:
    return jsonify(get_alias_map(map_name))


@alias_blueprint.post('/update/<map_name>/<list_name>')
def api_alias_update(map_name: str, list_name: str) -> ResponseType:
    alias_list = request.get_json()
    if not (
        isinstance(alias_list, list)
        and all(isinstance(alias, str) for alias in alias_list)
    ):
        return RESPONSE_INVALID_DATA
    update_alias_list(map_name, list_name, alias_list)
    return RESPONSE_SUCCESS


@alias_blueprint.get('/delete/<map_name>/<list_name>')
def api_alias_delete(map_name: str, list_name: str) -> ResponseType:
    alias_list = request.get_json()
    if not (
        isinstance(alias_list, list)
        and all(isinstance(alias, str) for alias in alias_list)
    ):
        return RESPONSE_INVALID_DATA
    delete_alias_list(map_name, list_name)
    return RESPONSE_SUCCESS
