import random
import os
from scipy.io import wavfile

from config import app_config
from constants import JWT_EXPIRY_TIME, JWT_SECRET
from logger import logger
import jwt
from datetime import datetime, timedelta
from http import HTTPStatus


def save_audio_file(audio, path="/tmp/"):
    # Specify the file path where you want to save the WAV file

    num = int(random.random() * 10) + 1
    file_path = path + "output_audio{}.wav".format(num)

    # Scale the audio data to the appropriate range (-32768 to 32767 for 16-bit PCM)
    # Save the audio data as a WAV file
    wavfile.write(file_path, 22050, audio)
    return file_path


def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        logger.info("File {} successfully deleted.".format(file_path))
    else:
        # If it fails, inform the user.
        logger.info("Error: {} file not found".format(file_path))


def create_jwt_token(payload_details: dict):
    """
    Function to create JWT Token with expiry time.
    @param payload_details: Dict containing payload

    @Return token.
    """
    payload_data = {
        "payload": payload_details,
        "exp": datetime.utcnow() + timedelta(days=app_config[JWT_EXPIRY_TIME])
    }
    my_secret = app_config[JWT_SECRET]
    token = jwt.encode(
        payload=payload_data,
        key=my_secret
    )

    return token


def is_token_valid(token):
    """
    Function to check token validity
    @param token

    Returns True/False based on token validity
    """
    try:
        jwt.decode(token, key=app_config[JWT_SECRET], algorithms=['HS256', ])
        return True
    except Exception as e:
        logger.info("Exception occured with error {}".format(e))
        return False
