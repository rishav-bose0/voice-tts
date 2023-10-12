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
from scipy.io import wavfile


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

    def voice_preview(self, tts_entity: TTSEntity):
        # wav_file_path = '/Users/rishavbose/PycharmProjects/voiceai/tmp/output_audio1.wav'

        # Read the WAV file using scipy
        # sample_rate, audio = wavfile.read(wav_file_path)
        # audio =
        audio = self.tts_model.run_tts(tts_entity)
        audio_file = io.BytesIO()
        sf.write(audio_file, audio, 22050, format='WAV')
        return audio_file

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

    def list_all_speakers(self) -> []:
        speaker_details = []
        speaker_entities = self.speaker_repo.list_all_speakers()
        for speaker_entity in speaker_entities:
            speaker_info = {
                "Name": speaker_entity.get_name(),
                "Gender": speaker_entity.get_gender(),
                "Id": speaker_entity.get_id()
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
