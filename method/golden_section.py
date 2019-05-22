from math import sqrt
from Equation import Equation
from typing import List
from decimal import Decimal


ERROR = 0.0000001
GOLDEN_RATIO = Decimal(sqrt(5) - 1) / 2
MAX_ITERATION = 100000


def golden_section(equation: Equation, vars_form: List[str], 
                   lower_bound: float, upper_bound: float, p: list, vector: list) -> Decimal:
    func = equation.eval_normal_form
    
    var_count = len(vars_form)
    a = Decimal(lower_bound)
    b = Decimal(upper_bound)
    d = GOLDEN_RATIO * (b - a)
    x = [a + d, b - d]
    count_iter = 0

    while abs(x[0] - x[1]) > ERROR and count_iter < MAX_ITERATION:
        f = []
        for i_x in range(2):
            parameter_list = []
            for i in range(var_count):
                parameter_list.append(p[i] + x[i_x] * vector[i])

            vars_dict = build_var_dict(vars_form, parameter_list)
            f.append(func(vars_dict))

        if f[0] < f[1]:
            a = x[1]

        else:
            b = x[0]

        d = GOLDEN_RATIO * (b - a)
        x = [a + d, b - d]
        count_iter += 1

    return x[0]


def build_var_dict(vars_form: List[str], vars_value: List[Decimal]):
    vars_dict = {}
    for i in range(len(vars_value)):
        vars_dict[vars_form[i]] = vars_value[i]

    return vars_dict


if __name__ == '__main__':
    pass
