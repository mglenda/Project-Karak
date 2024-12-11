from Interfaces.CombatInterface import CombatInterface
from GameEngine.Duelist import Duelist
from Interfaces.MinionInterface import MinionInterface
from Interfaces.HeroInterface import HeroInterface
from random import randint

class DuelistData:
    duelist: Duelist
    dice_power: int
    scroll_power: int
    ability_power: int

    def __init__(self, duelist: Duelist):
        self.duelist = duelist
        self.dice_power = 0
        self.scroll_power = 0
        self.ability_power = 0

    def get_power(self) -> int:
        return self.duelist.get_weapon_power()
    
    def get_ability_power(self) -> int:
        return self.ability_power
    
    def set_ability_power(self, value: int):
        self.ability_power = value
    
    def get_dice_power(self) -> int:
        return self.dice_power
    
    def set_dice_power(self, value: int):
        self.dice_power = value
    
    def get_scroll_power(self) -> int:
        return self.scroll_power
    
    def set_scroll_power(self, value: int):
        self.scroll_power = value
    
    def get_total_power(self) -> int:
        return self.get_power() + self.get_ability_power() + self.get_dice_power() + self.get_scroll_power()
    

class Combat(CombatInterface):
    duelists: list[DuelistData]
    active_duelist: Duelist

    def __init__(self,duelist_1: Duelist,duelist_2: Duelist):
        self.duelists = [
            DuelistData(duelist_1)
            ,DuelistData(duelist_2)
        ]
        self.duelists[0].set_dice_power(randint(1,6) + randint(1,6))
        self.active_duelist = duelist_1

    def get_duelist_data(self, id: int) -> DuelistData:
        return self.duelists[id]
    
    def is_finished(self) -> bool:
        return self.active_duelist == self.duelists[1].duelist or isinstance(self.duelists[1].duelist,MinionInterface)
    
    def active_next(self):
        self.active_duelist = self.duelists[1].duelist

    def is_draw(self) -> bool:
        return self.duelists[0].get_total_power() == self.duelists[1].get_total_power()
    
    def is_arena_duel(self) -> bool:
        return isinstance(self.duelists[0].duelist,HeroInterface) and isinstance(self.duelists[1].duelist,HeroInterface)
    
    def get_loser(self) -> Duelist:
        if self.duelists[0].get_total_power() < self.duelists[1].get_total_power():
            return self.duelists[0].duelist
        elif self.duelists[1].get_total_power() < self.duelists[0].get_total_power():
            return self.duelists[1].duelist
        else:
            return None
        
    def get_winner(self) -> Duelist:
        if self.get_loser() == self.duelists[1].duelist:
            return self.duelists[0].duelist
        elif self.get_loser() == self.duelists[0].duelist:
            return self.duelists[1].duelist
        else:
            return None
