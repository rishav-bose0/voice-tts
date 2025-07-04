import json
from dataclasses import dataclass, field

from common.utils.rzp_id import RzpID


@dataclass
class BaseEntity:
    id: RzpID = field(default_factory=RzpID)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
