import io
import json
import os

import boto3
import librosa
import numpy as np

import aws.constants as aws_const
import constants
from config import app_config
from entity.tts_entity import TTSEntity
from logger import logger


class Aws:
    def __init__(self):
        self.sagemaker_runtime = boto3.client("sagemaker-runtime", region_name=app_config[aws_const.AWS_REGION_TTS],
                                              aws_access_key_id=app_config[aws_const.AWS_KEY_ID],
                                              aws_secret_access_key=app_config[aws_const.AWS_ACCESS_KEY])
        self.s3 = boto3.client('s3', region_name=app_config[aws_const.AWS_REGION],
                               aws_access_key_id=app_config[aws_const.AWS_KEY_ID],
                               aws_secret_access_key=app_config[aws_const.AWS_ACCESS_KEY])

    def run_tts(self, speaker_details: {}, tts_entity: TTSEntity):
        # request_body = {
        #     "text": tts_entity.get_text(),
        #     "voice_conditioning_link": speaker_details.get("voice_conditioning_link"),
        #     "process_type": "tts",
        #     # "speaker_id": tts_entity.get_speech_metadata().get_speaker_id(),
        #     # "duration": tts_entity.get_speech_metadata().get_duration(),
        #     # "speaker_name": speaker_details.get("speaker_name", ""),  # TODO REmove
        #     # "tts_type": "api_fast"  # TODO REmove
        # }
        endpoint_name, request_body = self.get_details_based_on_speaker_model(speaker_details, tts_entity)
        request_string = json.dumps(request_body).encode()
        try:
            response = self.sagemaker_runtime.invoke_endpoint(EndpointName=endpoint_name,
                                                              ContentType=aws_const.JSON_APPLICATION_TYPE,
                                                              Body=request_string)
            result = response['Body'].read().decode('utf-8')

            json_load = json.loads(result)
            audio_np = np.array(json_load[aws_const.RESPONSE_KEY])
            logger.info("Response is")
        except Exception as e:
            logger.info("TTS processing failed with exception {}".format(e))
            return []
        # ipd.display(ipd.Audio(audio_np, rate=aws_const.SAMPLE_RATE, normalize=False))
        return audio_np

    def add_voice_clone(self, clone_details: {}):
        request_body = {
            "process_type": "clone_voice",
            "voice_folder": clone_details.get("voice_clone_s3_link"),
            "latent_file_name": "{}_{}.pth".format(clone_details.get("speaker_name"), clone_details.get("user_id"))
        }
        request_string = json.dumps(request_body).encode()
        response = self.sagemaker_runtime.invoke_endpoint(EndpointName=aws_const.ENDPOINT_NAME_FAST,
                                                          ContentType=aws_const.JSON_APPLICATION_TYPE,
                                                          Body=request_string)
        result = response['Body'].read().decode('utf-8')

        json_load = json.loads(result)
        latent_conditioning_s3_link = json_load[aws_const.RESPONSE_KEY]
        return latent_conditioning_s3_link

    def upload_to_s3(self, file_path, s3_upload_path, upload_args=None) -> (bool, str, str):
        """
        Function to upload file to s3.
        @param file_path
        @param upload_args
        @param s3_upload_path
        @Return is_upload_success, s3_link and Error (if any).
        """
        try:
            # file_name = file_path.split("/")[2]
            self.s3.upload_file(file_path, app_config[aws_const.AWS_BUCKET_NAME],
                                s3_upload_path,
                                ExtraArgs=upload_args)
            s3_url_link = aws_const.S3_LINK.format(app_config[aws_const.AWS_BUCKET_NAME],
                                                   app_config[aws_const.AWS_REGION],
                                                   s3_upload_path)
            return True, s3_url_link, None
        except Exception as e:
            logger.error("Upload to s3 failed with exception {}".format(e))
            return False, "", e.__str__()

    def upload_folder_to_s3(self, local_folder_path, s3_folder_path):
        for root, dirs, files in os.walk(local_folder_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                s3_file_path = "{}/{}".format(s3_folder_path, file)
                is_success, s3_link, err = self.upload_to_s3(local_file_path, s3_file_path)
                if err is not None:
                    logger.info("Error uploading to s3 with err {}".format(err))
                    return None

        return aws_const.S3_LINK.format(app_config[aws_const.AWS_BUCKET_NAME],
                                        app_config[aws_const.AWS_REGION],
                                        s3_folder_path)

    def download_audio_from_s3(self, s3_link):
        bucket_name = app_config[aws_const.AWS_BUCKET_NAME]
        file_key = '/'.join(s3_link.split('/')[3:])

        # Download the audio file from S3
        response = self.s3.get_object(Bucket=bucket_name, Key=file_key)
        audio_data = response['Body'].read()

        # Convert the audio data to a NumPy array using librosa
        audio, sr = librosa.load(io.BytesIO(audio_data))
        return audio

    def get_details_based_on_speaker_model(self, speaker_details: {}, tts_entity: TTSEntity) -> (str, dict):
        model_name = speaker_details.get("model_name", constants.VCTK_VIT_MODEL)
        if model_name == constants.VCTK_VIT_MODEL:
            request_body = {
                "text": tts_entity.get_text(),
                "speaker_id": tts_entity.get_speech_metadata().get_speaker_id(),
                "duration": tts_entity.get_speech_metadata().get_duration(),
            }
            return aws_const.ENDPOINT_VITS, request_body

        request_body = {
            "text": tts_entity.get_text(),
            "voice_conditioning_link": speaker_details.get("voice_conditioning_link"),
            "process_type": "tts",
        }
        return aws_const.ENDPOINT_NAME_FAST, request_body
