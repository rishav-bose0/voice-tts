import numpy as np
from flask import send_file

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

        return self.tts_core.save_file_and_upload(combined_audio)

    def to_tts_entity(self, request) -> TTSEntity:
        speech_metadata = SpeechMetadata(
            # pitch=request.get(constants.PITCH, 1),
            emotion=request.get(constants.EMOTION, "normal"),
            duration=request.get(constants.DURATION, 1),
        )
        tts_entity = TTSEntity(speaker_id=request.get(constants.SPEAKER_ID), text=request.get(constants.TEXT),
                               language=request.get(constants.LANGUAGE, "en"), speech_metadata=speech_metadata)

        return tts_entity

    def to_user_entity(self, request) -> UserEntity:
        user_entity = UserEntity(email=request.get(constants.EMAIL),
                                 privilege_type=request.get(constants.PRIVILEGE_TYPE))

        return user_entity

    def voice_preview(self, speaker_id, name):
        tts_request = {
            "speaker_id": speaker_id,
            "text": "Hello! My name is {}. I am one of the voices of vaux. You can use me for your text to speech tasks"
            .format(name)
        }
        tts_entity = self.to_tts_entity(tts_request)
        audio_file = self.tts_core.voice_preview(tts_entity)
        audio_file.seek(0)

        # Send the audio data as a response with the appropriate MIME type
        return send_file(
            audio_file,
            mimetype='audio/wav',  # You can use 'audio/mpeg' for MP3 or other suitable types
            as_attachment=True,
            download_name=f'{name}.wav'  # Customize the filename as needed
        )

    def list_all_speakers(self):
        return self.tts_core.list_all_speakers()

    def create_speakers(self, speaker_details):
        return self.tts_core.create_speakers(speaker_details)
