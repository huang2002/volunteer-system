#!/usr/bin/env python3

PORT = 2023

if __name__ == '__main__':

    from apis import app
    app.run(
        port=PORT,
    )

    import sys
    from getopt import getopt
    option_list, extra_args = getopt(sys.argv[1:], '', ['no-open'])
    options = dict(option_list)

    if not '--no-open' in options:
        import webbrowser
        webbrowser.open(f'http://127.0.0.1:{PORT:d}/')
