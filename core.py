import json
import time

import sqlalchemy.exc

import constants
import error_descriptions
import helper_utils as utils
from aws.aws_vits import Aws
from common.utils.rzp_id import RzpID
from entity.project_entity import ProjectEntity
from entity.speaker_entity import SpeakerEntity, CloneDetails
from entity.tts_entity import TTSEntity
from entity.user_entity import UserEntity
from factory import TTSApiFactory, UsersApiFactory, ProjectApiFactory
from logger import logger
from repository.project_repository import ProjectRepository
from repository.speaker_repository import SpeakerRepository
from repository.tts_repository import TTSRepository
from repository.user_repository import UserRepository


class TTSCore:
    def __init__(self):
        self.aws = Aws()
        self.tts_repo = TTSRepository()
        self.user_repo = UserRepository()
        self.speaker_repo = SpeakerRepository()
        self.project_repo = ProjectRepository()
        self.tts_api_factory = TTSApiFactory()
        self.user_api_factory = UsersApiFactory()
        self.project_api_factory = ProjectApiFactory()

    def process_tts_request(self, tts_entity: TTSEntity, is_tts_generated: bool):
        if not is_tts_generated:
            return self.process_tts(tts_entity=tts_entity)
        try:
            tts_aggregate = self.tts_repo.load_tts_aggregate_by_details(project_id=tts_entity.project_id,
                                                                        text=tts_entity.text,
                                                                        language=tts_entity.language,
                                                                        speech_metadata=tts_entity.speech_metadata.__dict__)
        except Exception as e:
            return self.process_tts(tts_entity=tts_entity)

        tts_s3_link = tts_aggregate.get_tts_entity().get_speech_s3_link()
        audio_np = self.aws.download_audio_from_s3(s3_link=tts_s3_link)
        return audio_np, tts_s3_link, None

    def process_tts(self, tts_entity: TTSEntity):
        """
        Function processes the text to speech and returns audio in numpy format, s3 link.
        @param tts_entity: TTSEntity
        returns: audio numpy, s3 link.
        """
        # Call speaker repo and check the model. Based on the model the endpoints are invoked.
        process_tts_start_time = time.time()
        speaker_id = tts_entity.get_speech_metadata().get_speaker_id()
        speaker_entity = self.get_speaker_detail(speaker_id=speaker_id)
        speaker_details = {
            "model_name": speaker_entity.model_name,
            "speaker_name": speaker_entity.name,
            # "voice_conditioning_link": speaker_entity.get_clone_details().get_auto_condition_link()
        }
        if speaker_entity.model_name == constants.VCTK_TORTOISE_MODEL or \
                speaker_entity.model_name == constants.TORTOISE_CLONE_MODEL:
            speaker_details["voice_conditioning_link"] = speaker_entity.get_clone_details().get_auto_condition_link()

        audio = self.aws.run_tts(speaker_details=speaker_details, tts_entity=tts_entity)
        process_tts_end_time = time.time()
        logger.info("Time taken for tts operation {} secs".format(process_tts_end_time - process_tts_start_time))
        logger.info("Received Audio")
        is_uploaded, s3_link, err = self.save_file_and_upload(audio)
        save_file_and_upload_end_time = time.time()
        logger.info("Time taken for save_file_and_upload operation {} secs".format(
            save_file_and_upload_end_time - process_tts_end_time))
        if not is_uploaded:
            return audio, "", err
        tts_entity.set_speech_s3_link(s3_link)
        tts_aggregate = self.tts_api_factory.build(tts_entity)
        self.tts_repo.create_tts_aggregate(tts_aggregate=tts_aggregate)
        save_aggregate_end_time = time.time()
        logger.info("Time taken for save_file_and_upload operation {} secs".format(
            save_aggregate_end_time - save_file_and_upload_end_time))
        logger.info("TTS task successful")
        return audio, s3_link, None

    def voice_preview(self, speaker_id):
        try:
            speaker_aggregate = self.speaker_repo.load_speaker_aggregate(speaker_id=speaker_id)
            return speaker_aggregate.get_speaker_entity().get_voice_preview_link()
        except Exception as e:
            return None

    def signup_user(self, user_entity: UserEntity, is_google_auth_token_present: bool):
        """
        Function to add user details to database and create jwt token.
        @param user_entity
        @param is_google_auth_token_present

        @return user_id, jwt token and Error (If any)
        """
        token = utils.create_jwt_token(user_entity.to_JSON())
        user_aggregate = self.user_api_factory.build(user_entity)
        user_entity.set_token(token)
        try:
            user_id = self.user_repo.create_user_aggregate(user_aggregate=user_aggregate)
            logger.info("User Creation successful")
            return user_id, token, None
        except Exception as e:
            err_class = sqlalchemy.exc.IntegrityError
            if e.__class__ == err_class and not is_google_auth_token_present:
                return "", "", error_descriptions.EMAIL_ID_ALREADY_EXISTS.format(user_entity.get_email())
            elif is_google_auth_token_present:
                return self.login_user(user_entity.get_email(), user_entity.get_password(), is_google_login=True)

            return "", "", e.__str__()

    def login_user(self, email_id, password, is_google_login):
        """
        Function returns user_id and token if credentials match
        @param email_id: user email
        @param password: user password
        @param is_google_login: Bool value. True if login done using google

        @Return user_id, token, Error (if any).
        """
        try:
            user_entity = self.user_repo.load_user_aggregate_by_details(email=email_id, password=password,
                                                                        is_google_login=is_google_login)
            if user_entity is None:
                logger.info("No user exists with emailId {} and password {}".format(email_id, password))
                return "", "", "Invalid email or password"

            if utils.is_token_valid(user_entity.get_token()):
                return user_entity.get_id().value(), user_entity.get_token(), None

            user_id = user_entity.get_id()
            token = utils.create_jwt_token(user_entity.to_JSON())
            user_entity.set_token(token)
            user_aggregate = self.user_api_factory.build(user_entity)
            user_aggregate.get_user_entity().set_id(user_id)
            user_id, err_msg = self.user_repo.update_user_aggregate(user_aggregate=user_aggregate)
            if err_msg is not None:
                return "", "", err_msg

            return user_id, token, None
        except Exception as e:
            return "", "", e.__str__()

    def save_file_and_upload(self, audio):
        # Specify the file path where you want to save the WAV file
        file_path = utils.save_audio_file(audio)
        print("File path is {}".format(file_path))
        upload_args = {'ContentType': 'audio/wav', 'ContentDisposition': 'attachment'}
        s3_upload_path = "audio_files/{}".format(file_path.split("/")[2])
        is_success, s3_link, err = self.aws.upload_to_s3(file_path, s3_upload_path, upload_args)
        utils.delete_file(file_path)
        return is_success, s3_link, err

    def list_all_speakers(self, user_id) -> []:
        """
        Returns a list of all speakers present in db. If speaker_ids is none, will return all.
        @param user_id
        """
        speaker_details = []

        speaker_entities = self.speaker_repo.list_all_speakers(user_id)
        for speaker_entity in speaker_entities:
            speaker_info = self.get_speaker_details_from_entity(speaker_entity)
            speaker_details.append(speaker_info)

        return speaker_details

    def list_sample_speakers(self, speaker_ids) -> []:
        """
        Returns a list of all speakers present in db. If speaker_ids is none, will return all.
        @param speaker_ids
        """
        speaker_details = []
        speaker_entities = self.speaker_repo.list_sample_speakers(speaker_ids=speaker_ids)

        for speaker_entity in speaker_entities:
            speaker_info = self.get_speaker_details_from_entity(speaker_entity)
            speaker_info["Preview_link"] = constants.sample_voice_preview.get(speaker_entity.get_id())
            speaker_details.append(speaker_info)

        return speaker_details

    def list_speakers_for_chrome_extension(self) -> []:
        """
        Returns a list of all speakers present in db. If speaker_ids is none, will return all.
        """
        speaker_details = []
        speaker_entities = self.speaker_repo.list_speakers_details_for_model(model_name=constants.VCTK_VIT_MODEL)

        for speaker_entity in speaker_entities:
            speaker_info = self.get_speaker_details_from_entity(speaker_entity)
            speaker_details.append(speaker_info)

        return speaker_details

    def get_speaker_details_from_entity(self, speaker_entity: SpeakerEntity) -> dict:
        return {
            "Name": speaker_entity.get_name(),
            "Gender": speaker_entity.get_gender(),
            "Id": int(speaker_entity.get_id()),
            "Language": speaker_entity.get_language(),
            "Emotion": speaker_entity.get_emotions(),
            "Country": speaker_entity.get_country(),
            "Img_url": speaker_entity.get_image_link(),
            "Preview_link": constants.sample_voice_preview.get(speaker_entity.get_voice_preview_link()),
            "Type": "standard" if speaker_entity.model_name == constants.VCTK_VIT_MODEL else "premium" if speaker_entity.model_name == constants.VCTK_TORTOISE_MODEL else "clone"
        }

    def create_speakers(self, speaker_details_list) -> bool:
        speaker_entity_list = []
        for speaker_detail in speaker_details_list:

            speaker_entity = SpeakerEntity(
                id=speaker_detail.get("id"),
                name=speaker_detail.get("name"),
                gender=speaker_detail.get("gender"),
                model_name=speaker_detail.get("model_name"),
                language="en",
                image_link=speaker_detail.get("image_link"),
                voice_preview_link=speaker_detail.get("voice_preview_link"),
                country="us",
                emotions=["Neutral"],
                speaker_type="public",
                # clone_details=CloneDetails(auto_condition_link=clone_details_json.get("auto_condition_link"))
            )
            clone_details = speaker_detail.get("clone_details")
            if clone_details != '':
                clone_details_json = json.loads(json.loads(clone_details))
                speaker_entity.clone_details = CloneDetails(
                    auto_condition_link=clone_details_json.get("auto_condition_link"))

            speaker_entity_list.append(speaker_entity)

        for speaker_entity in speaker_entity_list:
            self.speaker_repo.create_speaker_aggregate(speaker_entity)
        logger.info("Success")
        return True

    def get_speaker_detail(self, speaker_id) -> SpeakerEntity:
        try:
            speaker_aggregate = self.speaker_repo.load_speaker_aggregate(speaker_id)
            return speaker_aggregate.get_speaker_entity()
        except Exception as e:
            return None

    def get_user_details(self, user_id) -> UserEntity:
        """
        Function returns all details about a particular user
        @param user_id

        @returns UserEntity
        """
        return self.user_repo.load_user_aggregate(user_id=user_id)

    def create_project(self, project_entity: ProjectEntity):
        project_aggregate = self.project_api_factory.build(project_entity)
        try:
            return self.project_repo.create_project_aggregate(project_aggregate)
        except Exception as e:
            return None

    def get_project_details(self, project_id) -> {}:
        get_block_details = {}
        try:
            project_entity = self.project_repo.load_project_aggregate(project_id=project_id)
            tts_entities_by_block_num = self.tts_repo.load_tts_aggregate_by_project_id(project_id)
        except Exception as e:
            return {}, e.__str__()

        for block_num, tts_entity in tts_entities_by_block_num.items():
            speaker_entity = self.get_speaker_detail(tts_entity.get_speech_metadata().get_speaker_id())
            if speaker_entity is None:
                continue
            get_block_details[block_num] = {
                constants.TTS_DETAILS: {
                    "text": tts_entity.get_text(),
                    "speech_s3_link": tts_entity.get_speech_s3_link(),
                    "emotion": tts_entity.get_speech_metadata().get_emotion(),
                    "pitch": tts_entity.get_speech_metadata().get_pitch(),
                    "duration": tts_entity.get_speech_metadata().get_duration(),
                },
                constants.SPEAKER_DETAILS: {
                    "id": int(speaker_entity.get_id()),
                    "name": speaker_entity.get_name(),
                    "image_link": speaker_entity.get_image_link()
                }
            }

        get_project_details = {
            constants.NAME: project_entity.get_name(),
            constants.BLOCK_DETAILS: get_block_details
        }

        return get_project_details, None

    def list_all_projects_for_user(self, user_id):
        return self.project_repo.load_project_details_for_user(user_id=user_id)

    def update_user_details(self, user_entity):
        rzp_id = RzpID(id=user_entity.get_id())
        user_aggregate = self.user_api_factory.build(user_entity)
        user_aggregate.get_user_entity().set_id(rzp_id)
        try:
            id, err_msg = self.user_repo.update_user_aggregate(user_aggregate)
            if err_msg != "":
                return False, err_msg
            return True, ""
        except Exception as e:
            return False, "Internal Error"

    def create_voice_clone(self, voice_clone_details):
        """
        voice_clone_details = {
            "voice_folder": "/tmp/" + clone_name,
            "speaker_name": clone_name,
            "user_id": req.get("user_id")
        }
        """

        voice_folder_path = voice_clone_details.get("voice_folder")
        # Resample audio to 22050 sr
        logger.info("Resampling Audio ..")
        resampled_voice_folder_path = voice_folder_path + "_resampled"
        is_resampled = utils.resample_folder_audio(voice_folder_path, resampled_voice_folder_path)
        if not is_resampled:
            return False, error_descriptions.VOICE_CLONING_FAILED

        logger.info("Audio Resampling Done.")
        speaker_name = voice_clone_details.get("speaker_name")
        user_id = voice_clone_details.get("user_id")
        gender = voice_clone_details.get("gender")
        folder_s3_link = self.aws.upload_folder_to_s3(local_folder_path=resampled_voice_folder_path,
                                                      s3_folder_path="cloned_voice/{}_{}".format(speaker_name, user_id))
        if folder_s3_link is None:
            return False, error_descriptions.VOICE_CLONING_FAILED

        voice_clone_details["voice_clone_s3_link"] = folder_s3_link
        utils.delete_dir(resampled_voice_folder_path)

        # https://voaux.s3.ap-south-1.amazonaws.com/cloned_voice/Karen_N7mXC9iSRU0DgJ/
        auto_conditioning_s3_link = self.aws.add_voice_clone(clone_details=voice_clone_details)

        # speaker_agg = self.speaker_repo.load_speaker_aggregate_by_name(speaker_name)
        speaker_entity = SpeakerEntity(
            name=speaker_name,
            model_name=constants.TORTOISE_CLONE_MODEL,
            user_id=user_id,
            gender=gender,
            speaker_type="clone",
            clone_details=CloneDetails(
                auto_condition_link=auto_conditioning_s3_link
            ),
            # language="en",
            # country="us",
            emotions=["Neutral"],
            image_link=utils.get_image_avatar(gender),
            # voice_preview_link=speaker_agg.get_speaker_entity().get_voice_preview_link()
        )

        try:
            self.speaker_repo.create_speaker_aggregate(speaker_entity)
            return True, "Voice Cloning Successful"
        except Exception as e:
            return False, error_descriptions.VOICE_CLONING_FAILED
