from method.TestEquation import TestingEquation as Equation
from math import sqrt


error_value = 0.00000001
GR = float(sqrt(5) - 1) / 2


def golden_section(lower_bound: float, upper_bound: float, equation: Equation) -> float:
    a = lower_bound
    b = upper_bound
    func = equation.compute
    d = GR * (b - a)
    x1 = a + d
    x2 = b - d
    N = 0

    while abs(x1 - x2) > error_value and N < 100000:
        f1 = func([x1])
        f2 = func([x2])

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
    print(golden_section(0, 1, Equation()))
