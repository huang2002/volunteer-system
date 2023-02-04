#!/usr/bin/env python3
import os
import sys
from flask import Flask, jsonify
from common import *

PORT = 2023

app = Flask(
    __name__,
    static_url_path='',
    static_folder=FRONTEND_PATH,
)


@app.get('/api/list')
def api_list():
    tables_names = [
        os.path.basename(table_path)
        for table_path in os.listdir(DATA_PATH)
        if tables_path.endswith('.csv')
    ]
    return jsonify(tables_names)


if __name__ == '__main__':

    app.run(
        port=PORT,
    )

    from getopt import getopt
    option_list, extra_args = getopt(sys.argv[1:], 'o')
    options = dict(option_list)

    if '-o' in options:
        import webbrowser
        webbrowser.open(f'http://127.0.0.1:{PORT:d}/')
