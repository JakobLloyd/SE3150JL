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

    def it_opens_unlocked_doors():
        tram = Tram()
        tram.door_state = "Unlocked"
        tram.open()
        assert tram.door_state == "Open"

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

    def it_reports_a_valid_location():
        assert Tram(location=500).get_location() == 500

    def it_rejects_an_invalid_location():
        with pytest.raises(ValueError):
            Tram(location=1001)

    def it_uses_the_configured_station_stop_time():
        tram = Tram(stop_time=7)
        assert tram.stop_time == 7

    def it_accepts_a_configured_list_of_stops():
        assert Tram(stops=[2, 8, 20]).stops == [2, 8, 20]
