import boto3
import json
import numpy as np

import aws.constants as aws_const
from config import app_config
from logger import logger


class AwsVitsModel:
    def __init__(self):
        self.sagemaker_runtime = boto3.client("sagemaker-runtime", region_name=app_config[aws_const.AWS_REGION],
                                              aws_access_key_id=app_config[aws_const.AWS_KEY_ID],
                                              aws_secret_access_key=app_config[aws_const.AWS_ACCESS_KEY])

    def run_tts(self, request):
        request_string = json.dumps(request).encode()
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
