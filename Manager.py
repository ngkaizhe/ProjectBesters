from typing import List

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
    def __init__(self, equation_str: str, method_name: str, initial_point: List[float], intervals: List[List[float]]):
        self.equation_str = equation_str
        self.method_name = method_name
        self.initial_point = initial_point
        self.intervals = intervals

    def run(self):
        return 'successfully called runned!\n'
