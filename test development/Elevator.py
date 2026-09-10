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
        if floor < 1 or floor > 3:
            raise ValueError("destination must be 1, 2, or 3")
        if floor != self.floor and floor not in self.destinations:
            self.destinations.append(floor)

    def step(self):
        if not self.destinations:
            return
        if self.doors == "Open":
            self.close_doors()
            return
        destination = self.destinations[0]
        self.direction = "Up" if destination > self.floor else "Down"
        self.floor += 1 if destination > self.floor else -1
        if self.floor == destination:
            self.destinations.pop(0)
            self.direction = "Idle"
            self.doors = "Open"

    def open_doors(self):
        if self.direction == "Idle":
            self.doors = "Open"

    def close_doors(self):
        self.doors = "Closed"
