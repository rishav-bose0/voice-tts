from sqlalchemy.orm import backref

from common.model import db
from common.model import base
from common.utils.rzp_id import RzpID
from entity import tts_entity


class TTSDetails(base.Base, db.Model):
    __tablename__ = "tts_details"
    id = db.Column(db.String(14), primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    speech_metadata = db.Column(db.JSON, nullable=True)
    speaker_id = db.Column(db.String(14), db.ForeignKey('speaker_details.id'), nullable=False)
    user_id = db.Column(db.String(14), db.ForeignKey('user_details.id'), nullable=False)
    speaker_details = db.relationship('SpeakerDetails', backref=backref('tts_details', uselist=False))
    user_details = db.relationship('UserDetails', backref=backref('tts_details', uselist=False))

    def __init__(self, entity: tts_entity.TTSEntity):
        """
        constructor with TTSEntity as param
        :param entity:
        """
        super().__init__()
        self.id = entity.get_id().value()
        self.user_id = entity.get_user_id()
        self.speaker_id = entity.get_speaker_id()
        self.text = entity.get_text()
        self.language = entity.get_language()
        self.speech_metadata = entity.get_speech_metadata().to_JSON()

    def to_entity(self) -> tts_entity.TTSEntity:
        """
        converts database model to tts_entity
        :return: tts_entity.TTSEntity
        """
        entity = tts_entity.TTSEntity()
        rzp_id = RzpID(id=self.id)
        entity.set_id(rzp_id)
        entity.set_user_id(self.user_id)
        entity.set_text(self.text)
        entity.set_language(self.language)
        entity.set_speech_metadata_from_JSON(self.speech_metadata)
        return entity

    def update_data(self, tts_detail):
        self.user_id = tts_detail.user_id
        self.text = tts_detail.text
        self.language = tts_detail.language
        self.speech_metadata = tts_detail.speech_metadata
