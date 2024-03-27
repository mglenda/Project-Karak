from GUI.Dice import Dice as DiceGraphic
from GUI.Frame import FRAMEPOINT
from Game import GAME
import random
from typing import Callable
from Timer.Timer import Timer

class DiceRoller():
    _dices: list
    _func: Callable
    _func_params: tuple
    _func_begin: Callable
    _func_begin_params: tuple
    _roll_timers: list[Timer]
    _roll_types = [
        (1,2,3,4,5,6) # NORMAL
        ,(0,1,2,3)    # WARLOCK
        ,(2,3,4,5,6)  # Swordmaster
    ]

    def __init__(self,*args) -> None:
        self._dices = []
        roll_type: int
        for roll_type in args:
            self.create_dice(roll_type)
        
        self._attach_dices()
        self._func = None
        self._func_params = ()
        self._func_begin = None
        self._func_begin_params = ()
        self._roll_timers = []

    def register_on_roll(self,func,*args):
        self._func = func
        self._func_params = args

    def register_on_begin(self,func,*args):
        self._func_begin = func
        self._func_begin_params = args

    def _exec_on_begin(self):
        if self._func_begin is not None:
            if not isinstance(self._func_begin_params,tuple):
                self._func_begin(self._func_begin_params)
            else:
                self._func_begin(*self._func_begin_params)

    def roll(self):
        self.deactivate_dices()
        self._exec_on_begin()
        timer = GAME.register_timer(10,[
                (self._roll,())
            ],30,5
            ,[
                (self._func,(self._func_params))
            ])
        self._roll_timers.append(timer)
        timer.register_exit_func(self._roll_timers.remove,timer)

    def roll_dice(self,id: int):
        self.deactivate_dices()
        self._exec_on_begin()
        timer = GAME.register_timer(10,[
                (self._roll_dice,(id))
            ],30,5
            ,[
                (self._func,(self._func_params))
            ])
        self._roll_timers.append(timer)
        timer.register_exit_func(self._roll_timers.remove,timer)

    def add_dice(self,roll_type):
        self.create_dice(roll_type)
        self._attach_dices()

    def destroy(self):
        for t in self._roll_timers:
            t.kill()
        dice: DiceGraphic
        d: dict
        for d in reversed(self._dices):
            dice = d['dice']
            dice.destroy()
        del self

    def _roll(self) -> int:
        n: int = 0
        for id,_ in enumerate(self._dices):
            n += self._roll_dice(id)
        return n
    
    def get_result(self) -> int:
        n: int = 0
        for id,_ in enumerate(self._dices):
            n += self._dices[id]['last_roll']
        return n

    def _roll_dice(self,id: int) -> int:
        dice: DiceGraphic = self._dices[id]['dice']
        roll_type: int = self._dices[id]['roll_type']
        last_roll: int = self._dices[id]['last_roll']

        n = self._get_number(roll_type,last_roll)
        self._dices[id]['last_roll'] = n
        dice.set_type(n)
        return n

    def create_dice(self,roll_type: int):
        n = self._roll_types[roll_type][0]
        dice = {
            'roll_type': roll_type
            ,'dice': DiceGraphic(n,len(self._dices),self)
            ,'last_roll': 0
        }
        self._dices.append(dice)

    def activate_dices(self):
        for d in self._dices:
            dice: DiceGraphic = d['dice']
            dice.set_active(True)

    def deactivate_dices(self):
        for d in self._dices:
            dice: DiceGraphic = d['dice']
            dice.set_active(False)

    def _get_number(self,roll_type: int,skip: int = None) -> int:
        n = random.choice(self._roll_types[roll_type])
        if n == skip:
            n = self._get_number(roll_type,skip)
        return n
    
    def _attach_dices(self):
        for i,d in enumerate(self._dices):
            dice: DiceGraphic = d['dice']
            if i == 0:
                dice.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
            elif i % 2 == 1:
                dice.set_point(FRAMEPOINT.RIGHT,FRAMEPOINT.LEFT,-dice.get_w() * 0.1,0,self._dices[i-1]['dice'])
            else:
                dice.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,dice.get_w() * 0.1,0,self._dices[i-2]['dice'])