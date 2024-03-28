from Interfaces.Interface import Interface
from Interfaces.ItemInterface import ItemInterface
from GameEngine.ItemDefinition import ItemDefinition

class InventoryInterface(Interface):
    max_weapons: int
    max_scrolls: int
    max_keys: int
    hero: Interface

    weapons: list[ItemInterface]
    scrolls: list[ItemInterface]
    keys: list[ItemInterface]
    chests: list[ItemInterface]

    def has_item(self, definition: ItemDefinition) -> bool:
        pass

    def remove_item(self, item: ItemInterface):
        pass

    def add_item(self, item: ItemDefinition, slot_type: int, slot: int = None):
        pass

    def get_items(self) -> list[ItemInterface]:
        pass

    def get_weapons(self) -> list[ItemInterface]:
        pass
    
    def get_scrolls(self) -> list[ItemInterface]:
        pass
    
    def get_keys(self) -> list[ItemInterface]:
        pass
    
    def get_chests(self) -> list[ItemInterface]:
        pass