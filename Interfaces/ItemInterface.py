from Interfaces.PlaceableInterface import PlaceableInterface
from GameEngine.ItemDefinition import ItemDefinition

class ItemInterface(PlaceableInterface):
    definition: ItemDefinition
    power: int
    type: int

    def get_power(self) -> int:
        pass