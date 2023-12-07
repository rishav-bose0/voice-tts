import os
import random
import shutil
from datetime import datetime, timedelta

import jwt
import numpy as np
import requests
from pydub import AudioSegment
from scipy.io import wavfile

import constants
from common.utils.unique_id_generator import UniqueIdGenerator
from config import app_config
from constants import JWT_EXPIRY_TIME, JWT_SECRET
from logger import logger


def save_audio_file(audio, path="/tmp/"):
    # Specify the file path where you want to save the WAV file

    num = UniqueIdGenerator().generate_unique_id()
    file_path = path + "output_audio{}.wav".format(num)
    scaled_audio = (audio * 32767).astype(np.int16)
    # Scale the audio data to the appropriate range (-32768 to 32767 for 16-bit PCM)
    # Save the audio data as a WAV file
    wavfile.write(file_path, 22050, scaled_audio)
    return file_path


def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        logger.info("File {} successfully deleted.".format(file_path))
    else:
        # If it fails, inform the user.
        logger.info("Error: {} file not found".format(file_path))


def delete_dir(dir_path):
    try:
        shutil.rmtree(dir_path)
        print(f"Directory '{dir_path}' successfully deleted.")
    except OSError as e:
        print(f"Error: {dir_path} : {e.strerror}")


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


def decode_google_oath_token_to_user_details(token) -> {}:
    headers = {'Authorization': 'Bearer {}'.format(token)}
    user_details = requests.get(constants.GOOGLE_OAUTH_USER_INFO_URL, headers=headers)
    if user_details.status_code != 200:
        return False, user_details.json()
    user_details_json = user_details.json()
    return True, {
        constants.EMAIL: user_details_json.get("email"),
        constants.FIRST_NAME: user_details_json.get("given_name"),
        constants.LAST_NAME: user_details_json.get("family_name")
    }


def is_request_contain_oath_token(request) -> bool:
    return request.get("token") is not None


# def upload_audio_file_to_s3(file_path, bucket_name, object_key, content_type='audio/wav'):
#     # Initialize S3 client
#     s3 = boto3.client('s3')
#
#     # Set the content type for the audio file
#
#     # Upload the file to S3
#     s3.upload_file(
#         file_path,
#         bucket_name,
#         object_key,
#         ExtraArgs={'ContentType': content_type, 'ContentDisposition': 'attachment'}
#     )
#
#     print(f"File uploaded successfully to S3: {bucket_name}/{object_key}")

def get_image_avatar(gender):
    return random.choice(constants.avatar_pics.get(gender))


def process_audio(input_file, output_file, target_sr=22050):
    audio = AudioSegment.from_file(input_file)

    # Resample the audio to the target sample rate
    resampled_audio = audio.set_frame_rate(target_sr)

    # Export the processed audio
    resampled_audio.export(output_file, format="wav")


# Specify the directory containing the WAV files


# Process each WAV file in the input directory


def resample_folder_audio(folder_path: str, output_folder_path: str):
    os.makedirs(output_folder_path, exist_ok=True)
    target_sr = 22050
    for filename in os.listdir(folder_path):
        if filename.endswith(".wav"):
            input_file = os.path.join(folder_path, filename)
            output_file = os.path.join(output_folder_path, filename)
            audio = AudioSegment.from_file(input_file)

            # Resample the audio to the target sample rate
            resampled_audio = audio.set_frame_rate(target_sr)

            # Export the processed audio
            resampled_audio.export(output_file, format="wav")
