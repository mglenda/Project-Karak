import pygame
from typing import Callable, List, Tuple

class Timer():
    _loop_func: List[Tuple[Callable, Tuple]]
    _exit_func: List[Tuple[Callable, Tuple]]
    _millis: int
    _now: int
    _loops: int
    _loop_inc: int
    _running: bool
    _alive: bool
    _cur_loop: int
    # example of opeartions param
    # [(add, (3, 5)),
    # (multiply, (2, 3)),
    # (concat_strings, ("Hello", "World"))]
    def __init__(self,millis: int,loop_operations: List[Tuple[Callable, Tuple]], loops: int = 0, loop_inc_millis: int = 0, exit_operations: List[Tuple[Callable, Tuple]] = []) -> None:
        self._exit_func = exit_operations
        self._loop_func = loop_operations
        self._millis = millis
        self._now = pygame.time.get_ticks()
        self._loops = loops
        self._loop_inc = loop_inc_millis
        self._running = True
        self._alive = True
        self._cur_loop = 0

    def register_exit_func(self, exit_func: Callable, *params):
        self._exit_func.append((exit_func,params))

    def register_loop_func(self, loop_func: Callable,  *params):
        self._loop_func.append((loop_func,params))

    def _run(self):
        if self._running:
            now = pygame.time.get_ticks()
            if now - self._now >= self._millis:
                self._now = now
                self._cur_loop += 1
                self._millis += self._loop_inc
                if self._cur_loop > self._loops:
                    if len(self._exit_func) > 0:
                        for func, params in self._exit_func:
                            if func is not None:
                                if isinstance(params,str):
                                    func(params)
                                else:
                                    func(*params)
                    self._alive = False
                else:
                    if len(self._loop_func) > 0:
                        for func, params in self._loop_func:
                            if func is not None:
                                if not isinstance(params,tuple):
                                    func(params)
                                else:
                                    func(*params)

    def start(self):
        self._now = pygame.time.get_ticks()
        self._running = True

    def stop(self):
        self._running = False

    def kill(self):
        self._alive = False

    def destroy(self):
        del self

    def is_alive(self) -> bool:
        return self._alive
    
    def is_running(self) -> bool:
        return self._running