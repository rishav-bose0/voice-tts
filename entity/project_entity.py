import json
from dataclasses import dataclass
from dataclasses import field

from common.entity.base_entity import BaseEntity
from common.utils.rzp_id import RzpID


@dataclass
class ProjectEntity(BaseEntity):
    name: str = field(default_factory=str)
    user_id: str = field(default_factory=str)

    def get_id(self):
        return self.id

    def set_id(self, rzp_id):
        self.id = rzp_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def initialize(self):
        p_id = RzpID()
        p_id.create()
        self.id = p_id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
