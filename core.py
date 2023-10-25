import io
import soundfile as sf

from entity.speaker_entity import SpeakerEntity
from entity.tts_entity import TTSEntity
from entity.user_entity import UserEntity
from factory import TTSApiFactory, UsersApiFactory
import helper_utils as utils
from repository.repository import TTSRepository
from repository.speaker_repository import SpeakerRepository
from repository.user_repository import UserRepository
from logger import logger
from aws.aws_vits import AwsVitsModel


class TTSCore:
    def __init__(self):
        self.tts_model = AwsVitsModel()
        self.tts_repo = TTSRepository()
        self.user_repo = UserRepository()
        self.speaker_repo = SpeakerRepository()
        self.tts_api_factory = TTSApiFactory()
        self.user_api_factory = UsersApiFactory()

    def process_tts(self, tts_entity: TTSEntity):
        audio = self.tts_model.run_tts(tts_entity)
        logger.info("Received Audio")
        tts_aggregate = self.tts_api_factory.build(tts_entity)
        self.tts_repo.create_tts_aggregate(tts_aggregate=tts_aggregate)
        logger.info("TTS task successful")
        return audio

    def voice_preview(self, tts_entity: TTSEntity):
        audio = self.tts_model.run_tts(tts_entity)
        audio_file = io.BytesIO()
        sf.write(audio_file, audio, 22050, format='WAV')
        return audio_file

    def signup_user(self, user_entity: UserEntity):
        # create JWT Token
        token = utils.create_jwt_token(user_entity.to_JSON())
        user_aggregate = self.user_api_factory.build(user_entity)
        user_entity.set_token(token)
        try:
            user_id = self.user_repo.create_user_aggregate(user_aggregate=user_aggregate)
            logger.info("User Creation successful")
            return user_id, token, None
        except Exception as e:
            return "", "", e.__str__()

    def login_user(self, email_id, password):
        """
        Function returns user_id and token if credentials match
        :params email_id: user email
        :params password: user password

        Returns: user_id, token, Error (if any).
        """
        try:
            user_entity = self.user_repo.load_user_aggregate_by_details(email=email_id, password=password)
            if user_entity is None:
                logger.info("No user exists with emailId {} and password {}".format(email_id, password))
                return "", "", None

            if utils.is_token_valid(user_entity.get_token()):
                return user_entity.get_id().value(), user_entity.get_token(), None

            token = utils.create_jwt_token(user_entity.to_JSON())
            user_entity.set_token(token)
            user_aggregate = self.user_api_factory.build(user_entity)
            user_id = self.user_repo.update_user_aggregate(user_aggregate=user_aggregate)
            return user_id, token, None
        except Exception as e:
            return "", "", e.__str__()

    def save_file_and_upload(self, audio):
        # Specify the file path where you want to save the WAV file
        file_path = utils.save_audio_file(audio)
        print("File path is {}".format(file_path))
        is_success, s3_link, err = self.tts_model.upload_to_s3(file_path)
        utils.delete_file(file_path)
        return is_success, s3_link, err

    def list_all_speakers(self, speaker_ids) -> []:
        speaker_details = []
        if speaker_ids is None:
            speaker_entities = self.speaker_repo.list_all_speakers()
        else:
            speaker_entities = self.speaker_repo.list_sample_speakers(speaker_ids=speaker_ids)

        for speaker_entity in speaker_entities:
            speaker_info = {
                "Name": speaker_entity.get_name(),
                "Gender": speaker_entity.get_gender(),
                "Id": speaker_entity.get_id(),
                "Lang": speaker_entity.get_language()
            }
            speaker_details.append(speaker_info)

        return speaker_details

    def create_speakers(self, speaker_details_list) -> bool:
        speaker_entity_list = []
        for speaker_detail in speaker_details_list:
            speaker_entity = SpeakerEntity(
                id=speaker_detail.get("id"),
                name=speaker_detail.get("name"),
                gender=speaker_detail.get("gender"),
                model_name="VCTK",
                language="en"
            )
            speaker_entity_list.append(speaker_entity)

        for speaker_entity in speaker_entity_list:
            self.speaker_repo.create_speaker_aggregate(speaker_entity)
        logger.info("Success")
        return True

    def get_user_details(self, user_id) -> UserEntity:
        return self.user_repo.load_user_aggregate(user_id=user_id)

