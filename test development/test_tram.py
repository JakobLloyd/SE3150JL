import pytest

from Tram import Tram


def describe_tram():
    def it_moves_one_station_north():
        tram = Tram(stops=[1, 500, 1000], location=1, direction="North")
        tram.start()
        tram.move()
        assert tram.location == 500
