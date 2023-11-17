from dataclasses import dataclass
from dataclasses import field


@dataclass
class SpeakerEntity:
    id: str = field(default_factory=str)
    name: str = field(default_factory=str)
    gender: str = field(default_factory=str)
    model_name: str = field(default_factory=str)
    language: str = field(default_factory=str)
    country: str = field(default_factory=str)
    image_link: str = field(default_factory=str)
    voice_preview_link: str = field(default_factory=str)
    emotions: list[str] = field(default_factory=list[str])

    def get_id(self):
        return self.id

    def set_id(self, rzp_id):
        self.id = rzp_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_image_link(self):
        return self.image_link

    def set_image_link(self, image_link):
        self.image_link = image_link

    def get_voice_preview_link(self):
        return self.voice_preview_link

    def set_voice_preview_link(self, voice_preview_link):
        self.voice_preview_link = voice_preview_link

    def get_gender(self):
        return self.gender

    def set_gender(self, gender):
        self.gender = gender

    def get_model_name(self):
        return self.model_name

    def set_model_name(self, model_name):
        self.model_name = model_name

    def get_language(self):
        return self.language

    def set_language(self, language):
        self.language = language

    def get_country(self):
        return self.country

    def set_country(self, country):
        self.country = country

    def get_emotions(self):
        return self.emotions

    def set_emotions(self, emotions):
        self.emotions = emotions

    def to_JSON(self):
        return self.__dict__
