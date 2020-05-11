import inspect

from typing import Callable


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
            op = self.exec_stack.pop()
            if inspect.isgeneratorfunction(op):
                if len(self.result_stack):
                    call = op(self.result_stack[-1])
                else:
                    call = op()
                for res in call:
                    self.result_stack.append(res)
                    self._next_func(i+1)
            else:
                if len(self.result_stack):
                    res = op(self.result_stack[-1])
                else:
                    res = op()
                self.result_stack.append(res)
                self._next_func(i+1)

    def run(self):
        self._next_func(0)


class ChainFunc:

    def __init__(self, *args):
        self.chain = []
        self.exec: Exec = Exec([])
        if isinstance(args[0], Callable):
            self.next_fn(args[0])

    def next_fn(self, func: Callable):
        self.chain.append(func)
        return self

    def execute(self):
        self.exec = Exec(self.chain)
        self.exec.run()
        self.exec = Exec([])


next_fn = ChainFunc
