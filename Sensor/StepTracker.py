from StubStepSensor import StepSensor

class StepTracker:

    def __init__(self, sensor: StepSensor, goal: int = 10000):
        self.sensor = sensor
        self.goal = goal

    def get_current_steps(self):
        return self.sensor.read_steps()

    def get_goal(self):
        return self.goal

    def steps_to_go(self):
        return max(self.goal - self.get_current_steps(), 0)