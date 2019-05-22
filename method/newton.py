from typing import List
from Equation import Equation
from arrai.arrai import Arrai
from Exception.explosion import Explosion
from decimal import Decimal


ERROR = 0.000001
MAX_ITERATION = 100000


def newton(equation_str: str, vars_form: List[str], initial_point: List[float]):
    answer = ''
    current_equation = Equation(equation_str)
    var_count = len(vars_form)
    X = [Arrai(initial_point).transpose()]

    # check input type whether correct or not
    if (len(initial_point) == var_count) is False:
        Explosion.POWELL_LENGTH_INTERVAL_INITIAL_POINT_NOT_SAME_AS_INPUT_EQUATION.bang()

    # calculate first partial derivatives respect to all variables
    first_partial_derivatives = []

    for i in range(var_count):
        # print(current_equation.eval_diff_form(pos))
        first_partial_derivatives.append(current_equation.eval_diff_form([vars_form[i]]))

    # build F(x...)
    F = []
    for eqn in first_partial_derivatives:
        temp = []
        for c in range(var_count):
            temp.append(eqn.eval_diff_form([vars_form[c]]))
        F.append(temp)


    k = 0
    while k < MAX_ITERATION:
        if k != 0:
            if abs(Arrai.norm([X[k] - X[k-1]])) < ERROR:
                break

        # calculate Hessian
        hessian = []
        var_dict = build_var_dict(vars_form, X[k].transpose()[0])

        for eqn_list in F:
            temp = []
            for eqn in eqn_list:
                temp.append(eqn.eval_normal_form(var_dict))
            hessian.append(temp)
        hessian = Arrai(hessian)
        hessian_inverse = Arrai.inverse([hessian])
        answer += ('k=%s\n' % k)
        answer += ('Hessian = %s' % hessian)
        answer += ('Hessian Inverse = %s' % hessian_inverse)

        # calculate gradients
        gradients = []
        for eqn in first_partial_derivatives:
            gradients.append([eqn.eval_normal_form(var_dict)])
        gradients = Arrai(gradients)

        next_x = X[k] - Decimal(0.9) * (hessian_inverse * gradients)
        answer += ('%s = %s\n' % (vars_form, next_x))
        X.append(next_x)
        k += 1

    answer += ('\n%s = %sf(%s) = %s' % (vars_form, X[k], X[k], current_equation.eval_normal_form(build_var_dict(vars_form, X[k].transpose()[0]))))
    return answer, X


def build_var_dict(vars_form: List[str], vars_value: List[Decimal]):
    vars_dict = {}
    for i in range(len(vars_value)):
        vars_dict[vars_form[i]] = vars_value[i]

    return vars_dict


if __name__ == '__main__':
    print('Q1:')
    b = 'x^2+x-2*x^0.5'
    answer1, X = newton(b, ['x'], [7])
    print(answer1)
    print(X)
    # print('Q2:')
    # b = '7+x^2-3*x*y+3.25*y^2-4y'
    # answer1, X = newton(b, ['x', 'y'], [1, -1])
    # print(answer1)
    # print(X)
    pass
