import base64
import json

from flask import Flask, request, Response

from instance.settings import app_config
from shared.response_object import ResponseFailure, ResponseSuccess
from use_cases.generate_secure_link_use_cases import GenerateSecureLinkUseCase
from use_cases.request_objects import GenerateSecureLinkRequestObject

STATUS_CODES = {
    ResponseSuccess.SUCCESS: 200,
    ResponseFailure.RESOURCE_ERROR: 404,
    ResponseFailure.PARAMETERS_ERROR: 400,
    ResponseFailure.SYSTEM_ERROR: 500
}


def _create_request_object_from_request_args(request_args: dict):
    expires = request_args.get('t')
    if expires:
        try:
            expires = int(expires)
        except ValueError:
            pass
    url = request_args.get('u')
    if url:
        url = base64.b64decode(url).decode('utf-8')
    params = {
        'expires': expires,
        'url': url,
        'ip_address': request_args.get('ip'),
        'password': request_args.get('p')
    }
    return GenerateSecureLinkRequestObject(**params)


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('settings.py')

    @app.route('/')
    def index():
        request_object = _create_request_object_from_request_args(request.args)
        use_case = GenerateSecureLinkUseCase()
        response = use_case.execute(request_object)
        return Response(json.dumps(response.value).strip('"'), status=STATUS_CODES[response.type])

    return app
