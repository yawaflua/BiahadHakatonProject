class Apartment:
    def __init__(self, 
                 name: str,
                 contactData: str,
                 apartamentAddress: str,
                 roomsCount: int,
                 whereIsBombShelter: str,
                 costs: str
                 ):
        self.whereIsBombShelter = whereIsBombShelter
        self.roomsCount = roomsCount
        self.apartamentAddress = apartamentAddress
        self.contactData = contactData
        self.name = name
        self.costs = costs
