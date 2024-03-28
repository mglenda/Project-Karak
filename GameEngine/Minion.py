from GameEngine.MinionDefinition import MinionDefinition
from Interfaces.MinionInterface import MinionInterface
from GameEngine.Placeable import Placeable

class Minion(MinionInterface,Placeable):
    definition: MinionDefinition
    power: int
    agressive: bool

    def __init__(self, definition: MinionDefinition) -> None:
        super().__init__(definition)

        self.power = definition.power
        self.agressive = definition.agressive

    def get_wheel_value(self) -> int:
        if self.agressive:
            return self.power
        return None
    
    def set_definition(self, definition: MinionDefinition):
        super().set_definition(definition)

        self.power = definition.power
        self.agressive = definition.agressive
