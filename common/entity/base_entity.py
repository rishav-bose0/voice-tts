from dataclasses import dataclass

from common.utils.rzp_id import RzpID


@dataclass
class BaseEntity:
    id: RzpID = RzpID()
