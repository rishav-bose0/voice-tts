from service import TTSService
from web.controllers.base_controller import BaseController


class ProcessTTS(BaseController):
    def post(self):
        request = BaseController.get_request_input()
        headers = BaseController.get_headers()
        status = TTSService().process_tts(request, headers)
        response = {
            "Status": status,
        }
        return response, 200


class AddUser(BaseController):
    def post(self):
        request = BaseController.get_request_input()
        headers = BaseController.get_headers()
        response = TTSService().add_user(request, headers)
        return response, 200
