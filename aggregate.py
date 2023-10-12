from dataclasses import dataclass, field

from entity.speaker_entity import SpeakerEntity
from entity.tts_entity import TTSEntity
from entity.user_entity import UserEntity


@dataclass
class TTSAggregate:
    tts_entity: TTSEntity = field(default_factory=TTSEntity)

    def get_tts_entity(self):
        return self.tts_entity

    def set_tts_entity(self, tts_entity):
        self.tts_entity = tts_entity


@dataclass
class UserAggregate:
    user_entity: UserEntity = field(default_factory=UserEntity)

    def get_user_entity(self):
        return self.user_entity

    def set_user_entity(self, user_entity):
        self.user_entity = user_entity


@dataclass
class SpeakerAggregate:
    speaker_entity: SpeakerEntity = field(default_factory=SpeakerEntity)

    def get_speaker_entity(self):
        return self.speaker_entity

    def set_speaker_entity(self, speaker_entity):
        self.speaker_entity = speaker_entity
