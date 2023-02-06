from flask import Flask, request, jsonify
from common import *


def inject_table_apis(app: Flask):

    @app.get('/api/list/tables')
    def list_tables():
        return jsonify([
            os.path.splitext(table_path)[0]
            for table_path in os.listdir(DATA_PATH)
            if table_path.endswith('.csv')
        ])

    @app.get('/api/create/table/<table_name>')
    def create_table(table_name: str):

        if not is_valid_table_name(table_name):
            return RESPONSE_INVALID_TABLE_NAME

        table_path = get_table_path(table_name)
        if os.path.exists(table_path):
            return RESPONSE_DUPLICATE_TABLE_NAME

        init_table(table_path)
        return RESPONSE_SUCCESS

    @app.get('/api/view/table/<table_name>')
    def view_table(table_name: str):

        if not is_valid_table_name(table_name):
            return RESPONSE_INVALID_TABLE_NAME

        table_path = get_table_path(table_name)
        if not os.path.exists(table_path):
            return RESPONSE_TABLE_NOT_FOUND

        df = read_table(table_path)
        for col in DATE_COLUMNS:
            df[col] = df[col].dt.strftime(DATE_FORMAT)
        df.fillna('', inplace=True)
        df.reset_index(inplace=True)
        return jsonify(df.to_dict('records'))

    @app.post('/api/append/<table_name>')
    def append_record(table_name: str):

        if not is_valid_table_name(table_name):
            return RESPONSE_INVALID_TABLE_NAME

        table_path = get_table_path(table_name)
        if not os.path.exists(table_path):
            return RESPONSE_TABLE_NOT_FOUND

        record = request.get_json()
        if not isinstance(record, dict):
            return RESPONSE_INVALID_RECORD
        if any(not key in record for key in COLUMNS):
            return RESPONSE_INVALID_RECORD

        df_source = read_table(table_path)

        record_id = int(time.time())
        if record_id in df_source.index:
            return RESPONSE_TOO_FREQUENT

        record_index = pd.Index([record_id])
        df_addition = pd.DataFrame(
            columns=COLUMNS,
            index=record_index,
            data=[record[key] for key in COLUMNS],
            dtype=DTYPES,
        )
        df_result = df_source.append(df_addition)
        save_table(df_result, table_path)
        return RESPONSE_SUCCESS

    @app.get('/api/delete/<table_name>/<int:record_id>')
    def delete_record(table_name: str, record_id: int):

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

    @app.post('/api/update/<table_name>/<int:record_id>')
    def update_record(table_name: str, record_id: int):

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
            return RESPONSE_INVALID_RECORD
        for key, value in addition.items():
            if not key in COLUMNS:
                return RESPONSE_INVALID_RECORD
            raw_value = addition[key]
            dtype = DATE_DTYPE if key in DATE_COLUMNS else DTYPES[key]
            if dtype == 'string':
                value = str(raw_value)
            elif dtype.startswith('float'):
                try:
                    value = float(raw_value)
                except:
                    return RESPONSE_INVALID_RECORD
            elif dtype == DATE_DTYPE:
                try:
                    value = pd.to_datetime(raw_value, format=DATE_FORMAT)
                except:
                    return RESPONSE_INVALID_RECORD
            else:
                raise Exception(f'failed to set value of type: {dtype}')
            df.loc[record_id, key] = value

        save_table(df, table_path)
        return RESPONSE_SUCCESS
