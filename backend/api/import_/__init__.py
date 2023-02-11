from ..common import *
from .common import *
from .convert_table import convert_table

import_blueprint = Blueprint('import', __name__, url_prefix='/import')


@import_blueprint.post('/preview')
def api_import_preview():

    try:
        dataframes = [
            convert_table(file)
            for file in request.files.getlist('files[]')
        ]
    except ImportTableError as error:
        return error.message, 400

    df_result = pd.concat(dataframes, ignore_index=True)

    # set indices
    index_count = len(df_result.index)
    init_index = create_record_id()
    new_index = pd.Index([
        (init_index + i)
        for i in range(index_count)
    ])
    df_result.set_index(new_index, inplace=True)
    df_result.index.name = INDEX_NAME

    # Keep only first occurrances to avoid duplicates.
    df_result.drop_duplicates(inplace=True)

    trimWhitespaces(df_result)

    return make_table_response(df_result)
