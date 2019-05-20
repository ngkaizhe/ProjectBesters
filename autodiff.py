from typing import List
from math import sin, cos
from decimal import Decimal


class Node(object):
    def __init__(self):
        self.inputs: List[Node] = []
        self.op: Op = None
        self.const_attr = None
        self.normal_form = ''
        self.diff_form = ''

    def __add__(self, other):
        """Adding two nodes return a new node."""
        if isinstance(other, Node):
            if (self.op == const_op and other.op == const_op):
                new_node = const_op(self.const_attr + other.const_attr)
            else:
                new_node = add_op(self, other)
        else:
            new_node = add_op(self, const_op(other))
        return new_node

    def __sub__(self, other):
        """Adding two nodes return a new node."""
        if isinstance(other, Node):
            if (self.op == const_op and other.op == const_op):
                new_node = const_op(self.const_attr - other.const_attr)
            else:
                new_node = sub_op(self, other)
        else:
            new_node = sub_op(self, const_op(other))
        return new_node

    def __mul__(self, other):
        """Adding two nodes return a new node."""
        if isinstance(other, Node):
            if (self.op == const_op and other.op == const_op):
                new_node = const_op(self.const_attr * other.const_attr)
            else:
                new_node = mul_op(self, other)
        else:
            new_node = mul_op(self, const_op(other))
        return new_node

    def __truediv__(self, other):
        """Adding two nodes return a new node."""
        if isinstance(other, Node):
            if (self.op == const_op and other.op == const_op):
                new_node = const_op(self.const_attr / other.const_attr)
            else:
                new_node = div_op(self, other)
        else:
            new_node = div_op(self, const_op(other))
        return new_node

    def __pow__(self, other):
        """Adding two nodes return a new node."""
        if isinstance(other, Node):
            if (self.op == const_op and other.op == const_op):
                new_node = const_op(self.const_attr ** other.const_attr)
            else:
                new_node = pow_op(self, other)
        else:
            new_node = pow_op(self, const_op(other))
        return new_node

# operator inheritance, blank class
class Op(object):
    def __call__(self):
        new_node = Node()
        new_node.op = self
        return new_node

    def compute(self, node: Node, input_vals: list = None):
        assert False, 'Implemented in subclass!'

    def diff(self, node: Node, variable: str) -> None:
        assert False, 'Implemented in subclass!'


class PlaceholderOp(Op):
    def __call__(self, var_string: str) -> Node:
        new_node = Op.__call__(self)
        new_node.inputs = None
        new_node.normal_form = var_string
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert len(input_vals) == 1
        return input_vals[0]

    def diff(self, node: Node, variable: str) -> None:
        if variable == node.normal_form:
            node.diff_form = '1'
        else:
            node.diff_form = '0'
        return

class ConstOp(Op):
    def __call__(self, number: float) -> Node:
        new_node = Op.__call__(self)
        new_node.inputs = None
        new_node.const_attr = Decimal(number)
        new_node.normal_form = str(number)
        return new_node

    def compute(self, node: Node) -> float:
        return node.const_attr

    def diff(self, node: Node, variable: str) -> None:
        node.diff_form = '0'
        return

class NegOp(Op):
    def __call__(self, node: Node) -> Node:
        new_node = Op.__call__(self)
        new_node.inputs = [node]
        new_node.normal_form = "-(%s)" % (node.normal_form)
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert len(input_vals) == 1
        return -input_vals[0]

    def diff(self, node: Node, variable: str) -> None:
        if node.inputs[0].diff_form == '0':
            node.diff_form = '0'
        else:
            node.diff_form = "-(%s)" % (node.diff_form)
        return


class AddOp(Op):
    def __call__(self, node_A: Node, node_B: Node) -> Node:
        new_node = Op.__call__(self)
        new_node.inputs = [node_A, node_B]
        new_node.normal_form = "%s+%s" % (node_A.normal_form, node_B.normal_form)
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert len(input_vals) == 2
        return input_vals[0] + input_vals[1]

    def diff(self, node: Node, variable: str) -> None:
        if node.inputs[1].diff_form == '0' and node.inputs[0].diff_form == '0':
            node.diff_form = "0"
        elif node.inputs[1].diff_form == '0':
            node.diff_form = "%s" % node.inputs[0].diff_form
        elif node.inputs[0].diff_form == '0':
            node.diff_form = "%s" % node.inputs[1].diff_form
        else:
            node.diff_form = "%s+%s" % (
                node.inputs[0].diff_form, node.inputs[1].diff_form)
        return


