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
        if self.direction == "North":
            self.location = self.stops[index + 1]
        else:
            self.location = self.stops[index - 1]
        self.in_motion = False
