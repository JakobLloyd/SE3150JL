class StepSensor:
    
    # Represents a simple step sensor.
    # Pretend that this is actually talking to hardware.
    
    def __init__(self):
        self._steps = 0

    def read_steps(self):
        return self._steps

    def simulate_steps(self, steps: int):
        self._steps += steps