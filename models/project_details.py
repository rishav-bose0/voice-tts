from common.model import base
from common.model import db
from entity import project_entity
from models.tts_details import TTSDetails


class ProjectDetails(base.Base, db.Model):
    __tablename__ = "project_details"
    id = db.Column(db.String(14), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(14), db.ForeignKey('user_details.id'), nullable=False)

    # tts_details = db.relationship('TTSDetails', backref=backref('project_details'), lazy=True)

    def __init__(self, entity: project_entity.ProjectEntity):
        """
        constructor with ProjectEntity as param
        @param entity:
        """
        super().__init__()
        self.id = entity.get_id().value()
        self.name = entity.get_name()
        self.user_id = entity.get_user_id()

    def to_entity(self) -> project_entity.ProjectEntity:
        """
        converts database model to project_entity
        :return: project_entity.ProjectEntity
        """
        entity = project_entity.ProjectEntity()
        entity.set_id(self.id)
        entity.set_name(self.name)
        entity.set_user_id(self.user_id)
        return entity

    def update_data(self, project_detail):
        self.name = project_detail.name

    def get_tts_details_history(self) -> TTSDetails:
        return self.tts_details
