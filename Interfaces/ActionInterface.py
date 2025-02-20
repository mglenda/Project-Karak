from Interfaces.Interface import Interface
from Interfaces.CooldownInterface import CooldownInterface

class ActionInterface(Interface):
    hero: Interface
    path: str
    path_focused: str
    prio: int
    cooldown: CooldownInterface
    default_scope: int
    action_types: list[int]

    def is_available(self) -> bool:
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