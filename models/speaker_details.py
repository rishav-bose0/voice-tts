from sqlalchemy.dialects.postgresql import ARRAY

from common.model import db
from common.model import base
from common.utils.rzp_id import RzpID
from entity import speaker_entity


class SpeakerDetails(base.Base, db.Model):
    __tablename__ = "speaker_details"
    id = db.Column(db.String(14), primary_key=True)
    pretrained_link = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    emotions = db.Column(ARRAY(db.String), nullable=True)

    def __init__(self, entity: speaker_entity.SpeakerEntity):
        """
        constructor with SpeakerEntity as param
        :param entity:
        """
        super().__init__()
        self.id = entity.get_id().value()
        self.name = entity.get_name()
        self.pretrained_link = entity.get_pretrained_link()
        self.language = entity.get_language()
        self.emotions = entity.get_emotions()

    def to_entity(self) -> speaker_entity.SpeakerEntity:
        """
        converts database model to ocr_entity
        :return: speaker_entity.SpeakerEntity
        """
        entity = speaker_entity.SpeakerEntity()
        rzp_id = RzpID(id=self.id)
        entity.set_id(rzp_id)
        entity.set_name(self.name)
        entity.set_pretrained_link(self.pretrained_link)
        entity.set_language(self.language)
        entity.set_emotions(self.emotions)
        return entity

    def update_data(self, speaker_detail):
        self.name = speaker_detail.name
        self.pretrained_link = speaker_detail.pretrained_link
        self.language = speaker_detail.language
        self.emotions = speaker_detail.emotions
