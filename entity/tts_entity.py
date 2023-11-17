import json
from dataclasses import dataclass
from dataclasses import field

from common.entity.base_entity import BaseEntity
from common.utils.rzp_id import RzpID


@dataclass
class SpeechMetadata:
    pitch: str = field(default_factory=str)
    duration: str = field(default_factory=str)
    emotion: str = field(default_factory=str)
    speaker_id: str = field(default_factory=str)

    def get_pitch(self):
        return self.pitch

    def set_pitch(self, pitch):
        self.pitch = pitch

    def get_duration(self):
        return self.duration

    def set_duration(self, duration):
        self.duration = duration

    def get_emotion(self):
        return self.emotion

    def set_emotion(self, emotion):
        self.emotion = emotion

    def get_speaker_id(self):
        return self.speaker_id

    def set_speaker_id(self, speaker_id):
        self.speaker_id = speaker_id

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)


@dataclass
class TTSEntity(BaseEntity):
    project_id: str = field(default_factory=str)
    speech_metadata: SpeechMetadata = field(default_factory=SpeechMetadata)
    text: str = field(default_factory=str)
    language: str = field(default_factory=str)
    block_number: int = field(default_factory=int)
    speech_s3_link: str = field(default_factory=str)

    def get_id(self):
        return self.id

    def set_id(self, rzp_id):
        self.id = rzp_id

    def get_block_number(self):
        return self.block_number

    def set_block_number(self, block_number):
        self.block_number = block_number

    def get_project_id(self):
        return self.project_id

    def set_project_id(self, project_id):
        self.project_id = project_id

    def get_speech_s3_link(self):
        return self.speech_s3_link

    def set_speech_s3_link(self, speech_s3_link):
        self.speech_s3_link = speech_s3_link

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text

    def get_language(self):
        return self.language

    def set_language(self, language):
        self.language = language

    def get_speech_metadata(self):
        return self.speech_metadata

    def set_speech_metadata(self, speech_metadata):
        self.speech_metadata = speech_metadata

    def initialize(self):
        p_id = RzpID()
        p_id.create()
        self.id = p_id

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def set_speech_metadata_from_JSON(self, speech_metadata_JSON):
        if speech_metadata_JSON is None:
            self.speech_metadata = None
        else:
            pitch = speech_metadata_JSON.get("pitch", "")
            duration = speech_metadata_JSON.get("duration", "")
            emotion = speech_metadata_JSON.get("emotion", "")
            speaker_id = speech_metadata_JSON.get("speaker_id", "")
            speech_metadata = SpeechMetadata(pitch=pitch, duration=duration, emotion=emotion, speaker_id=speaker_id)
            self.speech_metadata = speech_metadata
