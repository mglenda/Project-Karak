from Interfaces.ActionInterface import ActionInterface
from Interfaces.HeroInterface import HeroInterface
from GameEngine.Constants import CooldownScopes

from Game import GAME

PATH = '_Textures\\Abilities\\'

class Action(ActionInterface):
    hero: HeroInterface
    path: str
    path_focused: str
    prio: int
    on_cooldown: bool
    cooldown_scope: int

    def __init__(self,hero: HeroInterface):
        self.hero = hero
        self.on_cooldown = False

    def is_available(self) -> bool:
        return not self.on_cooldown

    def run(self):
        if self.cooldown_scope is not None:
            self.on_cooldown = True

    def reset_cooldown(self):
        self.on_cooldown = False

class ActionCombat(Action):
    path = PATH + 'Combat.png'
    path_focused = PATH + 'CombatFocused.png'
    prio: int = 0
    cooldown_scope: int = None

    def __init__(self, hero):
        super().__init__(hero)

    def is_available(self) -> bool:
        return (self.hero.is_in_combat() or self.hero.is_in_hostile_tile()) and super().is_available()
    
    def run(self):
        super().run()
        if self.hero.is_in_combat():
            GAME.end_combat()
        else:
            GAME.start_combat()

class Stealth(Action):
    path = PATH + 'Stealth.png'
    path_focused = PATH + 'Stealth.png'
    prio: int = 1
    cooldown_scope: int = CooldownScopes.COOLDOWN_SCOPE_TILEMOVE

    def __init__(self, hero):
        super().__init__(hero)

    def is_available(self) -> bool:
        return self.hero.is_in_hostile_tile() and not(self.hero.is_in_combat()) and super().is_available()
    
    def run(self):
        super().run()
        GAME.load_move_options(forced=True)