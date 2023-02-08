#!/usr/bin/env python3

if __name__ == '__main__':

    from apis import app, PORT
    app.run(
        port=PORT,
    )

    import sys
    from getopt import getopt
    option_list, extra_args = getopt(sys.argv[1:], 'o')
    options = dict(option_list)

    if '-o' in options:
        import webbrowser
        webbrowser.open(f'http://127.0.0.1:{PORT:d}/')
