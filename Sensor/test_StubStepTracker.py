from StubStepSensor import StepSensor
from StepTracker import StepTracker

def describe_step_tracker():

    def describe_get_current_steps():

        def it_calls_read_steps_on_sensor():
            sensor = StepSensor()
            tracker = StepTracker(sensor, goal=5000)

            result = tracker.get_current_steps()

            assert result == 2000