class SubOp(Op):
    def __call__(self, node_A: Node, node_B: Node) -> Node:
        new_node = Op.__call__(self)
        new_node.inputs = [node_A, node_B]
        new_node.normal_form = "%s-(%s)" % (node_A.normal_form, node_B.normal_form)
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert len(input_vals) == 2
        return input_vals[0] - input_vals[1]

    def diff(self, node: Node, variable: str) -> None:
        if node.inputs[1].diff_form == '0' and node.inputs[0].diff_form == '0':
            node.diff_form = "0"
        elif node.inputs[1].diff_form == '0':
            node.diff_form = "%s" % node.inputs[0].diff_form
        elif node.inputs[0].diff_form == '0':
            node.diff_form = "-(%s)" % node.inputs[1].diff_form
        else:
            node.diff_form = "%s-(%s)" % (
            node.inputs[0].diff_form, node.inputs[1].diff_form)
        return


class MulOp(Op):
    def __call__(self, node_A: Node, node_B: Node) -> Node:
        new_node = Op.__call__(self)
        new_node.inputs = [node_A, node_B]
        new_node.normal_form = "(%s)*(%s)" % (node_A.normal_form, node_B.normal_form)
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert len(input_vals) == 2
        return input_vals[0] * input_vals[1]

    def diff(self, node: Node, variable: str) -> None:
        if node.inputs[1].diff_form == '0' and node.inputs[0].diff_form == '0':
            node.diff_form = "0"
        elif node.inputs[1].diff_form == '0':
            node.diff_form = "(%s)*(%s)" % (node.inputs[1].normal_form, node.inputs[0].diff_form)
        elif node.inputs[0].diff_form == '0':
            node.diff_form = "(%s)*(%s)" % (node.inputs[0].normal_form, node.inputs[1].diff_form)
        else:
            node.diff_form = "(%s)*(%s)+(%s)*(%s)" \
             %(node.inputs[1].normal_form, node.inputs[0].diff_form, node.inputs[0].normal_form, node.inputs[1].diff_form)
        return


class DivOp(Op):

    def __call__(self, node_A: Node, node_B: Node):
        new_node = Op.__call__(self)
        new_node.inputs = [node_A, node_B]
        new_node.normal_form = "(%s)/(%s)" % (node_A.normal_form, node_B.normal_form)
        return new_node

    def compute(self, node, input_vals):
        assert len(input_vals) == 2
        return input_vals[0] / input_vals[1]

    def diff(self, node: Node, variable: str) -> None:
        if node.inputs[1].diff_form == '0' and node.inputs[0].diff_form == '0':
            node.diff_form = "0"
        elif node.inputs[1].diff_form == '0':
            node.diff_form = "((%s)*(%s))/(%s)^2" % (
                node.inputs[1].normal_form, node.inputs[0].diff_form, node.inputs[1].normal_form)
        elif node.inputs[0].diff_form == '0':
            node.diff_form = "(-(%s)*(%s))/(%s)^2)" % (
                node.inputs[0].normal_form, node.inputs[1].diff_form, node.inputs[1].normal_form)
        else:
            node.diff_form = "(%s)*(%s)-(%s)*(%s))/(%s)^2)" %(
                node.inputs[1].normal_form, node.inputs[0].diff_form, node.inputs[0].normal_form, node.inputs[1].diff_form, node.inputs[1].normal_form)
        return


class PowOp(Op):
    def __call__(self, node_A: Node, node_B: Node) -> Node:
        new_node = Op.__call__(self)
        new_node.inputs = [node_A, node_B]
        new_node.normal_form = "(%s)^(%s)" % (node_A.normal_form, node_B.normal_form)
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert node.inputs[1].op == const_op
        assert len(input_vals) == 2
        return Decimal(pow(input_vals[0], input_vals[1]))

    def diff(self, node: Node, variable: str) -> None:
        if variable == node.inputs[0].normal_form:
            node.diff_form = "(%s)*(%s)^((%s)-1)" % (node.inputs[1].normal_form, node.inputs[0].normal_form, node.inputs[1].normal_form)
        else:
            node.diff_form = '0'
        return


