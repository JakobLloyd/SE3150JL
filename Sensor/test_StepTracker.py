from StepTracker import StepTracker
from StepSensor import StepSensor


def describe_step_tracker():

    def describe_get_current_steps():

        def it_calls_read_steps_on_sensor(mocker):
            sensor = StepSensor()
            tracker = StepTracker(sensor, goal=5000)

            mock_read = mocker.patch.object(sensor, "read_steps", return_value=1200)

            # Call the method under test
            result = tracker.get_current_steps()

            assert result == 1200

            mock_read.assert_called_once()

    def describe_steps_to_go():

        def it_returns_remaining_steps(mocker):
            sensor = StepSensor()
            tracker = StepTracker(sensor, goal=5000)

            mocker.patch.object(sensor, "read_steps", return_value=1000)

            assert tracker.steps_to_go() == 4000

        def it_returns_zero_if_goal_reached(mocker):
            sensor = StepSensor()
            tracker = StepTracker(sensor, goal=5000)

            mocker.patch.object(sensor, "read_steps", return_value=6000)

            assert tracker.steps_to_go() == 0

    def describe_get_goal():

        def it_returns_the_set_goal():
            sensor = StepSensor()
            tracker = StepTracker(sensor, goal=5000)

            assert tracker.get_goal() == 5000