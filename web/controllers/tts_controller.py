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


class VoicePreview(BaseController):
    def get(self, s_id, name):
        return TTSService().voice_preview(s_id, name)
        # response = {
        #     "Status": status,
        #     "Id": s_id,
        # }
        # return response, 200


class ListVoices(BaseController):
    def get(self):
        return TTSService().list_all_speakers()
