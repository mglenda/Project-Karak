import Interfaces.BuffModifierInterface as bMod
from typing import Type

class Opponent():
    pass

class Duelist(Opponent):
    power: int
    opponent: Opponent
    ability_power: int
    scroll_power: int
    dice_power: int

    def __init__(self):
        self.in_combat = False
        self.opponent = None
        self.ability_power = 0
        self.scroll_power = 0
        self.dice_power = 0

    def get_combat_icon_path(self) -> str:
        pass

    def get_dice_power(self) -> int:
        return self.dice_power
    
    def set_dice_power(self,value:int) -> int:
        self.dice_power = value

    def get_ability_power(self) -> int:
        return self.ability_power
    
    def add_ability_power(self,value: int):
        self.ability_power += value

    def get_scroll_power(self) -> int:
        return self.scroll_power
    
    def add_scroll_power(self,value: int):
        self.scroll_power += value

    def get_weapon_power(self) -> int:
        return self.power
    
    def is_in_combat(self) -> bool:
        return self.in_combat
    
    def get_opponent(self) -> Opponent:
        return self.opponent
    
    def get_ability_power(self) -> int:
        return self.ability_power
    
    def get_total_power(self) -> int:
        return self.get_weapon_power() + self.get_ability_power() + self.get_dice_power() + self.get_scroll_power()

    def enter_comat(self,opponent: Opponent):
        self.dice_power = 0
        self.opponent = opponent
        self.in_combat = True

    def leave_combat(self):
        self.opponent = None
        self.in_combat = False

    def has_modifier(self, mod_type: Type[bMod.BuffModifierInterface]) -> bool:
        return False