from Interfaces.BuffInterface import BuffInterface
import GameEngine.BuffModifier as bMod
from Interfaces.HeroInterface import HeroInterface
from GameEngine.Constants import DurationScopes
from typing import Type

class Buff(BuffInterface):
    default_duration_scope: int
    hero: HeroInterface
    modifiers_default: list[Type[bMod.BuffModifier]]
    active_modifiers: list[bMod.BuffModifier]
    duration_scope: int

    def __init__(self, hero: HeroInterface, duration_scope: int = None):
        self.active_modifiers = []
        for m_class in self.modifiers_default:
            self.active_modifiers.append(m_class(hero))

        self.duration_scope = self.default_duration_scope if duration_scope is None else duration_scope

    def remove(self):
        for m in self.active_modifiers:
            m.remove()

    def get_scope(self) -> int:
        return self.duration_scope
    
    def has_modifier(self, mod_type: Type[bMod.BuffModifier]) -> bool:
        for m in self.active_modifiers:
            if isinstance(m,mod_type):
                return True
        return False


class Stealth(Buff):
    default_duration_scope: int = DurationScopes.DURATION_SCOPE_TILEMOVE
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.IgnoreHostiles]

    def __init__(self, hero, duration_scope = None):
        super().__init__(hero, duration_scope)

class Exhausted(Buff):
    default_duration_scope: int = DurationScopes.DURATION_SCOPE_TURN
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.CannotStartCombat]

    def __init__(self, hero, duration_scope = None):
        super().__init__(hero, duration_scope)

class ChoosingTile(Buff):
    default_duration_scope: int = DurationScopes.DURATION_SCOPE_FOREVER
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.CannotEndTurn,bMod.CannotDoAnything]

    def __init__(self, hero, duration_scope = None):
        super().__init__(hero, duration_scope)

class CannotRollDices(Buff):
    default_duration_scope: int = DurationScopes.DURATION_SCOPE_COMBAT
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.CannotRollDice]

    def __init__(self, hero, duration_scope = None):
        super().__init__(hero, duration_scope)

class Unconsciousness(Buff):
    default_duration_scope: int = DurationScopes.DURATION_SCOPE_FOREVER
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.CannotStartCombat,bMod.Injured,bMod.CannotMove]

    def __init__(self, hero, duration_scope = None):
        super().__init__(hero, duration_scope)

class Injured(Buff):
    default_duration_scope: int = DurationScopes.DURATION_SCOPE_FOREVER
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.CannotStartCombat,bMod.Injured,bMod.CannotEndTurn,bMod.CannotMove]

    def __init__(self, hero, duration_scope = None):
        super().__init__(hero, duration_scope)
        
class Curse(Buff):
    default_duration_scope: int = DurationScopes.DURATION_SCOPE_FOREVER
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.Cursed]

    def __init__(self, hero, duration_scope = None):
        super().__init__(hero, duration_scope)

class HealedOnFountain(Buff):
    default_duration_scope: int = DurationScopes.DURATION_SCOPE_TURN
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.CannotStartCombat,bMod.Injured,bMod.CannotMove]

    def __init__(self, hero, duration_scope = None):
        super().__init__(hero, duration_scope)

class DisableAllActions(Buff):
    default_duration_scope: int = DurationScopes.DURATION_SCOPE_FOREVER
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.CannotEndTurn,bMod.CannotDoAnything,bMod.CannotMove]

    def __init__(self, hero, duration_scope = None):
        super().__init__(hero, duration_scope)