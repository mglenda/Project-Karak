from Interfaces.BuffInterface import BuffInterface
from GameEngine.BuffModifier import BuffModifier,bm_IgnoreHostiles
from Interfaces.HeroInterface import HeroInterface
from GameEngine.Constants import DurationScopes
from typing import Type

class Buff(BuffInterface):
    default_duration_scope: int
    hero: HeroInterface
    modifiers_default: list[Type[BuffModifier]]
    active_modifiers: list[BuffModifier]
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
    
    def has_modifier(self, mod_type: Type[BuffModifier]) -> bool:
        for m in self.active_modifiers:
            if isinstance(m,mod_type):
                return True
        return False


class BuffStealth(Buff):
    default_duration_scope: int = DurationScopes.DURATION_SCOPE_TILEMOVE
    modifiers_default: list[Type[BuffModifier]] = [bm_IgnoreHostiles]

    def __init__(self, hero, duration_scope = None):
        super().__init__(hero, duration_scope)

