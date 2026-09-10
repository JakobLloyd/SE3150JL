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
        }
