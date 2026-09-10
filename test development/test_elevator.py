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

    def it_opens_doors_at_a_destination():
        elevator = Elevator()
        elevator.request(2)
        elevator.step()
        assert elevator.doors == "Open"

    def it_closes_doors_before_moving():
        elevator = Elevator()
        elevator.open_doors()
        elevator.request(2)
        elevator.step()
        assert elevator.doors == "Closed"

    def it_ignores_duplicate_destinations():
        elevator = Elevator()
        elevator.request(2)
        elevator.request(2)
        assert elevator.destinations == [2]

    def it_rejects_a_floor_below_one():
        with pytest.raises(ValueError):
            Elevator().request(0)

    def it_rejects_a_floor_above_three():
        with pytest.raises(ValueError):
            Elevator().request(4)

    def it_accepts_passengers_when_doors_are_open():
        elevator = Elevator()
        elevator.open_doors()
        elevator.board(2)
        assert elevator.passengers == 2

    def it_rejects_over_capacity_boarding():
        elevator = Elevator(capacity=2)
        elevator.open_doors()
        with pytest.raises(ValueError):
            elevator.board(3)

    def it_rejects_negative_boarding_counts():
        elevator = Elevator()
        elevator.open_doors()
        with pytest.raises(ValueError):
            elevator.board(-1)

    def it_allows_passengers_to_leave_with_open_doors():
        elevator = Elevator()
        elevator.open_doors()
        elevator.board(2)
        elevator.exit(1)
        assert elevator.passengers == 1

    def it_cannot_move_when_overloaded():
        elevator = Elevator(capacity=1)
        elevator.open_doors()
        elevator.board(1)
        elevator.passengers = 2
        elevator.close_doors()
        elevator.request(2)
        elevator.step()
        assert elevator.floor == 1

    def it_enters_emergency_mode():
        elevator = Elevator()
        elevator.emergency_stop()
        assert elevator.emergency is True

    def it_opens_doors_when_emergency_is_idle():
        elevator = Elevator()
        elevator.emergency_stop()
        assert elevator.doors == "Open"

    def it_rejects_destinations_during_emergency():
        elevator = Elevator()
        elevator.emergency_stop()
        with pytest.raises(RuntimeError):
            elevator.request(2)

    def it_resets_emergency_when_stopped():
        elevator = Elevator()
        elevator.emergency_stop()
        elevator.reset()
        assert elevator.emergency is False

    def it_reports_when_full():
        elevator = Elevator(capacity=2)
        elevator.open_doors()
        elevator.board(2)
        assert elevator.is_full() is True

    def it_reports_when_idle():
        assert Elevator().is_idle() is True

    def it_accepts_a_valid_starting_floor():
        assert Elevator(floor=3).floor == 3
