from common.entity.base_entity import BaseEntity
from dataclasses import dataclass
from dataclasses import field

from common.utils.rzp_id import RzpID


@dataclass
class UserEntity(BaseEntity):
    email: str = field(default_factory=str)
    privilege_type: str = field(default_factory=str)

    def get_id(self):
        return self.id

    def set_id(self, rzp_id):
        self.id = rzp_id

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_privilege_type(self):
        return self.privilege_type

    def set_privilege_type(self, privilege_type):
        self.privilege_type = privilege_type

    def initialize(self):
        p_id = RzpID()
        p_id.create()
        self.id = p_id

    def to_JSON(self):
        return self.__dict__
