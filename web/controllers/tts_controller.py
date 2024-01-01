import csv
import os

from flask import request
from werkzeug.utils import secure_filename

import helper_utils
from service import TTSService
from web.controllers.base_controller import BaseController
from web.routing.auth import authenticate


class ProcessTTS(BaseController):
    method_decorators = [authenticate]

    def post(self):
        request = BaseController.get_request_input()
        headers = BaseController.get_headers()
        status, speech_s3_link, err = TTSService().process_tts(request, headers)
        response = {}
        if err is not None:
            response["error"] = err
        else:
            response["speech_s3_link"] = speech_s3_link
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
        if err is not None and err != "Invalid email or password":
            response["Error"] = err
            status_code = 500
        else:
            if user_id == "":
                status_code = 401
                response["Error"] = err
            else:
                response["Id"] = user_id
                response["Token"] = token

        return response, status_code


class CreateSpeakers(BaseController):
    def post(self):
        data_dict = {}

        # Open the CSV file for reading
        with open('../final_speaker.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)  # Use DictReader for easy column access

            # Iterate through the rows in the CSV file
            for row in csv_reader:
                # Extract data from each row
                id_value = row['id']
                name = row['name']
                gender = row['gender']
                image_link = row['image_link']
                voice_preview_link = row['voice_preview_link']
                model_name = row['model_name']
                clone_details = row['clone_details']
                speaker_type = row['speaker_type']
                # Add the data to the dictionary with Id as the key
                data_dict[id_value] = {
                    'id': id_value,
                    'name': name,
                    'gender': gender,
                    'image_link': image_link,
                    'voice_preview_link': voice_preview_link,
                    'model_name': model_name,
                    'clone_details': clone_details,
                    'speaker_type': speaker_type
                }
            return TTSService().create_speakers(list(data_dict.values()))


class GetUserDetails(BaseController):
    method_decorators = [authenticate]

    def get(self, user_id):
        user_details = TTSService().get_user_details(user_id=user_id)
        if user_details is None:
            return {}, 200

        return {
            "id": user_details.get_id().value(),
            "first_name": user_details.get_first_name(),
            "last_name": user_details.get_last_name(),
            "email": user_details.get_email(),
            "password": user_details.get_password(),
        }, 200


class VoicePreview(BaseController):

    def get(self, speaker_id, name):
        preview_link = TTSService().voice_preview(speaker_id, name)
        if preview_link is None:
            return {"Status": False}, 500

        return {
            "Preview_link": preview_link,
            "Status": True
        }, 200


class ListVoices(BaseController):
    method_decorators = [authenticate]

    def get(self, user_id):
        return TTSService().list_all_speakers(user_id)


class ListSampleVoices(BaseController):
    def get(self):
        return TTSService().list_sample_speakers()


class CreateProject(BaseController):
    method_decorators = [authenticate]

    def post(self):
        request = BaseController.get_request_input()
        proj_id = TTSService().create_project(request)
        if proj_id is None:
            return {}, 500

        return {"Id": proj_id}, 200


class GetProjectDetails(BaseController):
    method_decorators = [authenticate]

    def get(self, project_id):
        project_details, err = TTSService().get_project_details(project_id)
        if err is not None:
            return {}, 500

        return {"details": project_details}, 200


class ListAllProjectsForUser(BaseController):
    method_decorators = [authenticate]

    def get(self, user_id):
        project_details, err = TTSService().list_all_projects_for_user(user_id)
        if err is not None:
            return {}, 500

        return project_details, 200


class UpdateUserDetails(BaseController):
    method_decorators = [authenticate]

    def put(self):
        request = BaseController.get_request_input()
        headers = BaseController.get_headers()

        is_updated, err = TTSService().update_user_details(request)
        response = {"Status": is_updated}
        if err != "":
            response["error"] = err

        return response, 200


class CloneVoice(BaseController):
    method_decorators = [authenticate]

    def post(self):
        files = request.files.getlist("files")
        clone_name = request.form.get('clone_name')
        gender = request.form.get('gender')
        user_id = request.form.get('user_id')
        dir_name = os.path.dirname("/tmp/{}/".format(clone_name))
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        for file in files:
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join('/tmp/' + clone_name, filename))  # Save the file to the desired location

        voice_clone_details = {
            "voice_folder": "/tmp/" + clone_name,
            "speaker_name": clone_name,
            "user_id": user_id,
            "gender": gender
        }
        is_success, message = TTSService().create_voice_clone(voice_clone_details)
        helper_utils.delete_dir(voice_clone_details.get("voice_folder"))

        response = {"voice_clone_success": is_success, "message": message}
        return response, 200


### Chrome Extensions Logic
class ListSpeakerDetails(BaseController):
    def get(self):
        return TTSService().list_speakers_for_chrome_extension()


class TTSExtension(BaseController):
    def post(self):
        request = BaseController.get_request_input()
        status, speech_s3_link, err = TTSService().tts_extension(request)
        response = {}
        if err is not None:
            response["error"] = err
        else:
            response["speech_s3_link"] = speech_s3_link
        response["status"] = status

        return response, 200
