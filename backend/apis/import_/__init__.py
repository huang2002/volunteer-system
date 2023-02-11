from ..common import *
from .common import *
from .convert_table import convert_table


def inject_import_apis(app: Flask):

    @app.post('/api/import/preview')
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

        trimWhitespaces(df_result)

        return make_table_response(df_result)
