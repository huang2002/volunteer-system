import os
from flask import Flask
from api import api_blueprint

PORT = 2023
FRONTEND_PATH = os.path.join(
    os.path.dirname(__file__),
    '../frontend',
)

app = Flask(
    __name__,
    static_url_path='',
    static_folder=FRONTEND_PATH,
)

app.config['MAX_CONTENT_LENGTH'] = 233 * 1024 * 1024  # bytes

app.register_blueprint(api_blueprint)


@app.get('/')
def home_page():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(
        port=PORT,
    )
