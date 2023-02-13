#!/usr/bin/env python3
import multiprocessing as mp
from app import app, PORT


def run_app(queue: mp.Queue) -> None:

    @app.get('/api/close')
    def api_close():
        queue.put(1011)
        return 'never'

    app.run(
        port=PORT,
    )


if __name__ == '__main__':

    import sys
    from getopt import getopt

    option_list, extra_args = getopt(sys.argv[1:], '', ['no-open'])
    options = dict(option_list)

    queue = mp.Queue()
    process = mp.Process(target=run_app, args=(queue,))
    process.start()

    if not '--no-open' in options:
        import webbrowser
        webbrowser.open_new(f'http://127.0.0.1:{PORT:d}/')

    # Wait until `/api/close` is visited...
    queue.get()

    process.terminate()
    exit(0)
