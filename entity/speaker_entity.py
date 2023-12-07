import json
from dataclasses import dataclass
from dataclasses import field


@dataclass
class CloneDetails:
    auto_condition_link: str = field(default_factory=str)

    def get_auto_condition_link(self):
        return self.auto_condition_link

    def set_auto_condition_link(self, auto_condition_link):
        self.auto_condition_link = auto_condition_link

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)


@dataclass
class SpeakerEntity:
    id: int = field(default=None)
    name: str = field(default_factory=str)
    gender: str = field(default_factory=str)
    model_name: str = field(default_factory=str)
    language: str = field(default_factory=str)
    country: str = field(default_factory=str)
    image_link: str = field(default_factory=str)
    voice_preview_link: str = field(default_factory=str)
    emotions: list[str] = field(default_factory=list[str])
    user_id: str = field(default_factory=str)
    speaker_type: str = field(default_factory=str)
    clone_details: CloneDetails = field(default=None)

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

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_speaker_type(self):
        return self.speaker_type

    def set_speaker_type(self, speaker_type):
        self.speaker_type = speaker_type

    def get_clone_details(self):
        return self.clone_details

    def set_clone_details(self, clone_details):
        self.clone_details = clone_details

    def set_clone_details_from_JSON(self, clone_details_JSON):
        if clone_details_JSON is None:
            self.clone_details = None
        else:
            auto_condition_link = clone_details_JSON.get("auto_condition_link", "")
            clone_details = CloneDetails(auto_condition_link=auto_condition_link)
            self.clone_details = clone_details

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
