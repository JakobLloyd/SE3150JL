class Elevator:
    def __init__(self):
        self.floor = 1
        self.direction = "Idle"
        self.doors = "Closed"
        self.destinations = []

    def state(self):
        return {
            "floor": self.floor,
            "direction": self.direction,
            "doors": self.doors,
        }

    def request(self, floor):
        if floor != self.floor:
            self.destinations.append(floor)
