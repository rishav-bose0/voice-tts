import random
import os
from scipy.io import wavfile
from logger import logger


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
