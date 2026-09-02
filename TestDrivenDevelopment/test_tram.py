import pytest-describe
import Tram

describe test_movement():
#Calling move() advances the tram exactly ne station and never moves it beyond etier end station
    def it_moves_to_a_station():
        Tram.Tram my_tram
        my_tram.in_motion = False
        my_tram.door_state = "Locked"
        my_tram.location = 1
        my_tram.direction = "North"
        my_tram.emergency = False
        my_tram.reset = False
        my_tram.current_speed = 0
        my_tram.intended_speed = 0

        my_tram.move()
        assert my_tram.location == 500

#spec -> test case -> code is the assignment