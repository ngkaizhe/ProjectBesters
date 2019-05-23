from typing import List
from arrai.arrai import Arrai
from method.golden_section import golden_section, build_var_dict
from arrai.arrai import Arrai
from Equation import Equation
from Exception.explosion import Explosion
from decimal import Decimal

ERROR = 0.000001
MAXIMUM = 99999999
MINIMUM = -99999999


def conjugate_gradient(equation_str: str, vars_form: List[str], initial_point: List[float], interval: List[List[float]]):
    answer = ''
    equation = Equation(equation_str)
    var_count = len(vars_form)

    # check input type whether correct or not
    if (len(initial_point) == var_count == len(interval)) is False:
        Explosion.LENGTH_INTERVAL_INITIAL_POINT_NOT_SAME_AS_INPUT_EQUATION.bang()
    for i in interval:
        if len(i) == 2 is False:
            Explosion.LENGTH_INTERVAL_MUST_BE_ONLY_TWO.bang()

    list_X = [Arrai(initial_point).transpose()]
    list_results = [equation.eval_normal_form(build_var_dict(vars_form, initial_point))]

    # calculate the partial first derivative of the equation with respective to all variables
    first_partial_derivatives = []
    for i in range(var_count):
        first_partial_derivatives.append(equation.eval_diff_form([vars_form[i]]))

    k = 0
    step_size = 100

    list_gradients = []
    list_directions = []
    diff_results = -1

    #for k in range(var_count):
    while(True):
        # two break situations
        if k != 0:
            if abs(Arrai.norm([list_X[k] - list_X[k - 1]])) < ERROR or \
                abs(diff_results) < ERROR or \
                Arrai.to_scalar(list_X[k].transpose() * list_X[k]) < ERROR or \
               Arrai.norm([Arrai(list_gradients[k - 1])]) < ERROR:
               break

        var_dict = build_var_dict(vars_form, list_X[k].transpose()[0])

        # calculate gradient with respect to all variables
        gradients = []
        for i in range(var_count):
            gradients.append(first_partial_derivatives[i].eval_normal_form(var_dict))
        list_gradients.append(gradients)

        # Note that the type turned to Arrai
        current_gradients = Arrai(list_gradients[k])  # row vector
        previous_gradients = Arrai(list_gradients[k - 1])  # row vector

        directions = (-1 * current_gradients).transpose()  # col vector

        if k != 0:
            beta = Arrai.to_scalar((current_gradients * current_gradients.transpose()) /
                                   (previous_gradients * previous_gradients.transpose()))

            # Adjust Bounding according to the value of previous X
            '''diff_X = list_X[k] - list_X[k-1]
            for i in range(var_count):
                if diff_X[i][0] < 0:
                    interval[i][1] = list_X[k][i][0]
                else:
                    interval[i][0] = list_X[k][i][0]
            print(interval)'''

            directions += beta * list_directions[k - 1]  # Previous Search Direction

        list_directions.append(directions)

        # get the lower bound and upper bound of step_size
        lower_bound, upper_bound = get_lb_ub(interval, list_X[k].transpose()[0], directions.transpose()[0])
        step_size = golden_section(equation, vars_form, lower_bound, upper_bound, list_X[k].transpose()[0], directions.transpose()[0])
        
        #Step size is multiplied by 0.5, with increased iterations improves the accuracy
        step_size *= Decimal(0.5)

        list_X.append(list_X[k] + step_size * directions)

        list_results.append(equation.eval_normal_form(build_var_dict(vars_form, list_X[k + 1].transpose()[0])))
        diff_results = list_results[k + 1] - list_results[k]  # row vector

        answer += ('k=%s\n' % k)
        answer += ('Si=%s' % directions)
        if (k != 0):
            answer += ('beta=%.6f\n' % beta)
        answer += ('alpha=%.6f\n' % step_size)
        answer += ('%s=%s\n' % (vars_form, list_X[k + 1]))
        k += 1

    answer += ('\n%s=%s' % (vars_form, list_X[k]))
    answer += ('f(%s)=%.4f\n' % (list_X[k], equation.eval_normal_form(build_var_dict(vars_form, list_X[k].transpose()[0]))))
    return answer, list_X

# return the lower_bound and the upper_bound of the lambda
def get_lb_ub(interval: List[List[float]], pi: List[float], si: List[float]):
    total = len(interval)
    list_lower_bound = []
    list_upper_bound = []

    for k in range(total):
        if abs(si[k]) > 0.0000001:
            temp_low = Decimal(interval[k][0]) - pi[k]
            temp_low /= si[k]
            temp_high = Decimal(interval[k][1]) - pi[k]
            temp_high /= si[k]

            if si[k] < 0:
                temp_low, temp_high = temp_high, temp_low

            list_lower_bound.append(temp_low) 
            list_upper_bound.append(temp_high)

    # no upper bound and lower found for alpha, return 0 instead
    if len(list_upper_bound) == 0 or len(list_lower_bound) == 0:
        return 0, 0

    lower_bound = list_lower_bound[0]
    upper_bound = list_upper_bound[0]
    for i in range(1, len(list_lower_bound)):
        if list_lower_bound[i] > lower_bound:
            lower_bound = list_lower_bound[i]

    for i in range(1, len(list_upper_bound)):
        if list_upper_bound[i] < upper_bound:
            upper_bound = list_upper_bound[i]

    return lower_bound, upper_bound




if __name__ == '__main__':
    print('Q1:')
    equation1_str = 'x^0.5'
    answer1, X1 = conjugate_gradient(equation1_str, ['x', 'y'], [50, 30], [[-50,30], [-70, 70]])
    print(answer1)
    print(X1)

    print('Q2:')
    equation2_str = '0.001*x^3-0.07*x^2+0.06*x+0.0002*y^3-0.004*y^2+0.02*y'
    answer2, X2 = conjugate_gradient(equation2_str, ['x', 'y'], [50, 30], [[-50, 70], [-70, 70]])
    print(answer2)
    print(X2)
