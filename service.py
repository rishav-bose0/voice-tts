import numpy as np

import constants
import error_descriptions
import helper_utils as utils
from core import TTSCore
from entity.project_entity import ProjectEntity
from entity.tts_entity import TTSEntity, SpeechMetadata
from entity.user_entity import UserEntity


class TTSService:
    def __init__(self):
        self.tts_core = TTSCore()

    def signup_user(self, request, header):
        is_google_oath_token_present = False
        if utils.is_request_contain_oath_token(request):
            is_success, request = utils.decode_google_oath_token_to_user_details(request.get(constants.TOKEN))
            is_google_oath_token_present = True
            if not is_success:
                return "", "", request.get(constants.ERROR_DESCRIPTION)

        user_entity = self.to_user_entity(request)
        return self.tts_core.signup_user(user_entity=user_entity,
                                         is_google_auth_token_present=is_google_oath_token_present)

    def login_user(self, request, header):
        is_google_login = False
        if utils.is_request_contain_oath_token(request):
            is_google_login = True
            is_success, request = utils.decode_google_oath_token_to_user_details(request.get(constants.TOKEN))
            if not is_success:
                return "", "", request.get(constants.ERROR_DESCRIPTION)

        email_id = request.get(constants.EMAIL)
        password = request.get(constants.PASSWORD)
        if email_id is None or (password is None and not is_google_login):
            return "", "", error_descriptions.INVALID_EMAIL_OR_PASSWORD

        return self.tts_core.login_user(email_id=email_id, password=password, is_google_login=is_google_login)

    def get_user_details(self, user_id):
        return self.tts_core.get_user_details(user_id)

    def process_tts(self, request, header):
        audio_files = []
        s3_link = ""
        for req in request:
            tts_entity = self.to_tts_entity(req)
            # Check if tts already generated
            is_tts_generated = req.get(constants.IS_TTS_GENERATED, False)
            audio_np, s3_link, err = self.tts_core.process_tts_request(tts_entity, is_tts_generated)
            print("Processed TTS REquest")
            if err is not None:
                return False, s3_link, err

            audio_files.append(audio_np)

        # Single file TTs
        if len(audio_files) == 1:
            return True, s3_link, None

        combined_audio = np.array([])

        # Iterate through the list of audio files and concatenate them
        for audio_file in audio_files:
            combined_audio = np.concatenate((combined_audio, audio_file), axis=0)

        return self.tts_core.save_file_and_upload(combined_audio)

    def to_tts_entity(self, request) -> TTSEntity:
        speech_metadata = SpeechMetadata(
            pitch=request.get(constants.PITCH, 1),
            speaker_id=request.get(constants.SPEAKER_ID),
            emotion=request.get(constants.EMOTION, "normal"),
            duration=request.get(constants.DURATION, 1),
        )
        tts_entity = TTSEntity(project_id=request.get(constants.PROJECT_ID), text=request.get(constants.TEXT),
                               language=request.get(constants.LANGUAGE, "en"),
                               block_number=request.get(constants.BLOCK_NUMBER, 0),
                               speech_metadata=speech_metadata)

        return tts_entity

    def to_user_entity(self, request) -> UserEntity:
        user_entity = UserEntity(first_name=request.get(constants.FIRST_NAME),
                                 last_name=request.get(constants.LAST_NAME),
                                 password=request.get(constants.PASSWORD), email=request.get(constants.EMAIL),
                                 privilege_type=request.get(constants.PRIVILEGE_TYPE, "free"))

        return user_entity

    def voice_preview(self, speaker_id, name):
        return self.tts_core.voice_preview(speaker_id=speaker_id)

    def list_all_speakers(self, user_id):
        return self.tts_core.list_all_speakers(user_id)

    def list_sample_speakers(self):
        # speaker_ids = ["55", "59", "60", "88", "102", "103"]
        speaker_ids = [226, 296, 282, 286]
        return self.tts_core.list_sample_speakers(speaker_ids=speaker_ids)

    def create_speakers(self, speaker_details):
        return self.tts_core.create_speakers(speaker_details)

    def create_project(self, request):
        project_entity = self.to_project_entity(request)
        return self.tts_core.create_project(project_entity)

    def get_project_details(self, project_id):
        return self.tts_core.get_project_details(project_id=project_id)

    def to_project_entity(self, request):
        project_entity = ProjectEntity(
            name=request.get("name"),
            user_id=request.get("user_id")
        )

        return project_entity

    def list_all_projects_for_user(self, user_id):
        return self.tts_core.list_all_projects_for_user(user_id)

    def update_user_details(self, request):
        user_entity = self.to_user_entity(request)
        if user_entity.is_empty():
            return False, error_descriptions.INVALID_REQUEST_BODY
        user_id = request.get("user_id")
        if user_id is None:
            return False, error_descriptions.USER_ID_CANNOT_EMPTY
        user_entity.id = user_id
        return self.tts_core.update_user_details(user_entity=user_entity)

    def create_voice_clone(self, voice_clone_details):
        return self.tts_core.create_voice_clone(voice_clone_details)
