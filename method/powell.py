from typing import List
from math import sqrt
from method.TestEquation import TestingEquation as Equation
from method.golden_section import golden_section
import numpy as np


maximum_value = 99999999
minimum_value = -99999999
error_value = 0.0000001


def powell(equation_str: str, initial_point: List[float], interval: List[List[float]]):
    answer = ''
    equation = Equation(equation_str)
    total_var = equation.total_var

    # check input type whether correct or not
    assert len(initial_point) == total_var == len(interval)
    for i in interval:
        assert len(i) == 2

    # total iteration
    N = 100
    X = np.array([initial_point])
    S = np.identity(total_var)

    answer += ('First loop: f(%s)= %s\n\n' % (X[0], equation.compute(X[0])))

    for i in range(N):
        # check break situation:
        # distance between X[i] and X[i-1] smaller than error value
        if i > 0:
            if mag(X[i] - X[i-1]) < error_value:
                break

        P = np.array([X[i]])
        # save the value of alphas
        alphas = np.zeros(total_var, dtype=float)

        for j in range(total_var):
            alpha_lb, alpha_ub = get_lb_ub(interval, P[j], S[j])
            alphas[j] = golden_section(alpha_lb, alpha_ub, equation, P[j], S[j])
            P = np.append(P, [P[j] + alphas[j]*S[j]], axis=0)

            answer += ('i=%s\nj=%s\nalpha=%s\nf(%s)=%s\n\n' % (i, j, alphas[j], P[j+1], equation.compute(P[j+1])))

        # The new displacement vector(summation alphas[i]*S[i] from 0 to total_var-1) becomes a new search vector
        sn = P[total_var] - P[0]
        X = np.append(X, [P[total_var]], axis=0)

        # get the index to replaced, index = argmax alphas[k]*||S[k]|| for all k
        value = alphas[0] * mag(S[0])
        index = 0
        for k in range(1, total_var):
            temp_value = alphas[k] * mag(S[k])
            if temp_value > value:
                index = k

        S = np.delete(S, index, axis=0)
        S = np.append(S, [sn], axis=0)
        answer += ('New S{%s}\n\n' % S)

    answer += ('X Set = {%s}\n\n' % X)
    answer += ('Last loop: f(%s)= %s\n\n' % (X[len(X)-1], equation.compute(X[len(X)-1])))
    return answer


# get magnitude
def mag(vector: List[float]):
    total = 0
    for i in vector:
        total += i*i

    return sqrt(total)


# return the lower_bound and the upper_bound of the alpha
def get_lb_ub(interval: List[List[float]], pi: List[float], si: List[float]):
    total = len(interval)
    lower_bound = maximum_value
    upper_bound = minimum_value

    for k in range(total):
        if si[k] != 0:
            temp_low = interval[k][0] - pi[k]
            temp_low /= si[k]
            temp_high = interval[k][1] - pi[k]
            temp_high /= si[k]

            if temp_low < lower_bound:
                lower_bound = temp_low
            if temp_high > upper_bound:
                upper_bound = temp_high

            if si[k] < 0:
                lower_bound, upper_bound = upper_bound, lower_bound

    return lower_bound, upper_bound


if __name__ == '__main__':
    # print('Q1: x^2+x-2*x^0.5')
    # print(powell(equation_str='???', initial_point=[50], interval=[[0, 70]]))
    # print('Q2: sin(3x)+cos(x)')
    # print(powell(equation_str='???', initial_point=[1], interval=[[0.3, 3]]))
    print('Q2: 7 + x^2 - 3*x*y + 3.25*y^2 - 4*y')
    print(powell(equation_str='???', initial_point=[50, 30], interval=[[-50, 70], [-70, 70]]))
    pass
