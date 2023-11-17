import json

from common.model import base
from common.model import db
from common.utils.rzp_id import RzpID
from entity import tts_entity


class TTSDetails(base.Base, db.Model):
    __tablename__ = "tts_details"
    id = db.Column(db.String(14), primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    speech_s3_link = db.Column(db.String(400), nullable=True)
    speech_metadata = db.Column(db.JSON, nullable=True)
    block_number = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.String(14), db.ForeignKey('project_details.id'), nullable=False)

    def __init__(self, entity: tts_entity.TTSEntity):
        """
        constructor with TTSEntity as param
        @param entity:
        """
        super().__init__()
        self.id = entity.get_id().value()
        self.project_id = entity.get_project_id()
        self.text = entity.get_text()
        self.language = entity.get_language()
        self.speech_s3_link = entity.get_speech_s3_link()
        self.block_number = entity.get_block_number()
        self.speech_metadata = entity.get_speech_metadata().to_JSON()

    def to_entity(self) -> tts_entity.TTSEntity:
        """
        converts database model to tts_entity
        :return: tts_entity.TTSEntity
        """
        entity = tts_entity.TTSEntity()
        rzp_id = RzpID(id=self.id)
        entity.set_id(rzp_id)
        entity.set_project_id(self.project_id)
        entity.set_text(self.text)
        entity.set_language(self.language)
        entity.set_speech_s3_link(self.speech_s3_link)
        entity.set_block_number(self.block_number)
        speech_metadata_json = json.loads(self.speech_metadata)
        entity.set_speech_metadata_from_JSON(speech_metadata_json)
        return entity

    def update_data(self, tts_detail):
        self.project_id = tts_detail.project_id
        self.text = tts_detail.text
        self.language = tts_detail.language
        self.speech_s3_link = tts_detail.speech_s3_link
        self.speech_metadata = tts_detail.speech_metadata
