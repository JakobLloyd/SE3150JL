import pytest

from Elevator import Elevator


def describe_elevator():
    def it_starts_on_floor_one():
        assert Elevator().floor == 1

    def it_starts_idle():
        assert Elevator().direction == "Idle"

    def it_starts_with_closed_doors():
        assert Elevator().doors == "Closed"

    def it_reports_its_state():
        assert Elevator().state() == {
            "floor": 1,
            "direction": "Idle",
            "doors": "Closed",
            "passengers": 0,
            "emergency": False,
        }

    def it_accepts_a_valid_destination():
        elevator = Elevator()
        elevator.request(3)
        assert elevator.destinations == [3]

    def it_ignores_the_current_floor():
        elevator = Elevator()
        elevator.request(1)
        assert elevator.destinations == []

    def it_moves_up_one_floor_per_step():
        elevator = Elevator()
        elevator.request(3)
        elevator.step()
        assert elevator.floor == 2

    def it_stops_at_its_destination():
        elevator = Elevator()
        elevator.request(2)
        elevator.step()
        assert elevator.floor == 2
        assert elevator.direction == "Idle"
