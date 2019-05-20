from enum import Enum

"""
explosion.py

This is the exception class for method

"""


class Explosion(Enum):
    POWELL_LENGTH_INTERVAL_INITIAL_POINT_NOT_SAME_AS_INPUT_EQUATION = \
        ValueError('The initial point and interval doesnt have the same length as the total variables detect in input equation!')
    POWELL_LENGTH_INTERVAL_MUST_BE_ONLY_TWO = \
        ValueError('The length of interval should only be 2 as for upper bound and lower bound')
    NEWTON_LENGTH_INTERVAL_MUST_BE_ONLY_TWO = \
        ValueError('The initial point doesnt have the same length as the total variables detect in input equation!')

    def bang(self, msg = ""):
        self.value.args = (self.value.args[0] +'\n' + msg)
        raise self.value