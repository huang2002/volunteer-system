#!/usr/bin/env python3
import sys
from flask import Flask
from table_apis import inject_table_apis
from backup_apis import inject_backup_apis
from common import *

PORT = 2023

app = Flask(
    __name__,
    static_url_path='',
    static_folder=FRONTEND_PATH,
)

inject_table_apis(app)
inject_backup_apis(app)

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