# for calling const operator, assume that node A was a const number
# for AddConstOp and SubConstOp
# second list element inside const_attr save the of the var
# 0: var - const
# 1: const - var
class AddConstOp(Op):
    def __call__(self, node_A: Node, node_B: Node) -> Node:
        new_node = Op.__call__(self)
        new_node.inputs = [node_A, node_B]
        new_node.const_attr = [node_A.const_attr if node_A.const_attr is not None else node_B.const_attr, 1 if node_A.const_attr is not None else 0]
        new_node.normal_form = "%s+%s" % (node_A.normal_form, node_B.normal_form)
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert len(input_vals) == 1
        return node.const_attr + input_vals[0]

    def diff(self, node: Node, variable: str) -> None:
        if node.inputs[node.const_attr[1]].diff_form == '0':
            node.diff_form = '0'
        else:
            node.diff_form = "%s" % node.inputs[node.const_attr[1]].diff_form


class SubConstOp(Op):
    def __call__(self, node_A: Node, node_B: Node) -> Node:
        new_node = Op.__call__()
        new_node.inputs = [node_A, node_B]
        new_node.const_attr = [node_A.const_attr if node_A.const_attr is not None else node_B.const_attr, 1 if node_A.const_attr is not None else 0]
        new_node.normal_form = "%s-(%s)" % (node_A.normal_form, node_B.normal_form)
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert len(input_vals) == 1
        return node.const_attr - input_vals[0]

    def diff(self, node: Node, variable: str) -> None:
        if node.inputs[node.const_attr[1]].diff_form == '0':
            node.diff_form = '0'
        else:
            if node.const_attr[1] == 0:
                node.diff_form = "%s" % node.inputs[0].diff_form
            elif node.const_attr[1] == 1:
                node.diff_form = "-(%s)" % node.inputs[1].diff_form

class MulConstOp(Op):
    def __call__(self, node_A: Node, node_B: Node) -> Node:
        new_node = Op.__call__()
        new_node.inputs = [node_A, node_B]
        new_node.const_attr = node_A.const_attr
        new_node.normal_form = "(%s)*(%s)" % (node_A.normal_form, node_B.normal_form)
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert len(input_vals) == 1
        return node.const_attr * input_vals[0]

    def diff(self, node: Node) -> None:
        if node.inputs[1].diff_form == '0':
            node.diff_form = "0"
        else:
            node.diff_form = "(%s)*(%s)" % (
                node.inputs[0].normal_form, node.inputs[1].diff_form)
        return


"""
sinOp and cosOp part
"""


class SinOp(Op):
    def __call__(self, node: Node) -> Node:
        new_node = Op.__call__(self)
        new_node.inputs = [node]
        new_node.const_attr = 0
        new_node.normal_form = "sin(%s)" % node.normal_form
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert len(input_vals) == 1
        return Decimal(sin(input_vals[0]))

    def diff(self, node: Node, variable: str) -> None:
        if node.inputs[0].diff_form == '0':
            node.diff_form = '0'
        else:
            node.diff_form = "(%s)*cos(%s)" % (
                node.inputs[0].diff_form, node.inputs[0].normal_form)
        return


class CosOp(Op):
    def __call__(self, node: Node) -> Node:
        new_node = Op.__call__(self)
        new_node.inputs = [node]
        new_node.const_attr = 0
        new_node.normal_form = "cos(%s)" % node.normal_form
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert len(input_vals) == 1
        return Decimal(cos(input_vals[0]))

    def diff(self, node: Node, variable: str) -> None:
        if node.inputs[0].diff_form == '0':
            node.diff_form = '0'
        else:
            node.diff_form = "-(%s)*sin(%s)" % (
                node.inputs[0].diff_form, node.inputs[0].normal_form)
        return

add_op = AddOp()
sub_op = SubOp()
mul_op = MulOp()
div_op = DivOp()
pow_op = PowOp()
sin_op = SinOp()
cos_op = CosOp()
neg_op = NegOp()
placeholder_op = PlaceholderOp()
const_op = ConstOp()



