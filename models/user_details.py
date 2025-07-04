from common.model import base
from common.model import db
from common.utils.rzp_id import RzpID
from entity import user_entity


class UserDetails(base.Base, db.Model):
    __tablename__ = "user_details"
    id = db.Column(db.String(14), primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=True)
    token = db.Column(db.String(2000), nullable=False)
    privilege_type = db.Column(db.String(50), nullable=False)

    def __init__(self, entity: user_entity.UserEntity):
        """
        constructor with UserEntity as param
        @param entity:
        """
        super().__init__()
        self.id = entity.get_id().value()
        self.first_name = entity.get_first_name()
        self.last_name = entity.get_last_name()
        self.email = entity.get_email()
        self.password = entity.get_password()
        self.token = entity.get_token()
        self.privilege_type = entity.get_privilege_type()

    def to_entity(self) -> user_entity.UserEntity:
        """
        converts database model to user_entity
        :return: user_entity.UserEntity
        """
        entity = user_entity.UserEntity()
        rzp_id = RzpID(id=self.id)
        entity.set_id(rzp_id)
        entity.set_email(self.email)
        entity.set_first_name(self.first_name)
        entity.set_last_name(self.last_name)
        entity.set_password(self.password)
        entity.set_token(self.token)
        entity.set_privilege_type(self.privilege_type)
        return entity

    def update_data(self, user_detail):
        self.first_name = self.first_name if user_detail.first_name is None else user_detail.first_name
        self.last_name = self.last_name if user_detail.last_name is None else user_detail.last_name
        self.password = self.password if user_detail.password is None else user_detail.password
        self.privilege_type = self.privilege_type if user_detail.privilege_type is None else user_detail.privilege_type
        self.token = self.token if user_detail.token is None else user_detail.token
