from Interfaces.ActionInterface import ActionInterface
from Interfaces.HeroInterface import HeroInterface
from GameEngine.Cooldown import Cooldown
from GameEngine.Constants import DurationScopes
import GameEngine.Buff as buff
import GameEngine.BuffModifier as bMod
import GameEngine.DiceDefinition as diceType

from Game import GAME

PATH = '_Textures\\Abilities\\'


ACTION_TYPE_COMBAT: int = 3
ACTION_TYPE_SCROLL: int = 2
ACTION_TYPE_ABILITY: int = 1
ACTION_TYPE_GENERAL: int = 0

class Action(ActionInterface):
    hero: HeroInterface
    path: str
    path_focused: str
    prio: int
    cooldown: Cooldown
    default_scope: int
    action_types: list[int]

    def __init__(self,hero: HeroInterface):
        self.hero = hero
        self.cooldown = None

    def is_available(self) -> bool:
        return self.cooldown is None and (self.is_action_type(ACTION_TYPE_ABILITY) or not self.hero.has_modifier(bMod.Cursed)) and (self.is_action_type(ACTION_TYPE_COMBAT) or not self.hero.has_modifier(bMod.Injured))

    def run(self):
        self.set_cooldown(self.default_scope)

    def reset_cooldown(self):
        self.cooldown = None

    def set_cooldown(self, duration_scope: int):
        self.cooldown = Cooldown(duration_scope)

    def get_cooldown(self) -> Cooldown:
        return self.cooldown
    
    def is_action_type(self, action_type: int) -> bool:
        return action_type in self.action_types

class ActionCombat(Action):
    path = PATH + 'Combat.png'
    path_focused = PATH + 'CombatFocused.png'
    prio: int = 4
    action_types: list[int] = [ACTION_TYPE_GENERAL,ACTION_TYPE_COMBAT]

    def __init__(self, hero):
        super().__init__(hero)

    def is_available(self) -> bool:
        return (self.hero.is_in_combat() or (self.hero.is_in_hostile_tile() and not self.hero.has_modifier(bMod.CannotStartCombat))) and super().is_available()
    
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
    action_types: list[int] = [ACTION_TYPE_GENERAL]

    def __init__(self, hero):
        super().__init__(hero)

    def is_available(self) -> bool:
        return (not self.hero.is_in_hostile_tile() or self.hero.has_modifier(bMod.IgnoreHostiles) or self.hero.has_modifier(bMod.CannotStartCombat)) and not(self.hero.is_in_combat()) and not self.hero.has_modifier(bMod.CannotEndTurn)
    
    def run(self):
        GAME.end_turn()

    def set_cooldown(self, cooldown_scope):
        pass

class Stealth(Action):
    path = PATH + 'Stealth.png'
    path_focused = PATH + 'Stealth.png'
    prio: int = 5
    default_scope: int = DurationScopes.DURATION_SCOPE_TILEMOVE
    action_types: list[int] = [ACTION_TYPE_ABILITY]

    def __init__(self, hero):
        super().__init__(hero)

    def is_available(self) -> bool:
        return self.hero.is_in_hostile_tile() and not(self.hero.is_in_combat()) and not(self.hero.has_modifier(bMod.CannotStartCombat)) and super().is_available()
    
    def run(self):
        super().run()
        if not self.hero.is_action_on_cooldown(ActionCombat):
            self.hero.set_cooldown(ActionCombat,DurationScopes.DURATION_SCOPE_TILEMOVE)
        self.hero.add_buff(buff.Stealth)
        GAME.load_move_options()

class RollDice(Action):
    path = PATH + 'RollDice.png'
    path_focused = PATH + 'RollDiceFocused.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_GENERAL,ACTION_TYPE_COMBAT]

    def __init__(self, hero):
        super().__init__(hero)

    def is_available(self):
        return GAME.get_dice_manager() is not None and not self.hero.has_modifier(bMod.CannotRollDice) and super().is_available()
    
    def run(self):
        self.hero.add_buff(buff.CannotRollDices)
        GAME.get_dice_manager().roll()

class Revitalize(Action):
    path = PATH + 'Revitalize.png'
    path_focused = PATH + 'RevitalizeFocused.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_GENERAL]

    def __init__(self, hero):
        super().__init__(hero)

    def is_available(self):
        return self.hero.has_buff(buff.Injured)
    
    def run(self):
        self.hero.remove_buffs(buff.Injured)
        self.hero.heal(1)
        GAME.end_turn()