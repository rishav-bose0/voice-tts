from sqlalchemy.dialects.postgresql import ARRAY

from common.model import db
from common.model import base
from entity import speaker_entity


class SpeakerDetails(base.Base, db.Model):
    __tablename__ = "speaker_details"
    id = db.Column(db.String(14), primary_key=True)
    model_name = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    emotions = db.Column(ARRAY(db.String), nullable=True)

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
        self.gender = entity.get_gender()
        self.emotions = entity.get_emotions()

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
        entity.set_emotions(self.emotions)
        return entity

    def update_data(self, speaker_detail):
        self.name = speaker_detail.name
        self.model_name = speaker_detail.model_name
        self.language = speaker_detail.language
        self.emotions = speaker_detail.emotions
