import json
from dataclasses import dataclass
from dataclasses import field

from common.entity.base_entity import BaseEntity
from common.utils.rzp_id import RzpID


@dataclass
class ExtensionsUserEntity(BaseEntity):
    email: str = field(default_factory=str)
    email_id: str = field(default_factory=str)

    def initialize(self):
        p_id = RzpID()
        p_id.create()
        self.id = p_id

    def get_id(self):
        return self.id

    def set_id(self, rzp_id):
        self.id = rzp_id

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_email_id(self):
        return self.email_id

    def set_email_id(self, email_id):
        self.email_id = email_id

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
