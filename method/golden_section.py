from method.TestEquation import TestingEquation as Equation
from math import sqrt


error_value = 0.0000001
GR = float(sqrt(5) - 1) / 2


def golden_section(lower_bound: float, upper_bound: float, equation: Equation, p: list, vector: list) -> float:
    a = lower_bound
    b = upper_bound
    func = equation.compute
    d = GR * (b - a)
    x1 = a + d
    x2 = b - d
    N = 0

    while abs(x1 - x2) > error_value and N < 100000:
        parameter_list = []
        for i in range(equation.total_var):
            parameter_list.append(p[i] + x1 * vector[i])
        f1 = func(parameter_list)
        parameter_list = []
        for i in range(equation.total_var):
            parameter_list.append(p[i] + x2 * vector[i])
        f2 = func(parameter_list)

        if f1 < f2:
            a = x2

        else:
            b = x1

        d = GR * (b - a)
        x1 = a + d
        x2 = b - d
        N += 1

    return x1


if __name__ == '__main__':
    pass
