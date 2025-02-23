from Interfaces.Interface import Interface
from Interfaces.CooldownInterface import CooldownInterface
from Interfaces.BuffModifierInterface import BuffModifierInterface
from typing import Type

class ActionInterface(Interface):
    hero: Interface
    path: str
    path_focused: str
    prio: int
    cooldown: CooldownInterface
    default_scope: int
    action_types: list[int]
    modifiers_default: list[Type[BuffModifierInterface]]
    modifiers: list[BuffModifierInterface]
    available: bool
    passive: bool

    def get_availability(self) -> bool:
        pass

    def is_available(self) -> bool:
        pass
    
    def update(self):
        pass

    def has_modifier(self, mod_type: Type[BuffModifierInterface]) -> bool:
        pass

    def run(self):
        pass

    def reset_cooldown(self):
        pass

    def set_cooldown(self, duration_scope: int):
        pass

    def get_cooldown(self) -> CooldownInterface:
        pass

    def is_action_type(self, action_type: int) -> bool:
        pass

    def is_passive(self) -> bool:
        pass