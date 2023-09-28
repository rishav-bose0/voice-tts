from sqlalchemy.dialects.postgresql import ARRAY

from common.model import db
from common.model import base
from common.utils.rzp_id import RzpID
from entity import user_entity


class UserDetails(base.Base, db.Model):
    __tablename__ = "user_details"
    id = db.Column(db.String(14), primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    privilege_type = db.Column(db.String(50), nullable=False)

    def __init__(self, entity: user_entity.UserEntity):
        """
        constructor with UserEntity as param
        :param entity:
        """
        super().__init__()
        self.id = entity.get_id().value()
        self.email = entity.get_email()
        self.privilege_type = entity.get_privilege_type()

    def to_entity(self) -> user_entity.UserEntity:
        """
        converts database model to ocr_entity
        :return: user_entity.UserEntity
        """
        entity = user_entity.UserEntity()
        rzp_id = RzpID(id=self.id)
        entity.set_id(rzp_id)
        entity.set_email(self.email)
        entity.set_privilege_type(self.privilege_type)
        return entity

    def update_data(self, user_detail):
        self.email = user_detail.email
        self.privilege_type = user_detail.privilege_type
