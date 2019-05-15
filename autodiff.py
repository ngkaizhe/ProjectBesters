from typing import List

class Node(object):
    def __init__(self):
        self.inputs: List[Node] = []
        self.op: Op = None
        self.const_attr = None
        self.normal_form = ''
        self.diff_form = ''


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


class AddOp(Op):
    def __call__(self, node_A: Node, node_B: Node) -> Node:
        new_node = Op.__call__()
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
        new_node = Op.__call__()
        new_node.inputs = [node_A, node_B]
        new_node.normal_form = "%s-%s" % (node_A.normal_form, node_B.normal_form)
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert len(input_vals) == 2
        return input_vals[0] - input_vals[1]

    def diff(self, node: Node, variable: str) -> None:
        if node.inputs[1].diff_form == '0' and node.inputs[0].diff_form == '0':
            node.diff_form = "0"
        elif node.inputs[1].diff_form == '0':
            node.diff_form = "%s" %node.inputs[0].diff_form
        elif node.inputs[0].diff_form == '0':
            node.diff_form = "%s" %node.inputs[1].diff_form
        else:
            node.diff_form = "%s-%s" % (
            node.inputs[0].diff_form, node.inputs[1].diff_form)
        return


class MulOp(Op):
    def __call__(self, node_A: Node, node_B: Node) -> Node:
        new_node = Op.__call__()
        new_node.inputs = [node_A, node_B]
        new_node.normal_form = "%s*%s" % (node_A.normal_form, node_B.normal_form)
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert len(input_vals) == 2
        return input_vals[0] * input_vals[1]

    def diff(self, node: Node, variable: str) -> None:
        if node.inputs[1].diff_form == '0' and node.inputs[0].diff_form == '0':
            node.diff_form = "0"
        elif node.inputs[1].diff_form == '0':
            node.diff_form = "%s*%s" % (
            node.inputs[1].normal_form, node.inputs[0].diff_form)
        elif node.inputs[0].diff_form == '0':
            node.diff_form = "%s*%s" % (
            node.inputs[0].normal_form, node.inputs[1].diff_form)
        else:
            node.diff_form = "%s*%s+%s*%s" %(node.inputs[1].normal_form, node.inputs[0].diff_form, node.inputs[0].normal_form, node.inputs[1].diff_form)
        return


class PowOp(Op):
    def __call__(self, node_A: Node, pow: float) -> Node:
        new_node = Op.__call__()
        new_node.inputs = [node_A]
        new_node.const_attr = pow
        new_node.normal_form = "%s^%s" % (node_A.normal_form, str(pow))
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert isinstance(node, Node) and len(input_vals) == 1
        return pow(input_vals, node.const_attr)

    def diff(self, node: Node, variable: str) -> None:
        if variable == node.inputs[0].normal_form:
            if node.const_attr == 2:
                node.diff_form = "2*%s" %node.inputs[0].normal_form
            else:
                node.diff_form = "%s*%s^%s" % (node.const_attr, node.inputs[0].normal_form, node.const_attr - 1)
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
        new_node = Op.__call__()
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
        new_node.normal_form = "%s-%s" % (node_A.normal_form, node_B.normal_form)
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert len(input_vals) == 1
        return node.const_attr - input_vals[0]

    def diff(self, node: Node, variable: str) -> None:
        if node.inputs[node.const_attr[1]].diff_form == '0':
            node.diff_form = '0'
        else:
            if node.const_attr[1] == 0:
                node.diff_form = "%s" %node.inputs[0].diff_form
            elif node.const_attr[1] == 1:
                node.diff_form = "-%s" %node.inputs[1].diff_form

class MulConstOp(Op):
    def __call__(self, node_A: Node, node_B: Node) -> Node:
        new_node = Op.__call__()
        new_node.inputs = [node_A, node_B]
        new_node.const_attr = node_A.const_attr
        new_node.normal_form = "%s*%s" % (node_A.normal_form, node_B.normal_form)
        return new_node

    def compute(self, node: Node, input_vals: list) -> float:
        assert len(input_vals) == 1
        return node.const_attr * input_vals[0]

    def diff(self, node: Node) -> None:
        if node.inputs[1].diff_form == '0':
            node.diff_form = "0"
        else:
            node.diff_form = "%s*%s" % (
            node.inputs[0].normal_form, node.inputs[1].diff_form)
        return


class PlaceholderOp(Op):
    def __call__(self, var_string: str) -> Node:
        new_node = Op.__call__()
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
        new_node = Op.__call__()
        new_node.inputs = None
        new_node.const_attr = number
        new_node.normal_form = str(number)
        return new_node

    def compute(self, node: Node) -> float:
        return node.const_attr

    def diff(self, node: Node, variable: str) -> None:
        node.diff_form = '0'
        return


if __name__ == '__main__':
    print('testing')