from .base import BaseSchema


class UserSchema(BaseSchema):
    name: str
    contact: str
