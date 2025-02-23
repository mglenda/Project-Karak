from Interfaces.CombatInterface import CombatInterface
from GameEngine.Duelist import Duelist
from Interfaces.MinionInterface import MinionInterface
from Interfaces.HeroInterface import HeroInterface
import GameEngine.BuffModifier as bMod
import GameEngine.Buff as buff
from random import randint
    

class Combat(CombatInterface):
    duelists: list[Duelist]
    active_duelist: Duelist

    def __init__(self,duelist_1: Duelist,duelist_2: Duelist):
        self.duelists = [
            duelist_1
            ,duelist_2
        ]
        self.active_duelist = duelist_1

        duelist_1.enter_comat(opponent=duelist_2)
        duelist_2.enter_comat(opponent=duelist_1)

    def end(self):
        for d in self.duelists:
            d.leave_combat()
            if isinstance(d,HeroInterface):
                d.add_buff(buff.Exhausted)

    def get_duelist(self, id: int) -> Duelist:
        return self.duelists[id]
    
    def is_finished(self) -> bool:
        return self.active_duelist == self.duelists[1] or isinstance(self.duelists[1],MinionInterface)
    
    def active_next(self):
        self.active_duelist = self.duelists[1]

    def get_active_duelist(self) -> Duelist:
        return self.active_duelist

    def is_draw(self) -> bool:
        return (
            self.duelists[0].get_total_power() == self.duelists[1].get_total_power()
            and (
                    (self.duelists[0].has_modifier(bMod.WinOnDraw) and self.duelists[1].has_modifier(bMod.WinOnDraw))
                or 
                    (not self.duelists[0].has_modifier(bMod.WinOnDraw) and not self.duelists[1].has_modifier(bMod.WinOnDraw))
                )
        )
    
    def is_arena_duel(self) -> bool:
        return isinstance(self.duelists[0],HeroInterface) and isinstance(self.duelists[1],HeroInterface)
    
    def get_loser(self) -> Duelist:
        if self.duelists[0].get_total_power() < self.duelists[1].get_total_power():
            return self.duelists[0]
        elif self.duelists[1].get_total_power() < self.duelists[0].get_total_power():
            return self.duelists[1]
        elif self.duelists[1].get_total_power() == self.duelists[0].get_total_power() and self.duelists[0].has_modifier(bMod.WinOnDraw):
            return self.duelists[1]
        elif self.duelists[1].get_total_power() == self.duelists[0].get_total_power() and self.duelists[1].has_modifier(bMod.WinOnDraw):
            return self.duelists[0]
        else:
            return None
        
    def get_winner(self) -> Duelist:
        if self.get_loser() == self.duelists[1]:
            return self.duelists[0]
        elif self.get_loser() == self.duelists[0]:
            return self.duelists[1]
        else:
            return None
