from GUI.Dice import Dice as DiceGraphic
from GUI.Frame import FRAMEPOINT
import random

DICE_NORMAL = 0
DICE_WARLOCK = 1

class DiceRoller():
    _dices: list
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

    def add_dice(self,roll_type):
        self.create_dice(roll_type)
        self._attach_dices()

    def destroy(self):
        dice: DiceGraphic
        d: dict
        for d in reversed(self._dices):
            dice = d['dice']
            dice.destroy()
        del self

    def roll(self) -> int:
        n: int = 0
        for id,_ in enumerate(self._dices):
            n += self.roll_dice(id)
        return n

    def roll_dice(self,id: int) -> int:
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
            ,'dice': DiceGraphic(n)
            ,'last_roll': None
        }
        self._dices.append(dice)

    def _get_number(self,roll_type: int,skip: int = None) -> int:
        n = random.choice(self._roll_types[roll_type])
        if n == skip:
            n = self._get_number(roll_type,skip)
        return n
    
    def _attach_dices(self):
        dice: DiceGraphic
        d: dict
        x: int
        y: int
        w: int
        x_offset: int = 10
        for i,d in enumerate(self._dices):
            dice = d['dice']
            if i == 0:
                x,y = dice.get_parent().get_point(FRAMEPOINT.CENTER)
                y += dice.get_parent().get_h() * 0.1
                w = dice.get_w() / 2
                y -= dice.get_h() / 2
                x -= w * (len(self._dices))
                x -= (len(self._dices) - 1) * (x_offset / 2)
                dice.set_abs_point(x,y)
            else:
                dice.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,x_offset,0,self._dices[i-1]['dice'])
