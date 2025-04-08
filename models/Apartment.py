class Apartment:
    def __init__(self, owner, location, rooms, has_mamad, price, accepted_regions):
        self.owner = owner
        self.location = location
        self.rooms = rooms
        self.has_mamad = has_mamad
        self.price = price
        self.accepted_regions = accepted_regions
        self.is_available = True

    def __str__(self):
        return (f"Apartment in {self.location}, {self.rooms} rooms, "
                f"Safe Room: {'Yes' if self.has_mamad else 'No'}, "
                f"Price: {self.price}, Available for: {', '.join(self.accepted_regions)}")
