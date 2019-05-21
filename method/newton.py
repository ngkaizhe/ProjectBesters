from typing import List
from Equation import Equation
from arrai.arrai import Arrai
from Exception.explosion import Explosion
from decimal import Decimal


error_value = 0.000001


def newton(equation_str: str, vars_form: List[str], initial_point: List[float]):
    answer = ''
    current_equation = Equation(equation_str)
    total_var = len(vars_form)
    X = [Arrai(initial_point).transpose()]

    # check input type whether correct or not
    if (len(initial_point) == total_var) is False:
        Explosion.POWELL_LENGTH_INTERVAL_INITIAL_POINT_NOT_SAME_AS_INPUT_EQUATION.bang()

    # build gradient
    gradient = []

    for i in range(total_var):
        # print(current_equation.eval_diff_form(pos))
        gradient.append(current_equation.eval_diff_form([vars_form[i]]))

    # build F(x...)
    F = []
    for eqn in gradient:
        temp = []
        for c in range(total_var):
            temp.append(eqn.eval_diff_form([vars_form[c]]))
        F.append(temp)

    N = 100
    i = 0
    while i < N:
        if i != 0:
            if abs(Arrai.norm([X[i] - X[i-1]])) < error_value:
                break

        # calculate Hessian
        Hessian = []
        var_dict = build_var_dict(vars_form, X[i].transpose()[0])

        for eqn_list in F:
            temp = []
            for eqn in eqn_list:
                temp.append(eqn.eval_normal_form(var_dict))
            Hessian.append(temp)
        Hessian = Arrai(Hessian)
        Hessian_inverse = Arrai.inverse([Hessian])
        answer += ('i=%s\n' % i)
        answer += ('Hessian = %s' % Hessian)
        answer += ('Hessian Inverse = %s' % Hessian_inverse)

        # calculate g
        g = []
        for eqn in gradient:
            g.append([eqn.eval_normal_form(var_dict)])
        g = Arrai(g)

        x = X[i] - Decimal(0.9) * (Hessian_inverse * g)
        answer += ('%s = %s\n\n' % (vars_form, x))
        X.append(x)
        i += 1

    answer += ('%s = %sf(%s) = %s' % (vars_form, X[i], X[i], current_equation.eval_normal_form(build_var_dict(vars_form, X[i].transpose()[0]))))
    return answer, X


def build_var_dict(vars_form: List[str], vars_value: List[Decimal]):
    vars_dict = {}
    for i in range(len(vars_value)):
        vars_dict[vars_form[i]] = vars_value[i]

    return vars_dict


if __name__ == '__main__':
    # print('Q1:')
    # b = 'x^2+x-2*x^0.5'
    # newton(b, ['x'], [7])
    print('Q2:')
    b = '7+x^2-3*x*y+3.25*y^2-4y'
    answer, X = newton(b, ['x', 'y'], [1, -1])
    print(answer)
    print(X)
    pass
