#!/usr/bin/env python3
from getopt import getopt
import sys
from apis import app

PORT = 2023

option_list, extra_args = getopt(sys.argv[1:], '', ['no-open'])
options = dict(option_list)

if not '--no-open' in options:
    import webbrowser
    webbrowser.open(f'http://127.0.0.1:{PORT:d}/index.html')

app.run(
    port=PORT,
)
