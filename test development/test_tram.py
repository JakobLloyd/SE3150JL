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
