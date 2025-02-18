from Interfaces.ActionInterface import ActionInterface
from Interfaces.HeroInterface import HeroInterface
from GameEngine.Cooldown import Cooldown
from GameEngine.Constants import DurationScopes
from GameEngine.Buff import BuffStealth
from GameEngine.BuffModifier import bm_IgnoreHostiles

from Game import GAME

PATH = '_Textures\\Abilities\\'

class Action(ActionInterface):
    hero: HeroInterface
    path: str
    path_focused: str
    prio: int
    cooldown: Cooldown
    default_scope: int

    def __init__(self,hero: HeroInterface):
        self.hero = hero
        self.cooldown = None

    def is_available(self) -> bool:
        return self.cooldown is None

    def run(self):
        self.set_cooldown(self.default_scope)

    def reset_cooldown(self):
        self.cooldown = None

    def set_cooldown(self, duration_scope: int):
        self.cooldown = Cooldown(duration_scope)

    def get_cooldown(self) -> Cooldown:
        return self.cooldown

class ActionCombat(Action):
    path = PATH + 'Combat.png'
    path_focused = PATH + 'CombatFocused.png'
    prio: int = 0

    def __init__(self, hero):
        super().__init__(hero)

    def is_available(self) -> bool:
        return (self.hero.is_in_combat() or self.hero.is_in_hostile_tile()) and super().is_available()
    
    def run(self):
        if self.hero.is_in_combat():
            self.set_cooldown(DurationScopes.DURATION_SCOPE_TURN)
            GAME.end_combat()
        else:
            GAME.start_combat()

class EndTurn(Action):
    path = PATH + 'EndTurn.png'
    path_focused = PATH + 'EndTurnFocused.png'
    prio: int = 10

    def __init__(self, hero):
        super().__init__(hero)

    def is_available(self) -> bool:
        return (not self.hero.is_in_hostile_tile() or self.hero.has_modifier(bm_IgnoreHostiles)) and not(self.hero.is_in_combat())
    
    def run(self):
        GAME.end_turn()

    def set_cooldown(self, cooldown_scope):
        pass

class Stealth(Action):
    path = PATH + 'Stealth.png'
    path_focused = PATH + 'Stealth.png'
    prio: int = 1
    default_scope: int = DurationScopes.DURATION_SCOPE_TILEMOVE

    def __init__(self, hero):
        super().__init__(hero)

    def is_available(self) -> bool:
        return self.hero.is_in_hostile_tile() and not(self.hero.is_in_combat()) and super().is_available()
    
    def run(self):
        super().run()
        if not self.hero.is_action_on_cooldown(ActionCombat):
            self.hero.set_cooldown(ActionCombat,DurationScopes.DURATION_SCOPE_TILEMOVE)
        self.hero.add_buff(BuffStealth)
        GAME.load_move_options()