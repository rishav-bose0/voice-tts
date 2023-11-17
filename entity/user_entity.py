import json
from dataclasses import dataclass
from dataclasses import field

from common.entity.base_entity import BaseEntity
from common.utils.rzp_id import RzpID


@dataclass
class UserEntity(BaseEntity):
    email: str = field(default_factory=str)
    privilege_type: str = field(default_factory=str)
    first_name: str = field(default_factory=str)
    last_name: str = field(default_factory=str)
    password: str = field(default_factory=str)
    token: str = field(default_factory=str)

    def get_id(self):
        return self.id

    def set_id(self, rzp_id):
        self.id = rzp_id

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_first_name(self):
        return self.first_name

    def set_first_name(self, first_name):
        self.first_name = first_name

    def get_last_name(self):
        return self.last_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token

    def get_privilege_type(self):
        return self.privilege_type

    def set_privilege_type(self, privilege_type):
        self.privilege_type = privilege_type

    def initialize(self):
        p_id = RzpID()
        p_id.create()
        self.id = p_id

    def is_empty(self):
        return (not self.email and self.email == "") or (not self.first_name and self.first_name == "") or \
            (not self.last_name and self.last_name == "") or (not self.password and self.password == "")

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
