import boto3
import json
import numpy as np

import aws.constants as aws_const
from config import app_config
from entity.tts_entity import TTSEntity
from logger import logger


class AwsVitsModel:
    def __init__(self):
        self.sagemaker_runtime = boto3.client("sagemaker-runtime", region_name=app_config[aws_const.AWS_REGION],
                                              aws_access_key_id=app_config[aws_const.AWS_KEY_ID],
                                              aws_secret_access_key=app_config[aws_const.AWS_ACCESS_KEY])
        self.s3 = boto3.client('s3', region_name=app_config[aws_const.AWS_REGION],
                               aws_access_key_id=app_config[aws_const.AWS_KEY_ID],
                               aws_secret_access_key=app_config[aws_const.AWS_ACCESS_KEY])

    def run_tts(self, tts_entity: TTSEntity):
        request_body = {
            "text": tts_entity.get_text(),
            "speaker_id": tts_entity.get_speaker_id(),
            "duration": tts_entity.get_speech_metadata().get_duration()
        }
        request_string = json.dumps(request_body).encode()
        try:
            response = self.sagemaker_runtime.invoke_endpoint(EndpointName=aws_const.ENDPOINT_NAME,
                                                              ContentType=aws_const.JSON_APPLICATION_TYPE,
                                                              Body=request_string)
            result = response['Body'].read().decode('utf-8')

            json_load = json.loads(result)
            audio_np = np.array(json_load[aws_const.RESPONSE_KEY])
        except Exception as e:
            logger.info("TTS processing failed with exception {}".format(e))
            return []
        # ipd.display(ipd.Audio(audio_np, rate=aws_const.SAMPLE_RATE, normalize=False))
        return audio_np

    def upload_to_s3(self, file_path) -> (bool, str, str):
        try:
            file_name = file_path.split("/")[2]
            self.s3.upload_file(file_path, app_config[aws_const.AWS_BUCKET_NAME],
                                "audio_files/{}".format(file_name))
            s3_url_link = "https://{}.s3.{}.amazonaws.com/audio_files/{}".format(app_config[aws_const.AWS_BUCKET_NAME],
                                                                                 app_config[aws_const.AWS_REGION],
                                                                                 file_name)
            return True, s3_url_link, ""
        except Exception as e:
            logger.info("Upload to s3 failed with exception {}".format(e))
            return False, None, e.__str__()
