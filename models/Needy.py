from models.User import User


class Needy(User):
    def __init__(self, name: str, contact: str, region: str, how_much_peoples: int):
        super().__init__(name, contact)
        self.how_much_peoples = how_much_peoples
        self.region = region
