class Console:
    def __init__(self, tram):
        self._tram = tram

    def open_doors(self):
        self._tram.open()

    def close_doors(self):
        self._tram.close()

    def reset(self):
        self._tram.begin_reset()


class Tram:
    def __init__(self, stops=None, location=1, direction="North", door_state="Locked",
                 current_speed=0, intended_speed=0, stop_time=5, departure_speed=20,
                 loop=False):
        if not 1 <= location <= 1000:
            raise ValueError("location must be between 1 and 1000")
        self.stops = list(stops or [1, 500, 1000])
        self.location = location
        self.direction = direction
        self.door_state = door_state
        self.in_motion = False
        self.emergency = False
        self.reset = False
        self.current_speed = current_speed
        self.intended_speed = intended_speed
        self.stop_time = stop_time
        self.departure_speed = departure_speed
        self.loop = loop
        self.message = ""
        self.brakes = False
        self.console = Console(self)

    def remove_stop(self, stop):
        self.stops.remove(stop)

    def get_location(self):
        if not 1 <= self.location <= 1000:
            raise ValueError("location is out of bounds")
        return self.location

    def move(self):
        if self.door_state != "Locked" or self.emergency or not self.in_motion:
            return
        index = self.stops.index(self.location)
        step = 1 if self.direction == "North" else -1
        next_index = index + step
        if next_index not in range(len(self.stops)) and self.loop:
            next_index %= len(self.stops)
        elif next_index not in range(len(self.stops)):
            self.direction = "South" if step == 1 else "North"
            step *= -1
            next_index = index + step
        self.location = self.stops[next_index]
        self.in_motion = False
        self.current_speed = 0

    def start(self):
        if self.door_state == "Closed":
            self.lock_doors()
        if self.door_state == "Locked" and not self.emergency:
            self.in_motion = True
            self.intended_speed = self.departure_speed

    def stop(self):
        self.in_motion = False
        self.current_speed = 0

    def manual_start(self):
        self.start()

    def manual_stop(self):
        self.stop()

    def open(self):
        if self.door_state != "Locked":
            self.door_state = "Open"

    def close(self):
        if self.door_state == "Open" and self.reset:
            self.door_state = "Closed"

    def lock_doors(self):
        if self.door_state == "Closed":
            self.door_state = "Locked"

    def arrive(self):
        self.stop()
        self.door_state = "Open"
        self.message = "Arriving at station"

    def emergency_stop(self):
        self.emergency = True
        self.stop()
        self.door_state = "Unlocked"
        self.brakes = True

    def remote_emergency(self):
        self.emergency_stop()

    def force_open_doors(self):
        self.door_state = "Open"
        self.emergency = True

    def begin_reset(self):
        self.reset = True
        self.brakes = True

    def reset_system(self):
        if self.reset and self.door_state in {"Closed", "Locked"}:
            self.emergency = False
            self.brakes = False
            self.start()

    def update_brakes(self):
        self.brakes = self.intended_speed < self.current_speed

    def manual_override(self):
        self.emergency_stop()
