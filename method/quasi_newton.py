from typing import List
from Equation import Equation
from arrai.arrai import Arrai
from Exception.explosion import Explosion
from decimal import Decimal


ERROR = 0.000001
MAX_ITERATION = 100


def quasi_newton(equation_str: str, vars_form: List[str], initial_point: List[float]):
    answer = ''
    current_equation = Equation(equation_str)
    var_count = len(vars_form)
    X = [Arrai(initial_point).transpose()]

    # check input type whether correct or not
    if (len(initial_point) == var_count) is False:
        Explosion.INITIAL_POINT_NOT_SAME_AS_INPUT_EQUATION.bang()

    # build first_derivatives
    first_partial_derivatives = []
    for i in range(var_count):
        # print(current_equation.eval_diff_form(pos))
        first_partial_derivatives.append(current_equation.eval_diff_form([vars_form[i]]))

    # build F(x...), which is the second partial derivatives respect to all variables over first partial derivatives
    second_partial_derivatives = []
    for eqn in first_partial_derivatives:
        temp = []
        for i in range(var_count):
            temp.append(eqn.eval_diff_form([vars_form[i]]))
        second_partial_derivatives.append(temp)

    hessians = []
    hessian_inverse = []
    list_gradients = []
    list_direction = []
    alphas = []
    i = 0

    while i < MAX_ITERATION:
        # two break conditions, second condition is list_gradients[k] = 0
        if i != 0:
            if abs(Arrai.norm([X[i] - X[i - 1]])) < ERROR:
                break

        var_dict = build_var_dict(vars_form, X[i].transpose()[0])

        if i == 0:
            # calculate first Hessian and Hessian Inverse
            first_hessian = []
            for eqn_list in second_partial_derivatives:
                temp = []
                for eqn in eqn_list:
                    temp.append(eqn.eval_normal_form(var_dict))
                first_hessian.append(temp)

            first_hessian = Arrai(first_hessian)
            hessians.append(first_hessian)
            hessian_inverse.append(Arrai.inverse([first_hessian]))

            # calculate first list_gradients
            gradients = []
            for eqn in first_partial_derivatives:
                gradients.append([eqn.eval_normal_form(var_dict)])
            list_gradients.append(Arrai(gradients))
            list_direction.append(- Decimal(0.9) * (hessian_inverse[i] * list_gradients[i]))
            alpha = list_direction[i].transpose() * list_direction[i] / (
                        list_direction[i].transpose() * Arrai.inverse([hessian_inverse[i]]) * list_direction[i])
            alphas.append(alpha)

            answer += ('Initial Hessian: %s' % hessians[i])
            answer += ('Initial Hessian inverse: %s' % hessian_inverse[i])

        else:
            k = i - 1
            # calculate list_gradients[i]
            temp_g = []
            for eqn in first_partial_derivatives:
                temp_g.append([eqn.eval_normal_form(var_dict)])
            list_gradients.append(Arrai(temp_g))

            if is_all_zero(list_gradients[k]):
                break

            g_distance = list_gradients[k + 1] - list_gradients[k]
            x_distance = X[k + 1] - X[k]

            # use DFP to get Hessian Inverse:
            current_Hessian_inverse = hessian_inverse[k]
            first = current_Hessian_inverse
            second1 = x_distance * x_distance.transpose()
            second2 = x_distance.transpose() * g_distance
            second = (second1 / second2)
            third1 = (current_Hessian_inverse * g_distance) * (current_Hessian_inverse * g_distance).transpose()
            third2 = g_distance.transpose() * current_Hessian_inverse * g_distance
            third = (third1 / third2)
            # fourth1 = g_distance.transpose() * (current_Hessian_inverse * g_distance)
            # fourth2 = x_distance / (x_distance.transpose() * g_distance)
            # fourth3 = ((current_Hessian_inverse * g_distance) /
            #            (g_distance.transpose() * current_Hessian_inverse * g_distance))
            # fourth = fourth1 * (fourth2 - fourth3).transpose()
            # next_hessian_inverse = first + second - third + fourth
            next_hessian_inverse = first + second - third
            hessian_inverse.append(next_hessian_inverse)
            list_direction.append(-Decimal(0.9) * (hessian_inverse[i] * list_gradients[i]))
            alpha = list_direction[i].transpose() * list_direction[i] / (list_direction[i].transpose() * Arrai.inverse([hessian_inverse[i]]) * list_direction[i])
            alphas.append(alpha)

            answer += ('i=%s\n' % i)
            answer += ('Hessian inverse: %s' % hessian_inverse[i])

        x = X[i] + alphas[i] * list_direction[i]
        X.append(x)
        answer += ('%s: %s\n' % (vars_form, X[i + 1]))
        i += 1

    answer += ('\n%s = %sf(%s) = %s' %
               (vars_form, X[i], X[i], current_equation.eval_normal_form(build_var_dict(vars_form, X[i].transpose()[0]))))
    return answer, X


def build_var_dict(vars_form: List[str], vars_value: List[Decimal]):
    vars_dict = {}
    for i in range(len(vars_value)):
        vars_dict[vars_form[i]] = vars_value[i]

    return vars_dict


def is_all_zero(g: Arrai):
    for r in g:
        for c in r:
            if abs(c) > ERROR:
                return False
    return True


if __name__ == '__main__':
    # print('Q1:')
    # b = 'x^2+x-2*x^0.5'
    # answer1, X1 = quasi_newton(b, ['x'], [7])
    # print(answer1)
    # print(X1)
    print('Q2:')
    b = '7+x^2-3*x*y+3.25*y^2-4y'
    answer1, X1 = quasi_newton(b, ['x', 'y'], [6, 5])
    print(answer1)
    print(X1)
    pass
