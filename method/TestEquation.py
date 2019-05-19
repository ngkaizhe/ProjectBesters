from typing import List
from math import exp, sin , cos, sqrt


class TestingEquation(object):
    def __init__(self, equation_form: str):
        self.total_var = 2
        pass

    def compute(self, input_vals: List[float]) -> float:
        assert len(input_vals) == self.total_var
        x = input_vals[0]
        y = 0
        if self.total_var == 2:
            y = input_vals[1]
        return 7 + x**2 - 3*x*y + 3.25*y**2 - 4*y
