from flask_restx import Api

from web.controllers.ping_controller import Ping
from web.controllers.tts_controller import ProcessTTS, AddUser

default_routes = {
    '/ping': Ping,
}

api_routes = {
    '/process_tts': ProcessTTS,
    '/add_user': AddUser
}


def add_default_routes(api: Api) -> Api:
    for url, controller in default_routes.items():
        api.add_resource(controller, url)
    return api


def add_ocr_api_routes(api: Api) -> Api:
    for url, controller in api_routes.items():
        api.add_resource(controller, url)
    return api
