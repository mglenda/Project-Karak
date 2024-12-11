from Interfaces.Interface import Interface
from Interfaces.ItemInterface import ItemInterface
from GameEngine.ItemDefinition import ItemDefinition

class InventorySlotInterface(Interface):
    type: int
    item: ItemInterface

    def add_item(self, item: ItemInterface):
        pass

    def remove_item(self) -> ItemInterface:
        pass

    def get_item(self) -> ItemInterface:
        pass

    def set_type(self, type: int):
        pass

    def get_type(self) -> int:
        pass

    def get_item_definition(self) -> ItemDefinition:
        pass
    
    def verify_type(self, type: int) -> bool:
        pass

    def get_item_power(self) -> int:
        pass