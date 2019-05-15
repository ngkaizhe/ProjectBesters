from typing import List
from math import exp


class TestingEquation(object):
    def __init__(self):
        pass

    @staticmethod
    def compute(input_vals: List[float]) -> float:
        assert len(input_vals) == 1
        x = input_vals[0]
        return x**6 + 7*x**5 - exp(x)
