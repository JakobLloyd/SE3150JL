class TramFleet:
    def __init__(self):
        self._trams = {}

    def add(self, name, tram):
        self._trams[name] = tram

    def get(self, name):
        return self._trams[name]


class Tram:
    def __init__(self, stops=None, location=1, direction="North", door_state="Locked", stop_time=5, loop=False, current_speed=0, departure_speed=20, intended_speed=0):
        if location < 1 or location > 1000:
            raise ValueError("location must be between 1 and 1000")
        self.stops = list(stops) if stops is not None else [1, 500, 1000]
        self.location = location
        self.direction = direction
        self.door_state = door_state
        self.in_motion = False
        self.emergency = False
        self.stop_time = stop_time
        self.loop = loop
        self.current_speed = current_speed
        self.departure_speed = departure_speed
        self.intended_speed = intended_speed
        self.brakes = False
        self.message = ""

    def start(self):
        self.in_motion = True
        self.intended_speed = self.departure_speed

    def open(self):
        if self.door_state == "Unlocked":
            self.door_state = "Open"

    def emergency_stop(self):
        self.in_motion = False
        self.door_state = "Unlocked"
        self.emergency = True
        self.brakes = True

    def force_open_doors(self):
        self.door_state = "Open"
        self.emergency = True

    def remote_emergency(self):
        self.emergency_stop()

    def update_brakes(self):
        self.brakes = self.intended_speed < self.current_speed

    def get_location(self):
        return self.location

    def remove_stop(self, stop):
        self.stops.remove(stop)

    def arrive(self):
        self.in_motion = False
        self.current_speed = 0
        self.door_state = "Open"
        self.message = "Arriving at station"

    def lock_doors(self):
        if self.door_state == "Closed":
            self.door_state = "Locked"

    def begin_reset(self):
        self.reset = True

    def close(self):
        if self.door_state == "Open" and self.reset:
            self.door_state = "Closed"

    def move(self):
        if not self.in_motion or self.door_state != "Locked":
            return
        index = self.stops.index(self.location)
        if self.direction == "North":
            if index == len(self.stops) - 1:
                if self.loop:
                    self.location = self.stops[0]
                    self.in_motion = False
                    return
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
