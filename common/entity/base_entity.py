from dataclasses import dataclass, field

from common.utils.rzp_id import RzpID


@dataclass
class BaseEntity:
    id: RzpID = field(default_factory=lambda: RzpID())
