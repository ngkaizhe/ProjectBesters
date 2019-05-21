from typing import List
from method.golden_section import golden_section, build_var_dict
from arrai.arrai import Arrai
from Equation import Equation
from Exception.explosion import Explosion
from decimal import Decimal

MAXIMUM = 99999999
MINIMUM = -99999999
ERROR = 0.0000001
MAX_ITERATION = 100000


def steep_descent(equation_str: str, vars_form: List[str], initial_point: List[float], interval: List[List[float]]):
    answer = ''
    equation = Equation(equation_str)
    total_var = len(vars_form)

    # check input type whether correct or not
    if (len(initial_point) == total_var == len(interval)) is False:
        Explosion.STEEP_DESCENT_LENGTH_INTERVAL_INITIAL_POINT_NOT_SAME_AS_INPUT_EQUATION.bang()
    for i in interval:
        if len(i) == 2 is False:
            Explosion.STEEP_DESCENT_LENGTH_INTERVAL_MUST_BE_ONLY_TWO.bang()

    X = [Arrai(initial_point).transpose()]

    # build gradient
    gradient = []
    for i in range(total_var):
        gradient.append(equation.eval_diff_form([vars_form[i]]))

    i = 0
    Lambda = 100

    while i < MAX_ITERATION:
        # two break situations
        if i != 0:
            if abs(Arrai.norm([X[i] - X[i - 1]])) < ERROR:
                break
        if Lambda <= 0:
            break

        var_dict = build_var_dict(vars_form, X[i].transpose()[0])

        # calculate h
        h = []
        for k in range(total_var):
            h.append(gradient[k].eval_normal_form(var_dict))

        h = (-1 * Arrai(h)).transpose()

        # get the lower bound and upper bound of lambda
        lb, ub = get_lb_ub(interval, X[i].transpose()[0], h.transpose()[0])
        Lambda = golden_section(equation, vars_form, lb, ub, X[i].transpose()[0], h.transpose()[0])
        X.append(X[i] + Lambda * h)

        answer += ('i=%s\n' % i)
        answer += ('h=%s' % h)
        answer += ('Lamdba=%s\n' % Lambda)
        answer += ('%s=%s\n' % (vars_form, X[i + 1]))
        i += 1

    answer += ('\n%s=%s' % (vars_form, X[i]))
    answer += ('f(%s)=%s\n' % (X[i], equation.eval_normal_form(build_var_dict(vars_form, X[i].transpose()[0]))))
    return answer, X


# return the lower_bound and the upper_bound of the lambda
def get_lb_ub(interval: List[List[float]], xi: List[float], hi: List[float]):
    total = len(interval)
    lower_bound = MAXIMUM
    upper_bound = MINIMUM

    for k in range(total):
        if hi[k] != 0:
            temp_low = Decimal(interval[k][0]) - xi[k]
            temp_low /= hi[k]
            temp_high = Decimal(interval[k][1]) - xi[k]
            temp_high /= hi[k]

            if temp_low < lower_bound:
                lower_bound = temp_low
            if temp_high > upper_bound:
                upper_bound = temp_high

            if hi[k] < 0:
                lower_bound, upper_bound = upper_bound, lower_bound

    return lower_bound, upper_bound


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


