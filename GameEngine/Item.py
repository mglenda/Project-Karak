from Interfaces.ItemInterface import ItemInterface
from GameEngine.ItemDefinition import ItemDefinition
from GameEngine.Placeable import Placeable

class Item(ItemInterface,Placeable):
    definition: ItemDefinition
    power: int
    type: int
    
    def __init__(self, definition: ItemDefinition) -> None:
        super().__init__(definition)

        self.power = definition.power
        self.type = definition.type

    def get_wheel_value(self) -> int:
        if self.power > 0:
            return self.power
        return None

    def set_definition(self, definition: ItemDefinition):
        super().set_definition(definition)

        self.power = definition.power
        self.type = definition.type