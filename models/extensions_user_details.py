from common.model import base
from common.model import db
from common.utils.rzp_id import RzpID
from entity import extensions_user_entity


class ExtensionsUserDetails(base.Base, db.Model):
    __tablename__ = "extensions_user_details"
    id = db.Column(db.String(14), primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    email_id = db.Column(db.String(100), nullable=False)

    def __init__(self, entity: extensions_user_entity.ExtensionsUserEntity):
        """
        constructor with extensions_user_entity as param
        @param entity:
        """
        super().__init__()
        self.id = entity.get_id().value()
        self.email_id = entity.get_email_id()
        self.email = entity.get_email()

    def to_entity(self) -> extensions_user_entity.ExtensionsUserEntity:
        """
        converts database model to user_entity
        :return: extensions_user_entity.ExtensionsUserEntity
        """
        entity = extensions_user_entity.ExtensionsUserEntity()
        rzp_id = RzpID(id=self.id)
        entity.set_id(rzp_id)
        entity.set_email(self.email)
        entity.set_email_id(self.email_id)
        return entity
