from typing import List
from method.powell import powell
from method.conjugate_gradient import conjugate_gradient
from method.quasi_newton import quasi_newton
from method.newton import newton
from method.steep_descent import steep_descent

# value should be functions
Methods = {
    'None----': '',
    'Powell\'s Method': '???',
    'Newton Method': '???',
    'Steep Descent Algorithm': '???',
    'Quasi-Newton Method': '???',
    'Conjugate Gradient Methods': '???',
}


class Manager(object):
    def __init__(self, equation_str: str, vars_form: List[str], method_name: str, initial_point: List[float], intervals: List[List[float]]= None):
        self.equation_str = equation_str
        self.vars_form = vars_form
        self.method_name = method_name
        self.initial_point = initial_point
        self.intervals = intervals

    def run(self):
        if self.method_name == 'Powell\'s Method':
            answer, X = powell(self.equation_str, self.vars_form, self.initial_point, self.intervals)
            return answer, X

        elif self.method_name == 'Newton Method':
            answer, X = newton(self.equation_str, self.vars_form, self.initial_point)
            return answer, X

        elif self.method_name == 'Steep Descent Algorithm':
            answer, X = steep_descent(self.equation_str, self.vars_form, self.initial_point, self.intervals)
            return answer, X

        elif self.method_name == 'Quasi-Newton Method':
            answer, X = quasi_newton(self.equation_str, self.vars_form, self.initial_point)
            return answer, X

        elif self.method_name == 'Conjugate Gradient Methods':
            answer, X = conjugate_gradient(self.equation_str, self.vars_form, self.initial_point, self.intervals)
            return answer, X
