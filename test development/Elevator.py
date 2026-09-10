class Elevator:
    def __init__(self):
        self.floor = 1
        self.direction = "Idle"
        self.doors = "Closed"
        self.destinations = []
        self.passengers = 0
        self.emergency = False

    def state(self):
        return {
            "floor": self.floor,
            "direction": self.direction,
            "doors": self.doors,
            "passengers": self.passengers,
            "emergency": self.emergency,
        }

    def request(self, floor):
        if floor != self.floor:
            self.destinations.append(floor)

    def step(self):
        if not self.destinations:
            return
        destination = self.destinations[0]
        self.direction = "Up" if destination > self.floor else "Down"
        self.floor += 1 if destination > self.floor else -1
