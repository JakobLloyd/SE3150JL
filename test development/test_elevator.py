import pytest

from Elevator import Elevator


def describe_elevator():
    def it_starts_on_floor_one():
        assert Elevator().floor == 1
