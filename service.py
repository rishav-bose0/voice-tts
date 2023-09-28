import numpy as np
from flask import Response
from scipy.io import wavfile

import constants
from core import TTSCore
from entity.tts_entity import TTSEntity, SpeechMetadata
from entity.user_entity import UserEntity


class TTSService:
    def __init__(self):
        self.tts_core = TTSCore()

    def add_user(self, request, header):
        user_entity = self.to_user_entity(request)
        return self.tts_core.add_user(user_entity=user_entity)

    def process_tts(self, request, header):
        audio_files = []
        for req in request:
            tts_entity = self.to_tts_entity(req)
            audio_files.append(self.tts_core.process_tts(tts_entity))

        combined_audio = np.array([])

        # Iterate through the list of audio files and concatenate them
        for audio_file in audio_files:
            combined_audio = np.concatenate((combined_audio, audio_file), axis=0)

        audio_bytes = combined_audio.tobytes()

        # Create a Flask Response with the audio data and the appropriate content type
        Response(audio_bytes, content_type=constants.AUDIO_FORMAT)

        # Specify the file path where you want to save the WAV file
        file_path = '../tmp/output_audio2.wav'

        # Scale the audio data to the appropriate range (-32768 to 32767 for 16-bit PCM)
        # Save the audio data as a WAV file
        wavfile.write(file_path, 22050, combined_audio)
        return True

    def to_tts_entity(self, request) -> TTSEntity:
        speech_metadata = SpeechMetadata(
            # pitch=request.get(constants.PITCH, 1),
            emotion=request.get(constants.EMOTION, "normal"),
            duration=request.get(constants.DURATION, 1),
        )
        tts_entity = TTSEntity(speaker_id=request.get(constants.SPEAKER_ID), text=request.get(constants.TEXT),
                               language=request.get(constants.LANGUAGE), speech_metadata=speech_metadata)

        return tts_entity

    def to_user_entity(self, request) -> UserEntity:
        user_entity = UserEntity(email=request.get(constants.EMAIL),
                                 privilege_type=request.get(constants.PRIVILEGE_TYPE))

        return user_entity
