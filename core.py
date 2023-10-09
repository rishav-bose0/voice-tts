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
        tts_aggregate = self.tts_api_factory.build(tts_entity)
        self.tts_repo.create_tts_aggregate(tts_aggregate=tts_aggregate)
        logger.info("TTS task successful")
        return audio

    def add_user(self, user_entity: UserEntity):
        user_aggregate = self.user_api_factory.build(user_entity)
        user_id = self.user_repo.create_user_aggregate(user_aggregate=user_aggregate)
        logger.info("User Creation successful")
        return user_id

    def save_file_and_upload(self, audio):
        # Specify the file path where you want to save the WAV file
        file_path = utils.save_audio_file(audio)
        print("File path is {}".format(file_path))
        is_success = self.tts_model.upload_to_s3(file_path)
        utils.delete_file(file_path)
        return is_success
