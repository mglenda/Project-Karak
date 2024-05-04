from GameEngine.ItemDefinition import ItemDefinition
from Interfaces.InventorySlotInterface import InventorySlotInterface
from Interfaces.ItemInterface import ItemInterface

class InventorySlot(InventorySlotInterface):
    type: int
    item: ItemInterface
    
    def  __init__(self, type: int) -> None:
        self.type = type
        self.item = None

    def add_item(self, item: ItemInterface) -> ItemInterface:
        leftover = self.item
        self.item = item
        return leftover

    def remove_item(self) -> ItemInterface:
        item = self.item
        self.item = None
        return item
    
    def get_item(self) -> ItemInterface:
        return self.item

    def set_type(self, type: int):
        self.type = type

    def get_type(self) -> int:
        return self.type

    def get_item_definition(self) -> ItemDefinition:
        if self.item is not None:
            return self.item.definition
        return None
    
    def verify_type(self, type: int) -> bool:
        return self.type == type