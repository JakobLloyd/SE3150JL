class Tram:
    def __init__(self, stops=None, location=1, direction="North", door_state="Locked"):
        if location < 1 or location > 1000:
            raise ValueError("location must be between 1 and 1000")
        self.stops = list(stops or [1, 500, 1000])
        self.location = location
        self.direction = direction
        self.door_state = door_state
        self.in_motion = False

    def start(self):
        self.in_motion = True

    def open(self):
        if self.door_state == "Unlocked":
            self.door_state = "Open"

    def emergency_stop(self):
        self.in_motion = False
        self.door_state = "Unlocked"

    def get_location(self):
        return self.location

    def move(self):
        if not self.in_motion or self.door_state != "Locked":
            return
        index = self.stops.index(self.location)
        if self.direction == "North":
            if index == len(self.stops) - 1:
                self.direction = "South"
                index -= 1
            else:
                index += 1
        else:
            if index == 0:
                self.direction = "North"
                index += 1
            else:
                index -= 1
        self.location = self.stops[index]
        self.in_motion = False
