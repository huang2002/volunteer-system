from ..common import *
from .common import *


def inject_import_apis(app: Flask):

    @app.post('/api/import/preview')
    def import_preview():
        try:
            df_result = pd.concat([
                convert_table(file)
                for file in request.files.values()
            ])
        except ImportTableError as error:
            return error.message, 400
        return make_table_response(df)

    @app.post('/api/import/records')
    def import_records():

        # TODO:

        return RESPONSE_SUCCESS
