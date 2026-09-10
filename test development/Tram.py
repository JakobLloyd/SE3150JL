class Tram:
    def __init__(self, stops=None, location=1, direction="North"):
        self.stops = list(stops or [1, 500, 1000])
        self.location = location
        self.direction = direction
        self.door_state = "Locked"
        self.in_motion = False

    def start(self):
        self.in_motion = True

    def move(self):
        if not self.in_motion or self.door_state != "Locked":
            return
        index = self.stops.index(self.location)
        step = 1 if self.direction == "North" else -1
        self.location = self.stops[index + step]
        self.in_motion = False
