import json

from sqlalchemy.dialects.postgresql import ARRAY

from common.model import base
from common.model import db
from entity import speaker_entity


class SpeakerDetails(base.Base, db.Model):
    __tablename__ = "speaker_details"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(2), nullable=True)
    language = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    emotions = db.Column(ARRAY(db.String), nullable=True)
    image_link = db.Column(db.String(300), nullable=False)
    voice_preview_link = db.Column(db.String(300), nullable=True)
    user_id: str = db.Column(db.String(14), nullable=True)
    speaker_type: str = db.Column(db.String(20), nullable=False)
    clone_details = db.Column(db.JSON, nullable=True)

    def __init__(self, entity: speaker_entity.SpeakerEntity):
        """
        constructor with SpeakerEntity as param
        @param entity:
        """
        super().__init__()
        self.id = entity.get_id()
        self.name = entity.get_name()
        self.model_name = entity.get_model_name()
        self.language = entity.get_language()
        self.country = entity.get_country()
        self.gender = entity.get_gender()
        self.emotions = entity.get_emotions()
        self.image_link = entity.get_image_link()
        self.voice_preview_link = entity.get_voice_preview_link()
        self.user_id = entity.get_user_id()
        self.speaker_type = entity.get_speaker_type()
        if entity.get_clone_details() is not None:
            self.clone_details = entity.get_clone_details().to_JSON()

    def to_entity(self) -> speaker_entity.SpeakerEntity:
        """
        converts database model to speaker_entity
        :return: speaker_entity.SpeakerEntity
        """
        entity = speaker_entity.SpeakerEntity()
        entity.set_id(self.id)
        entity.set_name(self.name)
        entity.set_gender(self.gender)
        entity.set_model_name(self.model_name)
        entity.set_language(self.language)
        entity.set_country(self.country)
        entity.set_emotions(self.emotions)
        entity.set_image_link(self.image_link)
        entity.set_voice_preview_link(self.voice_preview_link)
        entity.set_user_id(self.user_id)
        entity.set_speaker_type(self.speaker_type)
        if self.clone_details is not None:
            clone_details_json = json.loads(self.clone_details)
            entity.set_clone_details_from_JSON(clone_details_json)
        return entity

    def update_data(self, speaker_detail):
        self.name = speaker_detail.name
        self.model_name = speaker_detail.model_name
        self.language = speaker_detail.language
        self.country = speaker_detail.country
        self.emotions = speaker_detail.emotions
        self.clone_details = speaker_detail.clone_details
