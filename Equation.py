from autodiff import Node
from autodiff import (AddOp, SubOp, MulOp, DivOp, PowOp, SinOp, CosOp)
from typing import List


class Equation(object):
    def __init__(self, equation: str)-> None:
        pass

    # Ex: z = x+y
    # dz/dx = [1,0]
    # dz/dy = [0,1]
    def get_diff_form(self, diff_parts: List[int]) -> str:
        pass

    def get_compute(self, input_vals: List[int]) -> float:
        pass

    def get_normal_form(self) -> str:
        pass

