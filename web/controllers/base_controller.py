import http
import json

from flask import request, Response
from flask_restx import Resource


class BaseController(Resource):

    @staticmethod
    def get_headers():
        return request.headers

    @staticmethod
    def get_json_request():
        return request.json

    @staticmethod
    def set_response(response, status_code=http.HTTPStatus.OK):
        return Response(json.dumps(response), status=status_code, mimetype=u'application/json')

    @staticmethod
    def get_request_params():
        return request.args

    @staticmethod
    def get_request_input():
        return request.json
