from enum import Enum

"""
explosion.py

This is the exception class for method

"""


class Explosion(Enum):
    NODE_POW_OP_POWER_TO_NON_CONST_NOT_SUPPORTED = \
        ValueError('Sorry! the power up to non constant term are not supported yet')
    EQUATION_BUILD_TREE_MISMATCHED_OPERAND = \
        ValueError('The operand is insufficient')
    EQUATION_BUILD_TREE_UNSUPPORTED_TYPE = \
        ValueError('The operation is currently not supported yet')
    POWELL_LENGTH_INTERVAL_INITIAL_POINT_NOT_SAME_AS_INPUT_EQUATION = \
        ValueError('The initial point and interval doesnt have the '
                   'same length as the total variables detect in input equation!')
    POWELL_LENGTH_INTERVAL_MUST_BE_ONLY_TWO = \
        ValueError('The length of interval should only be 2 as for upper bound and lower bound')
    NEWTON_LENGTH_INTERVAL_MUST_BE_ONLY_TWO = \
        ValueError('The initial point doesnt have the same length as the total variables detect in input equation!')
    STEEP_DESCENT_LENGTH_INTERVAL_INITIAL_POINT_NOT_SAME_AS_INPUT_EQUATION = \
        ValueError('The initial point and interval doesnt have the '
                   'same length as the total variables detect in input equation!')
    STEEP_DESCENT_LENGTH_INTERVAL_MUST_BE_ONLY_TWO = \
        ValueError('The length of interval should only be 2 as for upper bound and lower bound')

    def bang(self, msg=""):
        self.value.args = (self.value.args[0] +'\n' +msg,)
        raise self.value
