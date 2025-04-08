from .user import UserSchema


class NeedySchema(UserSchema):
    region: str
    how_much_peoples: int
