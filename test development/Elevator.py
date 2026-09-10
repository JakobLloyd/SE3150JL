class Elevator:
    def __init__(self):
        self.floor = 1
        self.direction = "Idle"
        self.doors = "Closed"

    def state(self):
        return {
            "floor": self.floor,
            "direction": self.direction,
            "doors": self.doors,
        }
