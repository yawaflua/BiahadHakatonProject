from .base import BaseSchema
from typing import List


class ApartmentSchema(BaseSchema):
    owner: str
    location: str
    rooms: int
    has_mamad: str
    price: str
    accepted_regions: str
    is_available: bool = True
