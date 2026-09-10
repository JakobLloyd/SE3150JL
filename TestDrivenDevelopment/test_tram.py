import pytest

from Tram import Tram


def describe_tram():
    def it_moves_one_station_north():
        tram = Tram(stops=[1, 500, 1000], location=1, direction="North")
        tram.start()
        tram.move()
        assert tram.location == 500

    def it_moves_one_station_south():
        tram = Tram(stops=[1, 500, 1000], location=1000, direction="South")
        tram.start()
        tram.move()
        assert tram.location == 500

    def it_reverses_at_the_north_end_before_moving():
        tram = Tram(stops=[1, 500, 1000], location=1000, direction="North")
        tram.start()
        tram.move()
        assert tram.direction == "South"
        assert tram.location == 500

    def it_reverses_at_the_south_end_before_moving():
        tram = Tram(stops=[1, 500, 1000], location=1, direction="South")
        tram.start()
        tram.move()
        assert tram.direction == "North"
        assert tram.location == 500

    def it_does_not_open_locked_doors():
        tram = Tram()
        tram.open()
        assert tram.door_state == "Locked"

    def it_does_not_close_locked_doors():
        tram = Tram()
        tram.close()
        assert tram.door_state == "Locked"

    def it_requires_locked_doors_before_moving():
        tram = Tram(door_state="Open")
        tram.start()
        tram.move()
        assert tram.location == 1

    def it_stops_and_unlocks_doors_when_emergency_is_pressed():
        tram = Tram()
        tram.start()
        tram.emergency_stop()
        assert tram.in_motion is False
        assert tram.door_state == "Unlocked"

    def it_opens_unlocked_doors():
        tram = Tram(door_state="Unlocked")
        tram.open()
        assert tram.door_state == "Open"

    def it_closes_open_doors_during_reset():
        tram = Tram(door_state="Open")
        tram.begin_reset()
        tram.close()
        assert tram.door_state == "Closed"

    def it_reports_a_valid_location():
        assert Tram(location=500).get_location() == 500

    def it_rejects_an_invalid_location():
        with pytest.raises(ValueError):
            Tram(location=1001)

    def it_moves_to_the_next_station_after_emergency_reset():
        tram = Tram(stops=[1, 500, 1000], location=500, direction="North")
        tram.emergency_stop()
        tram.begin_reset()
        tram.door_state = "Closed"
        tram.reset_system()
        tram.move()
        assert tram.location == 1000

    def it_always_stops_at_a_station():
        tram = Tram(stops=[1, 500, 1000], location=1)
        tram.start()
        tram.move()
        assert tram.location in tram.stops
        assert tram.in_motion is False

    def it_uses_the_configured_station_stop_time():
        tram = Tram(stop_time=7)
        assert tram.stop_time == 7

    def it_opens_doors_at_a_station():
        tram = Tram(door_state="Locked")
        tram.arrive()
        assert tram.door_state == "Open"

    def it_locks_doors_before_departure():
        tram = Tram(door_state="Open")
        tram.door_state = "Closed"
        tram.lock_doors()
        tram.start()
        assert tram.door_state == "Locked"

    def it_enters_emergency_when_doors_are_forced_open():
        tram = Tram()
        tram.force_open_doors()
        assert tram.emergency is True

    def it_exposes_reset_on_the_console():
        tram = Tram()
        assert callable(tram.console.reset)

    def it_resets_only_after_all_doors_are_closed():
        tram = Tram(door_state="Open")
        tram.emergency_stop()
        tram.begin_reset()
        tram.reset_system()
        assert tram.emergency is True

    def it_accepts_a_configured_list_of_stops():
        assert Tram(stops=[2, 8, 20]).stops == [2, 8, 20]

    def it_removes_a_configured_stop():
        tram = Tram(stops=[1, 500, 1000])
        tram.remove_stop(500)
        assert tram.stops == [1, 1000]

    def it_arrives_at_zero_speed():
        tram = Tram(current_speed=40)
        tram.arrive()
        assert tram.current_speed == 0

    def it_departures_at_the_configured_speed():
        tram = Tram(departure_speed=30)
        tram.start()
        assert tram.intended_speed == 30

    def it_sets_an_arrival_message():
        tram = Tram()
        tram.arrive()
        assert tram.message == "Arriving at station"

    def it_engages_brakes_when_speed_must_decrease():
        tram = Tram(current_speed=40, intended_speed=20)
        tram.update_brakes()
        assert tram.brakes is True

    def it_engages_brakes_in_an_emergency():
        tram = Tram()
        tram.emergency_stop()
        assert tram.brakes is True

    def it_tests_brakes_during_reset():
        tram = Tram()
        tram.begin_reset()
        assert tram.brakes is True

    def it_can_receive_a_remote_emergency_signal():
        tram = Tram()
        tram.remote_emergency()
        assert tram.emergency is True

    def it_allows_the_operator_to_start_and_stop_manually():
        tram = Tram()
        tram.manual_start()
        assert tram.in_motion is True
        tram.manual_stop()
        assert tram.in_motion is False

    def it_allows_the_operator_to_control_doors():
        tram = Tram(door_state="Unlocked")
        tram.console.open_doors()
        assert tram.door_state == "Open"
        tram.begin_reset()
        tram.console.close_doors()
        assert tram.door_state == "Closed"

    def it_allows_the_operator_to_reset_the_system():
        tram = Tram()
        tram.console.reset()
        assert tram.reset is True

    def it_activates_emergency_when_manual_override_is_used():
        tram = Tram()
        tram.manual_override()
        assert tram.emergency is True
