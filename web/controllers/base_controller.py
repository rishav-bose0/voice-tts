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
    def get_request_input(id=None):

        # request_input = {}
        #
        # request_json = request.get_json()
        # if request_json:
        #     request_input.update(request_json)
        #
        # request_values = request.values
        # if request_values:
        #     request_input.update(request_values)
        #
        # request_files = request.files
        # if request_files:
        #     request_input.update(request_files)
        #
        # if id:
        #     request_input.update(id=id)

        return request.json
