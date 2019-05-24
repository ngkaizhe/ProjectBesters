from math import sqrt
from Equation import Equation
from typing import List
from decimal import Decimal
from Exception.explosion import Explosion


ERROR = 0.000000000000000001
GOLDEN_RATIO = 1 - Decimal(sqrt(5) - 1) / 2
MAX_ITERATION = 100000


def golden_section(equation: Equation, vars_form: List[str], 
                   lower_bound: float, upper_bound: float, p: list, vector: list) -> Decimal:
    func = equation.eval_normal_form

    a = Decimal(lower_bound)
    b = Decimal(upper_bound)
    d = GOLDEN_RATIO * (b - a)

    x = (a + d, b - d)
    count_iter = 0

    while True:
        f = []
        for i_x in range(2):
            f.append(golden_eval_equation(func, vars_form, x[i_x], p, vector))

        if not isinstance(f[0], Explosion) and not isinstance(f[1], Explosion):  # Normal case
            if f[1] < f[0]:
                a = x[0]
            else:
                b = x[1]

        else:
            if isinstance(f[0], Explosion) and isinstance(f[1], Explosion):
                eval_a = golden_eval_equation(func, vars_form, a, p, vector)
                eval_b = golden_eval_equation(func, vars_form, b, p, vector)
                if isinstance(eval_a, Explosion) and isinstance(eval_b, Explosion):
                    Explosion.EQUATION_EVAL_NORMAL_INVALID_DOMAIN.bang()
                elif isinstance(eval_a, Explosion):
                    a = x[1]
                elif isinstance(eval_b, Explosion):
                    b = x[0]

            elif isinstance(f[0], Explosion):
                a = x[0]
            elif isinstance(f[1], Explosion):
                b = x[1]

        if abs(x[0] - x[1]) < ERROR or count_iter >= MAX_ITERATION:
            if not isinstance(f[0], Explosion) and not isinstance(f[1], Explosion):  # Normal case
                return x[0]

            else:
                if isinstance(f[0], Explosion) and isinstance(f[1], Explosion):
                    if isinstance(eval_a, Explosion):  # eval_a and eval_b should have been evaluated above
                        return b
                    elif isinstance(eval_b, Explosion):
                        return a

                else:
                    return x[0] if not isinstance(f[0], Explosion) else x[1]

        d = GOLDEN_RATIO * (b - a)
        x = (a + d, b - d)
        count_iter += 1


def golden_eval_equation(func, vars_form, x, p, vector):
    var_count = len(vars_form)
    parameter_list = []
    for i in range(var_count):
        parameter_list.append(p[i] + x * vector[i])

    vars_dict = build_var_dict(vars_form, parameter_list)

    try:
        eval_result = func(vars_dict)
    except:
        eval_result = Explosion.EQUATION_EVAL_NORMAL_INVALID_DOMAIN

    return eval_result


def build_var_dict(vars_form: List[str], vars_value: List[Decimal]):
    vars_dict = {}
    for i in range(len(vars_value)):
        vars_dict[vars_form[i]] = vars_value[i]

    return vars_dict


if __name__ == '__main__':
    pass
