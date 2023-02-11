from .table import table_blueprint
from .backup import backup_blueprint
from .import_ import import_blueprint
from .common import Blueprint

api_blueprint = Blueprint('api', __name__)

api_blueprint.register_blueprint(table_blueprint)
api_blueprint.register_blueprint(backup_blueprint)
api_blueprint.register_blueprint(import_blueprint)
