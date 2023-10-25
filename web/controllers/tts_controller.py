from service import TTSService
from web.controllers.base_controller import BaseController
from web.routing.auth import authenticate


class ProcessTTS(BaseController):
    method_decorators = [authenticate]

    def post(self):
        request = BaseController.get_request_input()
        headers = BaseController.get_headers()
        status, s3_link, err = TTSService().process_tts(request, headers)
        response = {}
        if err != "":
            response["error"] = err
        else:
            response["s3_link"] = s3_link
        response["status"] = status

        return response, 200


class SignUpUser(BaseController):
    def post(self):
        request = BaseController.get_request_input()
        headers = BaseController.get_headers()
        user_id, token, err = TTSService().signup_user(request, headers)
        if err is not None:
            return {
                "Error": err
            }, 500

        return {
            "Id": user_id,
            "Token": token
        }, 200


class LoginUser(BaseController):
    def post(self):
        request = BaseController.get_request_input()
        headers = BaseController.get_headers()
        user_id, token, err = TTSService().login_user(request, headers)
        response = {}
        status_code = 200
        if err is not None:
            response["Error"] = err
            status_code = 500
        else:
            if user_id == "":
                status_code = 400
            else:
                response["Id"] = user_id
                response["Token"] = token

        return response, status_code


class GetUserDetails(BaseController):
    method_decorators = [authenticate]

    def get(self, user_id):
        user_details = TTSService().get_user_details(user_id=user_id)
        return {
            "id": user_details.get_id().value(),
            "first_name": user_details.get_first_name(),
            "last_name": user_details.get_last_name(),
            "email": user_details.get_email(),
            "password": user_details.get_password(),
        }, 200


class VoicePreview(BaseController):
    method_decorators = [authenticate]

    def get(self, speaker_id, name):
        return TTSService().voice_preview(speaker_id, name)


class ListVoices(BaseController):
    method_decorators = [authenticate]

    def get(self):
        return TTSService().list_all_speakers()


class ListSampleVoices(BaseController):
    def get(self):
        return TTSService().list_sample_speakers()
