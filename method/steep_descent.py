from typing import List
import sys
sys.path.append("..")
from method.golden_section import golden_section, build_var_dict
from arrai.arrai import Arrai
from Equation import Equation
from Exception.explosion import Explosion
from method.powell import get_lb_ub
from decimal import Decimal

MAXIMUM = 99999999
MINIMUM = -99999999
ERROR = 0.0000001
MAX_ITERATION = 100000


def steep_descent(equation_str: str, vars_form: List[str], initial_point: List[float], interval: List[List[float]]):
    answer = ''
    equation = Equation(equation_str)
    var_count = len(vars_form)

    # check input type whether correct or not
    if (len(initial_point) == var_count == len(interval)) is False:
        Explosion.LENGTH_INTERVAL_INITIAL_POINT_NOT_SAME_AS_INPUT_EQUATION.bang()
    for i in interval:
        if len(i) == 2 is False:
            Explosion.LENGTH_INTERVAL_MUST_BE_ONLY_TWO.bang()

    X = [Arrai(initial_point).transpose()]

    # calculate the partial first derivative of the equation with respective to all variables
    first_partial_derivatives = []
    for i in range(var_count):
        first_partial_derivatives.append(equation.eval_diff_form([vars_form[i]]))

    k = 0
    step_size = 100

    while k < MAX_ITERATION:
        # two break situations
        if k != 0:
            if abs(Arrai.norm([X[k] - X[k - 1]])) < ERROR:
                break
        if step_size <= 0:
            break

        var_dict = build_var_dict(vars_form, X[k].transpose()[0])

        # calculate gradient with respect to all variables
        gradients = []
        for i in range(var_count):
            gradients.append(first_partial_derivatives[i].eval_normal_form(var_dict))

        gradients = (-1 * Arrai(gradients)).transpose()

        # get the step_size
        lower_bound, upper_bound = get_lb_ub(interval, X[k].transpose()[0], gradients.transpose()[0])
        step_size = golden_section(equation, vars_form, lower_bound, upper_bound, X[k].transpose()[0], gradients.transpose()[0])
        X.append(X[k] + step_size * gradients)

        answer += ('k=%s\n' % k)
        answer += ('h=%s' % gradients)
        answer += ('Lamdba=%s\n' % step_size)
        answer += ('%s=%s\n' % (vars_form, X[k + 1]))
        k += 1

    answer += ('\n%s=%s' % (vars_form, X[k]))
    answer += ('f(%s)=%s\n' % (X[k], equation.eval_normal_form(build_var_dict(vars_form, X[k].transpose()[0]))))
    return answer, X


if __name__ == '__main__':
    print('Q1:')
    equation1_str = 'x^2+x-2*x^0.5'
    answer1, X1 = steep_descent(equation1_str, ['x'], [50], [[0, 70]])
    print(answer1)
    print(X1)
    # print('Q2:')
    # equation1_str = '7+x^2-3*x*y+3.25*y^2-4y'
    # answer1, X1 = steep_descent(equation1_str, ['x', 'y'], [50, 30], [[-50, 70], [-70, 70]])
    # print(answer1)
    # print(X1)


