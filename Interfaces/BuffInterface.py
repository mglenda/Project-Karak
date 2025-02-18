from Interfaces.Interface import Interface
from Interfaces.BuffModifierInterface import BuffModifierInterface
from typing import Type

class BuffInterface(Interface):
    default_duration_scope: int
    hero: Interface
    modifiers_default: list[Type[BuffModifierInterface]]
    active_modifiers: list[BuffModifierInterface]
    duration_scope: int

    def remove(self):
        pass

    def get_scope(self) -> int:
        pass
    
    def has_modifier(self) -> bool:
        pass