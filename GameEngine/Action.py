from Interfaces.ActionInterface import ActionInterface
from Interfaces.HeroInterface import HeroInterface

from Game import GAME

PATH = '_Textures\\Abilities\\'

class Action(ActionInterface):
    hero: HeroInterface
    path: str
    path_focused: str
    prio: int

    def __init__(self,hero: HeroInterface):
        self.hero = hero

    def is_available(self) -> bool:
        return False

    def run(self):
        pass

class ActionCombat(Action):
    path = PATH + 'Combat.png'
    path_focused = PATH + 'CombatFocused.png'
    prio: int = 0

    def __init__(self, hero):
        super().__init__(hero)

    def is_available(self) -> bool:
        return self.hero.is_in_combat() or self.hero.is_in_hostile_tile()
    
    def run(self):
        if self.hero.is_in_combat():
            GAME.end_combat()
        else:
            GAME.start_combat()

class Stealth(Action):
    path = PATH + 'Stealth.png'
    path_focused = PATH + 'Stealth.png'
    prio: int = 1

    def __init__(self, hero):
        super().__init__(hero)

    def is_available(self) -> bool:
        return self.hero.is_in_hostile_tile() and not(self.hero.is_in_combat())
    
    def run(self):
        GAME.load_move_options(forced=True)