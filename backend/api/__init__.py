from .table import table_blueprint
from .record import record_blueprint
from .backup import backup_blueprint
from .import_ import import_blueprint
from .export import export_blueprint
from .alias import alias_blueprint
from .common import Blueprint

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

api_blueprint.register_blueprint(table_blueprint)
api_blueprint.register_blueprint(record_blueprint)
api_blueprint.register_blueprint(backup_blueprint)
api_blueprint.register_blueprint(import_blueprint)
api_blueprint.register_blueprint(export_blueprint)
api_blueprint.register_blueprint(alias_blueprint)
