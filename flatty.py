import inspect

from typing import Callable
from collections import namedtuple

executable = namedtuple('executable', ['op', 'args', 'kwargs'])


class Exec:

    def __init__(self, op_stack):
        self.op_stack = op_stack
        self.exec_stack = []
        self.result_stack = []

    def _next_func(self, i):
        if i == len(self.op_stack):
            return
        self.exec_stack.append(self.op_stack[i])
        while len(self.exec_stack):
            op, args, kwargs = self.exec_stack.pop()
            if inspect.isgeneratorfunction(op):
                if len(self.result_stack):
                    call = op(self.result_stack.pop())
                else:
                    call = op(*args, **kwargs)
                for res in call:
                    self.result_stack.append(res)
                    self._next_func(i+1)
            else:
                if len(self.result_stack):
                    arg = self.result_stack.pop()
                    res = op(arg)
                else:
                    res = op()
                self.result_stack.append(res)
                self._next_func(i+1)

    def run(self):
        self._next_func(0)


class ChainFunc:

    def __init__(self,):
        self.chain = []

    def next_fn(self, func: Callable, *args, **kwargs):
        self.chain.append(executable(func, args, kwargs))
        return self

    def execute(self):
        exec_ = Exec(self.chain)
        exec_.run()
        return exec_.result_stack


def next_fn(func: Callable, *args, **kwargs):
    return ChainFunc().next_fn(func, *args, **kwargs)
