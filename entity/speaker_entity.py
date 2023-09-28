from common.entity.base_entity import BaseEntity
from dataclasses import dataclass
from dataclasses import field

from common.utils.rzp_id import RzpID


@dataclass
class SpeakerEntity(BaseEntity):
    name: str = field(default_factory=str)
    pretrained_link: str = field(default_factory=str)
    language: str = field(default_factory=str)
    emotions: list[str] = field(default_factory=list[str])

    def get_id(self):
        return self.id

    def set_id(self, rzp_id):
        self.id = rzp_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_pretrained_link(self):
        return self.pretrained_link

    def set_pretrained_link(self, pretrained_link):
        self.pretrained_link = pretrained_link

    def get_language(self):
        return self.language

    def set_language(self, language):
        self.language = language

    def get_emotions(self):
        return self.emotions

    def set_emotions(self, emotions):
        self.emotions = emotions

    def initialize(self):
        p_id = RzpID()
        p_id.create()
        self.id = p_id

    def to_JSON(self):
        return self.__dict__
