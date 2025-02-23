from Interfaces.ActionInterface import ActionInterface
from Interfaces.HeroInterface import HeroInterface
from GameEngine.Cooldown import Cooldown
from GameEngine.Constants import DurationScopes
import GameEngine.Buff as buff
import GameEngine.BuffModifier as bMod
from typing import Type

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
    modifiers_default: list[Type[bMod.BuffModifier]]
    modifiers: list[bMod.BuffModifier]
    available: bool
    passive: bool

    def __init__(self,hero: HeroInterface):
        self.hero = hero
        self.cooldown = None
        self.available = True

        self.modifiers = []
        for m_class in self.modifiers_default:
            self.modifiers.append(m_class(hero))

    def get_availability(self) -> bool:
        return self.cooldown is None and not self.hero.has_modifier(bMod.CannotDoAnything) and (not self.is_action_type(ACTION_TYPE_ABILITY) or not self.hero.has_modifier(bMod.Cursed)) and (self.is_action_type(ACTION_TYPE_COMBAT) or not self.hero.has_modifier(bMod.Injured))

    def is_available(self) -> bool:
        return self.available
    
    def update(self):
        former_available = self.available
        self.available = self.get_availability()

        if former_available != self.available:
            for m in self.modifiers:
                if former_available:
                    m.disable()
                else:
                    m.enable()

    def has_modifier(self, mod_type: Type[bMod.BuffModifier]) -> bool:
        for m in self.modifiers:
            if isinstance(m,mod_type):
                return True
        return False

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

    def is_passive(self) -> bool:
        return self.passive

class ActionCombat(Action):
    path = PATH + 'Combat.png'
    path_focused = PATH + 'CombatFocused.png'
    prio: int = 4
    action_types: list[int] = [ACTION_TYPE_GENERAL,ACTION_TYPE_COMBAT]
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False

    def __init__(self, hero):
        super().__init__(hero)

    def get_availability(self) -> bool:
        return super().get_availability() and (self.hero.is_in_combat() or (self.hero.is_in_hostile_tile() and not self.hero.has_modifier(bMod.CannotStartCombat)))
    
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
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False

    def __init__(self, hero):
        super().__init__(hero)

    def get_availability(self) -> bool:
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
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False

    def __init__(self, hero):
        super().__init__(hero)

    def get_availability(self) -> bool:
        return super().get_availability() and self.hero.is_in_hostile_tile() and not(self.hero.is_in_combat()) and not(self.hero.has_modifier(bMod.CannotStartCombat))
    
    def run(self):
        super().run()
        if not self.hero.is_action_on_cooldown(ActionCombat):
            self.hero.set_cooldown(ActionCombat,DurationScopes.DURATION_SCOPE_TILEMOVE)
        self.hero.add_buff(buff.Stealth)
        self.hero.explore_minion()
        GAME.load_move_options()

class RollDice(Action):
    path = PATH + 'RollDice.png'
    path_focused = PATH + 'RollDiceFocused.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_GENERAL,ACTION_TYPE_COMBAT]
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False

    def __init__(self, hero):
        super().__init__(hero)

    def get_availability(self):
        return super().get_availability() and GAME.get_dice_manager() is not None and not self.hero.has_modifier(bMod.CannotRollDice)
    
    def run(self):
        self.hero.add_buff(buff.CannotRollDices)
        GAME.get_dice_manager().roll()

class Revitalize(Action):
    path = PATH + 'Revitalize.png'
    path_focused = PATH + 'RevitalizeFocused.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_GENERAL]
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False

    def __init__(self, hero):
        super().__init__(hero)

    def get_availability(self):
        return self.hero.has_buff(buff.Injured)
    
    def run(self):
        self.hero.remove_buffs(buff.Injured)
        self.hero.heal(1)
        GAME.end_turn()

class HealingFountain(Action):
    path = PATH + 'FountainHeal.png'
    path_focused = PATH + 'FountainHealFocused.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_GENERAL]
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False

    def __init__(self, hero):
        super().__init__(hero)

    def get_availability(self):
        return super().get_availability() and self.hero.is_on_fountain() and (self.hero.is_cursed() or self.hero.get_hit_points() < self.hero.get_max_hit_points())
    
    def run(self):
        self.hero.remove_buffs(buff.Curse)
        self.hero.heal()
        self.hero.set_move_points(0)
        self.hero.add_buff(buff.HealedOnFountain)
        GAME.load_move_options()

class AstralWalking(Action):
    path = PATH + 'AstralWalking.png'
    path_focused = PATH + 'AstralWalking.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_ABILITY]
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.CanWalkThroughWalls]
    modifiers: list[bMod.BuffModifier]
    passive = True

    def __init__(self, hero):
        super().__init__(hero)

    def get_availability(self):
        return super().get_availability()
    
    def run(self):
        pass

class Ambush(Action):
    path = PATH + 'Ambush.png'
    path_focused = PATH + 'Ambush.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_ABILITY]
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.AmbushBonus]
    modifiers: list[bMod.BuffModifier]
    passive = True

    def __init__(self, hero):
        super().__init__(hero)

    def get_availability(self):
        return super().get_availability() and self.hero.fighting_explored()
    
    def run(self):
        pass

class Backstab(Action):
    path = PATH + 'Backstab.png'
    path_focused = PATH + 'Backstab.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_ABILITY]
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.WinOnDraw]
    modifiers: list[bMod.BuffModifier]
    passive = True

    def __init__(self, hero):
        super().__init__(hero)

    def get_availability(self):
        return super().get_availability()
    
    def run(self):
        pass
