from math import sqrt
from Equation import Equation
from typing import List
from decimal import Decimal


ERROR = 0.0000001
GOLDEN_RATIO = Decimal(sqrt(5) - 1) / 2
MAX_ITERATION = 100000


def golden_section(equation: Equation, vars_form: List[str], 
                   lower_bound: float, upper_bound: float, p: list, vector: list) -> Decimal:
    a = Decimal(lower_bound)
    b = Decimal(upper_bound)
    func = equation.eval_normal_form
    total_var = len(vars_form)
    d = GOLDEN_RATIO * (b - a)
    x1 = a + d
    x2 = b - d
    count_iter = 0

    while abs(x1 - x2) > ERROR and count_iter < MAX_ITERATION:
        parameter_list = []
        for i in range(total_var):
            parameter_list.append(p[i] + x1 * vector[i])

        vars_dict = build_var_dict(vars_form, parameter_list)
        f1 = func(vars_dict)
        parameter_list = []
        for i in range(total_var):
            parameter_list.append(p[i] + x2 * vector[i])

        vars_dict = build_var_dict(vars_form, parameter_list)
        f2 = func(vars_dict)

        if f1 < f2:
            a = x2

        else:
            b = x1

        d = GOLDEN_RATIO * (b - a)
        x1 = a + d
        x2 = b - d
        count_iter += 1

    return x1


def build_var_dict(vars_form: List[str], vars_value: List[Decimal]):
    vars_dict = {}
    for i in range(len(vars_value)):
        vars_dict[vars_form[i]] = vars_value[i]

    return vars_dict


if __name__ == '__main__':
    pass
