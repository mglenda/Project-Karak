from typing import Callable

class Function():
    def __init__(self, func: Callable, *params, **kparams) -> None:
        self.func = func
        self.params = params
        self.kparams = kparams

    def execute(self):
        self.func(*self.params,**self.kparams)