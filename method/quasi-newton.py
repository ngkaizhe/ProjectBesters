from typing import List
from Equation import Equation
from arrai.arrai import Arrai
from Exception.explosion import Explosion
from decimal import Decimal


error_value = 0.000001


def quasi_newton(equation_str: str, vars_form: List[str], initial_point: List[float]):
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

    i = 0
    N = 100
    Hessians = []
    Hessians_inverses = []
    g = []

    while i < N:
        # two break conditions, second condition is g[k] = 0
        if i != 0:
            if abs(Arrai.norm([X[i] - X[i - 1]])) < error_value:
                break

        var_dict = build_var_dict(vars_form, X[i].transpose()[0])

        if i == 0:
            # calculate first Hessian and Hessian Inverse
            first_hessian = []
            for eqn_list in F:
                temp = []
                for eqn in eqn_list:
                    temp.append(eqn.eval_normal_form(var_dict))
                first_hessian.append(temp)

            first_hessian = Arrai(first_hessian)
            Hessians.append(first_hessian)
            Hessians_inverses.append(Arrai.inverse([first_hessian]))

            # calculate first g
            temp_g = []
            for eqn in gradient:
                temp_g.append([eqn.eval_normal_form(var_dict)])
            g.append(Arrai(temp_g))

            answer += ('Initial Hessian: %s' % Hessians[i])
            answer += ('Initial Hessian inverse: %s' % Hessians_inverses[i])

        else:
            k = i-1
            # calculate g[i]
            temp_g = []
            for eqn in gradient:
                temp_g.append([eqn.eval_normal_form(var_dict)])
            g.append(Arrai(temp_g))

            if is_all_zero(g[k]):
                break

            g_distance = g[k+1]-g[k]
            x_distance = X[k+1]-X[k]

            # use DFP to get Hessian Inverse:
            current_Hessian_inverse = Hessians_inverses[k]
            first = current_Hessian_inverse
            second1 = x_distance * x_distance.transpose()
            second2 = x_distance.transpose() * g_distance
            second = (second1 / second2)
            third1 = (current_Hessian_inverse * g_distance) * (current_Hessian_inverse * g_distance).transpose()
            third2 = g_distance.transpose() * current_Hessian_inverse * g_distance
            third = (third1 / third2)
            # fourth1 = g_distance.transpose() * (current_Hessian_inverse * g_distance).transpose()
            # fourth2 = x_distance / (x_distance.transpose() * g_distance)
            # fourth3 = (current_Hessian_inverse * g_distance).transpose() / \
            #           (g_distance.transpose() * current_Hessian_inverse * g_distance)
            # fourth = fourth1 * (fourth2 - fourth3)
            # next_Hessian_inverse = first + second - third + fourth
            next_Hessian_inverse = first + second - third
            Hessians_inverses.append(next_Hessian_inverse)

            answer += ('i=%s\n' % i)
            answer += ('Hessian inverse: %s' % Hessians_inverses[i])

        x = X[i] - Decimal(0.9) * (Hessians_inverses[i] * g[i])
        X.append(x)
        answer += ('%s: %s\n' % (vars_form, X[i + 1]))
        i += 1

    answer += ('\n%s = %sf(%s) = %s' % (vars_form, X[i], X[i], current_equation.eval_normal_form(build_var_dict(vars_form, X[i].transpose()[0]))))
    return answer, X


def build_var_dict(vars_form: List[str], vars_value: List[Decimal]):
    vars_dict = {}
    for i in range(len(vars_value)):
        vars_dict[vars_form[i]] = vars_value[i]

    return vars_dict


def is_all_zero(g: Arrai):
    for r in g:
        for c in r:
            if abs(c) > error_value:
                return False
    return True


if __name__ == '__main__':
    print('Q1:')
    b = 'x^2+x-2*x^0.5'
    answer1, X1 = quasi_newton(b, ['x'], [7])
    print(answer1)
    print(X1)
    # print('Q2:')
    # b = '7+x^2-3*x*y+3.25*y^2-4y'
    # answer1, X1 = quasi_newton(b, ['x', 'y'], [6, 5])
    # print(answer1)
    # print(X1)
    # pass
