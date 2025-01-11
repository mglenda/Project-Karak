from GameEngine.MinionDefinition import MinionDefinition
from Interfaces.MinionInterface import MinionInterface
from GameEngine.Placeable import Placeable
from GameEngine.Item import Item

class Minion(MinionInterface,Placeable):
    definition: MinionDefinition
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

    def get_icon_path(self) -> str:
        return self.definition.path
    
    def get_combat_icon_path(self) -> str:
        return self.definition.path
    
    def remove(self):
        super().remove()
        self.tile.add_placeable(Item(self.definition.reward))