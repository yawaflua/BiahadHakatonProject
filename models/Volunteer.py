from models.User import User


class Volunteer(User):
    def __init__(self, name, contact):
        super().__init__(name, contact)
        self.apartments = []
