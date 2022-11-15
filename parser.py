import math
import re

from numpy import double
from abc import ABC, abstractmethod


class Expression(ABC):
    @abstractmethod
    def calc(self) -> double:
        pass


# implement the classes here
class Num(Expression):
    def __init__(self, x) -> None:
        self._x = x

    def calc(self) -> double:
        return self._x


class BinExp(Expression):
    def calc(self) -> double:
        pass

    def __init__(self, left, right):
        self._left = left
        self._right = right


class Plus(BinExp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self._left = left
        self._right = right

    def calc(self) -> double:
        return self._left.calc() + self._right.calc()


class Minus(BinExp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self._left = left
        self._right = right

    def calc(self) -> double:
        return self._left.calc() - self._right.calc()


class Mul(BinExp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self._left = left
        self._right = right

    def calc(self) -> double:
        return self._left.calc() * self._right.calc()


class Div(BinExp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self._left = left
        self._right = right

    def calc(self) -> double:
        return self._left.calc() / self._right.calc()


# implement the parser function here
def parser(expression) -> float:
    # return 0.0
    queue = []
    stack = []
    stack_exp = []

    def is_number(str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    split = re.findall("[+/*()-]|\d+", expression)
    splits = []
    i = 0
    while i < (len(split) - 1):
        if split[i] == "(" and split[i + 1] == "-":
            splits.append(split[i + 1] + split[i + 2])
            i += 4
        else:
            splits.append(split[i])
            i += 1
    splits.append(split[len(split) - 1])

    for s in splits:
        if is_number(s):
            queue.append(s)
        else:
            if s == "/":
                stack.append(s)
            elif s == "*":
                stack.append(s)
            elif s == "(":
                stack.append(s)
            elif s == "+":
                while (len(stack) > 0) and (stack[-1] == "*" or stack[-1] == "/" or stack[-1] == "-"):
                    queue.append(stack.pop())
                stack.append(s)
            elif s == "-":
                while (len(stack) > 0) and (stack[-1] == "*" or stack[-1] == "/"):
                    queue.append(stack.pop())
                stack.append(s)
            elif s == ")":
                while (len(stack) > 0) and (not stack[len(stack) - 1] == "("):
                    queue.append(stack.pop())
                if len(stack) > 0 and stack[-1] == "(":
                    stack.pop()

    while len(stack) != 0:
        queue.append(stack.pop())

    for st in queue:
        if is_number(st):
            stack_exp.append(Num(int(st)))
        else:
            right = stack_exp.pop()
            left = stack_exp.pop()

            if st == "/":
                stack_exp.append(Div(left, right))
            elif st == "*":
                stack_exp.append(Mul(left, right))
            elif st == "+":
                stack_exp.append(Plus(left, right))
            elif st == "-":
                stack_exp.append(Minus(left, right))

    result = math.floor(double(stack_exp.pop().calc() * 1000)) / 1000.0
    # print(result)
    return result
