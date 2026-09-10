class Elevator:
    def __init__(self, capacity=8):
        self.floor = 1
        self.direction = "Idle"
        self.doors = "Closed"
        self.destinations = []
        self.passengers = 0
        self.capacity = capacity
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
        if self.emergency:
            raise RuntimeError("elevator is in emergency mode")
        if floor != self.floor and floor not in self.destinations:
            self.destinations.append(floor)

    def step(self):
        if self.passengers > self.capacity or not self.destinations:
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

    def board(self, count=1):
        if count < 0:
            raise ValueError("passenger count cannot be negative")
        if self.doors != "Open":
            raise RuntimeError("doors must be open")
        if self.passengers + count > self.capacity:
            raise ValueError("capacity exceeded")
        self.passengers += count

    def exit(self, count=1):
        if self.doors != "Open":
            raise RuntimeError("doors must be open")
        if count < 0 or count > self.passengers:
            raise ValueError("invalid passenger count")
        self.passengers -= count

    def emergency_stop(self):
        self.emergency = True
        self.destinations.clear()
        self.direction = "Idle"
        self.doors = "Open"
