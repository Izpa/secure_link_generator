from flask import Flask, request

from instance.settings import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('settings.py')

    @app.route('/')
    def index():
        t = request.args.get('t')
        u = request.args.get('u')
        ip = request.args.get('ip')
        p = request.args.get('p')
        return str(t)

    return app
